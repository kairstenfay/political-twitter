import os
import json
import tweepy
import logging
from typing import Any


LOG = logging.getLogger(__name__)



def place(details: dict) -> str:
    if details.get("place", None):
        return details["place"]["full_name"]

def possibly_sensitive(details: dict) -> dict:
    return details.get("possibly_sensitive", None)

def lang(details: dict) -> str:
    return details.get("lang", None)

def limit_handled(cursor):
    """ A method from the tweepy documentation, not currently being used """
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'],
                            os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'],
                        os.environ['TWITTER_ACCESS_SECRET'])

    api = tweepy.API(auth, wait_on_rate_limit=True,
                    wait_on_rate_limit_notify=True,
                    compression=True)


    for tweet in tweepy.Cursor(api.search, q='flu').items(10):
        details = tweet._json

        if details['metadata']['iso_language_code'] != 'en' and details['lang'] != 'en':
            continue

        data = {
            'location': details.get('location', 'None'),
            'place': place(details),
            'user_location': details['user'].get('location', 'None')
            'possibly_sensitive': possibly_sensitive(details),
            'lang': details.get('lang'),
            'text': details.get('text'),
        }

        if data['possibly_sensitive']:
            continue

        if 'seattle' in data['location'].lower() or data['place'] == 'Seattle, WA':
           print(details)
