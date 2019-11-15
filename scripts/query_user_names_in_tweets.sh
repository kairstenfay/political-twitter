#! ./bin/bash

for screen_name in 'AndrewYang' 'TulsiGabbard' 'AmyKlobuchar' 'realDonaldTrump' 'KamalaHarris' 'PeteButtigieg' 'ewarren' 'BernieSanders'
    do
        echo 'searching tweets to' $screen_name
        python search-tweets.py -q $screen_name > data/$screen_name.ndjson
    done
