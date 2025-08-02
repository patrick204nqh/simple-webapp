# Docker Hub Auto-Deploy Setup

Simple guide to automatically push Docker images to Docker Hub when you update your code.

## Quick Setup (5 minutes)

### 1. Get Docker Hub token
1. Login to [hub.docker.com](https://hub.docker.com)
2. Account Settings → Security → Access Tokens
3. Create token with **Read, Write** permissions
4. Copy the token

### 2. Add GitHub secrets
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add these secrets:
   - `DOCKER_USERNAME` = `patrick204nqh`
   - `DOCKER_PASSWORD` = the token from step 1

### 3. Done!
The workflow is already setup. Every time you push to `main`, it builds and pushes to Docker Hub.

## How Auto-Versioning Works

### When you push code:
```bash
git add .
git commit -m "your changes"
git push origin main
```

### Automatic tags created:
- `patrick204nqh/simple-webapp:latest` ← Always points to newest
- `patrick204nqh/simple-webapp:v1.0.3` ← Auto-incremented version
- `patrick204nqh/simple-webapp:1.0` ← Major.minor version
- `patrick204nqh/simple-webapp:main` ← Main branch version  
- `patrick204nqh/simple-webapp:main-abc1234` ← Specific commit

### Version increments automatically:
- First push: `v1.0.0`
- Second push: `v1.0.1` 
- Third push: `v1.0.2`
- And so on...

## Using the Images

### Latest version (recommended):
```bash
docker pull patrick204nqh/simple-webapp:latest
docker run -d -p 8080:80 patrick204nqh/simple-webapp:latest
```

### Specific version:
```bash
docker pull patrick204nqh/simple-webapp:v1.0.3
docker run -d -p 8080:80 patrick204nqh/simple-webapp:v1.0.3
```

### Update docker-compose.yml:
```yaml
services:
  webapp:
    image: patrick204nqh/simple-webapp:latest  # Always latest
    # OR
    image: patrick204nqh/simple-webapp:v1.0.3  # Specific version
    ports:
      - "8080:80"
```

## Common Issues

**Build fails?** 
- Check GitHub Actions tab for error logs
- Verify Docker Hub token is correct

**No new image?**
- Must push to `main` branch
- Check workflow triggered in Actions tab

## Manual Versioning (if needed)

### To create a major/minor version bump:
```bash
# Create a tag manually for major version
git tag v2.0.0
git push origin v2.0.0

# Next auto-increment will be v2.0.1, v2.0.2, etc.
```

### Manual push:
```bash
# Build locally
docker build -t patrick204nqh/simple-webapp:v1.5.0 .

# Push manually  
docker push patrick204nqh/simple-webapp:v1.5.0
```

## Version History

Check your versions:
- **GitHub**: Go to repo → Releases/Tags
- **Docker Hub**: Check [hub.docker.com/r/patrick204nqh/simple-webapp/tags](https://hub.docker.com/r/patrick204nqh/simple-webapp/tags)

That's it! Push code → Version increments automatically → Docker image updates.