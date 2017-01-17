# -*- coding: utf-8 -*-

from json import loads, dumps
from logsetup import log
import mq
from requests import put
import stopservice

COUCH_URL = 'http://couchdb:5984'

# Create the database if it doesn't already exist.
res = put(COUCH_URL + '/raw_tweets')
if not res.status_code in (201, 412): # OK or already exists
    raise Exception('Error creating database: ' + res.text)


with mq.channel() as channel:
    channel.exchange_declare(exchange='raw_tweet', type='fanout')
    q = channel.queue_declare(exclusive=True)
    queue_name = q.method.queue
    channel.queue_bind(exchange='raw_tweet', queue=queue_name)

    for method_frame, properties, body in channel.consume(queue_name):
        tweet = loads(body)
        res = put(COUCH_URL + '/raw_tweets/' + tweet['id_str'], data=body)
        if not res.status_code in (201, 409): # OK or conflict
            log.error('Problem inserting tweet (' + res.text + '); data: ' + body)
        channel.basic_ack(method_frame.delivery_tag)
        if stopservice.stop():
            break
