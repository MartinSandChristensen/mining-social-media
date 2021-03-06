# -*- coding: utf-8 -*-

from json import loads, dumps
from logsetup import log
import nltk.tokenize
import pika

COPY_FIELDS = ['retweet_count', 'lang', 'created_at']

# Set up RabbitMQ receiver and sender channels.
rec_channel = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')).channel()
rec_channel.exchange_declare(exchange='raw_tweet', type='fanout')
q = rec_channel.queue_declare(exclusive=True)
queue_name = q.method.queue
rec_channel.queue_bind(exchange='raw_tweet', queue=queue_name)

send_channel = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')).channel()
send_channel.exchange_declare(exchange='parsed_tweet', type='fanout')

# Define our tokenizer callback function. This is where the magic happens.
tokenize = nltk.tokenize.TweetTokenizer().tokenize
def parser_callback(channel, method, properties, body):
    """Parse and tokenise tweets on the queue, then output to another queue."""
    try:
        body = loads(body)
        tweet = {}
        tweet['tokens'] = tokenize(body['text'])
        tweet['user'] = body['user']['id_str']
        for field in COPY_FIELDS:
            tweet[field] = body[field]
        send_channel.basic_publish(exchange='parsed_tweet',
                                   routing_key='',
                                   body=dumps(tweet))
    except Exception, e:
        log.error(e.message + '; choked on: ' + repr(body))

rec_channel.basic_consume(parser_callback,
                          queue=queue_name,
                          no_ack=True)
rec_channel.start_consuming()
