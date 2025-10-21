# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY pyproject.toml Pipfile Pipfile.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy

# Copy application code
COPY . .

# Build the frontend
WORKDIR /app/client
RUN npm install && npm run build
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=app.web
ENV PYTHONPATH=/app

# Default command (can be overridden in Koyeb)
CMD ["flask", "--app", "app.web", "run", "--host", "0.0.0.0", "--port", "8000"]
