import random
from basefilter import BaseFilter
from corpus import Corpus
from test_filterbase import HAM_TAG, SPAM_TAG


class NaiveFilter(BaseFilter):
    def test(self, path: str):
        corpus = Corpus(path)

        prediction = {}
        for name, _ in corpus.emails():
            prediction[name] = HAM_TAG
        self.write_prediction_to_file(path, prediction)


class ParanoidFilter(BaseFilter):
    def test(self, path: str):
        corpus = Corpus(path)

        prediction = {}
        for name, _ in corpus.emails():
            prediction[name] = SPAM_TAG
        self.write_prediction_to_file(path, prediction)


class RandomFilter(BaseFilter):
    def test(self, path: str):
        corpus = Corpus(path)

        prediction = {}
        for name, _ in corpus.emails():
            prediction[name] = random.choice([HAM_TAG, SPAM_TAG])
        self.write_prediction_to_file(path, prediction)
