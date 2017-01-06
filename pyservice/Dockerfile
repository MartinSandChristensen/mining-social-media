FROM debian:8.6

RUN mkdir /dockerservice
WORKDIR /dockerservice
ADD logsetup.py .
RUN apt-get update
RUN apt-get -y --no-install-recommends install python-requests \
                                               python-pip
