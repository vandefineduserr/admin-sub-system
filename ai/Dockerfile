# Base python package
FROM python:3.11-slim-buster

# Working directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the files
COPY . .

# Executable commands
CMD [ "python3", "app.py"]
