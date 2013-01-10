# Drink the hose

Script to display or save tweets from the twitter stream. This shows how to use the python tweepy library to access
the twitter streaming API.

## Setup

1. Install tweepy `sudo pip install tweepy`
2. Grab this code `git clone git://github.com/edwardabraham/drink_the_hose.git`
3. Make a file `secrets.py` in the drink_the_hose directory that has your twitter access credentials in
  it. This file should contain the following string variables: `consumer_key`, `consumer_secret`, `access_token`, `access_token_secret`. 
  To get these keys, you need to create a [twitter app](https://dev.twitter.com/apps).

## Usage

To get help:
`python drink_the_hose.py --help`

To print the text of tweets from the twitter garden hose:
`python drink_the_hose.py`

To print the text of tweets that contain a smiley face:
`python drink_the_hose.py -u your_name ":-)"`

To only limit to 10 returns, specifiy a limit:
`python drink_the_hose.py -u your_name -l 10`

To save the tweets to file as JSON, specify a path:
`python drink_the_hose.py -p stash`

