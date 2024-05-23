from abc import ABC, abstractmethod
from evaluator.mapping_parser.mapping import Mapping

class Metric:
    def __call__(self, learned_ontology, referenced_ontology, **kwargs) -> float:
        return self.score(learned_ontology, referenced_ontology)#
    
    @abstractmethod
    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        pass