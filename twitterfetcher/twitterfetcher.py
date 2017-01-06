# -*- coding: utf-8 -*-
import json
from logsetup import log
import os
import pika
import requests
import sys
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

# Define the Listener that will grab tweets from the Twitter stream.
class Listener(tweepy.StreamListener):
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if 'in_reply_to_status_id' in data:
            try:
                mq.basic_publish(exchange='raw_tweet', routing_key='', body=raw_data)
            except Error, e:
                log.error(e + '; choked on: ' + raw_data)

# Set up Twitter connection.
auth = tweepy.OAuthHandler(envvars['CONSUMER_KEY'], envvars['CONSUMER_SECRET'])
auth.set_access_token(envvars['ACCESS_TOKEN'], envvars['ACCESS_TOKEN_SECRET'])

stream = tweepy.Stream(auth, Listener())
stream.filter(track=eval(envvars['TRACK']))
