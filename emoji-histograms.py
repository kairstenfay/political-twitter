import os
import re
import glob
import json
import collections
import logging
import argparse
import imageio
import emoji
import flag
import math
import numpy as np
import matplotlib.pyplot as plt
from os import path
from collections import Counter
from typing import Any, List, Dict, Optional
from wordcloud import WordCloud, ImageColorGenerator
import statistics


LOG = logging.getLogger(__name__)


def extract_emojis(str):
    regional_indicator_symbols = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿'
    # Build two lists. one is from filtered indicator symbols. other normal
    result = ''
    for char in str:
        if char not in emoji.UNICODE_EMOJI:
            continue

        if char in regional_indicator_symbols:
            result += char
        else:
            result += char + ' '

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""
        Create text-based histograms of emojis from Tweets.""")
    parser.add_argument('--field', metavar='<field>', type=str, required=True,
                        help='A field: either "text" or "users"')
    parser.add_argument('-n', metavar='<number of top emojis>', type=int,
                        required=True, help='The desired # of top emojis')
    args = parser.parse_args()

    # TODO walk the retweeted tweet to full_text

    stats: Dict[str, Dict[str, Any]] = {}

    for filename in glob.glob('data/*.ndjson'):
        screen_name = re.search(r'^data/(.*).ndjson$', filename)[1]

        with open(filename, "r") as f:
            all_emojis = []

            for line in f:
                tweet = json.loads(line)

                if args.field == 'text':
                    emojis = extract_emojis(tweet['full_text'])
                else:
                    emojis = extract_emojis(tweet['user']['name'])

                if emojis:
                    # temp = flag.dflagize(emojis)
                    # temp2 = temp.split(':')  # TODO hack workaround
                    all_emojis += emojis.split(' ')

            counter = Counter(all_emojis)
            most_common = counter.most_common(args.n)

            stats[screen_name] = {
                'emoji_frequencies': counter,
                'top_emojis': most_common,
            }


            if not dict(counter):
                continue

            if screen_name in stats:
                LOG.info(screen_name)
                print(f'Top user name emojis from recent  popular tweets to @{screen_name}')

                frequencies = stats[screen_name]['emoji_frequencies'].values()
                for entry, count in stats[screen_name]['top_emojis']:
                    print(math.ceil(count / most_common[len(most_common) - 1][1]) * entry)

                print()
