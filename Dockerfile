FROM python:3.7-alpine

RUN apk update && apk add git

# create user(app)
RUN adduser -h /home/app -S app

# set home dir
ENV HOME=/home/app

# copy package file
COPY requirements.txt $HOME/calconv/
RUN chown -R app $HOME/*

# set workdir
USER app
WORKDIR $HOME/calconv

USER root
# install dependency
RUN pip install -r requirements.txt
# copy source file
COPY . $HOME/calconv
RUN chown -R app $HOME/*
USER app

# run
CMD ["python3"]

