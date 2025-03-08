# Use official Python image
FROM python:3.8

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 5000
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]

