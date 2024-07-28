from abc import ABC, abstractmethod
from typing import List

class BaseTopicExtractor(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def extract(self, database_schema: str) -> List[str]:
        raise NotImplementedError