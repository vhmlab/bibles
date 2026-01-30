# Debian-slim based image for broader wheel compatibility and smaller build surprises
FROM python:3.14.2-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build dependencies for packages that require compilation (pydantic-core, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libssl-dev \
        python3-dev \
        cargo \
        rustc && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Create non-root user and switch
RUN useradd --create-home --shell /bin/sh appuser && chown -R appuser:appuser /app
USER appuser

# Default DB path (can be overridden at runtime with BIBLES_DB_PATH)
ENV BIBLES_DB_PATH=/app/bibles.db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
