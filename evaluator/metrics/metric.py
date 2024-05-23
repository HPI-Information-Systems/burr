from abc import ABC, abstractmethod


class Metric:
    def __call__(self, learned_ontology, referenced_ontology, **kwargs) -> float:
        return self.score(learned_ontology, referenced_ontology)#
    
    @abstractmethod
    def score(self, learned_ontology, referenced_ontology) -> float:
        pass