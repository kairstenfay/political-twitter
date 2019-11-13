#! ./bin/bash

for screen_name in 'AndrewYang' 'TulsiGabbard' 'AmyKlobuchar' 'realDonaldTrump' 'KamalaHarris' 'PeteButtigieg' 'ewarren' 'BernieSanders' 'CoryBooker'
    do
        echo 'searching tweets in the timeline of' $screen_name
        python search-tweets.py -u $screen_name -d 2018-11-12 > data/$screen_name-tweets.ndjson
    done
