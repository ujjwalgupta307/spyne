import os
from elasticsearch import Elasticsearch

# Get the Elasticsearch host from environment variables
es_host = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")

# Initialize the Elasticsearch client
es = Elasticsearch(hosts=[es_host])

def add_discussion_to_index(discussion):
    doc = {
        'user_id': discussion.user_id,
        'text': discussion.text,
        'image':discussion.image,
        'created_on': discussion.created_on.isoformat(),
        'hashtags': [tag.tag for tag in discussion.hashtags]
    }
    es.index(index='discussions', id=discussion.id, body=doc)

def update_discussion_in_index(discussion):
    doc = {
        'user_id': discussion.user_id,
        'text': discussion.text,
        'image': discussion.image,
        'created_on': discussion.created_on.isoformat(),
        'hashtags': [tag.tag for tag in discussion.hashtags]
    }
    es.index(index='discussions', id=discussion.id, body=doc)

def delete_discussion_from_index(discussion):
    es.delete(index='discussions', id=discussion.id)

def search_discussions(query):
    body = {
        'query': {
            'multi_match': {
            'query': query,
            'fields': ['text', 'hashtags']
            }
        }
    }
    res = es.search(index='discussions', body=body)
    return [hit['_source'] for hit in res['hits']['hits']]