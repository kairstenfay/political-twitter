import os
import tweepy

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'],
                            os.environ['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'],
                            os.environ['TWITTER_ACCESS_SECRET'])

    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth,
                            listener=myStreamListener)

    seattle_sw = [-122.410805, 47.499724]
    seattle_ne = [-122.264696, 47.733690]

    # See https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter.html
    s = myStream.filter(track=['flu'], languages=['en'], locations=seattle_sw + seattle_ne)
    print(s)
