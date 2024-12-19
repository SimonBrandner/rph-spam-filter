import unittest
from corpus import Corpus
from parsed_email import ParsedEmail

EMAILS_PATH = './assets/1/'
EMAIL_BODY_PREVIEW_LENGTH = 100  # Extracted constant for email body truncation length


class TestEmailParser(unittest.TestCase):
    corpus: Corpus

    def setUp(self):
        self.corpus = Corpus(EMAILS_PATH)

    def test_parse_all_emails(self):
        for filename, content in self.corpus.emails():
            self._parse_and_print_email(filename, content)

    @staticmethod
    def _parse_and_print_email(email_filename: str, content: str):
        print("====================")
        print(f"Parsing email from file {email_filename}.")
        email = ParsedEmail.from_string(content)
        email.body = email.body[:EMAIL_BODY_PREVIEW_LENGTH] + "..."
        email.text = email.text[:EMAIL_BODY_PREVIEW_LENGTH] + "..."
        print("Parsed email:")
        print(email)
