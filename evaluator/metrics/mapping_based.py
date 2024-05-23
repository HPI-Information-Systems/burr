from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import Mapping

class MappingBasedPrecision(Metric):
    def __init__(self):
        super(MappingBasedPrecision, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        relations = set(learned_ontology.relations).intersection(set(referenced_ontology.relations))
        return (len(classes) + len(relations)) / (len(learned_ontology.classes) + len(learned_ontology.relations))
    
    def __str__(self):
        return "MappingBasedPrecision"

class MappingBasedRecall(Metric):
    def __init__(self):
        super(MappingBasedRecall, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        relations = set(learned_ontology.relations).intersection(set(referenced_ontology.relations))
        return (len(classes) + len(relations)) / (len(referenced_ontology.classes) + len(referenced_ontology.relations))
    
    def __str__(self):
        return "MappingBasedRecall"
    
class MappingBasedF1(Metric):
    def __init__(self):
        super(MappingBasedF1, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        precision = MappingBasedPrecision().score(learned_ontology, referenced_ontology)
        recall = MappingBasedRecall().score(learned_ontology, referenced_ontology)
        return 2 * (precision * recall) / (precision + recall)
    
    def __str__(self):
        return "MappingBasedF1"