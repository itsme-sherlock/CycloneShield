# ==============================================================================
# CycloneShield - Production Container for Google Cloud Run
# ==============================================================================
# Multi-hazard tropical cyclone vulnerability forecaster & emergency command center.
# Optimized for Google Cloud Run serverless container runtime (HTTP/1.1 & HTTP/2).
#
# Free Tier Compliance:
#   - Conforms to Cloud Run 2 Million Free Requests/Month
#   - Stateless execution with non-root security context
#   - Dynamic PORT binding ($PORT default: 8080)
# ==============================================================================

FROM python:3.11-slim

# Prevent Python from writing pyc files & buffer stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    STREAMLIT_SERVER_PORT=8080 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Install minimal OS dependencies for geospatial packages, font rendering, & healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgdal-dev \
    libgeos-dev \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated non-root application user
RUN useradd -m -u 10001 -s /bin/bash appuser

WORKDIR /app

# Cache dependency installation layer
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application source code and pre-computed artifacts
COPY . /app

# Assign ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose standard Cloud Run HTTP container port
EXPOSE 8080

# Cloud Run Container Health Check
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/_stcore/health || exit 1

# Launch Streamlit Command Center with dynamic Cloud Run PORT binding
ENTRYPOINT ["sh", "-c", "streamlit run cycloneshield/app.py --server.port=${PORT:-8080} --server.address=0.0.0.0"]
