from typing import Tuple, Dict
import math

from basefilter import BaseFilter
from corpus import Corpus
from parsed_email import ParsedEmail
from quality import OK_TAG, SPAM_TAG
from training_corpus import TrainingCorpus


def get_words_in_email(email_content: str):
    email = ParsedEmail.from_string(email_content)

    words = email.text.split()
    words += email.subject.split()
    if email.sender is not None:
        words += list(
            filter(
                None,
                [email.sender.username, email.sender.real_name, email.sender.domain],
            )
        )

    return [word.lower() for word in words]


def calculate_word_score(
    word: str,
    word_dict: Dict[str, int],
    total_word_count: int,
):
    if word not in word_dict:
        return 0

    return math.log((word_dict[word]) / total_word_count)


class MyFilter(BaseFilter):
    number_of_spams: int
    number_of_hams: int
    spam_word_count: int
    ham_word_count: int
    spam_word_dict: Dict[str, int]
    ham_word_dict: Dict[str, int]

    def __init__(self):
        super().__init__()
        self.initialize_training()

    def initialize_training(self):
        self.spam_word_count = 0
        self.ham_word_count = 0
        self.number_of_spams = 0
        self.number_of_hams = 0
        self.spam_word_dict = {}
        self.ham_word_dict = {}

    def train(self, path: str):
        self.initialize_training()

        corpus = TrainingCorpus(path)
        for name, content in corpus.emails():
            is_spam = corpus.is_spam(name)

            if is_spam:
                self.number_of_spams += 1
            else:
                self.number_of_hams += 1

            for word in get_words_in_email(content):
                if word not in self.spam_word_dict:
                    self.spam_word_dict[word] = 1
                if word not in self.ham_word_dict:
                    self.ham_word_dict[word] = 1

                if is_spam:
                    self.spam_word_count += 1
                    self.spam_word_dict[word] += 1
                else:
                    self.ham_word_count += 1
                    self.ham_word_dict[word] += 1

    def test(self, path: str):
        corpus = Corpus(path)
        prediction = {}

        if self.number_of_spams + self.number_of_hams != 0:
            for name, content in corpus.emails():
                prediction[name] = self.get_email_class(content)
        else:
            # This has to be done, so that the tests do not fail. For some
            # reason, they do call the train() method
            for name, _ in corpus.emails():
                prediction[name] = OK_TAG

        self.write_prediction_to_file(path, prediction)

    def get_initial_scores(self) -> Tuple[float, float]:
        number_of_emails = self.number_of_spams + self.number_of_hams
        ham_score = math.log(self.number_of_hams / number_of_emails)
        spam_score = math.log(self.number_of_spams / number_of_emails)
        return (ham_score, spam_score)

    def get_email_class(self, email_content: str) -> str:
        ham_score, spam_score = self.get_initial_scores()
        for word in get_words_in_email(email_content):
            ham_score += calculate_word_score(
                word, self.ham_word_dict, self.ham_word_count
            )
            spam_score += calculate_word_score(
                word, self.spam_word_dict, self.spam_word_count
            )

        return OK_TAG if ham_score > spam_score else SPAM_TAG
