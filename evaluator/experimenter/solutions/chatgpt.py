import wandb
import time
from openai import OpenAI
from string import Template


from evaluator.experimenter.solutions.base_solution import BaseSolution
from evaluator.mapping_parser.mapping import R2RMLMapping, D2RQMapping

class ChatGPT(BaseSolution):
    solution_name = "chatgpt"
    
    def __init__(self):
        super(ChatGPT, self).__init__()

    def run(self, database_name, chatbot, script_path, output_path, meta, model) -> D2RQMapping:
        self.train(database_name)
        return self.test(database_name, chatbot, script_path, output_path, meta, model)
    
    def train(self):
        print("Training not required for ChatGPT")
        return None, 0

    def test(self, database_name, chatbot, sql_file_path, output_path, meta, schema_path, model):
        print("Running ChatGPT baseline with model:", chatbot)
        start_time = time.time()
        if schema_path is None:
            with open(sql_file_path, "r") as f:
                script = f.read()
        else:
            with open(schema_path, "r") as f:
                script = f.read()
        example_mapping = open("/experiment/evaluator/experimenter/solutions/example.prompt").read()
        representation = {
            "database_schema": script,
            "example_prompt": example_mapping
        }
        prompt = Template(open("/experiment/evaluator/experimenter/solutions/chatgpt.prompt").read()).substitute(representation)
        client = OpenAI()
        response = client.chat.completions.create(
            model=chatbot,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates R2RML mappings."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        print(prompt)
    
        mapping = response.choices[0].message.content
        
        print(mapping)
    
        # output_file = f"{output_path}/{database_name}.ttl"
        # with open(output_file, "w") as f:
        #     f.write(mapping)
        
        end_time = time.time()
        print("ChatGPT finished")
        return R2RMLMapping(mapping, database_name, meta).to_D2RQ_Mapping(), end_time - start_time
