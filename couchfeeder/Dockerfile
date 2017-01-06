FROM debian:8.6

RUN mkdir /srv
WORKDIR /srv
ADD ../logsetup.py .
RUN apt-get update
RUN apt-get -y --no-install-recommends install python-requests \
    	       			       	       python-pika

ADD couchfeeder.py .

ENTRYPOINT ["python", "couchfeeder.py"]
