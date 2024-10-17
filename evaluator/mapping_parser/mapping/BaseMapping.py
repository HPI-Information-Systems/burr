from abc import ABC, abstractmethod
from typing import List

from evaluator.mapping_parser.classmap import ClassMap
from evaluator.mapping_parser.relation import Relation

class BaseMapping(ABC):
    def __init__(self, mapping_content, database):
        self.parse_mapping(mapping_content)
        self.classes: List[ClassMap]
        self.relations: List[Relation]
        self.mapping_content = mapping_content
        self.database = database
    
    @abstractmethod
    def parse_mapping(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_classes(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_attributes(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_relations(self):
        raise NotImplementedError