# -*- coding: utf-8 -*-

from json import loads, dumps
from logsetup import log
import nltk.tokenize
import pika


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
    try:
        body = loads(body)
        tweet = {}
        tweet['tokens'] = tokenize(body['text'])
        tweet['retweet_count'] = body['retweet_count']
        tweet['lang'] = body['lang']
        tweet['created_at'] = body['created_at']
        tweet['user'] = body['user']['id_str']
        send_channel.basic_publish(exchange='parsed_tweet',
                                   routing_key='',
                                   body=dumps(tweet))
    except Exception, e:
        log.error(repr(e) + '; choked on: ' + repr(body))

rec_channel.basic_consume(parser_callback,
                          queue=queue_name,
                          no_ack=True)
rec_channel.start_consuming()
