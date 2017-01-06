FROM pyservice

RUN apt-get -y install python-tweepy \
		       python-pika
ADD twitterfetcher.py .

ENTRYPOINT ["python", "twitterfetcher.py"]
