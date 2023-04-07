# Use the official Python base image
FROM python:3.10
# Set the working directory
WORKDIR /app
# Update the Debian OS
RUN apt-get update -y && \
    apt-get upgrade -y
# Copy the requirements file into the container
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
# Install detectron2, used to read JPG file
RUN pip install 'git+https://github.com/facebookresearch/detectron2.git'
# Copy the rest of the application into the container
COPY . .
# Make port 5000 available to the world outside this container
EXPOSE 5000
# Define environment variable
ENV FLASK_APP=server.py
# Run app
CMD ["gunicorn", "--bind", "0.0.0.0:8000","--timeout","0", "server:app"]

