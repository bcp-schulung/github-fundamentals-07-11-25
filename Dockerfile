# Use a lightweight Python base image
FROM python:3.12-slim

# Environment settings for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install runtime dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create and use a non-root user
RUN useradd -m appuser
USER appuser

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]