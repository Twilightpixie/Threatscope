# ─── ThreatScope Dockerfile ───────────────────────────────────────────────────
FROM python:3.11-slim

LABEL maintainer="ThreatScope"
LABEL description="AI-powered SIEM — ThreatScope"

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpcap-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory (mounted as volume in production)
RUN mkdir -p logs models

# Health check — verifies Elasticsearch connectivity
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://${ES_HOST:-localhost}:${ES_PORT:-9200}/_cluster/health || exit 1

# Default: batch mode. Override CMD in docker-compose for streaming.
CMD ["python", "threatscope.py"]
