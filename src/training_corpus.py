from typing import Dict
import os
from corpus import Corpus
from quality import OK_TAG, SPAM_TAG, TRUTH_FILENAME
from utils import read_classification_from_file


class TrainingCorpus(Corpus):
    classification: Dict[str, str]

    def __init__(self, path: str):
        super().__init__(path)

        self.classification = read_classification_from_file(
            os.path.join(path, TRUTH_FILENAME)
        )

    def get_class(self, email_name: str):
        return self.classification[email_name]

    def is_ham(self, email_name: str):
        return self.classification[email_name] == OK_TAG

    def is_spam(self, email_name: str):
        return self.classification[email_name] == SPAM_TAG
