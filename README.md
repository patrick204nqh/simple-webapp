# Simple Web App

<div align="center">
  <img src="public/images/simple-webapp-transparent-bg.png" alt="Simple Web App Logo" width="200"/>

  [![Build Status](https://github.com/patrick204nqh/simple-webapp/actions/workflows/ghcr-build.yml/badge.svg)](https://github.com/patrick204nqh/simple-webapp/actions/workflows/ghcr-build.yml)
  [![Container Registry](https://img.shields.io/badge/container-ghcr.io-blue)](https://ghcr.io/patrick204nqh/simple-webapp)
  [![License](https://img.shields.io/github/license/patrick204nqh/simple-webapp)](https://github.com/patrick204nqh/simple-webapp/blob/main/LICENSE)
  [![Issues](https://img.shields.io/github/issues/patrick204nqh/simple-webapp)](https://github.com/patrick204nqh/simple-webapp/issues)
</div>

A flexible monitoring web application for infrastructure practice. Test connectivity, monitor system resources, and explore network configurations.

## Features

- 🔌 **Service Connectivity**: Test host:port combinations
- 📊 **System Monitoring**: Real-time metrics via Glances
- 🌐 **Network Scanning**: Port scanning (private networks only)
- 📝 **Configurable**: JSON service configuration
- 🐳 **Production Ready**: Health checks, logging, Docker deployment

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

Access: [Web UI](http://localhost) • [Glances](http://localhost:61208) • [Health](http://localhost/health)

## Screenshots

### Dashboard

<img width="1783" height="956" alt="image" src="https://github.com/user-attachments/assets/21c0e1cc-8f3c-4a20-8207-5fb5e84c7ad2" />

## Glances

<img width="1799" height="969" alt="image" src="https://github.com/user-attachments/assets/aed26cb1-66ce-4f83-8019-8e83a969f29c" />

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

| Method | Endpoint             | Description         |
| ------ | -------------------- | ------------------- |
| `GET`  | `/`                  | Web UI              |
| `GET`  | `/health`            | Health check        |
| `GET`  | `/ready`             | Readiness probe     |
| `GET`  | `/api/instance-info` | System metadata     |
| `GET`  | `/api/services`      | Configured services |
| `POST` | `/api/check-service` | Test connectivity   |
| `POST` | `/api/network-scan`  | Port scanning       |

## Use Cases

- **Infrastructure Practice**: Monitor AWS EC2 instances and services
- **Development**: Check local Docker containers and services
- **Network Troubleshooting**: Test connectivity and diagnose issues
- **Learning**: Understand networking, monitoring, and containerization

## Development

```bash
docker compose build && docker compose up
```

Access: [Web UI](http://localhost:8080) • [Glances](http://localhost:61208)


## Why Simple Web App?

✅ **Zero dependencies** - No database required  
✅ **Instant deployment** - Single Docker command  
✅ **Production ready** - Health checks and monitoring  
✅ **Security focused** - Private network scanning only
