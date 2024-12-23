import os
import shutil
import random

from simple_filters import RandomFilter as Filter
from quality import TRUTH_FILENAME, compute_quality_for_corpus
from utils import read_classification_from_file, write_classification_to_file

ASSETS_DIRECTORY = "./assets/"
TRAINING_DIRECTORY = "/tmp/spam-filter/training"
TESTING_DIRECTORY = "/tmp/spam-filter/testing"

TESTING_PROBABILITY = 0.2
"""The percentage of data to use for testing"""


def is_for_testing():
    return random.uniform(0, 1) < TESTING_PROBABILITY


def split_dataset(path: str):
    os.makedirs(TRAINING_DIRECTORY, exist_ok=True)
    os.makedirs(TESTING_DIRECTORY, exist_ok=True)

    testing_emails = {}
    training_emails = {}
    for email_name, email_classification in read_classification_from_file(
        os.path.join(path, TRUTH_FILENAME)
    ).items():
        source_path = os.path.join(path, email_name)
        if is_for_testing():
            destination_path = os.path.join(TESTING_DIRECTORY, email_name)
            shutil.copy(source_path, destination_path)
            testing_emails[email_name] = email_classification
        else:
            destination_path = os.path.join(TRAINING_DIRECTORY, email_name)
            shutil.copy(source_path, destination_path)
            training_emails[email_name] = email_classification

    write_classification_to_file(
        os.path.join(TESTING_DIRECTORY, TRUTH_FILENAME), testing_emails
    )
    write_classification_to_file(
        os.path.join(TRAINING_DIRECTORY, TRUTH_FILENAME), training_emails
    )


def cleanup():
    if os.path.exists(TRAINING_DIRECTORY):
        shutil.rmtree(
            TRAINING_DIRECTORY
        )  # Remove the training directory and its contents
    if os.path.exists(TESTING_DIRECTORY):
        shutil.rmtree(
            TESTING_DIRECTORY
        )  # Remove the testing directory and its contents


if __name__ == "__main__":
    # To be safe in the case this crashed when previously run and it did not
    # clean up after itself
    cleanup()

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
