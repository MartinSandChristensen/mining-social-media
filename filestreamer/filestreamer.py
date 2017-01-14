# -*- coding: utf-8 -*-

from logsetup import log
import os
import pika
import subprocess
import uuid

TWEETS_PER_ARCHIVE = int(os.getenv('TWEETS_PER_ARCHIVE'))
if not TWEETS_PER_ARCHIVE:
    sys.exit('Missing environment variable TWEETS_PER_ARCHIVE')

# Set up RabbitMQ channel.
channel = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')).channel()
channel.exchange_declare(exchange='raw_tweet', type='fanout')
q = channel.queue_declare(exclusive=True)
queue_name = q.method.queue
channel.queue_bind(exchange='raw_tweet', queue=queue_name)


def iterarchive():
    """Iterator to allow us to write to the same file TWEETS_PER_ARCHIVE times in a row."""
    while True:
        filename = '/data/' + str(uuid.uuid4())
        with open(filename, 'w') as archive:
            for i in range(TWEETS_PER_ARCHIVE):
                yield archive
        subprocess.call(['gzip', filename])
get_archive = iterarchive().next

def filestreamer_callback(channel, method, properties, body):
    """When a message arrives on the queue, write it to an archive."""
    get_archive().write(body + '\n')

channel.basic_consume(filestreamer_callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
