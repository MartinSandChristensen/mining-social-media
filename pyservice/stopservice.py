# -*- coding: utf-8 -*-
from logsetup import log
import signal

class StopGenerator(object):
    def __init__(self):
        self._stop = False
        def sigterm_handler(signal, frame):
            self._stop = True
            log.info("Received SIGTERM, stopping at earliest convenience.")
        signal.signal(signal.SIGTERM, sigterm_handler)

    def next(self):
        return self._stop

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self

stop = StopGenerator().next
