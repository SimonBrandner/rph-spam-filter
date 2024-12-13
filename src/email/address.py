import re
from dataclasses import dataclass
from typing import Optional


ADDRESS_EXTRACTION_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
START_AND_ENDING_SPACES_REGEX = r"(?:^\s*|\s*$)"


@dataclass
class Address:
    username: str
    domain: str
    real_name: Optional[str] = None

    SPECIAL_CHARACTERS = ('<', '>', '"', "(", ")")

    @classmethod
    def from_string(cls, string: str) -> 'Address':
        address = cls._extract_address(string)
        username, domain = cls._validate_and_split_address(address)

        string = string.replace(address, "")
        string = cls._clean_string(string)
        real_name = string if len(string) > 0 else None

        return cls(username, domain, real_name)

    @staticmethod
    def _clean_string(string: str) -> str:
        for char in Address.SPECIAL_CHARACTERS:
            string = string.replace(char, "")
        string = re.sub(START_AND_ENDING_SPACES_REGEX, "", string)
        return string

    @staticmethod
    def _extract_address(string: str) -> str:
        email_match = re.search(ADDRESS_EXTRACTION_REGEX, string)
        if email_match is None:
            raise ValueError(f'Failed to extract e-mail address from this string:\n\n{string}')
        return email_match.group(0)

    @staticmethod
    def _validate_and_split_address(address: str) -> tuple[str, str]:
        address_parts = address.split("@", maxsplit=1)
        if len(address_parts) != 2:
            raise ValueError(f'Failed to extract "username@domain" from this e-mail address:\n\n{address}')
        return address_parts[0], address_parts[1]
