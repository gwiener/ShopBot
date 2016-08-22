"""
Main script for tagging customer queries
"""

from sys import argv
import fileinput
from tagger import load_tagged_file, DocumentSimilarityTagger


def main(path):
    docs, tags = load_tagged_file(path)
    tagger = DocumentSimilarityTagger(docs, tags)
    print("Hello, human, how may I assist you?")
    for query in fileinput.input(files=argv[2:]):
        tag = tagger.predict(query)
        print(tag)


if __name__ == '__main__':
    main(argv[1])
