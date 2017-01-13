FROM pyservice

RUN apt-get -y --no-install-recommends install python-pika

ADD filestreamer.py .
RUN mkdir /data

ENTRYPOINT ["python", "filestreamer.py"]
