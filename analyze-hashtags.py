import os
import re
import glob
import json
import collections
import logging
import argparse
from typing import Any, List, Dict, Optional
from itertools import groupby
from collections import Counter
# -- wordmap
import multidict as multidict
import numpy as np
from PIL import Image
from os import path
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import imageio


LOG = logging.getLogger(__name__)


def build_hashtags_list(hashtags: List[Dict[str, Any]]) -> Optional[str]:
    """ """
    text = hashtags.get('text')
    if text:
        return text.lower()


def makeImage(text):
    # alice_mask = np.array(Image.open("us-flag.png", pilmode='RGB'))
    alice_mask = imageio.imread("us-flag.png", as_gray=False, pilmode="RGB")

    # create coloring from image
    image_colors = ImageColorGenerator(alice_mask)

    wc = WordCloud(background_color="white", max_words=1000, repeat=True, mask=alice_mask)
    # generate word cloud
    wc.generate_from_frequencies(text)

    # show
    # axes[0].imshow(wc, interpolation="bilinear")
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    # axes[2].imshow(alice_mask, cmap=plt.cm.gray, interpolation="bilinear")
    #for ax in axes:
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Process some tweets.')
    #parser.add_argument('--tweets', metavar='<tweets>', dest="filename", required=True,
    #                    help='a newline-delimited JSON file of Tweets to analyze.')
    #args = parser.parse_args()

    stats: Dict[str, Dict[str, Any]] = {}

    for filename in glob.glob('data/*.ndjson'):
        screen_name = re.search(r'^data/(.*).ndjson$', filename)[1]
        with open(filename, "r") as f:
            all_hashtags = []

            for line in f:
                tweet = json.loads(line)
                entities = tweet['entities']
                all_hashtags += list(map(build_hashtags_list, entities['hashtags']))

            counter = Counter(all_hashtags)

            stats[screen_name] = {
                'hashtag_frequences': counter,
                'top_5_hashtags': counter.most_common(5)
            }

            if not dict(counter):
                continue

            makeImage(dict(counter))

            if screen_name in stats:
                print(screen_name, stats[screen_name]['top_5_hashtags'])
