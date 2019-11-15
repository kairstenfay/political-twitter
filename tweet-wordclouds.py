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
stopwords.add('im')
stopwords.add('rt')
stopwords.add('&amp;')
stopwords.add('will')
stopwords.add('know')
stopwords.add('really')
# stopwords.add('...')
# stopwords.add('-')
stopwords.add('for')
stopwords.add('said')
stopwords.add('say')
stopwords.add('us')
stopwords.add('need')
stopwords.add('make')
stopwords.add('must')
stopwords.add('people')
stopwords.add('thank')
stopwords.add('thanks')
stopwords.add('one')
stopwords.add('w')
# stopwords.add('—')

printable = set(string.printable)

def remove_links(w: str) -> bool:
    return not w.startswith(('@', '#', 'http'))

def remove_stopwords(w: str) -> bool:
    return (bool(w) and w not in stopwords)

def make_image(text, mask_name: str, screen_name: str, background_color: str, mask_dir: str, output_dir: str):
    if not mask_name:
        mask_name = f'{mask_dir}/{screen_name}.png'

    image_mask = imageio.imread(mask_name, as_gray=False, pilmode="RGB")
    image_colors = ImageColorGenerator(image_mask)

    wc = WordCloud(background_color=background_color, max_words=5000, repeat=False,
        mask=image_mask, stopwords=stopwords)
    wc.generate_from_frequencies(text)

    plt.imshow(wc.recolor(color_func=image_colors),
                interpolation="bilinear")

    plt.axis("off")
    plt.title(f'@{screen_name}',  # Most common words in Tweets by 
        pad=15,
        fontdict={
            'fontsize': 'x-large',
            'fontfamily': 'monospace',
        })

    plt.savefig(f'{output_dir}/{screen_name}-tweet-text.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
        Create wordmaps from Tweets in the shape and color of a given mask.""")
    parser.add_argument('--filename', metavar='<filename>', type=str, required=True,
                        help='the file of newline-delimited Tweets to analyze.')
    parser.add_argument('--mask', metavar='<mask>', type=str, required=False,
                        help='a PNG file used to mask the output data viz.')
    parser.add_argument('--background-color', metavar='<background color>', type=str, default='white',
                        help='the background color of the generated word cloud. Defaults to white')
    parser.add_argument('--mask-dir', metavar='<mask directory>', type=str, required=True,
                        help='the directory from which to source the mask file used to make wordclouds')
    parser.add_argument('--output-dir', metavar='<output directory>', type=str, required=True,
                        help='the output directory of the wordclouds')
    args = parser.parse_args()


    stats: Dict[str, Dict[str, Any]] = {}

    #for filename in glob.glob('data/*-tweets.ndjson'):
    filename = args.filename

    screen_name = re.search(r'.*data/(.*)-tweets.ndjson$', filename)[1]

    with open(filename, "r") as f:
        all_hashtags = []
        lines = 0

        for line in f:
            lines += 1
            tweet = json.loads(line)

            if tweet.get('retweeted_status'):
                continue

            tweet_text = tweet['full_text'].lower()
            printable_words = ''.join(filter(lambda x: x in printable, tweet_text)).split(' ')
            stripped_words = [ w.strip('[".:!?-,+/]') for w in printable_words ]
            words_without_links = filter(remove_links, stripped_words)
            filtered_words = filter(remove_stopwords, words_without_links)
            all_hashtags += list(filtered_words)

        counter = Counter(all_hashtags)

        stats[screen_name] = {
            'hashtag_frequences': counter,
            'top_15_words': counter.most_common(15)
        }

        if not dict(counter):
            pass

        make_image(dict(counter), args.mask, screen_name, args.background_color, args.mask_dir, args.output_dir)

        if screen_name in stats:
            print(screen_name, lines)
            print(stats[screen_name]['top_15_words'])
