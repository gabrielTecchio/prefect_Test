# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Prefect
ENV PREFECT_API_URL="http://prefect-server:4200/api"

# Expose the port that Streamlit runs on
EXPOSE 4200

# Command to start the Prefect worker and connect to the specified work pool
CMD ["prefect", "worker", "start", "--pool", "my-work-pool"]