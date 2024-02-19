from gensim.models import Doc2Vec
from gensim.models.callbacks import CallbackAny2Vec
from gensim.models.doc2vec import TaggedDocument
from konlpy.tag import Okt, Kkma
from es import es
import os


class LossCallback(CallbackAny2Vec):
    '''Callback to print loss after each epoch.'''

    def __init__(self):
        self.epoch = 0
        self.previous_loss = 0

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss() - self.previous_loss
        self.previous_loss = model.get_latest_training_loss()
        print('Loss after epoch {}: {}'.format(self.epoch, loss))
        self.epoch += 1


if __name__ == "__main__":
    # korean word tokenizer
    kkm = Kkma()

    documents = es.get_contents_over_500_words()

    # tagged data
    tagged_data = [TaggedDocument(words=kkm.morphs(doc), tags=[idx]) for idx, doc in enumerate(documents)]

    # # Doc2Vec 모델 생성 및 훈련
    model = Doc2Vec(vector_size=50, window=2, min_count=1, dm=1, workers=4)
    model.build_vocab(tagged_data)
    model.random.seed(0)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=100, callbacks=[LossCallback()])

    model.save("./doc2vecmodel.mod")
