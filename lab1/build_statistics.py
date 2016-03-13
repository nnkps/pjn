#/!/user/bin/python

from pathlib import Path
import json
import shutil
import logging
import argparse

from corpus_parser import CorpusParser
from config import STATISTICS_FILENAME, NGRAMS_DIRNAME

logging.getLogger().setLevel(logging.INFO)


def build_statistics(corpuses_dir, statistics_dir):
    try:
        shutil.rmtree(statistics_dir.name)
    except FileNotFoundError:
        pass
    finally:
        statistics_dir.mkdir()

    lang_paths = [x for x in corpuses_dir.iterdir() if x.is_dir()]

    for n in range(2, 11):
        parser = CorpusParser(n)
        parser_dir = statistics_dir / NGRAMS_DIRNAME(n)
        parser_dir.mkdir()

        for p in lang_paths:
            logging.info('Started preparing statistics for %s language and %dgrams', p.name, n)
            lang_stat_dir = parser_dir / p.name
            lang_stat_dir.mkdir()

            lang_corpuses = [f for f in p.iterdir() if f.is_file()]

            language_text = ''

            for corpus in lang_corpuses:
                f = corpus.open('r')
                language_text += f.read()
                f.close()

            statistics = parser.parse_corpus(language_text)
            logging.info('Parsed')

            with (lang_stat_dir / STATISTICS_FILENAME).open('w') as f:
                f.write(json.dumps(statistics, indent=4))
                logging.info('Created statistics file')

parser = argparse.ArgumentParser(description='Build statistics')
parser.add_argument('--corpuses_dir', default='corpuses', help='Input directory with corpuses')
parser.add_argument('--statistics_dir', default='statistics', help='Output directory with statistics')

if __name__ == '__main__':
    args = parser.parse_args()
    corpuses_dir = Path(args.corpuses_dir)
    statistics_dir = Path(args.statistics_dir)

    build_statistics(corpuses_dir, statistics_dir)
