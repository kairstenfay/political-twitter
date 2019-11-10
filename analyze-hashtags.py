import os
import re
import glob
import json
import collections
import logging
import argparse
import imageio
import numpy as np
import matplotlib.pyplot as plt
from typing import Any, List, Dict, Optional
from itertools import groupby
from collections import Counter
# from PIL import Image
from os import path
from wordcloud import WordCloud, ImageColorGenerator


LOG = logging.getLogger(__name__)


def build_hashtags_list(hashtags: List[Dict[str, Any]]) -> Optional[str]:
    """ """
    text = hashtags.get('text')
    if text:
        return text.lower()


def make_image(text, mask_name: str, screen_name: str):
    image_mask = imageio.imread("us-flag.png", as_gray=False, pilmode="RGB")

    # create coloring from image
    image_colors = ImageColorGenerator(image_mask)

    wc = WordCloud(background_color="white", max_words=1000, repeat=True, mask=image_mask)
    wc.generate_from_frequencies(text)

    # axes[0].imshow(wc, interpolation="bilinear")
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
    # fig = plt.figure()
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    # axes[2].imshow(alice_mask, cmap=plt.cm.gray, interpolation="bilinear")
    #for ax in axes:
    plt.axis("off")
    plt.savefig(f'wordmaps/{screen_name}-{mask_name}')
    # plt.show()


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

            make_image(dict(counter), 'us-flag.png', screen_name)

            if screen_name in stats:
                print(screen_name, stats[screen_name]['top_5_hashtags'])
