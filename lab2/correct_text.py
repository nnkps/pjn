import argparse
from src.engine import CorrectionEngine

parser = argparse.ArgumentParser(description='Correct mistakes in text')
parser.add_argument('text', help='Input text')

if __name__ == '__main__':
    args = parser.parse_args()
    text = args.text

    engine = CorrectionEngine()
    corrected = engine.correct_text(text)
    print(corrected)


