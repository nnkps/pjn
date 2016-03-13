#/!/user/bin/python

import re


class CorpusParser:

    def __init__(self, n=2):
        self.n = n

    def __get_ngrams(self, word):
        n = self.n
        if len(word) < n:
            return [word]
        return [word[i : i+n] for i in range(len(word) - n + 1)]

    def parse_corpus(self, text):
        statistics = dict()

        def process_line(line):
            pattern = re.compile('[\W_]+')
            words = [pattern.sub('', word.lower()) for word in line.split()]

            for word in words:
                for ngram in self.__get_ngrams(word):
                    if ngram:
                        statistics[ngram] = statistics.get(ngram, 0) + 1

        if isinstance(text, str):
            process_line(text)
        else:
            for line in text:
                process_line(line)

        return statistics
