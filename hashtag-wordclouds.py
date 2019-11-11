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
from os import path
from collections import Counter
from typing import Any, List, Dict, Optional
from wordcloud import WordCloud, ImageColorGenerator


LOG = logging.getLogger(__name__)


def build_hashtags_list(hashtags: List[Dict[str, Any]]) -> Optional[str]:
    text = hashtags.get('text')
    if text:
        return text.lower()


def make_image(text, mask_name: str, screen_name: str):
    image_mask = imageio.imread("us-flag.png", as_gray=False, pilmode="RGB")
    image_colors = ImageColorGenerator(image_mask)

    wc = WordCloud(background_color="white", max_words=1000, repeat=True, mask=image_mask)
    wc.generate_from_frequencies(text)

    # axes[0].imshow(wc, interpolation="bilinear")
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    # axes[2].imshow(alice_mask, cmap=plt.cm.gray, interpolation="bilinear")
    #for ax in axes:
    plt.axis("off")
    plt.title(f'Top hashtags Tweeted to @{screen_name} recently',
        pad=10,
        fontdict={
            'fontsize': 'x-large',
            'fontfamily': 'monospace',
        })

    plt.savefig(f'wordmaps/{screen_name}-{mask_name}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
        Create hashtag wordmaps from Tweets in the shape and color of a given mask.""")
    parser.add_argument('--mask', metavar='<mask>', type=str, required=True,
                        help='a PNG file used to mask the output data viz.')
    args = parser.parse_args()


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

            make_image(dict(counter), args.mask, screen_name)

            if screen_name in stats:
                print(screen_name, stats[screen_name]['top_5_hashtags'])
