# -*- coding: utf-8 -*-

from logsetup import log
import mq
import os
import stopservice
import subprocess
import uuid


TWEETS_PER_ARCHIVE = int(os.getenv('TWEETS_PER_ARCHIVE'))
if not TWEETS_PER_ARCHIVE:
    sys.exit('Missing environment variable TWEETS_PER_ARCHIVE')


def iterarchive():
    """Iterator to allow us to write to the same file TWEETS_PER_ARCHIVE times in a row."""
    while True:
        filename = '/data/' + str(uuid.uuid4())
        with open(filename, 'w') as archive:
            for i in range(TWEETS_PER_ARCHIVE):
                yield archive
        subprocess.call(['gzip', filename])
get_archive = iterarchive().next


# This is where the magic happens.
with mq.channel() as channel:
    channel.exchange_declare(exchange='raw_tweet', type='fanout')
    q = channel.queue_declare(exclusive=True)
    queue_name = q.method.queue
    channel.queue_bind(exchange='raw_tweet', queue=queue_name)

    for method_frame, properties, body in channel.consume(queue_name):
        get_archive().write(body + '\n')
        channel.basic_ack(method_frame.delivery_tag)
        if stopservice.stop():
            break
