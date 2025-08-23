"""Configuration utilities for Simple Web App.

This module handles loading and validation of service configuration files.
"""
import json
import os
from typing import Dict, List, Any


SERVICES_CONFIG_PATH = '/app/config/services.json'


def load_services() -> Dict[str, List[Dict[str, Any]]]:
    """
    Load services configuration from JSON file.
    
    Returns:
        dict: Dictionary containing 'services' key with list of service configurations.
              Returns empty services list if file doesn't exist or is invalid.
              
    Example:
        >>> services = load_services()
        >>> print(services['services'])
        [{'name': 'redis', 'host': 'localhost', 'port': 6379, 'type': 'tcp'}]
    """
    if os.path.exists(SERVICES_CONFIG_PATH):
        try:
            with open(SERVICES_CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Validate basic structure
                if isinstance(config, dict) and 'services' in config:
                    return config
                return {"services": []}
        except (json.JSONDecodeError, IOError, UnicodeDecodeError):
            return {"services": []}
    return {"services": []}