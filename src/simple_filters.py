import random
from basefilter import BaseFilter
from corpus import Corpus
from quality import OK_TAG, SPAM_TAG


class NaiveFilter(BaseFilter):
    def test(self, path: str):
        corpus = Corpus(path)

        prediction = {}
        for name, _ in corpus.emails():
            prediction[name] = OK_TAG
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
            prediction[name] = random.choice([OK_TAG, SPAM_TAG])
        self.write_prediction_to_file(path, prediction)
