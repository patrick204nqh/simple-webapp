from flask import Flask, jsonify, request, g, render_template
from flask_cors import CORS
import subprocess
import time
import uuid
import os

from utils.config import load_services
from utils.system_info import get_system_info
from utils.aws_info import get_aws_info
from utils.network import validate_port, test_tcp_connection
from utils.validation import validate_scan_target
from utils.logging_config import setup_logging, get_logger

# Setup logging
logger = setup_logging()


def log_request_event(event_type, **kwargs):
    """Helper function for consistent request logging."""
    extra = {'request_id': g.get('request_id')}
    extra.update(kwargs)
    logger.info(event_type, extra=extra)

app = Flask(__name__, static_folder='static', static_url_path='/static', template_folder='templates')
CORS(app)


@app.before_request
def before_request():
    """Log request details and setup request context."""
    g.start_time = time.time()
    g.request_id = str(uuid.uuid4())[:8]
    
    log_request_event(
        "Request started",
        method=request.method,
        endpoint=request.endpoint or request.path,
        user_ip=request.remote_addr,
        user_agent=request.headers.get('User-Agent', '')
    )


@app.after_request
def after_request(response):
    """Log response details."""
    duration = time.time() - g.get('start_time', time.time())
    
    log_request_event(
        "Request completed",
        method=request.method,
        endpoint=request.endpoint or request.path,
        status_code=response.status_code,
        duration=f"{duration:.3f}s"
    )
    
    return response

@app.route('/')
def index():
    """Serve the main HTML page."""
    try:
        return render_template('index.html')
    except IOError as e:
        logger.error(
            "Failed to serve index page",
            extra={'request_id': g.get('request_id'), 'error': str(e)}
        )
        return "Application not found", 404

@app.route('/api/instance-info')
def instance_info():
    """Get comprehensive instance information."""
    try:
        log_request_event("Getting instance information")
        
        # Get comprehensive system info
        info = get_system_info()
        
        # Try to add AWS metadata if available
        aws_info = get_aws_info()
        if aws_info:
            info.update(aws_info)
            info['cloud_provider'] = 'AWS'
            log_request_event("AWS metadata retrieved")
        else:
            info['cloud_provider'] = 'Unknown/On-Premise'
        
        return jsonify(info)
    except Exception as e:
        log_request_event("Failed to get instance information", error=str(e))
        return jsonify({'error': 'Failed to retrieve instance information'}), 500

def _run_health_checks(check_level='basic'):
    """Run health checks with different levels of thoroughness."""
    checks = {}
    overall_status = 'healthy' if check_level == 'basic' else 'ready'
    
    # Config check (both levels)
    try:
        load_services()
        checks['config'] = 'ok'
    except Exception:
        checks['config'] = 'error'
        overall_status = 'degraded' if check_level == 'basic' else 'not_ready'
    
    # System info check (both levels)  
    try:
        get_system_info()
        checks['system' if check_level == 'basic' else 'system_info'] = 'ok'
    except Exception:
        checks['system' if check_level == 'basic' else 'system_info'] = 'error'
        overall_status = 'degraded' if check_level == 'basic' else 'not_ready'
    
    # Network check (readiness only)
    if check_level == 'readiness':
        try:
            if test_tcp_connection('localhost', int(os.getenv('PORT', 80))):
                checks['network'] = 'ok'
            else:
                checks['network'] = 'warning'
        except Exception:
            checks['network'] = 'error'
            overall_status = 'not_ready'
    else:
        # Basic health always includes app check
        checks['app'] = 'ok'
    
    return {
        'status': overall_status,
        'timestamp': time.time(),
        'checks': checks
    }


@app.route('/health')
def health_check():
    """Health check endpoint for container orchestration."""
    try:
        result = _run_health_checks('basic')
        status_code = 200 if result['status'] == 'healthy' else 503
        return jsonify(result), status_code
    except Exception as e:
        logger.error("Health check failed", extra={'error': str(e)})
        return jsonify({
            'status': 'unhealthy',
            'timestamp': time.time(),
            'error': 'Health check failed'
        }), 503


@app.route('/ready')
def readiness_check():
    """Readiness check endpoint for container orchestration."""
    try:
        result = _run_health_checks('readiness')
        status_code = 200 if result['status'] == 'ready' else 503
        return jsonify(result), status_code
    except Exception as e:
        logger.error("Readiness check failed", extra={'error': str(e)})
        return jsonify({
            'status': 'not_ready',
            'timestamp': time.time(),
            'error': 'Readiness check failed'
        }), 503


@app.route('/api/services')
def get_services():
    """Get configured services list."""
    return jsonify(load_services())

@app.route('/api/check-service', methods=['POST'])
def check_service():
    """Check connectivity to a specific service."""
    if not request.json:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    data = request.json
    host = data.get('host', 'localhost')
    service_type = data.get('type', 'tcp')
    
    logger.info(
        "Checking service connectivity",
        extra={
            'request_id': g.get('request_id'),
            'host': host,
            'port': data.get('port', 80),
            'service_type': service_type
        }
    )
    
    # Validate port
    try:
        port = validate_port(data.get('port', 80))
    except ValueError as e:
        logger.warning(
            "Invalid port provided",
            extra={
                'request_id': g.get('request_id'),
                'port': data.get('port', 80),
                'error': str(e)
            }
        )
        return jsonify({
            'host': host,
            'port': data.get('port', 80),
            'type': service_type,
            'status': 'error',
            'message': str(e)
        }), 400
    
    # Test connection
    is_online = test_tcp_connection(host, port)
    status = 'online' if is_online else 'offline'
    message = f'Successfully connected to {host}:{port}' if is_online else f'Cannot connect to {host}:{port}'
    
    logger.info(
        "Service connectivity check completed",
        extra={
            'request_id': g.get('request_id'),
            'host': host,
            'port': port,
            'status': status
        }
    )
    
    return jsonify({
        'host': host,
        'port': port,
        'type': service_type,
        'status': status,
        'message': message
    })

@app.route('/api/system-info')
def system_info():
    """Get system information via script."""
    try:
        result = subprocess.run(
            ['/app/scripts/system-info.sh'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        return jsonify({
            'output': result.stdout,
            'error': result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'System info script timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/network-scan', methods=['POST'])
def network_scan():
    """Perform network scan on target."""
    if not request.json:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    data = request.json
    target = data.get('target', 'localhost')
    
    # Enhanced input validation
    if not target or len(target.strip()) == 0:
        return jsonify({'error': 'Target cannot be empty'}), 400
    
    target = target.strip()
    
    logger.info(
        "Network scan requested",
        extra={'request_id': g.get('request_id'), 'target': target}
    )
    
    # Validate scan target for security
    is_valid, error_msg = validate_scan_target(target)
    if not is_valid:
        logger.warning(
            "Network scan blocked - invalid target",
            extra={
                'request_id': g.get('request_id'),
                'target': target,
                'reason': error_msg
            }
        )
        return jsonify({'error': f'Invalid target: {error_msg}'}), 400
    
    try:
        # Use safe command construction with limited scope
        cmd = ['nmap', '-sT', '-F', '--host-timeout', '10s', target]
        logger.info(
            "Starting network scan",
            extra={'request_id': g.get('request_id'), 'target': target}
        )
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        logger.info(
            "Network scan completed",
            extra={
                'request_id': g.get('request_id'),
                'target': target,
                'return_code': result.returncode
            }
        )
        
        return jsonify({
            'target': target,
            'output': result.stdout,
            'error': result.stderr if result.stderr else None
        })
    except subprocess.TimeoutExpired:
        logger.warning(
            "Network scan timed out",
            extra={'request_id': g.get('request_id'), 'target': target}
        )
        return jsonify({'error': 'Network scan timed out'}), 504
    except Exception as e:
        logger.error(
            "Network scan failed",
            extra={
                'request_id': g.get('request_id'),
                'target': target,
                'error': str(e)
            }
        )
        return jsonify({'error': 'Network scan failed'}), 500

if __name__ == '__main__':
    # Use port 80 for production, allow PORT override for development
    port = int(os.getenv('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')