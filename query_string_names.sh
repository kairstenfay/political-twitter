#! ./bin/bash

for screen_name in 'AndrewYang' 'TulsiGabbard' 'AmyKlobuchar' 'realDonaldTrump' 'KamalaHarris' # 'PeteButtigieg' 'ewarren' 'BernieSanders'
    do
        python search-tweets.py -q $screen_name > data/$screen_name.ndjson
    done


# for filename in 'realDonaldTrump.ndjson' 'ewarren.ndjson' 'BernieSanders.ndjson' 'AndrewYang.ndjson' 'KamalaHarris.ndjson' 'PeteButtigieg.ndjson' 'TulsiGabbard.ndjson' 'AmyKlobuchar.ndjson'
#     do
#         python analyze-hashtags.py --tweets data/$filename > data/$filename-hashtags.ndjson
#     done
