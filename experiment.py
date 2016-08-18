"""
Experiment file
"""

import json
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

class Experiment(object):
    def __init__(self):
        self.pros_cons = {}
        self.labels = {}
        self.defaults = {
            "size": 0, "weight": 0, "resolution": 0, "display": 0, "pixel_density": 0,
            "camera": 0, "cpu": 0, "ram": 0, "battery": 0, "data": 0
        }
        self.enc_labels = []

    def load_pros_cons(self, path):
        with open(path) as f:
            for line in f.readlines():
                values = line.split('|')
                phone = values[0]
                sentences = values[1:]
                self.pros_cons[phone] = sentences

    def load_labels(self, path):
        with open(path) as f:
            labels = json.load(f)
        for phone, attrs in labels.items():
            bats = [v for k, v in attrs.items() if k.startswith('battery')]
            battery = (bats and int(sum(bats) / len(bats))) or 1
            new_attrs = {k: v for k, v in attrs.items() if not k.startswith('battery')}
            new_attrs['battery'] = battery
            self.labels[phone] = self.defaults.copy()
            self.labels[phone].update(new_attrs)

    def encode_labels(self):
        ohe = OneHotEncoder()
        labels = [l.values() for k, l in self.labels.items()]
        ohe.fit(labels)
        self.enc_labels = ohe.transform(labels)

    def run(self):
        self.load_pros_cons('proscons.csv')
        self.load_labels('labels.json')
        self.encode_labels()
        print self.enc_labels.toarray()[:10, :]

if __name__ == '__main__':
    Experiment().run()
