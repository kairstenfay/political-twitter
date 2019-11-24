#! ./bin/bash
#
# 'AOC' 'IlhanMN' 'RashidaTlaib' 'AyannaPressley'
for screen_name in 'TomSteyer' # 'BernieSanders' 'CoryBooker' 'JoeBiden' 'realDonaldTrump' 'AndrewYang' 'TulsiGabbard' 'amyklobuchar' 'KamalaHarris' 'PeteButtigieg' 'ewarren'
    do
        echo 'searching tweets in the timeline of' $screen_name
        python3 search-tweets.py -u $screen_name -d 2018-11-13 > data/$screen_name-tweets.ndjson
    done
