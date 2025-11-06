# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set metadata
LABEL maintainer="AIGo Development Team"
LABEL description="AIGo Programming Language - Interpreter Container"
LABEL version="1.0.0-beta"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    AIGO_HOME=/app

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY pyproject.toml setup.py ./
COPY src/ ./src/
COPY examples/ ./examples/
COPY README.md LICENSE CHANGELOG.md ./

# Install AIGo in editable mode
RUN pip install -e .

# Create directory for user scripts
RUN mkdir -p /workspace

# Set working directory to workspace
WORKDIR /workspace

# Verify installation
RUN aigo --version || echo "AIGo installation check"

# Default command: show help
CMD ["aigo", "--help"]

# For REPL mode, use: docker run -it aigo aigo-repl
# For running a script: docker run -v $(pwd):/workspace aigo aigo your_script.aigo
