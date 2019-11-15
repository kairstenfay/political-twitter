#! ./bin/bash

for screen_name in 'realDonaldTrump' 'AndrewYang' 'JoeBiden' 'TulsiGabbard' 'AmyKlobuchar' 'KamalaHarris' 'PeteButtigieg' 'ewarren' 'BernieSanders' 'CoryBooker'
    do
        echo 'Make word clouds of words in tweets by' $screen_name
        python tweet-wordclouds.py --background-color white --filename data/$screen_name-tweets.ndjson --retweets exclude
    done
