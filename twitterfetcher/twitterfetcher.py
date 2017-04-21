# -*- coding: utf-8 -*-
from logsetup import log
import os
import requests
import stopservice
import sys
import time
import tweepy
import twitterutils


# Search string for the Twitter stream.
expr = os.getenv('TRACK')
if not expr:
    sys.exit('Missing evironment variable TRACK')
expr = eval(expr)


def track(listener=None, auth=None, expr=None):
    """Search the Twitter stream for a given expression"""
    log.info("Start listening for expression " + str(expr))
    stream = tweepy.Stream(auth, listener)
    stream.filter(track=expr)


log.info('Starting service.')
twitterutils.run(track, expr=expr)
