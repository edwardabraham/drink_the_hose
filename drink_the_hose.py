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

import httplib
from socket import timeout
from threading import Thread
from time import sleep
import urllib

import tweepy
from tweepy.models import Status
from tweepy.utils import import_simplejson
json = import_simplejson()

class NoisyStream(tweepy.Stream):
    def _run(self):
        # setup
        self.auth.apply_auth(None, None, self.headers, None)

        # enter loop
        error_counter = 0
        conn = None
        while self.running:
            if self.retry_count and error_counter > self.retry_count:
                # quit if error count greater than retry count
                break
            try:
                conn = httplib.HTTPConnection(self.host)
                conn.connect()
                conn.sock.settimeout(self.timeout)
                conn.request('POST', self.url, self.body, headers=self.headers)
                resp = conn.getresponse()
                if resp.status != 200:
                    if self.listener.on_error(resp.status) is False:
                        break
                    error_counter += 1
                    sleep(self.retry_time)
                else:
                    error_counter = 0
                    self._read_loop(resp)
            except timeout:
                if self.listener.on_timeout() == False:
                    break
                if self.running is False:
                    break
                conn.close()
                sleep(self.snooze_time)
            except Exception:
                # any other exception is fatal, so kill loop
                raise
                break

        # cleanup
        self.running = False
        if conn:
            conn.close()


class EchoListener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        try:
            self.count = 0
            self.limit = kwargs['limit']
            del kwargs['limit']
        except KeyError:
            self.limit = 0
        super(EchoListener, self).__init__(*args, **kwargs)

    def on_data(self, data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """
        if 'in_reply_to_status_id' in data:
            status = Status.parse(self.api, json.loads(data))
            #status = data
            if self.on_status(status) is False:
                return False
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False

    def on_status(self, status):
        print '-'*10
        print "%s (%s): %s"%(status.user.name, status.user.lang, status.text)
        self.count += 1
        if self.limit and (self.count > self.limit):
            return False
        return True

def drink(username, password, stringlist=[], limit=0):
    listener = EchoListener(limit=limit)
    stream = NoisyStream(username, password, listener)
    print 'streaming'
    try:
        if stringlist:
            stream.filter(track = stringlist, async=True)
        else:
            print 'sample'
            stream.sample(async=True)
    except:
        raise
        stream.disconnect()

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

