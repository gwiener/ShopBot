from sys import argv
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import pandas as pd


def load_pros_cons(path):
    pros_cons = {}
    stemmer = PorterStemmer()
    with open(path) as f:
        for line in f.readlines():
            values = line.split('|')
            phone = values[0]
            sentences = values[1:]
            text = ' '.join(sentences).lower()
            # Remove punctuation
            text = re.sub(r'[^\w\']+', ' ', text)
            # Tokenize
            tokens = word_tokenize(text)
            # Stem
            stemmed = map(stemmer.stem, tokens)
            pros_cons[phone] = ' '.join(stemmed)
    return pd.Series(pros_cons.values(), index=pros_cons.keys())

if __name__ == '__main__':
    pc = load_pros_cons(argv[1])
    print(pc.head())
