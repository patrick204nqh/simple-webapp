"""System information utilities."""
import socket
import platform
import time
import psutil
import os
from .logging_config import get_logger

logger = get_logger('utils.system_info')


def get_system_info():
    """Get comprehensive system information."""
    info = {}
    
    # Basic system info
    info['hostname'] = socket.gethostname()
    info['platform'] = platform.system()
    info['platform_release'] = platform.release()
    info['platform_version'] = platform.version()
    info['architecture'] = platform.machine()
    info['processor'] = platform.processor() or 'Unknown'
    
    # Network info
    try:
        info['private_ip'] = socket.gethostbyname(socket.gethostname())
    except (socket.gaierror, OSError) as e:
        logger.warning(f"Failed to get private IP: {e}")
        info['private_ip'] = 'Unknown'
    
    # System uptime
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_hours = int(uptime_seconds // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        info['uptime'] = f"{uptime_hours}h {uptime_minutes}m"
        info['boot_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(boot_time))
    except (OSError, ValueError) as e:
        logger.warning(f"Failed to get uptime info: {e}")
        info['uptime'] = 'Unknown'
        info['boot_time'] = 'Unknown'
    
    # CPU info
    try:
        info['cpu_cores'] = psutil.cpu_count(logical=False)
        info['cpu_threads'] = psutil.cpu_count(logical=True)
        info['cpu_usage'] = f"{psutil.cpu_percent(interval=None):.1f}%"
        
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            info['cpu_frequency'] = f"{cpu_freq.current:.0f} MHz"
    except (OSError, AttributeError) as e:
        logger.warning(f"Failed to get CPU info: {e}")
        info['cpu_cores'] = 'Unknown'
        info['cpu_threads'] = 'Unknown'
        info['cpu_usage'] = 'Unknown'
    
    # Memory info
    try:
        memory = psutil.virtual_memory()
        info['memory_total'] = f"{memory.total / (1024**3):.1f} GB"
        info['memory_used'] = f"{memory.used / (1024**3):.1f} GB"
        info['memory_usage'] = f"{memory.percent:.1f}%"
        info['memory_available'] = f"{memory.available / (1024**3):.1f} GB"
    except (OSError, AttributeError) as e:
        logger.warning(f"Failed to get memory info: {e}")
        info['memory_total'] = 'Unknown'
        info['memory_used'] = 'Unknown'
        info['memory_usage'] = 'Unknown'
        info['memory_available'] = 'Unknown'
    
    # Disk info
    try:
        disk_usage = psutil.disk_usage('/')
        info['disk_total'] = f"{disk_usage.total / (1024**3):.1f} GB"
        info['disk_used'] = f"{disk_usage.used / (1024**3):.1f} GB"
        info['disk_free'] = f"{disk_usage.free / (1024**3):.1f} GB"
        info['disk_usage'] = f"{(disk_usage.used / disk_usage.total * 100):.1f}%"
    except (OSError, ZeroDivisionError) as e:
        logger.warning(f"Failed to get disk info: {e}")
        info['disk_total'] = 'Unknown'
        info['disk_used'] = 'Unknown'
        info['disk_free'] = 'Unknown'
        info['disk_usage'] = 'Unknown'
    
    # Network interfaces
    try:
        interfaces = []
        for interface_name, interface_addresses in psutil.net_if_addrs().items():
            for address in interface_addresses:
                if address.family == socket.AF_INET:  # IPv4
                    interfaces.append(f"{interface_name}: {address.address}")
        info['network_interfaces'] = interfaces[:3]  # Limit to first 3
    except (OSError, AttributeError) as e:
        logger.warning(f"Failed to get network interfaces: {e}")
        info['network_interfaces'] = []
    
    # Container detection
    info['container_type'] = detect_container_type()
    
    return info


def detect_container_type():
    """Detect container environment type."""
    if os.path.exists('/.dockerenv'):
        return 'Docker'
    elif os.path.exists('/proc/1/cgroup'):
        try:
            with open('/proc/1/cgroup', 'r') as f:
                cgroup_content = f.read()
                if 'docker' in cgroup_content:
                    return 'Docker'
                elif 'kubepods' in cgroup_content:
                    return 'Kubernetes'
                elif 'lxc' in cgroup_content:
                    return 'LXC'
                else:
                    return 'Native'
        except (IOError, OSError) as e:
            logger.warning(f"Failed to read cgroup info: {e}")
            pass
    return 'Unknown'