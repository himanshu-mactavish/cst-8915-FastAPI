# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the service code into the container
COPY user_service.py /app/user_service.py

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn

# Expose the port on which the service will run
EXPOSE 8001

# Command to run the service
CMD ["uvicorn", "user_service:app", "--host", "0.0.0.0", "--port", "8001"]
