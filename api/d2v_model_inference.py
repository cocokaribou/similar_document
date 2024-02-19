from elasticsearch import Elasticsearch

from konlpy.tag import Okt, Kkma
from gensim.models import Doc2Vec

from config import HOST, PORT, USER, PW

if __name__ == "__main__":
    # korean word tokenizer
    kkm = Kkma()

    # load model
    model = Doc2Vec.load("./doc2vecmodel.mod")

    query = {
        "query": {
            "bool": {
                "filter": {
                    "script": {
                        "script": "doc['contents'].size() > 300"
                    }
                }
            }
        }
    }
    es = Elasticsearch(
        hosts=[{'host': HOST, 'port': PORT, 'scheme': "https"}],
        request_timeout=300, max_retries=10, retry_on_timeout=True,
        basic_auth=(USER, PW)
    )
    docs = es.search(index="dschool", body=query, size=10000)["hits"]["hits"]

    for doc in docs:
        text = doc["_source"]["contents"]
        tokens = kkm.morphs(text)
        vector = model.infer_vector(tokens)
        es.update(index="dschool", id=doc["_id"], body={"doc": {"vec": vector}})

    result = es.search(index="dschool", body=query, size=10)["hits"]["hits"]
