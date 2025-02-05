# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the .env file
COPY .env /app/.env

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE port 80
EXPOSE 80

# Run main.py when the container launches
CMD ["python", "main.py"]
