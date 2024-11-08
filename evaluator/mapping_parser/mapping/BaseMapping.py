from abc import ABC, abstractmethod
from rdflib import URIRef

from evaluator.utils.get_jinja_env import get_jinja_env


class BaseMapping(ABC):
    def __init__(self, mapping_content, database, meta):
        self.classes = []
        self.relations = []
        self.translation_tables = []
        self.meta = meta
        self.parse_mapping(mapping_content)
        self.mapping_content = mapping_content
        self.database = database
    
    @abstractmethod
    def parse_mapping(self):
        raise NotImplementedError
    
    def get_classes(self):
        return self.classes
    
    def get_attributes(self):
        return list(filter(lambda rel: rel.refersToClassMap is None, self.relations))
    
    def get_relations(self):
        return list(filter(lambda rel: rel.refersToClassMap is not None, self.relations))
    
    def shorten_uri(self, uri):
        uri = str(URIRef(uri)).replace("<", "").replace(">", "").replace(" ", "")
        for _, namespace in self.graph.namespaces():
            if str(uri).startswith(namespace):
                return str(uri)[len(namespace):]
        return uri
    
    def create_ttl_string(self, database):
        output = ""
        output += self.build_meta_data(database)
        for _cls in self.classes:
            output += str(_cls)
        for prop in self.relations:
            output += str(prop)
        for translation_table in self.translation_tables:
            output += str(translation_table)
        return output

    def build_meta_data(self, database): return get_jinja_env().get_template('meta.j2').render(prefixes=self.meta["prefixes"], database=database, database_username="lukaslaskowski") 
