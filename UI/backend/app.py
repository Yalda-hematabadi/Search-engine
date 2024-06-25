from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Initialize Elasticsearch connection
es = Elasticsearch(
    ['http://localhost:9200'],
    http_auth=('elastic', '_11+Wl9KHD+bUtuB3j35'),
)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    logging.info(f"Received query: {query}")
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "content", "tags", "keywords"]
            }
        }
    }

    try:
        res = es.search(index="search-engine", body=search_body)
        logging.info(f"Elasticsearch response: {res}")
        
        hits = res.get('hits', {})
        total = hits.get('total', {}).get('value', 0)
        results = hits.get('hits', [])
        
        formatted_results = []
        for hit in results:
            formatted_hit = {
                "id": hit['_id'],
                "score": hit['_score'],
                "title": hit['_source'].get('title', ''),
                "content": hit['_source'].get('content', '')[:200] + '...',
                "url": hit['_source'].get('url', ''),
            }
            formatted_results.append(formatted_hit)

        response = {
            "total": total,
            "results": formatted_results
        }
        logging.info(f"Sending response: {response}")
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error during search: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)