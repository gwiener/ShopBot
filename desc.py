""" Extract indicative n-grams from descriptions """

from sys import argv
import re
import nltk
from nltk.corpus import brown
from nltk.corpus import stopwords


stops = stopwords.words("english")
words = []
with open(argv[1]) as f:
    for line in f.readlines():
        phone, desc = line.split('|')
        sentence = re.sub(r'[^\w\']+', ' ', desc.strip().lower())
        phone_words = re.split(r'[-_]', phone)[:-1]
        desc_words = sentence.split()
        filtered_words = [word for word in desc_words
                          if word not in phone_words and word not in stops and len(word) > 1]
        words += [('phone', w) for w in filtered_words]

words.extend([('english', w) for w in brown.words(categories='news') if w not in stops])
words.extend([('english', w) for w in brown.words(categories='romance') if w not in stops])
cfd = nltk.ConditionalFreqDist(words)
most_common = cfd['phone'].most_common(200)
for w, freq in most_common:
    print(w)

