# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code and data directories
COPY src/ ./src
COPY data/ ./data

# Command to run the application
CMD [ "python", "-u", "src/pipeline.py" ]