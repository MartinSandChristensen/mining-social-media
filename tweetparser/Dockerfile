FROM debian:8.6

RUN mkdir /srv
WORKDIR /srv
ADD ../logsetup.py .
RUN apt-get update
RUN apt-get -y --no-install-recommends install python-pip
RUN pip install nltk # An up to date version? Yes, please.
RUN pip install pika

ADD tweetparser.py .

ENTRYPOINT ["python", "tweetparser.py"]
