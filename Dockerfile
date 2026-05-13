# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 8004 to allow communication to the Uvicorn server
EXPOSE 8004

# Define the command to run your app on port 8004
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]