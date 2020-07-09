# pull official base image
FROM python:3.5.2-alpine

# set work directory
# WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /genuinstagram_backend

# Set the working directory to /music_service
WORKDIR /genuinsta_backend

# Copy the current directory contents into the container at /music_service
ADD . /genuinsta_backend/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt