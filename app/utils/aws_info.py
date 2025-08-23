"""AWS metadata utilities for cloud instance information.

This module retrieves AWS EC2 instance metadata when running on AWS infrastructure.
"""
import urllib.request
import urllib.error


AWS_METADATA_URL = 'http://169.254.169.254/latest/meta-data/'


def get_aws_metadata(endpoint, timeout=2):
    """Fetch AWS metadata for a specific endpoint."""
    try:
        url = AWS_METADATA_URL + endpoint
        response = urllib.request.urlopen(url, timeout=timeout)
        return response.read().decode()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None


def get_aws_info():
    """Get AWS-specific metadata if available."""
    aws_info = {}
    aws_fields = {
        'instance_id': 'instance-id',
        'instance_type': 'instance-type',
        'public_ip': 'public-ipv4',
        'availability_zone': 'placement/availability-zone',
        'security_groups': 'security-groups'
    }
    
    for key, endpoint in aws_fields.items():
        value = get_aws_metadata(endpoint)
        if value:
            aws_info[key] = value
    
    return aws_info