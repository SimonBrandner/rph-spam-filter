import os
import random

from simple_filters import RandomFilter as Filter
from quality import TRUTH_FILENAME, compute_quality_for_corpus
from utils import read_classification_from_file, write_classification_to_file

ASSETS_DIRECTORY = "./assets/"
TRAINING_DIRECTORY = "/tmp/spam-filter/training"
TESTING_DIRECTORY = "/tmp/spam-filter/testing"


def is_for_testing():
    return random.uniform(0, 1) < 0.2


def split_dataset(path: str):
    os.makedirs(TRAINING_DIRECTORY, exist_ok=True)
    os.makedirs(TESTING_DIRECTORY, exist_ok=True)

    testing_emails = {}
    training_emails = {}
    for email_name, email_classification in read_classification_from_file(
        os.path.join(path, TRUTH_FILENAME)
    ).items():
        if is_for_testing():
            os.system(f"cp {path}/{email_name} {TESTING_DIRECTORY}/{email_name}")
            testing_emails[email_name] = email_classification
        else:
            os.system(f"cp {path}/{email_name} {TRAINING_DIRECTORY}/{email_name}")
            training_emails[email_name] = email_classification

        write_classification_to_file(
            os.path.join(TESTING_DIRECTORY, TRUTH_FILENAME), testing_emails
        )
        write_classification_to_file(
            os.path.join(TRAINING_DIRECTORY, TRUTH_FILENAME), training_emails
        )


def cleanup():
    os.system(f"rm -rf {TRAINING_DIRECTORY}")
    os.system(f"rm -rf {TESTING_DIRECTORY}")


if __name__ == "__main__":
    for dataset in os.listdir(ASSETS_DIRECTORY):
        if os.path.isfile(os.path.join(ASSETS_DIRECTORY, dataset)):
            continue

        split_dataset(os.path.join(ASSETS_DIRECTORY, dataset))

        filter = Filter()
        filter.train(TRAINING_DIRECTORY)
        filter.test(TESTING_DIRECTORY)
        quality = compute_quality_for_corpus(TESTING_DIRECTORY)

        print(
            f"Filter has quality {quality} for {os.path.join(ASSETS_DIRECTORY, dataset)}"
        )

        cleanup()
