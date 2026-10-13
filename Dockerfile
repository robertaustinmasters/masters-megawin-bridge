# Use the official lightweight Python image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core bridge script
COPY main.py .

# Render injects the PORT env var; the app binds to it inside the container
ENV PORT=10000
EXPOSE 10000

# Command to execute the application binding to the cloud-assigned PORT
CMD ["python", "main.py"]