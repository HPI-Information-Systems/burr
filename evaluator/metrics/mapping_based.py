from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import Mapping

class MappingBasedPrecision(Metric):
    def __init__(self):
        super(MappingBasedPrecision, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        #classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes)) this does not work because if multiple concepts have the same mapping query they get removed becuase of set creation
        classes = [x for x in referenced_ontology.classes if x in learned_ontology.classes]

        #relations = set(learned_ontology.relations).intersection(set(referenced_ontology.relations))
        relations = [x for x in referenced_ontology.relations if x in learned_ontology.relations]
        #oru
        #print(classes)
        #print("\n")
        #print(relations)
        return (len(classes) + len(relations)) / (len(learned_ontology.classes) + len(learned_ontology.relations))
    
    def __str__(self):
        return "MappingBasedPrecision"

class MappingBasedRecall(Metric):
    def __init__(self):
        super(MappingBasedRecall, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        #classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        classes = [x for x in referenced_ontology.classes if x in learned_ontology.classes]
        #relations = set(learned_ontology.relations).intersection(set(referenced_ontology.relations))
        relations = [x for x in referenced_ontology.relations if x in learned_ontology.relations]
        return (len(classes) + len(relations)) / (len(referenced_ontology.classes) + len(referenced_ontology.relations))
    
    def __str__(self):
        return "MappingBasedRecall"