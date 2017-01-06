# -*- coding: utf-8 -*-

from json import loads, dumps
import logging
import pika
from requests import get, put

COUCH_URL = 'http://couchdb:5984'

log = logging.getLogger('couchfeeder')

# Create the database if it doesn't already exist.
res = put(COUCH_URL + '/raw_tweets')
if not res.status_code in (201, 412): # OK or already exists
    raise Exception('Error creating database: ' + res.text)

# Set up RabbitMQ channel.
channel = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')).channel()
channel.exchange_declare(exchange='raw_tweet', type='fanout')
q = channel.queue_declare(exclusive=True)
queue_name = q.method.queue
channel.queue_bind(exchange='raw_tweet', queue=queue_name)


def couchfeeder_callback(channel, method, properties, body):
    tweet = loads(body)
    res = put(COUCH_URL + '/raw_tweets/' + tweet['id_str'], data=body)
    if not res.status_code in (201, 409):
        logging.error('Problem parsing tweet (' + res.text + '); data: ' + body)

channel.basic_consume(couchfeeder_callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
