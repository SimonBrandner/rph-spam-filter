from dataclasses import dataclass
from typing import Optional

@dataclass
class Address:
    username: str
    domain: str
    real_name: Optional[str] = None

    @classmethod
    def from_string(cls, string: str) -> 'Address':
        string = string.replace("<", "").replace(">", "").replace('"', "")
        string_parts = string.split(" ")
        string_includes_real_name = len(string_parts) > 1
        real_name = " ".join(string_parts[0:-1]) if string_includes_real_name else None
        address = string_parts[-1]

        address_parts = address.split("@", maxsplit=1)
        if len(address_parts) != 2:
            raise ValueError(f'Failed to extract "username@domain" from this e-mail address:\n\n{string}')
        [username, domain] = address_parts

        return cls(username, domain, real_name)