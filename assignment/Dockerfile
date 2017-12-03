# Set the base image
FROM python:2.7

# File Author / Maintainer
MAINTAINER bjg

# Update the sources list
RUN apt-get update

# Update the sources list
RUN apt-get -y upgrade

# Copy the application folder inside the container
ADD /my_application /my_application

# Get pip to download and install requirements:
RUN pip install -r /my_application/requirements.txt

# Expose listener port
EXPOSE 5000

# Set the default directory where CMD will execute
WORKDIR /my_application
RUN mkdir /data
# Set the default command to execute
# when creating a new container
CMD python app.py
