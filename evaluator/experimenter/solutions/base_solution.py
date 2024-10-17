from abc import ABC, abstractmethod

class BaseSolution(ABC):

    @abstractmethod
    def run(self, database_name):
        raise NotImplementedError
    
    def train(self, database_name):
        raise NotImplementedError
    
    def test(self, database_name):
        raise NotImplementedError