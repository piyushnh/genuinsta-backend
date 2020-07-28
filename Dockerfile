# pull official base image
FROM python:3.5.2-slim

# set work directory
# WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /genuinstagram_backend

# Set the working directory to /music_service
WORKDIR /genuinsta_backend


RUN apt-get update 
RUN apt-get install -y gdal-bin python3-gdal

RUN apt-get install -y gcc python-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get install -y libgdal-dev

RUN pip uninstall -y stream-framework 

# RUN apt-get install -y redis-server
# RUN apt-get install postgres

# Copy the current directory contents into the container at /music_service
COPY . /genuinsta_backend/