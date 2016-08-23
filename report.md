# Implementing ShopBot

In this work I focused mainly on the problem of finding the objective of the 
customer query in a robust way. I based my work on the given example where a
set of given keywords is used for tagging. The drawback of this method that I
aimed at improving is that determining the most indicative set of keywords is
not a trivial task. There may be additional keywords that the writer is not
aware of, or some set phrases may be better indicators than a single word.

Ideally, we would prefer the keywords and their relative weights in different
contexts would be learn automatically by tha tagging algorithm.