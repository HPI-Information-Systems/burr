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
        for group, base_scenarios in self.experiment_config["scenarios"].items(): #that attrbutes
            for base_scenario, scenarios in base_scenarios.items():
                for scenario, scenario_config in scenarios.items():
                    scenario_id = f"{group}__{base_scenario}__{scenario}"
                    database_name = scenario_config["database_name"] if "database_name" in scenario_config else scenario_id
                    for system in self.experiment_config["systems"]: # thats rdb2onto
                        system_config = system["config"]
                        system = system["name"]
                        print(f"Running experiment {experiment_name} for scenario {scenario} (Base scenario: {base_scenario}, group: {group}) with system {system}")
                        metric_result, runtime = self.run_experiment(experiment_name, database_name, system, system_config, scenario_id, group, base_scenario, scenario, scenario_config["sql_file"], scenario_config["meta_file_path"], scenario_config["groundtruth_mapping"])
                        wandb.log(metric_result)
                        wandb.log({"training_time": runtime["training"], "inference_time": runtime["inference"]})
                        wandb.finish()
        
    def run_experiment(self, experiment_name, database_name, system, system_config,scenario_id, group, base_scenario, scenario, sql_file_path, meta_file_path, groundtruth_mapping_path):
        if system == "rdb2onto":
            module = importlib.import_module("evaluator.experimenter.solutions.rdb2onto")
            system = getattr(module, "RDB2Onto")
        else:
            raise ValueError("System not found")
        system = system(**self.config[system.solution_name])
        experiment = Experiment(experiment_name, database_name=database_name , scenario_id=scenario_id, database=self.database, group=group, base_scenario=base_scenario, scenario=scenario, solution=system, sql_file_path=sql_file_path, meta_file_path=meta_file_path, groundtruth_mapping_path=groundtruth_mapping_path, tag=self.tag, use_wandb=self.use_wandb)
        output = experiment.run(system_config)
        return output["metrics"], output["runtime"]

    