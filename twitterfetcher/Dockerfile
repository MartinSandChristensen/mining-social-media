FROM debian

RUN apt-get update && apt-get -y install python-requests \
					 python-tweepy \
					 python-pika
ADD slurp.py .

ENTRYPOINT ["python", "slurp.py"]
