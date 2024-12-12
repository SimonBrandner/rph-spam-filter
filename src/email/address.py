from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    username: str
    domain: str
    real_name: Optional[str] = None

    SPECIAL_CHARACTERS = ('<', '>', '"')

    @classmethod
    def from_string(cls, string: str) -> 'Address':
        string = cls._clean_string(string)
        real_name, address = cls._extract_name_and_address(string)
        username, domain = cls._validate_and_split_address(address)
        return cls(username, domain, real_name)

    @staticmethod
    def _clean_string(string: str) -> str:
        """Remove special characters like '<', '>', and '"' from the string."""
        for char in Address.SPECIAL_CHARACTERS:
            string = string.replace(char, "")
        return string

    @staticmethod
    def _extract_name_and_address(string: str) -> tuple[Optional[str], str]:
        parts = string.split(" ")
        if len(parts) > 1:
            real_name = " ".join(parts[:-1])
        else:
            real_name = None
        address = parts[-1]
        return real_name, address

    @staticmethod
    def _validate_and_split_address(address: str) -> tuple[str, str]:
        address_parts = address.split("@", maxsplit=1)
        if len(address_parts) != 2:
            raise ValueError(f'Failed to extract "username@domain" from this e-mail address:\n\n{address}')
        return address_parts[0], address_parts[1]
