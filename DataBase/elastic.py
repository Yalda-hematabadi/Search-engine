from elasticsearch import Elasticsearch, RequestsHttpConnection

es = Elasticsearch(
    ['http://localhost:9200'],
    http_auth=('elastic', '_11+Wl9KHD+bUtuB3j35'),
    connection_class=RequestsHttpConnection
)

resp = es.indices.delete(
    index="search-engine",
)
print(resp)

index_name = 'search-engine'
mapping = {
        "mappings": {
            "properties": {
                "url": {"type": "keyword"},
                "title": {"type": "text"},
                "content": {"type": "text"},
                "tags": {"type": "keyword"},
                "keywords": {"type": "keyword"},
                "published_date": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis||strict_date_optional_time"
                },
                "crawled_date": {
                    "type": "date",
                    "format": "strict_date_optional_time||epoch_millis"
                },
                "label": {"type": "keyword"}
            }
        }
    }

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists.")