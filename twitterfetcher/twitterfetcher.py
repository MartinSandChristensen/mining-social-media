# -*- coding: utf-8 -*-
from json import loads, dumps
from logsetup import log
import os
import pika
import requests
import signal
import sys
import time
import tweepy


# Twitter access and search parameters are configured by these
# environment variables. Exits with an error if they're not found.
envvars = {}
for envvar in ('CONSUMER_KEY', 'CONSUMER_SECRET',
               'ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET',
               'TRACK'):
    val = os.getenv(envvar)
    if not val:
        sys.exit('Missing evironment variable ' + envvar)
    envvars[envvar] = val


# Set up RabbitMQ connection.
mq = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')).channel()
mq.exchange_declare(exchange='raw_tweet', type='fanout')

# In case of "docker stop twitterfetcher", call an end to festivities.
stop_stream = False
def sigterm_handler(signal, frame):
    stop_stream = True # Let tweepy finish what it's doing.
    time.sleep(1)
    sys.exit(0)
signal.signal(signal.SIGTERM, sigterm_handler)

# Define the Listener that will grab tweets from the Twitter stream.
class Listener(tweepy.StreamListener):
    def on_data(self, raw_data):
        """Only handle tweets"""
        # First, check if we should stop the stream.
        if stop_stream:
            return False

        data = loads(raw_data)
        if 'in_reply_to_status_id' in data:
            try:
                mq.basic_publish(exchange='raw_tweet',
                                 routing_key='',
                                 body=dumps(data))
            except Exception as e:
                log.error(e.message + '; choked on: ' + raw_data)

# Set up Twitter connection.
auth = tweepy.OAuthHandler(envvars['CONSUMER_KEY'], envvars['CONSUMER_SECRET'])
auth.set_access_token(envvars['ACCESS_TOKEN'], envvars['ACCESS_TOKEN_SECRET'])

INITIAL_BACKOFF = 1  # One second backoff to start with.
backoff = INITIAL_BACKOFF
while not stop_stream:
    try:
        latest_con_attempt = time.time()
        stream = tweepy.Stream(auth, Listener())
        stream.filter(track=eval(envvars['TRACK']))
    except Exception as e:
        # Exponential backoff unless five minutes have passed since last attempt.
        if (time.time() - latest_con_attempt) > 5*60:
            backoff = INITIAL_BACKOFF
        else:
            backoff = backoff*2
        log.error('Stream stopped, backing off for %d seconds; reason: %s' %
                  (backoff, e.message))
        time.sleep(backoff)
