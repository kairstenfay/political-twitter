#! ./bin/bash
# 'realDonaldTrump' 'AndrewYang' 'TulsiGabbard' 'AmyKlobuchar' 'KamalaHarris' 'PeteButtigieg' 'ewarren' 'BernieSanders' 'CoryBooker'
for screen_name in 'AOC' 'IlhanMN' 'RashidaTlaib' 'AyannaPressley'
    do
        echo 'Make word clouds of words in tweets by' $screen_name
        python tweet-wordclouds.py --background-color white --filename data/$screen_name-tweets.ndjson --output-dir wordclouds --mask-dir masks
    done
