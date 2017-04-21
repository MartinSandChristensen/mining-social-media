# -*- coding: utf-8 -*-
from json import loads, dumps
from logsetup import log
import os
import pika
import stopservice
import time
import tweepy


INITIAL_BACKOFF = 1  # One second backoff to start with.
MAX_BACKOFF = 5*60   # Stop backing off after 5 minutes.

# Twitter access and search parameters are configured by these
# environment variables. Exits with an error if they're not found.
credentials = {}
for envvar in ('CONSUMER_KEY', 'CONSUMER_SECRET',
               'ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET'):
    val = os.getenv(envvar)
    if not val:
        sys.exit('Missing evironment variable ' + envvar)
    credentials[envvar] = val


# Define the Listener that will grab tweets from the Twitter stream.
class Listener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        self.mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        self.mq_channel = self.mq_connection.channel()
        self.mq_channel.exchange_declare(exchange='raw_tweet', type='fanout')

    def on_error(self, status_code):
        log.error("Encountered error with HTTP status code " + str(status_code))

    def on_data(self, raw_data):
        """Only handle tweets"""
        print "Received message"

        # First, check if we should stop the stream.
        if stopservice.stop():
            return False

        data = loads(raw_data)
        if 'in_reply_to_status_id' in data:
            try:
                self.mq_channel.basic_publish(exchange='raw_tweet',
                                              routing_key='',
                                              body=dumps(data))
            except Exception as e:
                log.error(e.message + '; choked on: ' + raw_data)


def run(func, **args):
    """Start consuming from Twitter"""
    backoff = INITIAL_BACKOFF
    while not stopservice.stop():
        try:
            latest_con_attempt = time.time()
            listener = Listener()
            auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'],
                                       credentials['CONSUMER_SECRET'])
            auth.set_access_token(credentials['ACCESS_TOKEN'],
                                  credentials['ACCESS_TOKEN_SECRET'])

            func(listener=listener, auth=auth, **args)
        except Exception as e:
            print e
            try:
                listener.mq_channel.close()
                listener.mq_connection.close()
            except:
                pass
            # Exponential backoff unless five minutes have passed since last.
            if (time.time() - latest_con_attempt) > MAX_BACKOFF:
                backoff = INITIAL_BACKOFF
            else:
                backoff = backoff*2
            log.error('Stream stopped, backing off for %d seconds; reason: %s' %
                      (backoff, e.message))
            time.sleep(backoff)
