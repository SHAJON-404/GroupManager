# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables to prevent python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies if any are needed (none for this bot)
# Copy requirements file first to take advantage of Docker caching
COPY requirements.txt /app/

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Run the application
CMD ["python", "main.py"]
