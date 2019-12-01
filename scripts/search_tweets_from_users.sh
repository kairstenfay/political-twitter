#! ./bin/bash
#
# 'AOC' 'IlhanMN' 'RashidaTlaib' 'AyannaPressley'
for screen_name in 'MikeBloomberg' 'TomSteyer' 'BernieSanders' 'CoryBooker' 'JoeBiden' 'realDonaldTrump' 'AndrewYang' 'TulsiGabbard' 'amyklobuchar' 'KamalaHarris' 'PeteButtigieg' 'ewarren'
    do
        echo 'searching tweets in the timeline of' $screen_name
        python3 search-tweets.py -u $screen_name -d 2018-11-29 > data/$screen_name.ndjson
    done
