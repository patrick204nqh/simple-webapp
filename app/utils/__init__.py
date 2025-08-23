"""
Simple Web App Utilities Package

This package contains utility modules for the Simple Web App:
- config: Service configuration management
- system_info: System information gathering
- aws_info: AWS metadata retrieval
- network: Network connectivity utilities
- validation: Input validation and security
- logging_config: Structured logging setup
"""

__version__ = "1.0.0"
__author__ = "Simple Web App Team"

# Import commonly used functions
from .config import load_services
from .system_info import get_system_info
from .network import test_tcp_connection, validate_port
from .validation import validate_scan_target

__all__ = [
    'load_services',
    'get_system_info', 
    'test_tcp_connection',
    'validate_port',
    'validate_scan_target'
]