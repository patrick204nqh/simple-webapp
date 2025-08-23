"""Input validation utilities for network security.

This module provides security-focused validation functions to ensure that
network operations are restricted to safe, private networks and valid inputs.
"""
import re
import ipaddress
from typing import Tuple


# Define allowed scanning targets (private networks and localhost)
ALLOWED_NETWORKS = [
    ipaddress.IPv4Network('10.0.0.0/8'),
    ipaddress.IPv4Network('172.16.0.0/12'), 
    ipaddress.IPv4Network('192.168.0.0/16'),
    ipaddress.IPv4Network('127.0.0.0/8'),
]

# Define blocked networks (public internet ranges to avoid)
BLOCKED_NETWORKS = [
    ipaddress.IPv4Network('0.0.0.0/0'),  # Will be checked after allowed networks
]

# Define allowed hostnames patterns (for internal services)
ALLOWED_HOSTNAME_PATTERNS = [
    r'^localhost$',
    r'^[\w\-]+\.local$',
    r'^[\w\-]+\.internal$',
    r'^[\w\-]+$',  # Simple hostnames without dots
]


def validate_scan_target(target: str) -> Tuple[bool, str]:
    """
    Validate network scan target for security compliance.
    
    This function ensures that network scanning is restricted to private networks
    and localhost only, preventing scanning of external/public networks.
    
    Args:
        target: Target hostname or IP address to validate
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if target is allowed, False otherwise
            - error_message (str): None if valid, error description if invalid
            
    Security Policy:
        - Only private networks are allowed (RFC 1918)
        - Localhost and loopback addresses are allowed
        - External IP addresses and public hostnames are blocked
        
    Example:
        >>> validate_scan_target('192.168.1.1')
        (True, None)
        >>> validate_scan_target('8.8.8.8')
        (False, 'Scanning of external IP addresses is not allowed')
    """
    if not target or not isinstance(target, str):
        return False, "Target cannot be empty"
    
    target = target.strip()
    
    if len(target) > 255:
        return False, "Target name too long"
    
    # Check for suspicious characters
    if re.search(r'[;&|`$]', target):
        return False, "Invalid characters in target"
    
    # Try to parse as IP address first
    try:
        ip = ipaddress.IPv4Address(target)
        
        # Check if IP is in allowed networks
        for network in ALLOWED_NETWORKS:
            if ip in network:
                return True, None
                
        return False, "Scanning of external IP addresses is not allowed"
        
    except ipaddress.AddressValueError:
        # Not a valid IP, check as hostname
        pass
    
    # Validate hostname format
    for pattern in ALLOWED_HOSTNAME_PATTERNS:
        if re.match(pattern, target, re.IGNORECASE):
            return True, None
    
    return False, "Invalid hostname format or external hostname not allowed"
