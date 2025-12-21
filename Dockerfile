# Use official Python image
FROM python:3.12-slim

# Set work directory
WORKDIR /code

# Install system dependencies (for Pillow, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run server (we'll override with docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]