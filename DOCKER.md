# Docker Usage Guide for AIGo

This guide explains how to use AIGo with Docker for easy deployment and consistent development environments.

## Table of Contents

- [Quick Start](#quick-start)
- [Building the Image](#building-the-image)
- [Running AIGo in Docker](#running-aigo-in-docker)
- [Docker Compose Services](#docker-compose-services)
- [Development with Docker](#development-with-docker)
- [Common Use Cases](#common-use-cases)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites

- Docker 20.10 or higher
- Docker Compose 2.0 or higher

Check your installation:

```bash
docker --version
docker-compose --version
```

### Build and Run

```bash
# Build the Docker image
docker-compose build aigo

# Run a simple example
docker-compose run --rm aigo aigo /app/examples/hello.aigo

# Start REPL (when implemented)
docker-compose run --rm aigo-repl
```

## Building the Image

### Standard Build

Build the production image:

```bash
docker build -t aigo-lang:latest .
```

### Development Build

For development with all tools:

```bash
docker build -t aigo-lang:dev --target development .
```

### Multi-Platform Build

Build for multiple architectures:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t aigo-lang:latest .
```

## Running AIGo in Docker

### Execute an AIGo Script

Run a script from your current directory:

```bash
docker run --rm -v $(pwd):/workspace aigo-lang:latest aigo your_script.aigo
```

### Interactive Shell

Start an interactive shell:

```bash
docker run -it --rm aigo-lang:latest /bin/bash
```

Inside the container:

```bash
aigo examples/basics/variables.aigo
```

### REPL Mode

Run the interactive REPL (when implemented):

```bash
docker run -it --rm aigo-lang:latest aigo-repl
```

## Docker Compose Services

We provide several pre-configured services:

### 1. Main Interpreter Service

Run AIGo interpreter:

```bash
# Show help
docker-compose run --rm aigo

# Run a script
docker-compose run --rm aigo aigo /app/examples/hello.aigo

# Run your own script
docker-compose run --rm aigo aigo /workspace/my_script.aigo
```

### 2. Development Environment

Full development environment with source code:

```bash
# Start development container
docker-compose run --rm aigo-dev

# Inside container, you can:
# - Edit code
# - Run tests
# - Use debugging tools
```

### 3. REPL Service

Interactive REPL:

```bash
docker-compose run --rm aigo-repl
```

### 4. Test Runner

Run the test suite:

```bash
# Run all tests
docker-compose run --rm aigo-test

# Run specific test file
docker-compose run --rm aigo-test pytest tests/test_parser.py

# Run with coverage
docker-compose run --rm aigo-test pytest --cov=src/aigo --cov-report=html
```

### 5. Benchmark Runner

Run performance benchmarks:

```bash
docker-compose run --rm aigo-bench
```

## Development with Docker

### Volume Mounting

Mount your local directory for live development:

```bash
docker run -it --rm \
  -v $(pwd):/app \
  -v $(pwd)/workspace:/workspace \
  aigo-lang:dev \
  /bin/bash
```

### Running Tests

```bash
# Unit tests
docker-compose run --rm aigo-dev pytest tests/

# With coverage
docker-compose run --rm aigo-dev pytest --cov=src/aigo --cov-report=term

# Specific test
docker-compose run --rm aigo-dev pytest tests/test_lexer.py::TestLexer::test_tokenize
```

### Code Quality Checks

Run linters and formatters:

```bash
# Format code
docker-compose run --rm aigo-dev black src/ tests/
docker-compose run --rm aigo-dev isort src/ tests/

# Lint
docker-compose run --rm aigo-dev flake8 src/ tests/
docker-compose run --rm aigo-dev mypy src/aigo

# All checks
docker-compose run --rm aigo-dev sh -c "black --check src/ tests/ && isort --check src/ tests/ && flake8 src/ tests/ && mypy src/aigo"
```

## Common Use Cases

### 1. Running Examples

Run all examples in the examples directory:

```bash
# Single example
docker-compose run --rm aigo aigo /app/examples/basics/variables.aigo

# All basics examples
for file in examples/basics/*.aigo; do
  docker-compose run --rm aigo aigo /app/$file
done
```

### 2. Developing AIGo Programs

Create a workspace directory and develop there:

```bash
# Create workspace
mkdir -p workspace
cd workspace

# Create your AIGo program
cat > hello.aigo << 'EOF'
module main

import std.io

fn main() -> Result<void, Error> {
    io.println("Hello from Docker!")?
    return Ok(void)
}
EOF

# Run it
docker-compose run --rm aigo aigo /workspace/hello.aigo
```

### 3. CI/CD Integration

Use Docker in your CI/CD pipeline:

```yaml
# GitHub Actions example
- name: Run AIGo tests in Docker
  run: |
    docker-compose build aigo-test
    docker-compose run --rm aigo-test
```

### 4. Isolated Testing

Test different AIGo versions:

```bash
# Build specific version
docker build -t aigo-lang:1.0.0 .

# Run with specific version
docker run --rm -v $(pwd)/workspace:/workspace aigo-lang:1.0.0 aigo script.aigo
```

## Environment Variables

Configure AIGo behavior with environment variables:

```bash
# Enable debug mode
docker run --rm -e AIGO_DEBUG=1 aigo-lang:latest aigo script.aigo

# Set custom paths
docker run --rm \
  -e AIGO_HOME=/custom/path \
  -e PYTHONPATH=/app/src \
  aigo-lang:latest aigo script.aigo
```

Available variables:

- `AIGO_DEBUG`: Enable debug output (0 or 1)
- `AIGO_HOME`: AIGo installation directory
- `PYTHONPATH`: Python module search path
- `PYTHONUNBUFFERED`: Force unbuffered output (default: 1)

## Performance Considerations

### Image Size

The production image is optimized for size:

```bash
# Check image size
docker images aigo-lang:latest

# Expected: ~200-300 MB
```

### Build Cache

Use BuildKit for better caching:

```bash
export DOCKER_BUILDKIT=1
docker build -t aigo-lang:latest .
```

### Multi-Stage Builds

For even smaller images:

```dockerfile
# Future enhancement: separate build and runtime stages
FROM python:3.11-slim AS builder
# ... build steps

FROM python:3.11-slim AS runtime
COPY --from=builder /app /app
```

## Troubleshooting

### Permission Issues

If you encounter permission issues with mounted volumes:

```bash
# Run as current user
docker run --rm \
  -u $(id -u):$(id -g) \
  -v $(pwd):/workspace \
  aigo-lang:latest aigo script.aigo
```

### Python Module Not Found

Ensure PYTHONPATH is set correctly:

```bash
docker run --rm \
  -e PYTHONPATH=/app/src \
  aigo-lang:latest python -c "import aigo; print(aigo.__version__)"
```

### Container Won't Start

Check logs:

```bash
docker-compose logs aigo
docker logs aigo-interpreter
```

### Out of Memory

Increase Docker memory limit:

```bash
# In docker-compose.yml, add:
services:
  aigo:
    mem_limit: 512m
```

### Clean Up

Remove all AIGo containers and images:

```bash
# Stop all containers
docker-compose down

# Remove images
docker rmi aigo-lang:latest aigo-lang:dev

# Clean system
docker system prune -a
```

## Best Practices

### 1. Use .dockerignore

Always use `.dockerignore` to exclude unnecessary files:

```
__pycache__/
*.pyc
.git/
venv/
```

### 2. Layer Caching

Order Dockerfile commands from least to most frequently changing:

```dockerfile
# Good: dependencies first
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/

# Bad: source code first (cache invalidated often)
COPY . .
RUN pip install -r requirements.txt
```

### 3. Security

- Don't run as root in production
- Use specific version tags
- Scan images for vulnerabilities

```bash
# Run as non-root user
docker run --rm -u 1000:1000 aigo-lang:latest aigo script.aigo

# Scan for vulnerabilities
docker scan aigo-lang:latest
```

### 4. Reproducible Builds

Pin all versions:

```dockerfile
FROM python:3.11.5-slim  # Specific version
RUN pip install package==1.2.3  # Pinned versions
```

## Advanced Usage

### Custom Entrypoint

Create a custom entrypoint script:

```bash
# entrypoint.sh
#!/bin/bash
set -e

if [ "$1" = "test" ]; then
  pytest tests/
elif [ "$1" = "repl" ]; then
  aigo-repl
else
  exec "$@"
fi
```

### Debugging

Debug inside container:

```bash
# Install debugging tools
docker run -it --rm \
  aigo-lang:dev \
  sh -c "pip install ipdb && python -m ipdb script.py"
```

### Health Checks

Add health check to docker-compose.yml:

```yaml
services:
  aigo:
    healthcheck:
      test: ["CMD", "aigo", "--version"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [AIGo Main README](README.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## Support

For Docker-specific issues:

- Check existing issues: [GitHub Issues](https://github.com/aigo-lang/aigo/issues)
- Docker tag: Use `docker` label when creating issues
- Community: [GitHub Discussions](https://github.com/aigo-lang/aigo/discussions)

---

**Note**: Some features like REPL are under development. This documentation will be updated as new features are released.
