import re
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def load_tagged_file(path):
    """
    Load tagged docs from colon-separated text file
    :param path: path to file
    :return: a pair of lists (docs, tags)
    """
    df = pd.read_csv(path, sep='|', names=['doc', 'tag'], comment='#', skip_blank_lines=True)
    return df['doc'].str.strip().tolist(), df['tag'].str.strip().tolist()


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
        self.docs = [self.prepare(doc) for doc in docs]
        self.x = self.vec.fit_transform(self.docs)

    @staticmethod
    def vote(scores):
        """
        Given a list of scored tags, return the tag with the highest total score
        :param scores: a list of {tag, score} dictionaries, where tag is not unique, and score is numerical
        :return: selected tag
        """
        df = pd.DataFrame(scores)
        return df.groupby('tag')['score'].sum().argmax()

    @staticmethod
    def vote_proba(scores):
        """
        Given a list of scored tags, return the tag with the highest total score and its probability
        :param scores: a list of {tag, score} dictionaries, where tag is not unique, and score is numerical
        :return: a pair of the selected tag and the sum of its scores, normalized
        """
        df = pd.DataFrame(scores)
        sums = df.groupby('tag')['score'].sum()
        total = sum(sums)
        tag = sums.argmax()
        proba = sums[tag] / total
        return tag, proba

    def _score(self, query):
        """
        Return scoring for each tag of each one of the K most similar documents
        :param query: short text
        :return: a list of dictionaries {tag, score}
        """
        prep_query = self.prepare(query)
        q = self.vec.transform([prep_query])[0]
        sim = (q * self.x.T).A[0]
        idx = sim.argsort()[-self.k:]
        tag_scores = [{'tag': self.tags[i], 'score': sim[i]} for i in idx]
        return tag_scores

    def predict(self, query):
        """
        Predict the tag for a query sentence using weighted k-nearest-neighbor classification
        :param query: short text
        :return: voted tag out of the k most similar documents from the tagged set
        """
        tag_scores = self._score(query)
        return self.vote(tag_scores)

    def predict_proba(self, query):
        """
        Predict the probability of a tag for a query sentence using weighted k-nearest-neighbor classification
        :param query: short text
        :return: voted tag out of the k most similar documents from the tagged set and its normalized probability
        """
        tag_scores = self._score(query)
        return self.vote_proba(tag_scores)

    def add(self, doc, tag):
        """
        Add a tagged sample to the corpus, re-fit the vectorizer and re-transform the data.
        Since the corpus may be small, the added doc may be influential.
        Therefore re-running fit_transform is required, albeit slow.
        :param doc: Additional short text
        :param tag: a tag for the text
        """
        prep_doc = self.prepare(doc)
        self.docs.append(prep_doc)
        self.tags.append(tag)
        self.x = self.vec.fit_transform(self.docs)
