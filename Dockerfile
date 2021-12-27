FROM python:3.7
MAINTAINER Hans Yen <ohya0915@gmail.com>

COPY . /www
WORKDIR /www

RUN apt-get update && apt-get upgrade -y && apt-get install -y python3-pip python3-dev build-essential && \
    mkdir -p /www/log &&\
    chmod -R +777 /www &&\
    pip3 install -r requirements.txt

ENV LANG C.UTF-8
CMD ["python3", "./start_api.py"]
