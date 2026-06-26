# Use an official lightweight Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first (so Docker can cache this layer if code changes but deps don't)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code into the container
COPY . .

# Tell Docker which port the app runs on
EXPOSE 8000

# Command to run the app when the container starts
CMD ["python", "app.py"]