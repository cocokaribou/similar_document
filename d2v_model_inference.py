from elasticsearch import Elasticsearch
from config import INDEX
from es import es

from konlpy.tag import Okt
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument

from es import es

from gensim.models.callbacks import CallbackAny2Vec

if __name__ == "__main__":
    # korean word tokenizer
    okt = Okt()

    model = Doc2Vec.load("./doc2vecmodel.mod")
    # test
    doc1 = "청담安 이라고 들어보셨나요 ?"
    doc2 = ""
    #
    vec1 = model.infer_vector(okt.morphs(doc1))
    similarity1 = model.dv.similarity(0, 1)
    print(similarity1)


