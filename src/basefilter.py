import os
from abc import abstractmethod
from typing import Dict
from quality import PREDICTION_FILENAME


class BaseFilter:
    @abstractmethod
    def train(self, path: str):
        pass

    @abstractmethod
    def test(self, path: str):
        pass

    def write_prediction_to_file(self, path: str, predictions: Dict[str, str]):
        with open(
            os.path.join(path, PREDICTION_FILENAME), "w", encoding="utf-8"
        ) as file:
            for name, prediction in predictions.items():
                file.write(f"{name} {prediction}\n")
