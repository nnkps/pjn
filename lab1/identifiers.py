#/!/user/bin/python

from pathlib import Path
import math
import json

from corpus_parser import CorpusParser
from config import STATISTICS_FILENAME, NGRAMS_DIRNAME


def innerproduct(d1, d2):
    if len(d1) > len(d2):
        d1, d2 = d2, d1
    return sum(d1[key] * d2[key] for key in d1 if key in d2)

def cosinusdistance(d1, d2):
    try:
        return 1 - (innerproduct(d1, d2) / math.sqrt(innerproduct(d1, d1) * innerproduct(d2, d2)))
    except ZeroDivisionError:
        return 1.0


class LanguageIdentifier:
    def __init__(self, statistics_dir, n=[2, 11]):
        ngram_stats = {}
        for i in range(*n):
            language_statistics = {}
            for language in Path(statistics_dir, NGRAMS_DIRNAME(i)).iterdir():
                with (language / STATISTICS_FILENAME).open('r') as f:
                    language_statistics[language.name] = json.loads(f.read())
            ngram_stats[i] = language_statistics
        self.ngram_stats = ngram_stats

    def identify(self, text, n):
        lang_stats = self.ngram_stats[n]
        stats = CorpusParser(n).parse_corpus(text)
        distances = {x: cosinusdistance(stats, lang_stats[x]) for x  in lang_stats}
        return distances, min(distances, key=lambda x: distances[x])


class NgramLanguageIdentifier(LanguageIdentifier):
    def __init__(self, statistics_dir, n=2):
        super().__init__(statistics_dir, [n, n + 1])
        self.n = n

    def identify(self, text):
        return super().identify(text, self.n)
