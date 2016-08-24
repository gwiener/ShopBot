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

