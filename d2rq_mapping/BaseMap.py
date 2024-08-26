from jinja2 import Environment, FileSystemLoader
from abc import ABC, abstractmethod

class BaseMap(ABC):
    def __init__(self, prefix, datastorage="database"):
        self.prefix = prefix
        self.datastorage = datastorage
        
    @abstractmethod
    def get_d2rq_mapping(self):
        raise NotImplementedError("Please Implement this method")
    
    def get_jinja_env(self):
        file_loader = FileSystemLoader('./templates')
        return Environment(loader=file_loader)