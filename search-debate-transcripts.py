"""
Parses debate transcripts.
"""
import re
import os
import json
import logging
import imageio
import argparse
import matplotlib.pyplot as plt
from typing import Any, List, Dict
from collections import Counter
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

LOG = logging.getLogger(__name__)
SPEAKER_NAME_PADDING = ': '

parser = argparse.ArgumentParser(description="""
    Search Debate transcripts.""")
parser.add_argument('--date', metavar='<debate date>', type=str, required=True,
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

def make_image(text: Counter, date: str):
    # image_mask = imageio.imread("us-flag.png", as_gray=False, pilmode="RGB")
    # image_colors = ImageColorGenerator(image_mask)

    wc = WordCloud(background_color="white", max_words=5000, repeat=True) # mask=image_mask)
    wc.generate_from_frequencies(text)

    plt.imshow(#wc.recolor(color_func=image_colors),
        wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f'Most common words {speaker} spoke in Debate {debate_nights[date]}', # TODO
        pad=10,
        fontdict={
            'fontsize': 'x-large',
            'fontfamily': 'monospace',
        })

    plt.savefig(f'wordclouds/speeches/{speaker}-{date}.png')

if __name__ == '__main__':

    with open(f"nbcnews_debate_transcript_{args.date}.txt", "r") as f:
        lines = f.readlines()

        dialogue: Dict[str, List[str]] = {}
        speaker: str = None

        for line in lines:
            line = re.sub(r'\n|\\|\-|\,|\.|\?', '', line)
            if not line:
                continue

            is_speech_start = re.match(r'^[A-Z]{3,}(?:)', line)
            line = line.lower()

            if is_speech_start:
                speaker = is_speech_start[0]
                speech = line[len(speaker + SPEAKER_NAME_PADDING):]

                if not dialogue.get(speaker):
                    dialogue[speaker] = [speech]  # TODO
                else:
                    dialogue[speaker].append(speech)

            else:
                if not speaker:
                    continue
                dialogue[speaker].append(line)

        for speaker in dialogue:
            # Create corpus
            corpus = ' '.join(s for s in dialogue[speaker]).split(' ')
            meaningful_words = [ w for w in corpus if w and w not in stopwords and not w.startswith('(')]
            print('Analyzing candidate ' + speaker)
            counter = Counter(meaningful_words)
            if not counter:
                continue
            print(counter.most_common(15))

            make_image(counter, args.date)
# avg num followers; top tweet hashtags ; top user hashtags ; top emojis ; sentiment score
