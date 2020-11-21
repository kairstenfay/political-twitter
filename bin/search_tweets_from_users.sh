#! ./bin/bash
#
for screen_name in 'realDonaldTrump'
    do
        echo 'searching tweets in the timeline of' $screen_name
        python3 ./bin/search-tweets.py -u $screen_name -d 2020-11-21 > data/$screen_name.ndjson
    done
