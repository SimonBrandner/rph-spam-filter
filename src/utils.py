from typing import Dict


def read_classification_from_file(path: str) -> Dict[str, str]:
    classification_table = {}

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            name, classification = line.split(" ")
            classification_table[name] = classification.strip()

    return classification_table
