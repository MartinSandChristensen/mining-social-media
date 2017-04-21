FROM pyservice

RUN apt-get -y install python-tweepy \
		       python-pika
ADD twitterfetcher.py .
ADD twitterutils.py .

ENTRYPOINT ["python", "twitterfetcher.py"]
