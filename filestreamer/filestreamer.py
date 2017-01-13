# -*- coding: utf-8 -*-

from logsetup import log
import os
import pika
import subprocess
import uuid


# Set up RabbitMQ channel.
channel = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq')).channel()
channel.exchange_declare(exchange='raw_tweet', type='fanout')
q = channel.queue_declare(exclusive=True)
queue_name = q.method.queue
channel.queue_bind(exchange='raw_tweet', queue=queue_name)


def filestreamer_callback(channel, method, properties, body):
    while True:
        filename = '/data/' + str(uuid.uuid4())
        with archive as open(filename, 'w'):
            for i in range(10000):
                archive.write(body + '\n')
        subprocess.call(['gzip', filename])

channel.basic_consume(filestreamer_callback,
                      queue=queue_name,
                      no_ack=True)
channel.start_consuming()
