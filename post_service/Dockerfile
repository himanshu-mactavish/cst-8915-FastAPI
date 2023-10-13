# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the service code into the container
COPY post_service.py /app/post_service.py

# Install FastAPI, Uvicorn, and requests library
RUN pip install fastapi uvicorn requests

# Expose the port on which the service will run
EXPOSE 8002

# Command to run the service
CMD ["uvicorn", "post_service:app", "--host", "0.0.0.0", "--port", "8002"]
