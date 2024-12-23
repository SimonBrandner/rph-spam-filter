import os
from abc import abstractmethod
from typing import Dict
from quality import PREDICTION_FILENAME
from utils import write_classification_to_file


class BaseFilter:
    @abstractmethod
    def train(self, path: str):
        pass

    @abstractmethod
    def test(self, path: str):
        pass

    def write_prediction_to_file(self, path: str, predictions: Dict[str, str]):
        write_classification_to_file(
            os.path.join(path, PREDICTION_FILENAME), predictions
        )
