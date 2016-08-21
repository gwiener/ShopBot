from sys import argv
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

stemmer = PorterStemmer()


def prepare(s):
    # lowercase and remove punctuation
    t = re.sub(r'[^\w\']+', ' ', s.strip().lower())
    # tokenize
    l = word_tokenize(t)
    # stem
    map(stemmer.stem, l)
    # re-join
    return ' '.join(l)


def load_tagged(path):
    docs = []
    tags = []
    with open(path) as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            values = line.split('|')
            doc = prepare(values[0])
            tag = values[1].strip()
            docs.append(doc)
            tags.append(tag)
    return docs, tags


def main():
    docs, tags = load_tagged(argv[1])
    vec = TfidfVectorizer(stop_words='english')
    x = vec.fit_transform(docs)
    q = prepare("I want a light phone")
    qv = vec.transform([q])[0]
    sim = (qv * x.T).A[0]
    s = sim.argsort()[-3:]
    for i in s:
        print(docs[i], tags[i], '%.2f' % sim[i])


if __name__ == '__main__':
    main()
