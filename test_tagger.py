import unittest
from tagger import DocumentSimilarityTagger, load_tagged_file


class TaggerTest(unittest.TestCase):
    def test_prepare(self):
        s = "I am trying-to hunt rabbits"
        t = DocumentSimilarityTagger.prepare(s)
        self.assertEqual(t, "i am tri to hunt rabbit")

    def test_vote(self):
        scores = [{'tag': a, 'score': b}
                  for a, b in [('a', 0.2), ('b', 0.5), ('c', 0.1), ('a', 0.4), ('c', 0.2)]]
        tag = DocumentSimilarityTagger.vote(scores)
        self.assertEqual(tag, 'a')

    def test_simple_predict(self):
        tagged = {
            'I want a big phone': 'size',
            'I want a small phone': 'size',
            "I'm concerned about water on phone": 'water'
        }
        tagger = DocumentSimilarityTagger(list(tagged.keys()), list(tagged.values()), k=1)
        query = "I want a water-resistant phone"
        tag = tagger.predict(query)
        self.assertEqual(tag, 'water')

    def test_simple_predict_proba(self):
        tagged = {
            'I want a big display': 'size',
            'I am looking for a small phone': 'size',
            "I'm concerned about water on phone": 'water'
        }
        tagger = DocumentSimilarityTagger(list(tagged.keys()), list(tagged.values()), k=3)
        query = "I want a water-resistant phone"
        tag, proba = tagger.predict_proba(query)
        self.assertEqual(tag, 'water')
        self.assertGreater(proba, 0)
        self.assertLess(proba, 1)

    def test_load_tagged(self):
        docs, tags = load_tagged_file('tagged.csv')
        self.assertEqual(len(docs), len(tags))
        self.assertGreater(len(docs), 0)

    def test_add(self):
        tagged = {
            'I want a big phone': 'size',
            'I want a small phone': 'size',
        }
        tagger = DocumentSimilarityTagger(list(tagged.keys()), list(tagged.values()), k=1)
        tagger.add("I'm concerned about water on phone", 'water')
        query = "I want a water-resistant phone"
        tag = tagger.predict(query)
        self.assertEqual(tag, 'water')

    def test_answer_correctly(self):
        train_docs, train_tags = load_tagged_file('tagged.csv')
        test_docs, test_tags = load_tagged_file('test.csv')
        tagger = DocumentSimilarityTagger(train_docs, train_tags, k=3)
        for doc, tag in zip(test_docs, test_tags):
            prediction = tagger.predict(doc)
            self.assertEqual((doc, prediction), (doc, tag))
