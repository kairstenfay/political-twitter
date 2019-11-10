"""
Searches Twitter for tweets matching a query.

Returns only Tweets coded in English.
"""
import os
import json
import tweepy
import logging
import argparse
from typing import Any, List


LOG = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="""
    Search Twitter for Tweets. Returns the most popular Tweets until 2019-11-08 coded in English.""")
parser.add_argument('-q', metavar='<query>', type=str,
                    help='a query phrase to send to Twitter\'s Search API.')
args = parser.parse_args()


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'],
        os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'],
        os.environ['TWITTER_ACCESS_SECRET'])

    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        compression=True)

    for tweet in tweepy.Cursor(api.search, q=args.q, result_type='mixed', until='2019-11-08', tweet_mode='extended',
        ).items(5000):

        details = tweet._json

        if details['metadata']['iso_language_code'] != 'en' and details['lang'] != 'en':
            continue

        print(json.dumps(details))


# avg num followers; top tweet hashtags ; top user hashtags ; top emojis ; sentiment score
