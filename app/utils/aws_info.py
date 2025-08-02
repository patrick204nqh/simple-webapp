"""AWS metadata utilities."""
import urllib.request


AWS_METADATA_URL = 'http://169.254.169.254/latest/meta-data/'


def get_aws_metadata(endpoint, timeout=2):
    """Fetch AWS metadata for a specific endpoint."""
    try:
        url = AWS_METADATA_URL + endpoint
        response = urllib.request.urlopen(url, timeout=timeout)
        return response.read().decode()
    except:
        return None


def get_aws_info():
    """Get AWS-specific metadata if available."""
    aws_info = {}
    aws_fields = {
        'instance_id': 'instance-id',
        'instance_type': 'instance-type',
        'public_ip': 'public-ipv4',
        'availability_zone': 'placement/availability-zone',
        'security_groups': 'security-groups',
        'vpc_id': 'network/interfaces/macs/*/vpc-id'
    }
    
    for key, endpoint in aws_fields.items():
        if '*' not in endpoint:  # Simple endpoint
            value = get_aws_metadata(endpoint)
            if value:
                aws_info[key] = value
    
    return aws_info