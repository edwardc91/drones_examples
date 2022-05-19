FROM python:3.8.9-buster

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# RUN env

RUN mkdir /project && \
    mkdir /project/static 

# Change the working directory. 
# Every command after this will be run from the /project directory.
WORKDIR /project

# Copy the requirements.txt file.
COPY ./api/requirements.txt /project/


#RUN pip install --upgrade pip
# RUN apt update && \
# apt install -y 

# Install the requirements.
RUN pip install -r requirements.txt && pip install uwsgi

WORKDIR /project
    