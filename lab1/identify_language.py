#/!/user/bin/python

import argparse
from pprint import pprint

from src.identifiers import NgramLanguageIdentifier


parser = argparse.ArgumentParser(description='Determine language of given text')
parser.add_argument('n', help='Length of single ngram', type=int)
parser.add_argument('text', help='Input text')
parser.add_argument('--statistics_dir', default='statistics', help='Directory with language statistics')

if __name__ == '__main__':
    args = parser.parse_args()
    n, text = args.n, args.text
    statistics_dir = args.statistics_dir

    identifier = NgramLanguageIdentifier(statistics_dir, n)
    distances, possible_lang = identifier.identify(text)
    pprint(distances)
    print('Is it %s?' % possible_lang)
