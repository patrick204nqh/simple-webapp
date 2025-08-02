"""Configuration utilities."""
import json
import os


SERVICES_CONFIG_PATH = '/app/config/services.json'


def load_services():
    """Load services configuration from JSON file."""
    if os.path.exists(SERVICES_CONFIG_PATH):
        try:
            with open(SERVICES_CONFIG_PATH, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"services": []}
    return {"services": []}