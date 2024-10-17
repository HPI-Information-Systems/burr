import wandb
import json

from evaluator.metrics.caclulate_metrics import calculate_metrics
from evaluator.mapping_parser.mapping import JsonMapping, D2RQMapping

class Experiment:
    def __init__(self, name, database_name, database, solution, sql_file_path, meta_file_path, groundtruth_mapping_path, tag, use_wandb=False):
        run = wandb.init(
            project="rdb2onto",
            mode = "online" if use_wandb else "disabled",
            tags=[tag],
    		entity="Lasklu",
            config={
                "system": solution.solution_name,
                "scenario": database_name,
                "sql_file_path": sql_file_path,
                "groundtruth_mapping_path": groundtruth_mapping_path,
                "meta_file_path": meta_file_path
            })
        self.name = name
        self.database = database
        self.database_name = database_name
        self.sql_file_path = sql_file_path
        self.groundtruth_mapping_path = groundtruth_mapping_path
        with open(meta_file_path) as json_file:
                self.meta = json.load(json_file)
        self.solution = solution

    def setup(self):
        print("Setting up experiment")
        file_ending_is_json =  self.groundtruth_mapping_path.endswith(".json")
        print("Loading groundtruth mapping")
        if file_ending_is_json:
            with open(self.groundtruth_mapping_path) as json_file:
                data = json.load(json_file)
            
            self.groundtruth_mapping = JsonMapping(data, self.database_name, self.meta).to_D2RQ_Mapping()
            print("JSONGroundtruth mapping loaded")
        elif self.groundtruth_mapping_path.endswith(".ttl"):
            self.groundtruth_mapping = D2RQMapping(self.groundtruth_mapping_path, self.database_name)
            print("TTLGroundtruth mapping loaded")
        else:
            raise ValueError("File ending not supported")
        print("Rewriting database")
        self.database.update_database(self.sql_file_path)        
        print("Experiment setup complete")
    
    def run(self, solution_config):
        self.setup()
        train_config = solution_config["train"]
        test_config = solution_config["test"]
        trained_model, training_time = self.solution.train(**train_config)
        print(test_config)
        print(self.database_name)
        output_mapping, inference_time = self.solution.test(**test_config, model=trained_model, meta=self.meta, database_name=self.database_name)
        metrics = self.evaluate(self.groundtruth_mapping, output_mapping)    
        return {"output_mapping": output_mapping, "metrics": metrics, "runtime": {"training": training_time, "inference": inference_time}}  
    
    def evaluate(self, groundtruth_mapping: D2RQMapping, output_mapping: D2RQMapping):
        metrics = calculate_metrics(groundtruth_mapping, output_mapping)
        wandb.log(metrics)
        return metrics