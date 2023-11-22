from elasticsearch import Elasticsearch
from config import INDEX
from es import es

from konlpy.tag import Okt
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

model_save_path = "path/to/save/model"
if __name__ == "__main__":
    # korean word tokenizer
    okt = Okt()

    # fetch data from Elasticsearch
    scroll_query = {
        "query" : {
            "match_all" : {}
        }
    }
    scroll_size = 1000
    result = es.search(index=INDEX, scroll='2m', size=scroll_size, body=scroll_query)
    scroll_id = result['_scroll_id']

    # extract "contents" field from documents
    documents = [hit['_source']['contents'] for hit in result['hits']['hits']]

    # scroll api
    while len(result['hits']['hits']) > 0:
        result = es.scroll(scroll_id=scroll_id, scroll='2m')
        documents.extend([hit['_source']['contents'] for hit in result['hits']['hits']])

    es.clear_scroll(scroll_id=scroll_id)

    # convert documents into TaggedDocument
    tagged_data = [TaggedDocument(words=okt.morphs(doc), tags=[str(i)]) for i, doc in enumerate(documents)]

    # train Doc2Vec
    model = Doc2Vec(vector_size=256, window=2, min_count=1, workers=4, epochs=100)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)
    model.random.seed(0)

    # save model to persistent disk
    model.save(model_save_path)

    # Use a scroll query to iterate through all documents in the index
    scroll_query = {
        "query": {
            "match_all": {}
        }
    }

    result = es.search(index=index_name, scroll='2m', size=scroll_size, body=scroll_query)
    scroll_id = result['_scroll_id']

    # Update documents with the inferred vectors
    for hit in result['hits']['hits']:
        contents_value = hit['_source']['contents']
        vector_value = model.infer_vector(okt.morphs(contents_value))

        update_query = {
            "doc": {
                "d2v_vector": vector_value.tolist()
            }
        }

        es.update(index=index_name, id=hit['_id'], body=update_query)

    # Continue scrolling to update all documents
    while len(result['hits']['hits']) > 0:
        result = es.scroll(scroll_id=scroll_id, scroll='2m')

        for hit in result['hits']['hits']:
            contents_value = hit['_source']['contents']
            vector_value = model.infer_vector(okt.morphs(contents_value))

            update_query = {
                "doc": {
                    "d2v_vector": vector_value.tolist()
                }
            }

            es.update(index=index_name, id=hit['_id'], body=update_query)

    # Clear the scroll
    es.clear_scroll(scroll_id=scroll_id)
