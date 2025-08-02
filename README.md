# Simple Web App

A flexible monitoring web application for infrastructure practice. Check connectivity to any service, monitor system resources, and explore network configurations.

## Features

- 🔌 **Universal Service Checker**: Test connectivity to any host:port combination
- 📊 **System Monitoring**: Glances integration for real-time metrics
- 🌐 **Network Tools**: Port scanning and network discovery
- 📝 **Configurable Services**: Optional JSON configuration for predefined services
- 🐳 **Fully Containerized**: Easy deployment with Docker
- 🚀 **No Dependencies**: Works with any backend services (or none at all)

## Quick Start

```bash
# Pull and run
docker run -d \
  -p 80:80 \
  -p 61208:61208 \
  --name simple-webapp \
  ghcr.io/patrick204nqh/simple-webapp:latest

# With service configuration
docker run -d \
  -p 80:80 \
  -p 61208:61208 \
  -v /path/to/services.json:/app/config/services.json:ro \
  --name simple-webapp \
  ghcr.io/patrick204nqh/simple-webapp:latest
```

## Configuration

### Optional Services Configuration

Create a `services.json` file to define services to monitor:

```json
{
  "services": [
    {
      "name": "my-database",
      "host": "192.168.1.100",
      "port": 5432,
      "type": "tcp"
    }
  ]
}
```

Mount it to `/app/config/services.json` in the container.

## API Endpoints

- `GET /` - Web UI
- `GET /api/instance-info` - Instance metadata
- `GET /api/services` - List configured services
- `POST /api/check-service` - Check service connectivity
- `GET /api/system-info` - System information
- `POST /api/network-scan` - Scan network ports

## Use Cases

1. **AWS Practice**: Monitor EC2 instances and services
2. **Local Development**: Check Docker containers
3. **Network Troubleshooting**: Test connectivity
4. **Learning Tool**: Understand networking and monitoring

## Development

```bash
# Build locally
docker-compose build

# Run with test services
docker-compose up

# Access at
# - Web UI: http://localhost
# - Glances: http://localhost:61208
```

## Environment Variables

All environment variables are optional:
- `FLASK_ENV`: Set to 'development' for debug mode

## No Lock-in

This app doesn't require any specific:
- Database (MySQL, PostgreSQL, Redis, etc.)
- Cloud provider (AWS, GCP, Azure)
- Service configuration

It adapts to whatever environment you deploy it in!