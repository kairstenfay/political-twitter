#! ./bin/bash
for screen_name in 'realDonaldTrump' 'JoeBiden'
    do
        echo 'Make word clouds of words in tweets by' $screen_name
        python ./bin/tweet-wordclouds.py --background-color white --filename data/$screen_name.ndjson --output-dir wordclouds --mask-dir masks
    done
