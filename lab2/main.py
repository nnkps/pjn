import argparse
import re
from functools import partial

from lev import ModifiedLevenshteinDistance, NormalLevenshteinDistance

class CorrectionEngine:

    def __init__(self):
        f = open('forms/formy.txt', encoding='ISO-8859-2')
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
        word_len = len(word)
        len_range = range(word_len - 1, word_len + 2)

        obj = partial(ModifiedLevenshteinDistance, word.lower())
        distance_to_word = lambda form: obj(form).compute()

        for form in self._forms:
            if len(form) in len_range:
                dist = distance_to_word(form)
                print(dist)
                if dist < 1:
                    return form
        return word
        # return min(filter(lambda x: len(x) in len_range, self._forms), key=distance_to_word)

parser = argparse.ArgumentParser(description='Correct mistakes in text')
parser.add_argument('text', help='Input text')

if __name__ == '__main__':
    args = parser.parse_args()
    text = args.text

    engine = CorrectionEngine()
    corrected = engine.find_similar(text)
    print(corrected)


