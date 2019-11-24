#! ./bin/bash

for screen_name in 'JoeBiden' 'realDonaldTrump' 'AndrewYang' 'TulsiGabbard' 'amyklobuchar' 'KamalaHarris' 'PeteButtigieg' 'ewarren' 'BernieSanders' 'CoryBooker'
    do
        echo 'searching tweets to' $screen_name
        python search-tweets.py -q $screen_name -d $1 > data/$screen_name.ndjson
    done
