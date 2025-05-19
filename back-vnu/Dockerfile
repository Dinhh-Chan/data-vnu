FROM python:3.10-slim

WORKDIR /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies (bao gồm psql)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install watchdog
RUN pip install watchdog

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install pydantic-settings

# Copy project
COPY . /app/

# Copy and make start.sh executable
COPY start.sh /app/
RUN chmod +x /app/start.sh
