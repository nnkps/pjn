import argparse


class NormalLevenshteinDistance:

    def __init__(self, a, b):
        if len(a) < len(b):
            a, b = b, a

        self._len_a = len(a)
        self._len_b = len(b)
        self._a = a.lower()
        self._b = b.ljust(len(a)).lower()

    def _comparison(self, i, j):
        return int(self._a[i - 1] != self._b[j - 1])

    def _compute(self, i, j):
        if min(i, j) == 0:
            return max(i, j)
        return min(self._compute(i - 1, j) + 1,
                   self._compute(i, j - 1) + 1,
                   self._compute(i - 1, j - 1) + self._comparison(i, j)
                   )

    def compute(self):
        return self._compute(self._len_a, self._len_b)


assert NormalLevenshteinDistance('BIURKO', 'PIÓRO').compute() == 3


class ModifiedLevenshteinDistance(NormalLevenshteinDistance):
    _SCORE_FOR_MISTAKE = 0.25
    _PAIRS = (
        # ortographic
        {'ó', 'u'},
        {'ż', 'rz'},
        {'h', 'ch'},
        {'b', 'p'},
        {'i', 'ji'},
        {'i', 'ii'},
        {'c', 'dz'},
        {'sz', 'rz'},
        {'ń', 'ni'},
        {'ć', 'ci'},
        {'ć', 'dź'},
        {'ą', 'on'},
        {'ą', 'an'},
        {'z', 's'},
        {'ś', 'si'},
        {'w', 'f'},
        # diactric
        {'a', 'ą'},
        {'c', 'ć'},
        {'e', 'ę'},
        {'l', 'ł'},
        {'n', 'ń'},
        {'o', 'ó'},
        {'s', 'ś'},
        {'z', 'ż'},
        {'z', 'ź'},
    )

    def _comparison(self, i, j):
        a, b = self._a, self._b
        if a[i - 1] == b[j - 1]:
            return 0

        try:
            if a[i - 1] == b[j] and a[i] == b[j - 1]:
                return self._SCORE_FOR_MISTAKE
        except IndexError:
            pass

        try:
            if a[i - 2] == b[j - 1] and a[i - 1] == b[j - 2]:
                return self._SCORE_FOR_MISTAKE
        except IndexError:
            pass

        possible_pairs = [{a[i - 1], b[j - 1]},
                          {a[i - 1], b[j - 1 : j + 1]},
                          {a[i - 1 : i + 1], b[j - 1]},
                          {a[i - 1: i + 1], b[j - 1 : j + 1]}]

        for pair in possible_pairs:
            if pair in self._PAIRS:
                return self._SCORE_FOR_MISTAKE

        return super()._comparison(i, j)

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



