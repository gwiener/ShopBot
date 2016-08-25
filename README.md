# ShopBot

The ShopBot project is a proof-of-concept for tagging shoppers' queries 
with their objective.

## Prerequisites
Running ShopBot requires Python 3.5 with the following packages installed: 
`scikit-learn`, `pandas`, `klein` and `nltk` with `punkt` tokenizer models.

Execute the following commands, if needed:
    
    $ pip install scikit-learn pandas klein nltk
    $ python
    >>> import nltk
    >>> nltk.download('punkt')

Alternatively, run `python install.py`.

## Running the service

To try ShopBot, clone this repository, `cd` into the main folder and run

    python bot.py [options]

Options include:

option | meaning | default
---|---|--- 
`--port` | web server port | 8080
`--file` | tagged samples file to load | `tagged.csv`
`-K` | number of similar docs to consider | 3

## Operations
The service exposes the following REST API operations

### Query
`POST /v1/tags` where the request content is the query to tag.
The query is expected to be a single sentence, and the service returns a single tag
with its probability in JSON format.

#### Examples
```bash
$ curl -s -d "I want a lightweight phone" "http://localhost:8080/v1/tags"
{"tagging": "weight", "probability": 0.692, "text": "lightweight phone"}
```
```bash
$ curl -s -d "does it have enough RAM?" "http://localhost:8080/v1/tags"
{"tagging": "memory", "probability": 1.0, "text": "does it have enough RAM?"}
```
```bash
$ curl -s -d "I want to take selfies!" "http://localhost:8080/v1/tags"
{"tagging": "camera", "probability": 1.0, "text": "I want to take selfies!" }
```
### Update
`PUT /v1/tags` where the request content is a JSON object with `text` and `tag`
fields. The service will add the tagged sample to its documents set. 
The operation returns 'OK'

#### Example
```bash
$ curl -s -X PUT -d '{"text": "Java applets", "tag": "java"}' "http://localhost:8080/v1/tags"
OK
$ curl -s -d "I like java games" "http://localhost:8080/v1/tags"
{"tagging": "java", "probability": 0.542, "text": "java phone"}
```

## Details
Read [the full report](report.md) for the implementation details, algorithms and background.