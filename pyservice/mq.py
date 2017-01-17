# -*- coding: utf-8 -*-
import contextlib
from logsetup import log
import pika
import time

@contextlib.contextmanager
def channel(host='rabbitmq'):
    """Get a RabbitMQ channel."""
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host))
            channel = connection.channel()
        except:
            log.error("Couldn't connect to RabbitMQ; retrying in a bit.")
            sleep.sleep(5)
        else:
            break
    yield channel
    try:
        channel.close()
        connection.close()
    except:
        pass
