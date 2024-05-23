from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import Mapping

class MappingBasedPrecision(Metric):
    def __init__(self):
        super(MappingBasedPrecision, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        for class_map in learned_ontology.classes:
            print(class_map)