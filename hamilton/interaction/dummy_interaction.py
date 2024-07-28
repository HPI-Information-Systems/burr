from hamilton.interaction.base_interaction import BaseInteractionModule

class DummyInteractionModule(BaseInteractionModule):
    def __init__(self):
        super().__init__()
    
    def feedback_from_user(self, topics):
        return topics