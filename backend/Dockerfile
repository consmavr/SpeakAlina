# Use official Python base image
FROM python:3.11-slim

# Install ffmpeg & cleanup
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment variables
ENV PORT=8082
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8082

# Start the Flask app
CMD ["python", "app.py"]
