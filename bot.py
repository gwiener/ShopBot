"""
Main script for tagging customer queries
"""
from klein import Klein
from argparse import ArgumentParser
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
        tag, proba = self.tagger.predict_proba(text)
        reply = {'text': text, 'tagging': tag, 'probability': proba}
        return json.dumps(reply)

    @app.route('/v1/tags', methods=['PUT'])
    def put(self, request):
        cont = request.content.read().decode('utf-8')
        d = json.loads(cont)
        doc = d['text']
        tag = d['tag']
        self.tagger.add(doc, tag)
        return 'OK'


def serve(tagger, port):
    bot = BotServer(tagger)
    bot.app.run('localhost', port)


def main(args):
    docs, tags = load_tagged_file(args.file)
    tagger = DocumentSimilarityTagger(docs, tags, k=args.K)
    serve(tagger, args.port)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--port', nargs='?', type=int, default=8080, help='REST API port')
    parser.add_argument('--file', nargs='?', type=str, default='tagged.csv', help='Path to tagged samples file')
    parser.add_argument('-K', nargs='?', type=int, default=3, help='Number of similar documents to consider')
    args = parser.parse_args()
    main(args)
