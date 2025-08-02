from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess

from utils.config import load_services
from utils.system_info import get_system_info
from utils.aws_info import get_aws_info
from utils.network import validate_port, test_tcp_connection

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    """Serve the main HTML page."""
    try:
        with open('/app/index.html', 'r') as f:
            return f.read()
    except IOError:
        return "Application not found", 404

@app.route('/api/instance-info')
def instance_info():
    """Get comprehensive instance information."""
    try:
        # Get comprehensive system info
        info = get_system_info()
        
        # Try to add AWS metadata if available
        aws_info = get_aws_info()
        if aws_info:
            info.update(aws_info)
            info['cloud_provider'] = 'AWS'
        else:
            info['cloud_provider'] = 'Unknown/On-Premise'
        
        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
    
    # Validate port
    try:
        port = validate_port(data.get('port', 80))
    except ValueError as e:
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
    
    # Basic input validation
    if not target or len(target.strip()) == 0:
        return jsonify({'error': 'Target cannot be empty'}), 400
    
    try:
        # Use safe command construction
        cmd = ['nmap', '-sT', '-F', target]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        return jsonify({
            'target': target,
            'output': result.stdout,
            'error': result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Network scan timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)