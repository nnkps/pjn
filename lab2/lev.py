
class LevenshteinDistance:

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


assert LevenshteinDistance('BIURKO', 'PIÓRO').compute() == 3


class ModifiedLevenshteinDistance(LevenshteinDistance):
    _SCORE_FOR_MISTAKE = 0.5
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

        possible_pairs = [{a[i - 1], b[j - 1]},
                          {a[i - 1], b[j - 1 : j + 1]},
                          {a[i - 1 : i + 1], b[j - 1]},
                          {a[i - 1: i + 1], b[j - 1 : j + 1]}]

        for pair in possible_pairs:
            if pair in self._PAIRS:
                return self._SCORE_FOR_MISTAKE

        try:
            if {a[i - 1], a[i]} == {b[j - 1], b[j]}:
                return self._SCORE_FOR_MISTAKE
        except IndexError:
            pass

        try:
            if {a[i - 2], a[i - 1]} == {b[j - 2], b[j - 1]}:
                return self._SCORE_FOR_MISTAKE
        except IndexError:
            pass

        return super()._comparison(i, j)


if __name__ == '__main__':
    print(ModifiedLevenshteinDistance('wtorek', 'wotrek').compute())


