import re
import logging
from functools import partial

from .distances import ModifiedLevenshteinDistance, NormalLevenshteinDistance

logging.getLogger().setLevel(logging.INFO)


class CorrectionEngine:

    def __init__(self, forms_file='forms/formy.txt'):
        f = open(forms_file, encoding='ISO-8859-2')
        self._forms = set(word.strip() for word in f)

    def correct_text(self, text):
        pattern = re.compile('\w+')

        def replace_word(match):
            word = match.group(0)
            if word not in self._forms:
                return self.find_similar(word)
            return word

        return pattern.sub(replace_word, text)

    def find_similar(self, word):
        logging.info('Starting to search for similar form for word %s', word)
        word_len = len(word)
        len_range = range(word_len - 1, word_len + 2)

        obj = partial(ModifiedLevenshteinDistance, word.lower())
        distance_to_word = lambda form: obj(form).compute()

        min_dist = None
        best_form = None
        for form in self._forms:
            if len(form) in len_range:
                dist = distance_to_word(form)
                if min_dist is None or dist < min_dist:
                    min_dist = dist
                    best_form = form
        logging.info('Replacing %s with %s, distance: %.2f', word, best_form, min_dist)
        return best_form
        # return min(filter(lambda x: len(x) in len_range, self._forms), key=distance_to_word)
