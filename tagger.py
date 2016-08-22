import re
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


class DocumentSimilarityTagger(object):
    stemmer = PorterStemmer()

    @classmethod
    def prepare(cls, s):
        """
        Prepare a sentence for tf-idf processing:
        Strip, convert to lowercase, tokenize and stem.
        :param s: short text
        :return: prepared s
        """
        t = re.sub(r'[^\w\']+', ' ', s.strip().lower())
        l = map(cls.stemmer.stem, word_tokenize(t))
        return ' '.join(l)

    def __init__(self, docs, tags, k=3):
        """
        Initialize the tagger: fit the tf-idf vectorizer and transform the documents
        :param docs: a list of sample documents
        :param tags: a list of tags, must be in the same length as the docs, each tags a single doc
        """
        self.tags = tags
        self.k = k
        self.vec = TfidfVectorizer(stop_words='english')
        self.x = self.vec.fit_transform(docs)

    @staticmethod
    def vote(scores):
        """
        Given a list of scored tags, return the tag with the highest total score
        :param scores: a list of {tag, score} dictionaries, where tag is not unique, and score is numerical
        :return: selected tag
        """
        df = pd.DataFrame(scores)
        return df.groupby('tag')['score'].sum().argmax()

    def predict(self, query):
        """
        Predict the tag for a query sentence using weighted k-nearest-neighbor classification
        :param query: short text
        :return: voted tag out of the k most similar documents from the tagged set
        """
        prep_query = self.prepare(query)
        q = self.vec.transform([prep_query])[0]
        sim = (q * self.x.T).A[0]
        idx = sim.argsort()[-self.k:]
        tag_scores = [{'tag': self.tags[i], 'score': sim[i]} for i in idx]
        return self.vote(tag_scores)
