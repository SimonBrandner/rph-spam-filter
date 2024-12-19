from corpus import Corpus
from quality import TRUTH_FILENAME


class TrainingCorpus(Corpus):
    def get_class(self, email_name: str):
        pass

    def is_ham(self, email_name: str):
        pass

    def is_spam(self, email_name: str):
        pass

    def spams(self):
        pass

    def hams(self):
        pass
