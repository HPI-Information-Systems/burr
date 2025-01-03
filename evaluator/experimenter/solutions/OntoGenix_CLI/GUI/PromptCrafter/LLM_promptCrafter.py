from abc import ABC
from typing import Optional

from evaluator.experimenter.solutions.OntoGenix_CLI.GUI.LLM_base.LlmBase import AbstractLlm
from evaluator.experimenter.solutions.OntoGenix_CLI.GUI.tools.text_tools import extract_text


class LlmPromptCrafter(AbstractLlm, ABC):
    """
    This class represents a language learning model (LLM_base) ontology. It extends the AbstractLlm class and provides
    methods for interacting with the model.

    TODO: the long_term_memory mechanism is not implemented.
    """
    name = 'PromptCrafter'

    def __init__(self, metadata: dict):
        """
        Initialize the LlmOntology object.

        Parameters:
        metadata (dict): A dictionary containing metadata for the LLM_base.
        """
        super().__init__(metadata)

        # initialize prompts
        self.data_description_prompt = self.load_string_from_file(metadata['prompt_crafting'])
        # initialize containers
        self.crafted_prompt = None


    def interaction(self, prompt: Optional[str] = None, json_data: Optional[str] = None):
        """
        Perform the first interaction or a subsequent interaction with the LLM_base based on the arguments provided.

        Parameters:
        input_task (str): The input message.
        json_data (str): The input data in JSON format.
        data_description (str): The description of the JSON data.
        Yields:
        str: Chunks of the response from the LLM_base.
        """
        try:
            # Act as first_interaction
            self.current_prompt = self.data_description_prompt.format(prompt=prompt, json_data=json_data)
            # Get the response from the LLM_base
            self.get_api_response(self.current_prompt)#yield chunk
            # permanently store the generated prompt
            self.crafted_prompt = extract_text(
                self.answer,
                start_marker="**Prompt:**",
                end_marker="**Critique:**"
            )
            print(f"Crafted prompt: {self.crafted_prompt}")
        except GeneratorExit as ge:
            print(f"Process stopped/cancelled by user: {ge}")
            return
        except ValueError as e:
            print(f"An error occurred: {e}")
        finally:
            self.last_prompt = self.current_prompt
