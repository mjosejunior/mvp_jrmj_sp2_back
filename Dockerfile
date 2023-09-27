# Dockerfile

# Use a lightweight Python image
FROM python:3.11.5-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 5001

# Command to run the application
CMD ["python", "app.py"]
