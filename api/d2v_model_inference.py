from konlpy.tag import Okt
from gensim.models import Doc2Vec

from es import es

if __name__ == "__main__":
    # korean word tokenizer
    okt = Okt()

    # load model
    model = Doc2Vec.load("./doc2vecmodel.mod")

    query = {"query": {"match_all": {}}}
    docs = es.search(index="dschool", body=query, size=10000)["hits"]["hits"]

    for doc in docs:
        text = doc["_source"]["contents"]
        tokens = okt.morphs(text)
        vector = model.infer_vector(tokens)
        es.update(index="dschool", id=doc["_id"], body={"doc": {"vec": vector}})

    result = es.search(index="dschool", body=query, size=10)["hits"]["hits"]
