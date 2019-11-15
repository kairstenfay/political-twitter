#! ./bin/bash

for screen_name in 'BillGates' 'fannychoir' 'marwilliamson'
    do
        echo 'searching tweets in the timeline of' $screen_name
        python search-tweets.py -u $screen_name -d 2018-11-14 > requests/data/$screen_name-tweets.ndjson
    done
