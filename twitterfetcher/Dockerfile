FROM debian:8.6

RUN mkdir /srv
WORKDIR /srv
ADD ../logsetup.py .
RUN apt-get update
RUN apt-get -y install python-requests \
		       python-tweepy \
		       python-pika
ADD twitterfetcher.py .

ENTRYPOINT ["python", "twitterfetcher.py"]
