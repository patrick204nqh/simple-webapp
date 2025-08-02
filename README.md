# Simple Web App

<div align="center">
  <img src="public/images/simple-webapp-transparent-bg.png" alt="Simple Web App Logo" width="200"/>
</div>

A flexible monitoring web application for infrastructure practice. Test connectivity, monitor system resources, and explore network configurations.

## Features

- 🔌 **Service Connectivity**: Test any host:port combination
- 📊 **System Monitoring**: Real-time metrics via Glances integration
- 🌐 **Network Tools**: Port scanning and discovery
- 📝 **Configurable**: Optional JSON configuration for predefined services
- 🐳 **Containerized**: Docker deployment ready
- 🚀 **Zero Dependencies**: Works standalone or with any backend

## Quick Start

```bash
# Basic deployment
docker run -d -p 80:80 -p 61208:61208 --name simple-webapp \
  ghcr.io/patrick204nqh/simple-webapp:latest

# With custom services configuration
docker run -d -p 80:80 -p 61208:61208 \
  -v /path/to/services.json:/app/config/services.json:ro \
  --name simple-webapp ghcr.io/patrick204nqh/simple-webapp:latest
```

Access: [Web UI](http://localhost) • [Glances](http://localhost:61208)

## Screenshots

### Dashboard

## Configuration

Create `services.json` to define monitored services:

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

Mount to `/app/config/services.json` in container.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web UI |
| `GET` | `/api/instance-info` | Instance metadata |
| `GET` | `/api/services` | List configured services |
| `POST` | `/api/check-service` | Check service connectivity |
| `GET` | `/api/system-info` | System information |
| `POST` | `/api/network-scan` | Scan network ports |

## Use Cases

- **Infrastructure Practice**: Monitor AWS EC2 instances and services
- **Development**: Check local Docker containers and services
- **Network Troubleshooting**: Test connectivity and diagnose issues
- **Learning**: Understand networking, monitoring, and containerization

## Development

```bash
docker-compose build && docker-compose up
```

Access: [Web UI](http://localhost) • [Glances](http://localhost:61208)

**Environment Variables** (optional):
- `FLASK_ENV=development` - Enable debug mode

## Why Simple Web App?

✅ **No vendor lock-in** - Works with any infrastructure  
✅ **Zero dependencies** - No database or cloud provider required  
✅ **Instant deployment** - Single Docker command to start  
✅ **Flexible** - Adapts to your environment automatically