FROM andrejreznik/python-gdal:stable

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# RUN env

RUN mkdir /project && \
    mkdir /project/static && \
    mkdir /api_media

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

COPY ./docker/wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for

RUN apt-get -o Acquire::http::proxy=$HTTP_PROXY -q update && \
    apt-get -o Acquire::http::proxy=$HTTP_PROXY -qy install netcat

WORKDIR /project
    