#! ./bin/bash
# 'JoeBiden' 'realDonaldTrump' 'AndrewYang' 'TulsiGabbard' 'amyklobuchar' 'KamalaHarris' 'PeteButtigieg' 'ewarren' 'BernieSanders' 'CoryBooker'

for screen_name in 'AOC' 'IlhanMN' 'RashidaTlaib' 'AyannaPressley'
    do
        echo 'searching tweets in the timeline of' $screen_name
        python search-tweets.py -u $screen_name -d 2018-11-13 > data/$screen_name-tweets.ndjson
    done
