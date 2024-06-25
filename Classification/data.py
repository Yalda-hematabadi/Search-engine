from elasticsearch import Elasticsearch
import pandas as pd
import csv

es = Elasticsearch(
    ['http://localhost:9200'],
    http_auth=('elastic', '_11+Wl9KHD+bUtuB3j35')
)

query = {
    "query": {
        "match_all": {}
    },
    "size": 10000
}

response = es.search(index="search-engine", body=query, scroll='2m')

all_hits = []

scroll_id = response['_scroll_id']
scroll_size = len(response['hits']['hits'])

while scroll_size > 0:
    all_hits.extend(response['hits']['hits'])
    
    response = es.scroll(scroll_id=scroll_id, scroll='2m')
    
    scroll_id = response['_scroll_id']
    scroll_size = len(response['hits']['hits'])

df = pd.DataFrame([hit['_source'] for hit in all_hits])

df.to_csv('elasticsearch_data.csv', index=False)

print(f"Data saved to elasticsearch_data.csv")