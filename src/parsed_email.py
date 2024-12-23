from address import Address
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urlparse, ParseResult
from bs4 import BeautifulSoup
import re

REPLY_PREFIXES = ['Re:', 'RE:']
FORWARD_PREFIXES = ['Fw:', 'FW:']
HEAD_KEY_FROM = 'From'
HEAD_KEY_SUBJECT = 'Subject'
HEAD_KEY_IN_REPLY_TO = 'In-Reply-To'
HEAD_KEY_REFERENCES = 'References'
URL_EXTRACTION_REGEX = r"https?:\/\/.*?(?=(?:\s|$))"

@dataclass
class ParsedEmail:
    body: str
    text: str
    subject: str
    urls: List['ParseResult']
    sender: Optional['Address'] = None
    is_reply: bool = False
    is_forward: bool = False

    @classmethod
    def from_string(cls, string: str) -> 'ParsedEmail':
        sections = string.split('\n\n', maxsplit=1)
        head, body = sections[0], "\n\n".join(sections[1:])

        sender_entries = cls._extract_head_entries(HEAD_KEY_FROM, head)
        subject_entries = cls._extract_head_entries(HEAD_KEY_SUBJECT, head)

        if len(sender_entries) < 1:
            raise ValueError(
                f'Failed to extract mandatory "{HEAD_KEY_FROM}" entry from email head:\n\n{head}'
            )

        sender = None
        try:
            sender = Address.from_string(sender_entries[0])
        except ValueError:
            pass
        subject = subject_entries[0] if len(subject_entries) > 0 else ""

        is_reply = cls._is_reply(subject, head)
        is_forward = cls._is_forward(subject)

        text = cls._extract_text(body)
        urls = cls._extract_urls(body)

        return cls(body=body, text=text, subject=subject, urls=urls, sender=sender, is_reply=is_reply, is_forward=is_forward)

    @staticmethod
    def _extract_text(body: str) -> str:
        soup = BeautifulSoup(body, 'html.parser')
        return soup.get_text()

    @staticmethod
    def _extract_urls(body: str) -> List['ParseResult']:
        parsed_urls = []
        url_matches = re.findall(URL_EXTRACTION_REGEX, body)

        for url in url_matches:
            try:
                parsed_url = urlparse(url)
                if parsed_url.netloc:
                    parsed_urls.append(parsed_url)
            except:
                pass

        return parsed_urls

    @staticmethod
    def _extract_head_entries(entry_key: str, head: str) -> List[str]:
        entry_splitter = '\n' + entry_key + ': '
        entries = []
        after_key = head

        while True:
            parts = after_key.split(entry_splitter, maxsplit=1)
            if len(parts) == 1:
                break

            after_key = parts[1]
            after_key_lines = after_key.splitlines()
            if len(after_key_lines) < 1:
                entries.append('')
                continue

            content = after_key_lines[0].strip()
            for line in after_key_lines[1:]:
                if not len(line) > 5:
                    break
                line_starts_with_spaces = line.startswith("    ")
                line_starts_with_tab = line.startswith("\t")
                if line_starts_with_spaces or line_starts_with_tab:
                    start_shift = 4 if line_starts_with_spaces else 1
                    content += " " + line[start_shift:].strip()
                else:
                    break
            entries.append(content)

        return entries

    @classmethod
    def _is_head_entry_present(cls, entry_key: str, head: str) -> bool:
        return len(cls._extract_head_entries(entry_key, head)) > 0

    @classmethod
    def _is_reply(cls, subject: str, head: str) -> bool:
        return (
                any(subject.startswith(prefix) for prefix in REPLY_PREFIXES) or
                cls._is_head_entry_present(HEAD_KEY_IN_REPLY_TO, head) or
                cls._is_head_entry_present(HEAD_KEY_REFERENCES, head)
        )

    @staticmethod
    def _is_forward(subject: str) -> bool:
        return any(subject.startswith(prefix) for prefix in FORWARD_PREFIXES)
