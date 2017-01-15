# -*- coding: utf-8 -*-
import contextlib
import pika

@contextlib.contextmanager
def channel(host='rabbitmq'):
    """Get a RabbitMQ channel."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    yield channel
    try:
        channel.close()
        connection.close()
    except:
        pass
