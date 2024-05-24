import numpy as np

from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import Mapping

class TaxonomyMappingBasedPrecision(Metric):
    def __init__(self):
        super(TaxonomyMappingBasedPrecision, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        shared_classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        learned_ontology.classes = list(shared_classes)
        referenced_ontology.classes = list(shared_classes)
        # shared_relations = set(learned_ontology.relations).intersection(set(referenced_ontology.relations))
        # learned_ontology.relations = list(shared_relations)
        # referenced_ontology.relations = list(shared_relations)
        # shared_elements = shared_classes.union(shared_relations)
        shared_elements = shared_classes
    
        return np.mean(list(map(lambda el: LocalTaxonomyMappingBasedPrecision().score(el, learned_ontology, referenced_ontology), shared_elements)))
    
    def __str__(self):
        return "TaxonomyMappingBasedPrecision"

class TaxonomyMappingBasedRecall(Metric):
    def __init__(self):
        super(TaxonomyMappingBasedRecall, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        # shared_classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        # learned_ontology.classes = list(shared_classes)
        # referenced_ontology.classes = list(shared_classes)
        shared_relations = set(learned_ontology.relations).intersection(set(referenced_ontology.relations))
        print("shared_relations", shared_relations)
        learned_ontology.relations = list(shared_relations)
        referenced_ontology.relations = list(shared_relations)
        # shared_elements = shared_classes.union(shared_relations)

        shared_elements = shared_relations
        return np.mean(list(map(lambda el: LocalTaxonomyMappingBasedRecall().score(el, learned_ontology, referenced_ontology), shared_elements)))
    
    def __str__(self):
        return "TaxonomyMappingBasedRecall"
    
class TaxonomyMappingBasedF1(Metric):
    def __init__(self):
        super(TaxonomyMappingBasedF1, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        precision = TaxonomyMappingBasedPrecision().score(learned_ontology, referenced_ontology)
        recall = TaxonomyMappingBasedRecall().score(learned_ontology, referenced_ontology)
        return 2 * (precision * recall) / (precision + recall)
    
    def __str__(self):
        return "TaxonomyMappingBasedF1"
    
class LocalTaxonomyMappingBasedPrecision(Metric):
    def __init__(self):
        super(LocalTaxonomyMappingBasedPrecision, self).__init__()

    def score(self, schema_element, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        learned_context_elements = learned_ontology.get_context_elements(schema_element)
        referenced_context_elements = referenced_ontology.get_context_elements(schema_element)
        if len(learned_context_elements) == 0:
            assert len(referenced_context_elements) == 0, "Something wrong with mappings and the calculation code, because this cannot happen."
            return 1
        return len(set(learned_context_elements).intersection(set(referenced_context_elements))) / len(learned_context_elements)
    
    def __str__(self):
        return "LocalTaxonomyMappingBasedPrecision"
    
class LocalTaxonomyMappingBasedRecall(Metric):
    def __init__(self):
        super(LocalTaxonomyMappingBasedRecall, self).__init__()

    def score(self, schema_element, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        print("schema_element", schema_element)
        learned_context_elements = learned_ontology.get_context_elements(schema_element)
        referenced_context_elements = referenced_ontology.get_context_elements(schema_element)
        if len(learned_context_elements) == 0:
            assert len(referenced_context_elements) == 0, "Something wrong with mappings and the calculation code, because this cannot happen."
            return 1
        print("learned_context_elements", learned_context_elements)
        print("referenced_context_elements", referenced_context_elements)
        print("score", len(set(learned_context_elements).intersection(set(referenced_context_elements))) / len(referenced_context_elements))
        return len(set(learned_context_elements).intersection(set(referenced_context_elements))) / len(referenced_context_elements)
    
    def __str__(self):
        return "LocalTaxonomyMappingBasedRecall"