import pandas as pd
from prep_text import load_pros_cons
from sys import argv
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer


class Detector(object):
    def __init__(self, column):
        self.column = column
        self.vec = CountVectorizer(stop_words='english', max_features=100)
        # self.clf = SGDClassifier()
        self.clf = DecisionTreeClassifier()

    def fit(self, df):
        data = df[['text', self.column]].dropna()
        print('training %s on %d samples' % (self.column, len(data)))
        text = data['text']
        col = data[self.column]
        x = self.vec.fit_transform(text)
        # ql = col.quantile([0.2, 0.8])
        ql = col.quantile(0.2)
        # y = ~col.between(*ql)
        y = col <= ql
        self.clf.fit(x, y)
        weights = self.clf.feature_importances_
        args = reversed(weights.argsort()[-10:])
        names = self.vec.get_feature_names()
        print(self.column, [(names[arg], '%.2f' % weights[arg]) for arg in args])

    def predict(self, queries):
        q = self.vec.transform(queries)
        return self.clf.predict(q)


def main():
    text = load_pros_cons(argv[1])
    df = pd.read_csv(argv[2], index_col=[0])
    df['text'] = text
    detectors = [Detector('weight'), Detector('thickness'), Detector('memory'), Detector('standby_time')]
    for det in detectors:
        det.fit(df)
    queries = [
        "I want a lightweight phone",
        "the camera is not good",
        "phone too heavy",
        "weak battery",
        "thin phone",
        "not enough ram"
    ]
    results = {det.column: det.predict(queries) for det in detectors}
    for name, res in results.items():
        print(name)
        for q, p in zip(queries, res):
            print(q, p)

if __name__ == '__main__':
    main()
