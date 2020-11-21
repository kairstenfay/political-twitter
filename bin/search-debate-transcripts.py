"""
Parses debate transcripts.
"""
import re
import os
import json
import glob
import logging
import imageio
import argparse
import matplotlib.pyplot as plt
from typing import Any, List, Dict, Tuple
from collections import Counter, defaultdict
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS


LOG = logging.getLogger(__name__)


stopwords = set(STOPWORDS)
stopwords.add('i')
stopwords.add('u')
stopwords.add('im')
stopwords.add('rt')
stopwords.add('&amp;')
stopwords.add('will')
stopwords.add('know')
stopwords.add('really')
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
stopwords.add('go')
stopwords.add('got')
stopwords.add('let')
stopwords.add('going')
stopwords.add('now')
stopwords.add('want')
stopwords.add('right')
stopwords.add('every')
stopwords.add('sure')


LOG = logging.getLogger(__name__)
SPEAKER_NAME_PADDING = ': '

parser = argparse.ArgumentParser(description="""
    Search Debate transcripts.""")
parser.add_argument('--mask', metavar='<mask>', type=str, required=False,
                    help='a mask to use to project a word cloud onto.')
parser.add_argument('--date', metavar='<debate date>', type=str, required=False,
                    help='a string in mon-DD-YYYY format on which debate date to parse.')

args = parser.parse_args()


debate_nights = {
    'jun-26-2019': '1, night 1',
    'jun-27-2019': '1, night 2',
    'jul-30-2019': '2, night 1',
    'jul-31-2019': '2, night 2',
    'sep-12-2019': '3',
    'oct-15-2019': '4',
    'nov-20-2019': '5',
    'dec-19-2019': '6',
}

def make_image(text: Counter, speaker: str, mask_name: str, date: str):
    """ """
    def title(speaker: str, date: str) -> str:
        """ """
        title = f'Top words {speaker} spoke \nin '
        title += f"the {date} debate" if date else "all debates"

        return title

    def standardize_name(speaker: str) -> str:
        """ """
        name_map = {
            'WARREN': 'Elizabeth Warren',
            'BIDEN': 'Joe Biden',
            'SANDERS': 'Bernie Sanders',
            'YANG': 'Andrew Yang',
            'GABBARD': 'Tulsi Gabbard',
            'BUTTIGIEG': 'Pete Buttigieg',
            'KLOBUCHAR': 'Amy Klobuchar',
            'BOOKER': 'Cory Booker',
            'STEYER': 'Tom Steyer',
            'HARRIS': 'Kamala Harris'
        }

        return name_map.get(speaker) or speaker

    def generate_masked_image(text: str, mask_name: str):
        """ """
        image_mask = imageio.imread(mask_name, as_gray=False, pilmode="RGB")
        image_colors = ImageColorGenerator(image_mask)

        wc = WordCloud(background_color="white", max_words=5000, repeat=True, mask=image_mask)
        wc.generate_from_frequencies(text)
        plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")


    def generate_image(text: str):
        """ """
        wc = WordCloud(background_color="white", max_words=5000, repeat=True)
        wc.generate_from_frequencies(text)
        plt.imshow(wc, interpolation="bilinear")


    if mask_name:
        generate_masked_image(text, mask_name)

    else:
        generate_image(text)

    speaker = standardize_name(speaker)

    plt.axis("off")
    plt.title(
        title(speaker, date),
        pad=10,
        fontdict={
            'fontsize': 'x-large',
            'fontfamily': 'monospace',
        })

    suffix = date or "all-debates"
    plt.savefig(f'wordclouds/speeches/{speaker}-{suffix}.png')


def candidate_or_moderator(speaker: str) -> str:
    """ """
    moderators = ['WELKER', 'PARKER', 'MITCHELL', 'MADDOW']

    if speaker in moderators:
        return 'the moderators'

    return speaker


def most_common_word_and_frequency(speaker: str, counter: Counter):
    """ """
    most_common = counter.most_common(1)[0]
    print(f"{speaker}: {most_common[0]}, {most_common[1]}")


def word_count(speaker: str, counter: Counter) -> Tuple[int, str]:
    """ """
    return len(counter), speaker


if __name__ == '__main__':
    dialogue: Dict[str, List[str]] = defaultdict(list)
    speaker: str = None
    word_counts: Dict[str, List[str]] = {}

    search_text = f'*{args.date}.txt' or '*.txt'

    for file in (glob.glob(f"data/debates/{search_text}")):

        with open(file, "r") as f:
            lines = f.readlines()

            for line in lines:
                line = re.sub(r'\n|\\|\-|\,|\.|\?', '', line)
                if not line:
                    continue

                is_speech_start = re.match(r'^[A-Z]{3,}(?:)', line)
                line = line.lower()
                word_counts[speaker] = word_count(speaker, counter)

                if is_speech_start:
                    start = is_speech_start[0]
                    speaker = candidate_or_moderator(start)

                    speech = line[len(speaker + SPEAKER_NAME_PADDING):]

                    dialogue[speaker].append(speech)

                else:
                    if not speaker:
                        continue

                    dialogue[speaker].append(line)


    for speaker in dialogue:
        # Create corpus
        corpus = ' '.join(s for s in dialogue[speaker]).split(' ')
        meaningful_words = [ w for w in corpus if w and w not in stopwords and not w.startswith('(')]
        # print('Analyzing candidate ' + speaker)
        counter = Counter(meaningful_words)
        if not counter:
            continue

        word_count(speaker, counter)
       #  breakpoint()
        # most_common_word_and_frequency(speaker, counter)
        #make_image(counter, speaker, args.mask, args.date)
