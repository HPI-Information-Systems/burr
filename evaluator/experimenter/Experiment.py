import wandb
import json

from evaluator.metrics import MappingBasedPrecision, MappingBasedRecall, TaxonomyMappingBasedRecall, TaxonomyMappingBasedPrecision, F1Score
from evaluator.mapping_parser.mapping import JsonMapping, D2RQMapping

class Experiment:
    def __init__(self, name, database_name, database, solution, evaluator):
        self.name = name
        self.database = database
        self.database_name = database_name
        self.solution = solution
        self.evaluator = evaluator

    def setup(self, sql_file_path, groundtruth_mapping_path):
        file_ending_is_json =  groundtruth_mapping_path.endswith(".json")
        if file_ending_is_json:
            data = json.load(groundtruth_mapping_path)
            self.groundtruth_mapping = JsonMapping(data, self.database_name, meta).to_D2RQ_Mapping()
        elif groundtruth_mapping_path.endswith(".ttl"):
            self.groundtruth_mapping = D2RQMapping(groundtruth_mapping_path, self.database_name)
        else:
            raise ValueError("File ending not supported")
        self.database.update_database(sql_file_path)        
    
    def run(self, solution_config, sql_file_path):
        self.setup(sql_file_path, )
        output_mapping = self.solution.run(**solution_config)
        metrics = self.evaluate(self.groundtruth_mapping, output_mapping)    
        return {"output_mapping": output_mapping, "metrics": metrics}  
    
    def evaluate(self, groundtruth_mapping, output_mapping):
        precision = MappingBasedPrecision()(groundtruth_mapping, output_mapping)
        recall = MappingBasedRecall()(groundtruth_mapping, output_mapping)
        f1 = F1Score()(precision, recall)
        tr = TaxonomyMappingBasedRecall().score(groundtruth_mapping, output_mapping)
        tp = TaxonomyMappingBasedPrecision()(groundtruth_mapping, output_mapping)
        tf1 = F1Score()(tp, tr)
        metrics = {"precision": precision, "recall": recall, "f1": f1, "taxonomy_precision": tp, "taxonomy_recall": tr, "taxonomy_f1": tf1}
        wandb.log(metrics)
        return metrics