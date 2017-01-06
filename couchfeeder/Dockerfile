FROM pyservice

RUN apt-get -y --no-install-recommends install python-pika

ADD couchfeeder.py .

ENTRYPOINT ["python", "couchfeeder.py"]
