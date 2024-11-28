from typing import Any, Dict


class BinaryConfusionMatrix:
    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int

    def __init__(self, pos_tag: Any, neg_tag: Any) -> None:
        self.positive_tag = pos_tag
        self.negative_tag = neg_tag

        self.true_positive = 0
        self.true_negative = 0
        self.false_positive = 0
        self.false_negative = 0

    def as_dict(self) -> Dict[str, int]:
        return {
            "tp": self.true_positive,
            "tn": self.true_negative,
            "fp": self.false_positive,
            "fn": self.false_negative,
        }

    def update(self, truth: Any, prediction: Any) -> None:
        match (prediction, truth):
            case self.positive_tag, self.positive_tag:
                self.true_positive += 1
            case self.negative_tag, self.negative_tag:
                self.true_negative += 1
            case self.positive_tag, self.negative_tag:
                self.false_positive += 1
            case self.negative_tag, self.positive_tag:
                self.false_negative += 1
            case _:
                raise ValueError

    def compute_from_dicts(
        self, truth: Dict[str, Any], prediction: Dict[str, Any]
    ) -> None:
        for name in truth.keys():
            self.update(truth[name], prediction[name])
