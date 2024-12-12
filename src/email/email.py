from address import Address
from dataclasses import dataclass


@dataclass
class Email:
    body: str
    sender: 'Address'
    subject: str
    is_reply: bool = False
    is_forward: bool = False

    @classmethod
    def from_string(cls, string: str) -> 'Email':

        def extract_head_entries(entry_key: str) -> list[str]:
            entry_splitter = '\n' + entry_key + ': '
            entries = []
            after_key = head

            while True:
                before_and_after_key = after_key.split(entry_splitter, maxsplit=1)
                if len(before_and_after_key) == 1:
                    return entries

                after_key = before_and_after_key[1]
                possible_content_lines = after_key.splitlines()
                content = possible_content_lines[0].strip()

                for line in possible_content_lines[1:]:
                    if not len(line) > 5:
                        break
                    line_starts_with_spaces = line[0:4] == "    "
                    line_starts_with_tab = line[0] == "\t"

                    if line_starts_with_spaces or line_starts_with_tab:
                        start_shift = 4 if line_starts_with_spaces else 1
                        content += " " + line[start_shift:].strip()
                    else:
                        break

                entries.append(content)

        head_and_body = string.split('\n\n', maxsplit=1)
        [head, body] = head_and_body if len(head_and_body) == 2 else [head_and_body[0], '']

        sender = extract_head_entries('From')
        subject = extract_head_entries('Subject')
        if (len(sender) != 1) or (len(subject) != 1):
            raise ValueError(
                f'Failed to extract mandatory "From" or "Subject" entry from this e-mail head:\n\n{head}')

        sender = Address.from_string(sender[0])
        subject = subject[0]
        is_reply = subject.startswith('Re:') or subject.startswith('RE:') or len(
            extract_head_entries("In-Reply-To")) > 0 or len(extract_head_entries("References")) > 0
        is_forward = subject.startswith("Fw:") or subject.startswith('FW:')

        return cls(body, sender, subject)
