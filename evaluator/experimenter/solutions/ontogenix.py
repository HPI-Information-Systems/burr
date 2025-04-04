import wandb
import time

from evaluator.experimenter.solutions.base_solution import BaseSolution
from evaluator.mapping_parser.mapping import R2RMLMapping, D2RQMapping

from evaluator.experimenter.solutions.OntoGenix_CLI.GUI.ontogenix import OntoGenix as OntoGenix_CLI

class OntoGenix(BaseSolution):
    solution_name = "ontogenix"
    def __init__(self):
        super(OntoGenix, self).__init__()

    def run(self, database_name) -> D2RQMapping:
        self.train(database_name)
        return self.test(database_name)
    
    def train(self):
        print("Training not required for Ontogenix")
        return None, 0

    def test(self, database_name,sql_file_path, meta, chatbot, schema_path,model):
        print("Running OntoGenix with model: ", chatbot)
        start_time = time.time()
        mapping = OntoGenix_CLI(database_name, api_model=chatbot).run()
        
        path = f"output/ontogenix/{database_name}.ttl"
        with open(path, "w") as f:
            f.write(mapping)
        end_time = time.time()
        print("OntoGenix finished")
        #fix this
        # return D2RQMapping(mapping_content=mapping, database=database_name, meta=meta), end_time - start_time
        return R2RMLMapping(mapping, database_name, meta).to_D2RQ_Mapping(), end_time - start_time