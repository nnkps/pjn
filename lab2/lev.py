import argparse


class NormalLevenshteinDistance:

    def __init__(self, a, b):
        if len(a) < len(b):
            a, b = b, a

        self._a = a.lower()
        self._b = b.lower()

    def _comparison(self, i, j):
        return int(self._a[i] != self._b[j])

    def compute(self):
        a, b = self._a, self._b
        if a == b: return 0
        elif len(a) == 0: return len(a)
        elif len(b) == 0: return len(b)
        v0 = [None] * (len(b) + 1)
        v1 = [None] * (len(b) + 1)

        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(a)):
            v1[0] = i + 1
            for j in range(len(b)):
                cost = self._comparison(i, j)
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
                
        return v1[len(b)]


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
        if a[i] == b[j]:
            return 0

        try:
            if a[i] == b[j + 1] and a[i + 1] == b[j]:
                return self._SCORE_FOR_MISTAKE / 2
        except IndexError:
            pass

        try:
            if a[i - 1] == b[j] and a[i] == b[j - 1]:
                return self._SCORE_FOR_MISTAKE / 2
        except IndexError:
            pass

        possible_pairs = [{a[i], b[j]},
                          {a[i], b[j : j + 2]},
                          {a[i : i + 2], b[j]},
                          {a[i : i + 2], b[j : j + 2]}]

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



