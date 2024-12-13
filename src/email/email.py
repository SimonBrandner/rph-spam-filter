from address import Address
from dataclasses import dataclass
from typing import List

# Extract constants for better readability and reusability
REPLY_PREFIXES = ['Re:', 'RE:']
FORWARD_PREFIXES = ['Fw:', 'FW:']
HEAD_KEYS = {
    'FROM': 'From',
    'SUBJECT': 'Subject',
    'IN_REPLY_TO': 'In-Reply-To',
    'REFERENCES': 'References'
}


@dataclass
class Email:
    body: str
    sender: 'Address'
    subject: str
    is_reply: bool = False
    is_forward: bool = False

    @classmethod
    def from_string(cls, string: str) -> 'Email':
        sections = string.split('\n\n', maxsplit=1)
        head, body = sections if len(sections) == 2 else (sections[0], '')

        sender_entries = cls.extract_head_entries(HEAD_KEYS['FROM'], head)
        subject_entries = cls.extract_head_entries(HEAD_KEYS['SUBJECT'], head)

        if len(sender_entries) != 1 or len(subject_entries) != 1:
            raise ValueError(
                f'Failed to extract mandatory "{HEAD_KEYS["FROM"]}" or "{HEAD_KEYS["SUBJECT"]}" entry from email head:\n\n{head}'
            )

        sender = Address.from_string(sender_entries[0])
        subject = subject_entries[0]
        is_reply = cls._determine_is_reply(subject, head)
        is_forward = cls._determine_is_forward(subject)

        return cls(body=body, sender=sender, subject=subject, is_reply=is_reply, is_forward=is_forward)

    @staticmethod
    def extract_head_entries(entry_key: str, head: str) -> List[str]:
        """Utility function to extract specific entries from the email header."""
        entry_splitter = '\n' + entry_key + ': '
        entries = []
        after_key = head
        while True:
            parts = after_key.split(entry_splitter, maxsplit=1)
            if len(parts) == 1:
                break
            after_key = parts[1]
            possible_content_lines = after_key.splitlines()
            content = possible_content_lines[0].strip()
            for line in possible_content_lines[1:]:
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
    def _determine_is_reply(cls, subject: str, head: str) -> bool:
        return (
                any(subject.startswith(prefix) for prefix in REPLY_PREFIXES) or
                len(cls.extract_head_entries(HEAD_KEYS['IN_REPLY_TO'], head)) > 0 or
                len(cls.extract_head_entries(HEAD_KEYS['REFERENCES'], head)) > 0
        )

    @staticmethod
    def _determine_is_forward(subject: str) -> bool:
        return any(subject.startswith(prefix) for prefix in FORWARD_PREFIXES)
