# Builds the container image for our fleet optimization application.

FROM python:3.9-slim

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory.
WORKDIR /app

# Install system dependencies.
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application source code.
COPY . /app/

# Expose the application port.
EXPOSE 8000

# Define entrypoint.
CMD ["uvicorn", "src.services.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]
