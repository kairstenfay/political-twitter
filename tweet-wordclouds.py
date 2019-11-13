import os
import re
import glob
import json
import collections
import logging
import argparse
import imageio
import string
import numpy as np
import matplotlib.pyplot as plt
from os import path
from collections import Counter
from typing import Any, List, Dict, Optional
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS


LOG = logging.getLogger(__name__)

stopwords = set(STOPWORDS)
stopwords.add('i')
stopwords.add('rt')
stopwords.add('&amp;')
stopwords.add('will')
stopwords.add('know')
stopwords.add('really')
stopwords.add('...')
stopwords.add('-')
stopwords.add('for')
stopwords.add('said')
stopwords.add('say')
stopwords.add('—')

printable = set(string.printable)

def build_hashtags_list(hashtags: List[Dict[str, Any]]) -> Optional[str]:
    text = hashtags.get('text')
    if text:
        return text.lower()


def make_image(text, mask_name: str, screen_name: str):
    image_mask = imageio.imread('AndrewYang.jpg', as_gray=False, pilmode="RGB")
    image_colors = ImageColorGenerator(image_mask)

    wc = WordCloud(background_color="white", max_words=2000, repeat=True, mask=image_mask,
        stopwords=stopwords)
    wc.generate_from_frequencies(text)

    # axes[0].imshow(wc, interpolation="bilinear")
    plt.imshow(wc.recolor(color_func=image_colors),
                interpolation="bilinear")
    # axes[2].imshow(alice_mask, cmap=plt.cm.gray, interpolation="bilinear")
    #for ax in axes:
    plt.axis("off")
    plt.title(f'Top words in recent Tweets to @{screen_name}',
        pad=15,
        fontdict={
            'fontsize': 'x-large',
            'fontfamily': 'monospace',
        })

    plt.savefig(f'wordclouds/{screen_name}-tweet-text.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
        Create hashtag wordmaps from Tweets in the shape and color of a given mask.""")
    parser.add_argument('--mask', metavar='<mask>', type=str, required=False,
                        help='a PNG file used to mask the output data viz.')
    args = parser.parse_args()


    stats: Dict[str, Dict[str, Any]] = {}

    for filename in glob.glob('data/*-tweets.ndjson'):
        screen_name = re.search(r'^data/(.*)-tweets.ndjson$', filename)[1]

        with open(filename, "r") as f:
            all_hashtags = []

            for line in f:
                tweet = json.loads(line)
                # normalized_tweet = re.sub('’', '\'', tweet['full_text'])
                normalized_tweet = ''.join(filter(lambda x: x in printable, tweet['full_text']))
                # normalized_tweet = re.sub('[\n|\\|...]', ' ', normalized_tweet)
                words = normalized_tweet.lower().split(' ')
                stripped_words = [ w.strip('[".:]') for w in words ]
                filtered_words = [ w for w in stripped_words if w and not w.startswith('@') and not w.startswith('.@') and not w.startswith('http') and w not in stopwords ]
                all_hashtags += filtered_words
            counter = Counter(all_hashtags)

            stats[screen_name] = {
                'hashtag_frequences': counter,
                'top_15_hashtags': counter.most_common(15)
            }

            if not dict(counter):
                continue

            make_image(dict(counter), args.mask, screen_name)

            if screen_name in stats:
                print(screen_name, stats[screen_name]['top_15_hashtags'])
