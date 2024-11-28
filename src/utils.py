from typing import Dict


def read_classification_from_file(path: str) -> Dict[str, str]:
    classification_table = {}

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            words = line.split(" ")
            word_count = len(words)
            last_word_index = word_count - 1

            email_filename = " ".join(words[0:last_word_index])
            classification = words[last_word_index]

            classification_table[email_filename] = classification.strip()

    return classification_table
