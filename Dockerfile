# Use a base image with Python
FROM python:3.9-slim


# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libhdf5-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

    
# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the environment variables (if any)
ENV FLASK_ENV=production

# Expose the port the app runs on
EXPOSE 9010

# Command to run the app
CMD ["python", "app/main.py"]
