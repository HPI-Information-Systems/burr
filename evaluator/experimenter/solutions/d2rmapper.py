import subprocess
import json
from dotenv import load_dotenv
import os
import time
import wandb

from evaluator.experimenter.solutions.base_solution import BaseSolution
from evaluator.mapping_parser.mapping import D2RQMapping

from evaluator.experimenter.solutions.OntoGenix_CLI.GUI.ontogenix import OntoGenix as OntoGenix_CLI

class D2RMapper(BaseSolution):
    solution_name = "d2rmapper"
    def __init__(self):
        super(D2RMapper, self).__init__()
        

    def run(self, database_name) -> D2RQMapping:
        self.train(database_name)
        return self.test(database_name)
    
    def train(self):
        print("Training not required for D2RMapper")
        return None, 0

    def test(self, database_name, script_path, output_path, meta, model):
        print("Running d2r_mapper")
        assert os.path.exists(script_path), "Script path does not exist"
        if (not os.path.exists(os.path.dirname(output_path))):
            os.mkdir(os.path.dirname(output_path))
        load_dotenv('./evaluator/experimenter/database_client/.env')
        database_url = "jdbc:postgresql://{host}:{port}/{database_name}".format(host=os.getenv("POSTGRES_HOST"), port=os.getenv("POSTGRES_PORT"), database_name=database_name)
        try:
            start_time = time.time()
            result = subprocess.run(
                [script_path, "-o", output_path, "-u", os.getenv("POSTGRES_USER"), "--debug", "--w3c", "-p", os.getenv("POSTGRES_PASSWORD"), database_url],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            end_time = time.time()
            print("Script output:", result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print("An error occurred:", e.stderr.decode())
            wandb.log({"error": str(e)})
            wandb.finish(exit_code=1)
        print("D2RMapper finished")
        return D2RQMapping(output_path, database_name, meta), end_time - start_time