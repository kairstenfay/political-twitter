#!/usr/bin/python

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


def extract_emojis(string: str) -> str:

    def is_emoji(char: str) -> bool:
        return char in emoji.UNICODE_EMOJI


    regional_indicator_symbols = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿'
    skin_tone_modifiers = '🏻🏼🏽🏾🏿'

    non_standalone_emojis = regional_indicator_symbols + skin_tone_modifiers + '🏳'

    emojis = ''
    current_emoji = ''

    for char in string:
        if not is_emoji(char):
            continue

        if len(current_emoji) == 2:
            emojis += current_emoji + ' '
            # Reset
            current_emoji = ''

        if char in non_standalone_emojis:
            current_emoji += char

        else:
            if current_emoji:
                current_emoji += char
            else:
                emojis += char + ' '

    return emojis

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

    LOG.info("Iterating over files now")
    for filename in glob.glob('data/*.ndjson'):
        LOG.info(f"Opening {filename}")

        screen_name = re.search(r'^data/(.*).ndjson$', filename)[1]

        with open(filename, "r") as f:
            all_emojis = []

            lines = 0
            for line in f:
                lines += 1
                tweet = json.loads(line)

                if args.field == 'text':
                    emojis = extract_emojis(tweet['full_text'])
                else:
                    emojis = extract_emojis(tweet['user']['name'])

                if emojis:
                    # temp = flag.dflagize(emojis)
                    # temp2 = temp.split(':')  # TODO hack workaround
                    all_emojis += [ e for e in emojis.split(' ') if e != '' ]

            counter = Counter(all_emojis)
            most_common = counter.most_common(args.n)

            stats[screen_name] = {
                'emoji_frequencies': counter,
                'top_emojis': most_common,
                'most_common': counter.most_common(args.n),
                'tweets': lines,
            }

            lines = 0

            if not dict(counter):
                continue

            #if screen_name in stats:
                #LOG.info(screen_name)
                # print(f'Top emojis from users recently tweeting to @{screen_name} #dataviz')

                #frequencies = stats[screen_name]['emoji_frequencies'].values()
                #for entry, count in stats[screen_name]['most_common']:
                    # print(f"@{screen_name}", entry)
                    #print(math.ceil(count / most_common[len(most_common) - 1][1]) * entry)

    # print('Top emojis from users recently tweeting to the following U.S. Democratic presidential candidates:\n')

    print(json.dumps(stats))
