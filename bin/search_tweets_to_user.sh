#! ./bin/bash

for screen_name in 'amyklobuchar' 'KamalaHarris' 'ewarren' 'BernieSanders' 'CoryBooker' 'MikeBloomberg' 'TomSteyer' 'realDonaldTrump' # 'AndrewYang' 'TulsiGabbard' 'PeteButtigieg' 'JoeBiden'
    do
        echo 'searching tweets to' $screen_name
        python3 search-tweets.py -q $screen_name -d $1 > data/$screen_name.ndjson
    done
