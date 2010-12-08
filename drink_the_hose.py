#!/usr/bin/python
"""
Script to display information from the twitter stream

To print the text of tweets from the twitter garden hose:
$ python drink_the_hose.py -u your_name

To print the text of tweets that contain a smiley face:
$ python drink_the_hose.py -u your_name ":-)"

"""
from optparse import OptionParser
from getpass import getpass

import tweepy

class EchoListener(tweepy.StreamListener):
    def on_status(self, status):
        print '-'*10
        print status.text
        return

def drink(username, password, stringlist=[]):
    auth = tweepy.BasicAuthHandler(username, password)
    listener = EchoListener()
    stream = tweepy.Stream(auth, listener)
    try:
        if stringlist:
            stream.filter(track = stringlist)
        else:
            stream.sample()
    except:
        print "Bye!"
        stream.disconnect()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username", help= "Twitter username", default=None)
    parser.add_option("-p", "--password", dest="password", help= "Twitter password", default=None)

    (options, args) = parser.parse_args()
    if options.username is None:
        options.username = options.raw_input()
    if options.password is None:
        options.password = getpass()
        
    drink(username=options.username, password=options.password, stringlist=args)

