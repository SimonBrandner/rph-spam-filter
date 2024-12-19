from typing import Iterable, Tuple
import os

METADATA_FILE_PREFIX = "!"


class Corpus:
    path: str

    def __init__(self, path: str):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(dir_path, path)

    def emails(self) -> Iterable[Tuple[str, str]]:
        for file_name in os.listdir(self.path):
            if file_name.startswith(METADATA_FILE_PREFIX):
                continue

            with open(os.path.join(self.path, file_name), encoding="utf-8") as file:
                body = file.read()
                yield (file_name, body)
