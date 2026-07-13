# Dockerized ML Deployment

**Status:** 🚀 Completed  
**Tech Stack:** Docker, FastAPI, Python, Scikit-learn, Linux

## Overview
"It works on my machine" is a phrase ML Engineers avoid at all costs. This project solves that problem by taking a machine learning REST API (built with FastAPI and Scikit-learn) and packaging it into a **Docker Container**. 

By containerizing the application, we guarantee that the model, its dependencies, the web server, and the operating system environment remain perfectly identical whether it is running on a local laptop, a Kaggle notebook, or a production AWS server.

The Dockerfile
(Included here for quick reference)

## Dockerfile
```
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 for the FastAPI server
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

## Setup & Installation

Navigate to the project directory:

```Bash
Build the Docker Image:
```
```Bash
docker build -t ml-fastapi-app .
```
```Bash
docker run -p 8000:8000 ml-fastapi-app
Test the Live API:
```

Open your browser and navigate to the API docs: http://localhost:8000/docs

The API is now running completely isolated from your local machine!

## Architecture & Flow
1. **The Base Image:** The Dockerfile starts from a lightweight Linux Python image (`python:3.10-slim`) to keep the container size small and deployment fast.
2. **Dependency Isolation:** The `requirements.txt` is copied and installed inside the container independently of the host machine, preventing package version conflicts.
3. **Application Porting:** The trained model (`.joblib`) and the FastAPI server (`main.py`) are copied into the container's working directory.
4. **Network Binding:** The container exposes port `8000`. Uvicorn is instructed to run on host `0.0.0.0` so that the API can accept incoming HTTP requests from outside the isolated Docker network.                       # This documentation