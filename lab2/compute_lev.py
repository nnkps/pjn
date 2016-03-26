import argparse

from src.distances import NormalLevenshteinDistance, ModifiedLevenshteinDistance

parser = argparse.ArgumentParser(description='Compute levenshtein distance')
parser.add_argument('word1', help='First word')
parser.add_argument('word2', help='Second word')

if __name__ == '__main__':
    args = parser.parse_args()
    word1 = args.word1
    word2 = args.word2

    print('Normal: "{}", "{}": {}'.format(word1, word2,
        NormalLevenshteinDistance(word1, word2).compute()))

    print('Modified: "{}", "{}": {}'.format(word1, word2,
        ModifiedLevenshteinDistance(word1, word2).compute()))



