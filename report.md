# Implementing ShopBot

In this work I focused on the problem of finding the objective of the 
customer query in a robust way. I based my work on the given example where a
set of given keywords is used for tagging. The drawback of this method that I
aimed at improving is that determining the most indicative set of keywords is
not a trivial task. There may be additional keywords that the writer is not
aware of, or some set phrases may be better indicators than a single word.

Ideally, we would prefer the keywords and their relative weights would be learn
automatically by the tagging algorithm. That is, given a large volume of 
relevant text, a data mining algorithm would deduce both the topic and its
indicative keywords. However, despite a sincere attempt, this goal remained
beyond the scope of this project at the given time frame.

Instead, I worked toward obtaining a samples set of manageable size, tagging it
manually, and using it as ground truth for a machine learning algorithm. 
The design goals and assumptions for the algorithm were:

1. Work with short, natural sentences, so that minimal post-processing
 over the text is required.
1. Match one sentence with one tag. Analyzing multiple objectives
 at once is out of scope.
1. Return a confidence score, so that an application using it can decide when
 not to present the result to the user, and ask for input instead.
1. Support adding tagged samples, so that users' input may be incorporated into
 the system.
1. If possible, the set of tags should not be limited, allowing more flexible
user input.

## Obtaining data
As the main source of data I downloaded mobile phones specs pages from 
[Phone Arena](http://www.phonearena.com/). 
See for example this [Samsung Galaxy Express ](http://www.phonearena.com/phones/Samsung-Galaxy-Express-3_id10039) page.

After crawling and downloading 7456 phone pages, I extracted their pros and cons
lists, appearing in the middle-left panel. These were meant to serve as a 
representative body of text for what customers are saying about mobile phones.
Since there where only 37 set phrases used as cons and pros, I tagged them 
manually according to the objective appearing in the specs: size, weight, 
resolution, pixel density, etc. The result is the [tagged samples](tagged.csv) file.

## Analyzing data

Since 37 phrases may be a too small corpus, I also extracted each phone description
into a [descriptions](desc.scv) file. I then compared the descriptions vocabulary
with baseline English, using the *Brown corpus* 
(see [NLTK data](http://www.nltk.org/nltk_data/) item 5) and 
Conditional Frequency Distribution analysis (see [Chapter 2 of the NLTK book](http://www.nltk.org/book/ch02.html), section 2.2).
The [desc.py](desc.py) script includes the code for this analysis (also requiring additional downloads).

The above analysis resulted in a set of 200 keywords that are more common to the domain of
mobile phones than new or romance English. I selected the more unique ones, and appended
them as to the tagged samples set.

## Tagging customer queries

To withstand the above design goals, I implemented a K-Nearest-Neighbors tagger
where document similarity is the distance metrics, and tags from the most similar
samples are weighted by their similarity. 
The tagged samples are tokenized, stemmed, and transformed using TF-IDF to the
data matrix. Queries are likewise tokenized and stemmed. The TF-IDF similarity
score is computed for each sample, and the top K "vote" for the selected tag.
The [tagger module](tagger.py) implements this algorithm, 
with a similar interface to scikit-learn classifiers.

The [bot module](bot.py) exposes the `predict_proba` method 
as a REST API POST operation using [Klein](http://klein.readthedocs.io/).
 
## Adding samples

One advantage of KNN is that samples can be added without an expensive re-training.
This way, when the probability of the prediction is too low, the application may
decide to ask the user for additional input.
The tagger `add` method takes a document and a tag and add its data set.
Since in the current settings the number of samples may be small, each new sentence
may affect the terms frequencies significantly. Therefore, the TF-IDF matrix is
recalculated. This may not be necessary once the data set is large enough.

The [bot module](bot.py) exposes the this method as a REST API PUT operation.

## Roads not taken
Due to the short time-frame, I have not followed these possible approaches:

1. As mentioned before, ideally the tags where learned from the text as well,
making manual tagging redundant. This is not impossible, since, for example,
[Phone Arena](http://www.phonearena.com/) pages include specs for each phone.
By comparing these specs, an algorithm may be able to determine that a phone
is, e.g., heavier than others, and therefore its reviewers are likely to
complain about its weight.

1. I did not use the full text of phone reviewers, although it is richer than
the succinct pros-and-cons list and descriptions.
 
1. KNN is one possible algorithm. Other algorithms, e.g. Neural Networks, may
yield better accuracy and performance. However, the small data set that I had
the time to extract and analyze was not sufficient for training large models.

1. I did not not implement a tagger for the constraint attached the objective.
A very similar approach may be used to the same end, i.e. use a tagger with
a samples set of positive ("I want...") and negative ("I don't want...")
short samples.


