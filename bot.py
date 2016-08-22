"""
Main script for tagging customer queries
"""
from sys import argv
import fileinput
from klein import Klein
import json
from tagger import load_tagged_file, DocumentSimilarityTagger


class BotServer(object):
    app = Klein()

    def __init__(self, tagger):
        self.tagger = tagger

    @app.route('/v1/tags', methods=['POST'])
    def tag(self, request):
        text = request.content.read().decode('utf-8')
        request.setHeader('Content-Type', 'application/json')
        tag = self.tagger.predict(text)
        reply = {'text': text, 'tagging': tag}
        return json.dumps(reply)

    @app.route('/v1/tags', methods=['PUT'])
    def put(self, request):
        cont = request.content.read().decode('utf-8')
        d = json.loads(cont)
        doc = d['text']
        tag = d['tag']
        self.tagger.add(doc, tag)
        return 'OK'


def serve(tagger):
    bot = BotServer(tagger)
    bot.app.run('localhost', 8080)


def loop(tagger):
    print("Hello, human, how may I assist you?")
    for query in fileinput.input(files=argv[2:]):
        tag = tagger.predict(query)
        print(tag)


def main(op, path):
    docs, tags = load_tagged_file(path)
    tagger = DocumentSimilarityTagger(docs, tags)
    if op.lower() == 'rest':
        serve(tagger)
    else:
        loop(tagger)

if __name__ == '__main__':
    main(argv[1], argv[2])
