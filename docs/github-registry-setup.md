# GitHub Container Registry Auto-Deploy Setup

Simple guide to automatically push Docker images to GitHub Container Registry when you update your code.

## Quick Setup (2 minutes)

### 1. No additional secrets needed!
GitHub Actions automatically has access to push to GitHub Container Registry using the built-in `GITHUB_TOKEN`.

### 2. Enable GitHub Actions permissions (if not already done)
1. Go to your GitHub repo → Settings → Actions → General
2. Under "Workflow permissions", select:
   - **Read and write permissions**
   - ✅ Check "Allow GitHub Actions to create and approve pull requests"

### 3. Done!
The workflow is already setup. Every time you push to `main`, it builds and pushes to GitHub Container Registry.

## How Auto-Versioning Works

### When you push code:
```bash
git add .
git commit -m "your changes"
git push origin main
```

### Automatic tags created:
- `ghcr.io/patrick204nqh/simple-webapp:latest` ← Always points to newest
- `ghcr.io/patrick204nqh/simple-webapp:v1.0.3` ← Auto-incremented version
- `ghcr.io/patrick204nqh/simple-webapp:1.0` ← Major.minor version
- `ghcr.io/patrick204nqh/simple-webapp:main` ← Main branch version  
- `ghcr.io/patrick204nqh/simple-webapp:main-abc1234` ← Specific commit

### Version increments automatically:
- First push: `v1.0.0`
- Second push: `v1.0.1` 
- Third push: `v1.0.2`
- And so on...

## Using the Images

### Latest version (recommended):
```bash
docker pull ghcr.io/patrick204nqh/simple-webapp:latest
docker run -d -p 8080:80 ghcr.io/patrick204nqh/simple-webapp:latest
```

### Specific version:
```bash
docker pull ghcr.io/patrick204nqh/simple-webapp:v1.0.3
docker run -d -p 8080:80 ghcr.io/patrick204nqh/simple-webapp:v1.0.3
```

### Update docker-compose.yml:
```yaml
services:
  webapp:
    image: ghcr.io/patrick204nqh/simple-webapp:latest  # Always latest
    # OR
    image: ghcr.io/patrick204nqh/simple-webapp:v1.0.3  # Specific version
    ports:
      - "8080:80"
```

## Common Issues

**Build fails?** 
- Check GitHub Actions tab for error logs
- Verify GitHub Actions has write permissions

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
docker build -t ghcr.io/patrick204nqh/simple-webapp:v1.5.0 .

# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u patrick204nqh --password-stdin

# Push manually  
docker push ghcr.io/patrick204nqh/simple-webapp:v1.5.0
```

## Version History

Check your versions:
- **GitHub**: Go to repo → Releases/Tags
- **GitHub Packages**: Go to repo → Packages tab to view container images

That's it! Push code → Version increments automatically → Docker image updates.