import pandas as pd
from prep_text import load_pros_cons
from sys import argv
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer

text = load_pros_cons(argv[1])
df = pd.read_csv(argv[2], index_col=[0])
df['text'] = text
data = df[['text', 'weight']].dropna()
ql = data.weight.quantile([0.2, 0.8])
y = data.weight.between(*ql)
print(y.value_counts())
vec_ = CountVectorizer(stop_words='english', max_features=50)
x = vec_.fit_transform(data['text'])
# clf = DecisionTreeClassifier()
clf = SGDClassifier()
score = cross_val_score(clf, x, y)
print(score)

clf.fit(x, y)
queries = ["I want a lightweight phone", "the camera is not good", "phone too heavy", "weak battery", "thin phone"]
q = vec_.transform(queries)
print(clf.predict(q))
# print(clf.predict_proba(q))

