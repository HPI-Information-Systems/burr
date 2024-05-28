from abc import ABC, abstractmethod
from typing import Any
from evaluator.mapping_parser.mapping import Mapping

class Metric(ABC):
    def __call__(self, learned_ontology, referenced_ontology, **kwargs) -> float:
        return self.score(learned_ontology, referenced_ontology)#
    
    @abstractmethod
    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        ...

class F1Score():
    def __call__(self, precision, recall) -> float:
        return 2 * (precision * recall) / (precision + recall)

    def __str__(self):
        return "F1Score"