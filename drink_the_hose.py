#!/usr/bin/python
"""
Script to display information from the twitter stream

To print the text of tweets from the twitter garden hose:
$ python drink_the_hose.py -u your_name

To print the text of tweets that contain a smiley face:
$ python drink_the_hose.py -u your_name ":-)"

To only limit to 10 returns:
$ python drink_the_hose.py -u your_name -l 10

To get help:
$ python drink_the_hose.py --help
"""
from optparse import OptionParser
from getpass import getpass
from collections import deque
import time
from time import sleep
import logging

import tweepy
from tweepy.models import Status
from tweepy.utils import import_simplejson
from tweepy.api import API
json = import_simplejson()
api = API()

BACKOFF = 0.5 #Initial wait time before attempting to reconnect
MAX_BACKOFF = 300 #Maximum wait time between connection attempts
UNICODE_LINES = (u'\u000a', u'\u000b', u'\u000c', u'\u000d', u'\u0085', u'\u2028', u'\u2029')
logging.basicConfig(level=logging.INFO)

class EchoListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        try:
            self.queue = deque(maxlen = kwargs['maxlen'])
            del kwargs['maxlen']
        except KeyError:
            self.queue = deque(maxlen = 1000)
        super(EchoListener, self).__init__(*args, **kwargs)

    def on_data(self, data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """
        if 'in_reply_to_status_id' in data: 
            self.queue.append(data)
            logging.debug("Append data (%s)"%(len(self.queue)))
            return True

        elif 'delete' in data:
            logging.debug('Delete received')
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            logging.info('Limit received')
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False

    def connect(self, username, password, stringlist=[], async=True):
        self.stream = tweepy.Stream(username, password, self)
        try:
            if stringlist:
                self.stream.filter(track = stringlist, async=async)
            else:
                self.stream.sample(async=async)
            logging.debug('Connected to twitter')
        except:
            self.stream.disconnect()
            logging.debug('Something went wrong - disconnected from twitter')

    def running(self):
        return self.stream.running

    def disconnect(self):
        return self.stream.disconnect()

class AbstractConsumer(object):
    """Consumes tweets"""
    def process(self, tweet):
       raise NotImplementedError

class Lineprinter(AbstractConsumer):
    def process(self, tweet):
        status = Status.parse(api, json.loads(tweet))
        for lf in UNICODE_LINES:
            text = status.text.replace(lf, ' ')
        print "@%s (%s, %s, %s, %s): %s"%(status.user.screen_name, 
            status.user.lang, status.user.statuses_count, status.user.friends_count, 
            status.user.followers_count, text)

class Rawprinter(AbstractConsumer):
    def process(self, tweet):
        print tweet

def drink(username, password, stringlist=[], limit=0, maxlen=1000, consumers=[Rawprinter()]):
    listener = EchoListener(maxlen=maxlen)
    listener.connect(username, password, stringlist=stringlist)
    count = 0
    backoff = BACKOFF
    backoff_warning = False
    #Consume tweets until the queue is empty, and then wait
    try:
        while True:
            if listener.running and (not limit or count < limit):
                    logging.debug('Try and get a tweet from the queue ...')
                    try:
                        tweet = listener.queue.popleft()
                        count += 1
                        logging.debug('... pulled tweet %s from the queue (%s)'%(count, len(listener.queue)))
                        for consumer in consumers:
                            try:
                                consumer.process(str(tweet))
                            except:
                                logging.warn("Something went wrong with the consumer %s on the tweet %s"%(consumer, tweet))
                    except IndexError:
                        logging.debug('... queue empty, wait a while')
                        time.sleep(1)
            elif not limit or count < limit:
                try:
                    logging.debug("Wait %i s before reconnecting"%(backoff,))
                    time.sleep(backoff)
                    listener = EchoListener(maxlen=maxlen)
                    listener.connect(username, password, stringlist=stringlist)
                    if listener.running:
                        backoff = BACKOFF
                        backoff_warning = False
                finally:
                    backoff = min(MAX_BACKOFF, backoff*2)
                    if backoff == MAX_BACKOFF and not backoff_warning:
                        logging.warn('Having trouble connecting to twitter')
                        backoff_warning = True
            elif count >= limit:
                logging.debug('Limit reached')
                break
    finally:
        listener.disconnect()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username", help= "Twitter username", default=None)
    parser.add_option("-p", "--password", dest="password", help= "Twitter password", default=None)
    parser.add_option("-l", "--limit", dest="limit", help= "Number of status updates to harvest", default=0, type='int')

    (options, args) = parser.parse_args()
    if options.username is None:
        options.username = raw_input()
    if options.password is None:
        options.password = getpass()
        
    drink(username=options.username, password=options.password, limit=options.limit, stringlist=args)

