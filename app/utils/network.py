"""Network utilities for service checking."""
import socket


DEFAULT_TIMEOUT = 3


def validate_port(port_data):
    """Validate and convert port to integer."""
    try:
        port = int(port_data)
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")
        return port
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid port number: {str(e)}")


def test_tcp_connection(host, port, timeout=DEFAULT_TIMEOUT):
    """Test TCP connection to host:port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False