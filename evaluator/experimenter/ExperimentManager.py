import wandb
import importlib
import configparser
import rdflib
from io import BytesIO
import os

from evaluator.experimenter.config_template import experiment_configs
from evaluator.experimenter.database_client.postgresclient import PostgresClient
from evaluator.experimenter.Experiment import Experiment

class ExperimentManager():
    def __init__(self, config_file, tag, use_wandb=False) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        print(self.config.sections)
        print(self.config)
        self.database = PostgresClient(self.config['DATABASE']['host'], self.config['DATABASE']['port'], self.config['DATABASE']['user'], self.config['DATABASE']['password'], self.config['DATABASE']['database'])
        self.experiment_config = experiment_configs
        self.use_wandb = use_wandb
        self.tag = tag

    def start_experiments(self, experiment_name):
        self.experiment_config = self.experiment_config[experiment_name]
        for base_scenario, scenarios in self.experiment_config["scenarios"].items():
            for scenario, scenario_config in scenarios.items():
                for system in self.experiment_config["systems"]:
                    system_config = system["config"]
                    system = system["name"]
                    print(f"Running experiment {experiment_name} for scenario {scenario} (Base scenario: {base_scenario}) with system {system}")
                    metric_result, runtime = self.run_experiment(experiment_name, system, system_config, scenario, scenario_config["sql_file"], scenario_config["meta_file_path"], scenario_config["groundtruth_mapping"])
                    wandb.log(metric_result)
                    wandb.log({"training_time": runtime["training"], "inference_time": runtime["inference"]})
        
    def run_experiment(self, experiment_name, system, system_config, scenario, sql_file_path, meta_file_path, groundtruth_mapping_path):
        if system == "rdb2onto":
            module = importlib.import_module("evaluator.experimenter.solutions.rdb2onto")
            system = getattr(module, "RDB2Onto")
        else:
            raise ValueError("System not found")
        system = system(**self.config[system.solution_name])
        experiment = Experiment(experiment_name, database_name=scenario, database=self.database, solution=system, sql_file_path=sql_file_path, meta_file_path=meta_file_path, groundtruth_mapping_path=groundtruth_mapping_path, tag=self.tag, use_wandb=self.use_wandb)
        output = experiment.run(system_config)
        self.save_ttl_to_wandb(experiment_name, output['output_mapping'].create_ttl_string(scenario))
        return output["metrics"], output["runtime"]

    def save_ttl_to_wandb(self, filename, ttl):
        print("dhajwal", ttl)
        file_like_object = BytesIO()
        graph = rdflib.Graph()
        graph.parse(data=ttl, format="turtle")
        graph.serialize(file_like_object, format='turtle')
        with open("graph.ttl", "wb") as f:
            f.write(file_like_object.getvalue())
        artifact = wandb.Artifact(filename, type='dataset')
        artifact.add_file(filename)