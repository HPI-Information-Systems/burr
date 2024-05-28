from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import Mapping

class MappingBasedPrecision(Metric):
    def __init__(self):
        super(MappingBasedPrecision, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        #print("sda", learned_ontology.classes )
        #print("sda", learned_ontology.relations )
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