import subprocess
import json

from evaluator.experimenter.solutions.base_solution import BaseSolution
from evaluator.mapping_parser.mapping import JsonMapping, D2RQMapping

# somehow run it using java

class RDB2Onto(BaseSolution):
    def __init__(self, jar_path):
        super(RDB2Onto, self).__init__()
        self.jar_path = jar_path

    def run(self, database_name, output_path="/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/") -> D2RQMapping:
        command = ['java', '-jar', self.jar_path, database_name, output_path]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            data_path = output_path + database_name + ".json"
            data = json.load(data_path)
            return JsonMapping(data, database_name, meta).to_D2RQ_Mapping()
        else:
            print("JAR execution failed with return code:", result.returncode)
            print("Error output:")
            print(result.stderr)