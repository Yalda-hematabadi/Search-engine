from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
es = Elasticsearch(['http://localhost:9200'])

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content", "tags", "keywords"]
            }
        }
    }

    res = es.search(index="webpages", body=search_body)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
