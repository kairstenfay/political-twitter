#! ./bin/bash

for screen_name in 'BillGates' 'fannychoir' 'marwilliamson'
    do
        echo 'Make word clouds of words in tweets by' $screen_name
        python tweet-wordclouds.py --background-color white --filename requests/data/$screen_name-tweets.ndjson --output-dir requests/wordclouds --mask-dir requests/masks
    done
