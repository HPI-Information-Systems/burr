import wandb
import time
from openai import OpenAI
from string import Template
import os
from google import genai
import io

from evaluator.experimenter.solutions.base_solution import BaseSolution
from evaluator.mapping_parser.mapping import D2RQMapping
from evaluator.experimenter.solutions.instance_data import collect_samples
from evaluator.experimenter.solutions.llama import extract_ttl_block
from evaluator.experimenter.solutions.utils import extract_between
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

    def test(self, database_name,database, prompt_base_path, prompt,chatbot, sql_file_path, output_path, meta, schema_path, model):
        print("Running ChatGPT baseline with model:", chatbot)
        start_time = time.time()

        path_to_load = schema_path or sql_file_path
        with open(path_to_load, "r") as f:
            script = f.read()
        print("Loaded script/schema:", script)
        script = extract_between(script, "-- schema_start", "-- schema_end") or script

        samples = collect_samples(database_name)
        if not samples:
            raise ValueError("No samples collected from the database.")
        prompt_path = os.path.join(prompt_base_path, f"{prompt}.prompt")
        example_mapping = open("./evaluator/experimenter/solutions/example.prompt").read()
        d2rq_example_mapping = open("./evaluator/experimenter/solutions/d2rq_example.prompt").read()
        template = Template(open(prompt_path).read())
        prompt = template.substitute({
            "database_schema": script,
            "instance_data": "\n".join([f"{table}:\n{df.to_csv(index=False)}" for table, df in samples.items()]),
            "example_prompt": example_mapping,
            "d2rq_example": d2rq_example_mapping
        })
        if "gpt" in chatbot:
            client = OpenAI()
            response = client.chat.completions.create(
                model=chatbot,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates D2RQ mappings."},
                    {"role": "user", "content": prompt}
                ]
            )
        
            mapping = response.choices[0].message.content
        elif "gemini" in chatbot:
            client = genai.Client()
            response = client.models.generate_content(
                model=chatbot,
                contents=prompt,
            )
            mapping = response.text
        else:
            raise ValueError(f"Unsupported chatbot model: {chatbot}")
        os.makedirs("./evaluator/experimenter/results", exist_ok=True)
        with open("./evaluator/experimenter/results/output_mapping.txt", "w") as f:
            f.write(mapping)
        wandb.save("./evaluator/experimenter/results/output_mapping.txt")

        
        if "```" in mapping:
            print("Extracting TTL block from response")
            mapping = extract_ttl_block(mapping)

        end_time = time.time()
        print("Chatgpt finished")
        try: 
            d2r_mapping = D2RQMapping(mapping, database_name, meta)
        except Exception as e:
            import traceback
            e = traceback.format_exc()
            print(traceback.format_exc())
            wandb.log({"error": str(e)})
            wandb.log({"parsing_error": True})
            return None, 0
        return d2r_mapping, end_time - start_time
