"""
Experiment file
"""

import json


class Experiment(object):
    def __init__(self):
        self.pros_cons = {}
        self.labels = {}

    def load_pros_cons(self, path):
        with open(path) as f:
            for line in f.readlines():
                values = line.split('|')
                phone = values[0]
                sentences = values[1:]
                self.pros_cons[phone] = sentences

    def load_labels(self, path):
        with open(path) as f:
            self.labels = json.load(f)

    def run(self):
        self.load_pros_cons('proscons.csv')
        self.load_labels('labels.json')

if __name__ == '__main__':
    Experiment().run()
