from evaluator.experimenter.solutions.OntoGenix_CLI.GUI.LLM_base.LlmBase import AbstractLlm
from evaluator.experimenter.solutions.OntoGenix_CLI.GUI.tools.text_tools import extract_text
import wandb

class LlmOntoMapper(AbstractLlm):
    name = 'OntoMapper'
    def __init__(self, metadata: dict):
        super().__init__(metadata)
        # initialize prompts
        self.instructions = self.load_string_from_file(metadata['instructions'])
        self.error_instructions = self.load_string_from_file(metadata['error_instructions'])
        self.example_extension = self.load_string_from_file(metadata['example_extension'])
        # path setting to write outputs
        self._dataset_path = metadata['dataset']
        # initialize memories
        self.rml_codeblock = None

    @property
    def dataset_path(self):
        return self._dataset_path

    # Setter for name
    @dataset_path.setter
    def dataset_path(self, path):
        if not isinstance(path, str):
            raise ValueError("Name must be a string!")
        self._dataset_path = path

    def interact(self, rationale: str=None, ontology:str=None, error: str=None,
                       mapping_extension:str="R2RML", example_extension:str=None, 
                       ontology_extension:str="TTL"):
        try:
            csv_data = self._dataset_path
            print("---------- csv_data ->", csv_data)
            print("---------- error ->", error)
            if not error:
                self.current_prompt = self.instructions.format(
                    rationale=rationale, ontology=ontology, csv_data=csv_data, 
                    mapping_extension=mapping_extension, example_extension=example_extension,
                    ontology_extension=ontology_extension
                )
            else:
                self.current_prompt = self.error_instructions.format(
                    rationale=rationale, error=error, ontology=ontology, csv_data=csv_data, 
                    mapping_extension=mapping_extension, example_extension=example_extension,
                    ontology_extension=ontology_extension
                )
            # Get the response from the LLM_base
            print("mapping prompt", self.current_prompt)
            self.get_api_response(self.current_prompt)
            with open("r2rml.ttl", "w") as f:
                f.write(self.answer)
            wandb.save("r2rml.ttl")
            print("MAPPING", self.answer)
        except ValueError as e:
            print(f"An error occurred during interaction: {e}")
        finally:
            self.last_prompt = self.current_prompt

    def get_rml_codeblock(self):
        # NOTE: If the start mark is not found, we return the whole text
        try:
            return extract_text(self.answer, start_marker="```rml", end_marker="```")
        except:
            return self.answer
