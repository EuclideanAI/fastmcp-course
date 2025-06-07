# Use the official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_CACHE_DIR=/tmp/uv-cache

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Create a non-root user early
RUN useradd --create-home --shell /bin/bash app

# Set working directory and change ownership
WORKDIR /app
RUN chown app:app /app

# Switch to app user before any uv operations
USER app

# Copy dependency files first for better Docker layer caching
COPY --chown=app:app pyproject.toml uv.lock ./

# Install dependencies (production only)
RUN uv sync --frozen --no-dev --no-install-project

# Copy application code
COPY --chown=app:app . .

# Install the project itself
RUN uv sync --frozen --no-dev

# Expose the port
EXPOSE 8000

# Set the entrypoint to run the server
# Use server-prod.py as it's the production entry point
CMD ["uv", "run", "server.py"]
