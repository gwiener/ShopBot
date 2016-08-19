"""
Experiment file
"""

import pandas as pd
import json
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


class Experiment(object):
    def __init__(self):
        self.defaults = {
            "size": 0, "weight": 0, "resolution": 0, "display": 0, "pixel_density": 0,
            "camera": 0, "cpu": 0, "ram": 0, "battery": 0, "data": 0
        }
        self.enc_labels = []
        self.enc = DictVectorizer(sparse=False)

    def load_pros_cons(self, path):
        pros_cons = {}
        with open(path) as f:
            for line in f.readlines():
                values = line.split('|')
                phone = values[0]
                sentences = values[1:]
                pros_cons[phone] = ' '.join(sentences)
        return pd.Series(pros_cons)

    def load_labels(self, path):
        data = {}
        with open(path) as f:
            labels = json.load(f)
        for phone, attrs in labels.items():
            bats = [v for k, v in attrs.items() if k.startswith('battery')]
            battery = (bats and int(sum(bats) / len(bats))) or 1
            new_attrs = {k: v for k, v in attrs.items() if not k.startswith('battery')}
            new_attrs['battery'] = battery
            data[phone] = self.defaults.copy()
            data[phone].update(new_attrs)
        return pd.DataFrame(data=data.values(), index=data.keys())

    def load(self, labels_path, pros_cons_path):
        df = self.load_labels(labels_path)
        pc = self.load_pros_cons(pros_cons_path)
        df['text'] = pc
        self.data = df

    def run(self):
        self.load('labels.json', 'proscons.csv')
        print self.data.head()
        lab_cols = self.defaults.keys()
        lab_data = self.data[lab_cols]
        recs = lab_data.to_dict('records')
        self.enc.fit(recs)
        Y = self.enc.transform(recs)
        Y_ = self.enc.inverse_transform(Y)
        print Y_[:10]

if __name__ == '__main__':
    Experiment().run()
