# Use an official Python runtime as a base image
FROM python:3.13

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the application with Uvicorn
CMD ["uvicorn", "myproject.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
