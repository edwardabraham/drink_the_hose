# Drink the hose

Script to display or save tweets from the twitter stream. This shows how to use the python tweepy library to access
the twitter streaming API.

# Example

The command
```
python drink_the_hose.py -l 5 ":-)"
```
grabs 5 tweets that contain smiley face. Each tweet is printed on a separate line, with the user name, the user
declared language, the number of tweets that user has made, the number of their friends, and the number of the followers:

```
@LutfiWijayanto (en, 3584, 44, 15): @HarukaN_JKT48 ohayou gon. Luar biasa.. :-)
@joaco_iturrieta (es, 158, 69, 22): Triunfo historico de chile en argentima :-) grande chile
@BhabhyAngela (en, 17571, 308, 732): @itsmejeremias @ravuena1 nabasa ko na :-)
@GuvRai (en, 14603, 1648, 1214): @andy_round oh I read them ages ago :-) But yea pretty much along the same lines :-) xx
@JessicaCHarris (en, 11963, 239, 173): Oh man, baby took me to see the hobbit :-) soooooo good
```

## Setup

1. Install tweepy `sudo pip install tweepy` (requires python 2.x)
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

