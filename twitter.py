import os
import json
import tweepy
import logging
import argparse
from typing import Any, List


LOG = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Search Twitter for Tweets.')
parser.add_argument('-q', metavar='<query>', type=str,
                    help='a query phrase to send to Twitter\'s Search API.')
args = parser.parse_args()

def place(details: dict) -> str:
    if details.get("place", None):
        return details["place"]["full_name"]

def possibly_sensitive(details: dict) -> dict:
    return details.get("possibly_sensitive", None)

def lang(details: dict) -> str:
    return details.get("lang", None)


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'],
        os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'],
        os.environ['TWITTER_ACCESS_SECRET'])

    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True,
        compression=True)

    for tweet in tweepy.Cursor(api.search, q=args.q, result_type='mixed', until='2019-11-07', tweet_mode='extended',
        ).items(5000):

        details = tweet._json

        if details['metadata']['iso_language_code'] != 'en' and details['lang'] != 'en':
            continue

        data = {
            'location': details.get('location', 'None'),
            'place': place(details),
            'user_location': details['user'].get('location', 'None'),
            'possibly_sensitive': possibly_sensitive(details),
            'lang': details.get('lang'),
            'text': details.get('text'),
        }

        # if data['possibly_sensitive']:
        #     continue

        # print('checking locale')
        # if 'seattle' in data['location'].lower() or data['place'] == 'Seattle, WA':
        print(json.dumps(details))


# avg num followers; top tweet hashtags ; top user hashtags ; top emojis ; sentiment score
