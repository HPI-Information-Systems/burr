import wandb
import json
import rdflib
from io import BytesIO

from evaluator.metrics.caclulate_metrics import calculate_metrics
from evaluator.mapping_parser.mapping import JsonMapping, D2RQMapping

class Experiment:
    def __init__(self, name, database_name, database, scenario_id, group, base_scenario, scenario, solution, sql_file_path, meta_file_path, groundtruth_mapping_path, tag, use_wandb=False):
        run = wandb.init(
            project="rdb2onto",
            mode = "online" if use_wandb else "disabled",
            tags=[tag],
    		entity="Lasklu",
            config={
                "database_name": database_name,
                "group": group,
                "system": solution.solution_name,
                "scenario": scenario,
                "base_scenario": base_scenario,
                "sql_file_path": sql_file_path,
                "groundtruth_mapping_path": groundtruth_mapping_path,
                "meta_file_path": meta_file_path
            })
        self.name = name
        self.database = database
        self.scenario_id = scenario_id
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
            self.save_to_file(self.groundtruth_mapping.create_ttl_string(self.database_name), f"/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/groundtruths/{self.scenario_id}.ttl")
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
        output_mapping, inference_time = self.solution.test(**test_config, model=trained_model, meta=self.meta, database_name=self.database_name)
        print(output_mapping)
        metrics = self.evaluate(self.groundtruth_mapping, output_mapping)    
        self.save_ttl_to_wandb(output_mapping.create_ttl_string(self.database_name))
        return {"output_mapping": output_mapping, "metrics": metrics, "runtime": {"training": training_time, "inference": inference_time}}  
    
    def evaluate(self, groundtruth_mapping: D2RQMapping, output_mapping: D2RQMapping):
        metrics = calculate_metrics(groundtruth_mapping, output_mapping)
        wandb.log(metrics)
        return metrics
    
    def save_to_file(self, ttl, filepath):
        file_like_object = BytesIO()
        graph = rdflib.Graph()
        graph.parse(data=ttl, format="turtle")
        graph.serialize(file_like_object, format='turtle')
        with open(filepath, "wb") as f:
            f.write(file_like_object.getvalue())

    def save_ttl_to_wandb(self, ttl):
        file_like_object = BytesIO()
        graph = rdflib.Graph()
        graph.parse(data=ttl, format="turtle")
        graph.serialize(file_like_object, format='turtle')
        with open("graph.ttl", "wb") as f:
            f.write(file_like_object.getvalue())
        wandb.save("graph.ttl")
        artifact = wandb.Artifact("graph.ttl", type='dataset')
        artifact.add_file("./graph.ttl", file_like_object)