import wandb
import importlib
import configparser
import rdflib
from io import BytesIO



from evaluator.experimenter.config_template import experiment_config
from evaluator.experimenter.database_client.postgresclient import PostgresClient
from evaluator.experimenter.Experiment import Experiment

class ExperimentManager():
    def __init__(self, config_file) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.database = PostgresClient(self.config['DATABASE']['host'], self.config['DATABASE']['port'], self.config['DATABASE']['user'], self.config['DATABASE']['password'], self.config['DATABASE']['database'])
        self.experiment_config = experiment_config
        self.evaluator = pass #some evaluator
        pass

    def start_experiments(self, experiment_name):
        
        pass
        
    def run_experiment(self, experiment_name, system, scenario):
        run = wandb.init(
            project="rdb2onto",
            config={
                "system": system,
                "scenario": scenario
            },
            group=experiment_name)
        if system == "rdb2onto":
            module = importlib.import_module("evaluator.experimenter.solutions.rdb2onto")
            system = getattr(module, "RDB2Onto")
        else:
            raise ValueError("System not found")
        experiment = Experiment(experiment_name, database_name=scenario, database=self.database, solution=system, evaluator=self.evaluator)
        output = experiment.run(scenario)
        self.save_ttl_to_wandb(experiment_name, output['mapping_file'])

    def save_ttl_to_wandb(self, filename, ttl):
        file_like_object = BytesIO()
        graph = rdflib.Graph()
        graph.parse(data=ttl, format="turtle")
        graph.serialize(file_like_object, format='turtle')
        with open("graph.ttl", "wb") as f:
            f.write(file_like_object.getvalue())
        artifact = wandb.Artifact(filename, type='dataset')
        artifact.add_file(filename)