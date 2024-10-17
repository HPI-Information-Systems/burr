from abc import ABC, abstractmethod

class BaseSolution(ABC):

    @abstractmethod
    def run(self, database_name):
        raise NotImplementedError