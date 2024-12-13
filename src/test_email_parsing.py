import unittest
from corpus import Corpus
from src.email.email import Email

EMAILS_PATH = './assets/1/'
EMAIL_BODY_PREVIEW_LENGTH = 100  # Extracted constant for email body truncation length


class TestEmailParser(unittest.TestCase):
    corpus: Corpus

    def setUp(self):
        self.corpus = Corpus(EMAILS_PATH)

    def test_parse_all_emails(self):
        for file_name, content in self.corpus.emails():
            self._parse_and_print_email(file_name, content)

    @staticmethod
    def _parse_and_print_email(email_id: str, content: str):
        print("====================")
        print(f"Parsing email {email_id}:")
        print(content)
        email = Email.from_string(content)
        email.body = email.body[:EMAIL_BODY_PREVIEW_LENGTH] + "..."
        print("====================")
        print("Parsed email:")
        print(email)
