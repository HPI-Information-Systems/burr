from abc import ABC, abstractmethod

class BaseInteractionModule(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def feedback_from_user(self, topics):
        raise NotImplementedError