from abc import ABC, abstractmethod
from typing import Any
from evaluator.mapping_parser.mapping import D2RQMapping

class Metric(ABC):
    def __call__(self, learned_ontology, referenced_ontology, **kwargs) -> float:
        return self.score(learned_ontology, referenced_ontology)#
    
    @abstractmethod
    def score(self, learned_ontology: D2RQMapping, referenced_ontology: D2RQMapping) -> float:
        ...

class F1Score():
    def __call__(self, precision, recall) -> float:
        return 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0.0

    def __str__(self):
        return "F1Score"
    
from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import D2RQMapping

class Precision(Metric):
    def __init__(self):
        super(Precision, self).__init__()

    def score(self, el1, el2) -> float:
        el1 = list(set(el1))
        el2 = list(set(el2))
        shared_elements = [x for x in el2 if x in el1]
        return len(shared_elements) / len(el2) if len(el2) > 0 else 0.0

    def __str__(self):
        return "Precision"


class Recall(Metric):
    def __init__(self):
        super(Recall, self).__init__()

    def score(self, el1, el2) -> float:
        el1 = list(set(el1))
        el2 = list(set(el2))
        shared_elements = [x for x in el2 if x in el1]
        return len(shared_elements) / len(el1) if len(el1) > 0 else 0.0

    def __str__(self):
        return "Recall"