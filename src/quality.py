from confmat import BinaryConfusionMatrix
from utils import read_classification_from_file
import os

TRUTH_FILENAME = "!truth.txt"
PREDICTION_FILENAME = "!prediction.txt"

SPAM_TAG = "SPAM"
OK_TAG = "OK"


def quality_score(tp: int, tn: int, fp: int, fn: int) -> float:
    return (tp + tn) / (tp + tn + 10 * fp + fn)


def compute_quality_for_corpus(corpus_dir: str) -> float:
    true_classification = read_classification_from_file(
        os.path.join(corpus_dir, TRUTH_FILENAME)
    )
    predicted_classification = read_classification_from_file(
        os.path.join(corpus_dir, PREDICTION_FILENAME)
    )

    confusion_matrix = BinaryConfusionMatrix(SPAM_TAG, OK_TAG)
    confusion_matrix.compute_from_dicts(true_classification, predicted_classification)
    return quality_score(**confusion_matrix.as_dict())
