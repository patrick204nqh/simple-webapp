"""Network utilities for service checking and connectivity testing.

This module provides utilities for validating network parameters and testing
TCP connections to remote services.
"""
import socket
from typing import Union


DEFAULT_TIMEOUT = 3


def validate_port(port_data: Union[str, int]) -> int:
    """
    Validate and convert port to integer.
    
    Args:
        port_data: Port number as string or integer
        
    Returns:
        int: Valid port number between 1 and 65535
        
    Raises:
        ValueError: If port is invalid or out of range
        
    Example:
        >>> validate_port("8080")
        8080
        >>> validate_port(443)
        443
    """
    try:
        port = int(port_data)
        if port < 1 or port > 65535:
            raise ValueError("Port must be between 1 and 65535")
        return port
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid port number: {str(e)}")


def test_tcp_connection(host: str, port: int, timeout: int = DEFAULT_TIMEOUT) -> bool:
    """
    Test TCP connection to specified host and port.
    
    Args:
        host: Target hostname or IP address
        port: Target port number
        timeout: Connection timeout in seconds (default: 3)
        
    Returns:
        bool: True if connection successful, False otherwise
        
    Example:
        >>> test_tcp_connection('localhost', 80)
        True
        >>> test_tcp_connection('unreachable.host', 443)
        False
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except (socket.error, OSError):
        return False