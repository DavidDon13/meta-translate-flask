# Base image
# FROM python:3.11.4
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . /app

# Expose the port
EXPOSE 5000

# Set the entrypoint command
CMD ["python", "app/app.py"]
