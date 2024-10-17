import subprocess
import json
import os
import time

from evaluator.experimenter.solutions.base_solution import BaseSolution
from evaluator.mapping_parser.mapping import JsonMapping, D2RQMapping

class RDB2Onto(BaseSolution):
    solution_name = "rdb2onto"
    def __init__(self, jar_path):
        super(RDB2Onto, self).__init__()
        self.jar_path = jar_path

    def run(self, database_name, output_path="/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/") -> D2RQMapping:
        self.train(database_name)
        return self.test(database_name, output_path)
    
    def train(self):
        print("Training not required for RDB2Onto")
        return None, 0

    def test(self, database_name, output_path, meta, model):
        command = ['java', '-jar', self.jar_path, database_name, output_path]
        print("Running RDB2Onto: ", command)

        start_time = time.time()
        result = subprocess.run(command, capture_output=True, text=True)
        end_time = time.time()
        if result.returncode == 0:
            print("RDB2Onto finished")
            data_path = os.path.join(output_path, f"{database_name}.json")
            with open(data_path) as data:
                data = json.load(data)
            return JsonMapping(data, database_name, meta).to_D2RQ_Mapping(), end_time - start_time
        else:
            print("JAR execution failed with return code:", result.returncode)
            print("Error output:")
            print(result.stderr)