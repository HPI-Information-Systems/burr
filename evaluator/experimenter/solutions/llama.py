import wandb
import time
import gc
from string import Template
from vllm import LLM, SamplingParams
import os
import torch
from evaluator.experimenter.solutions.base_solution import BaseSolution
from evaluator.mapping_parser.mapping import D2RQMapping
from evaluator.experimenter.solutions.instance_data import collect_samples
from evaluator.experimenter.solutions.utils import extract_between
import re

def extract_ttl_block(text):
    pattern = r"```(?:ttl|turtle)?\s*(.*?)```"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None
class LlamaSolution(BaseSolution):
    solution_name = "llama"
    
    def __init__(self):
        super(LlamaSolution, self).__init__()

    def run(self, database_name, chatbot, script_path, output_path, meta, model) -> D2RQMapping:
        self.train(database_name)
        return self.test(database_name, chatbot, script_path, output_path, meta, model)

    def train(self):
        print("Training not required for Llama")
        return None, 0

    def test(self, database_name, chatbot, database,prompt_base_path, prompt, sql_file_path, output_path, meta, schema_path, model):
        print("Running Llama baseline with model:", chatbot)
        start_time = time.time()
        path_to_load = schema_path or sql_file_path
        with open(path_to_load, "r") as f:
            script = f.read()
        script = extract_between(script, "-- schema_start", "-- schema_end") or script
        print("Extracted schema:", script)

        samples = collect_samples(database_name)
        if not samples:
            raise ValueError("No samples collected from the database.")
        print("Collected samples:", samples)
        
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
        conversation = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        llm = LLM(model=chatbot, tensor_parallel_size=1, dtype="float16", max_model_len=2**14)
        sampling_params = SamplingParams(temperature=0.7, top_p=0.8, top_k=20,min_p=0, max_tokens=30672)
        messages = [conversation]
        response = llm.chat(
            messages,
            sampling_params,
            chat_template_kwargs={"enable_thinking": False}
        )[0]
        del llm
        torch.cuda.empty_cache()
        gc.collect()
        mapping = response.outputs[0].text.strip()
        os.makedirs("./evaluator/experimenter/results", exist_ok=True)
        with open("./evaluator/experimenter/results/output_mapping.txt", "w") as f:
            f.write(mapping)
        wandb.save("./evaluator/experimenter/results/output_mapping.txt")

        if "```" in mapping:
            print("Extracting TTL block from response")
            mapping = extract_ttl_block(mapping)

        end_time = time.time()
        print("Llama/vLLM finished")
        try: 
            d2r_mapping = D2RQMapping(mapping, database_name, meta)
        except Exception as e:
            print("Parsing:", e)
            wandb.log({"error": str(e)})
            wandb.log({"parsing_error": True})
            return None, 0
        return d2r_mapping, end_time - start_time

