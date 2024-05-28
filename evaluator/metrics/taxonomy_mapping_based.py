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
        learned_ontology.set_eq_strategy(classes=False)
        referenced_ontology.set_eq_strategy(classes=False)
        shared_relations_referenced = set(learned_ontology.relations).intersection(set(referenced_ontology.relations))
        shared_relations_learned = set(referenced_ontology.relations).intersection(set(learned_ontology.relations))
        learned_ontology.relations = list(shared_relations_learned)
        referenced_ontology.relations = list(shared_relations_referenced)
        shared_elements = shared_relations_referenced
        return np.mean(list(map(lambda el: LocalTaxonomyMappingBasedPrecision().score(el, learned_ontology, referenced_ontology), shared_elements)))
    
    def __str__(self):
        return "TaxonomyMappingBasedPrecision"

class TaxonomyMappingBasedRecall(Metric):
    def __init__(self):
        super(TaxonomyMappingBasedRecall, self).__init__()

    def score(self, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        #intersect ontology
        shared_classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        learned_ontology.classes = list(shared_classes)
        referenced_ontology.classes = list(shared_classes)
        learned_ontology.set_eq_strategy(classes=False)
        referenced_ontology.set_eq_strategy(classes=False)
        shared_relations_referenced = set(learned_ontology.relations).intersection(set(referenced_ontology.relations))
        shared_relations_learned = set(referenced_ontology.relations).intersection(set(learned_ontology.relations))
        learned_ontology.relations = list(shared_relations_learned)
        referenced_ontology.relations = list(shared_relations_referenced)
        shared_elements = shared_relations_referenced
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
        learned_ontology.set_eq_strategy(classes=False)
        referenced_ontology.set_eq_strategy(classes=False)
        schema_element_in_learned = list(filter(lambda x: x == schema_element, learned_ontology.classes + learned_ontology.relations))[0]
        learned_context_elements = learned_ontology.get_context_elements(schema_element_in_learned)
        referenced_context_elements = referenced_ontology.get_context_elements(schema_element)
        learned_ontology.set_eq_strategy(classes=True)
        referenced_ontology.set_eq_strategy(classes=True)
        if len(learned_context_elements) == 0:
            assert len(referenced_context_elements) == 0, "Something wrong with mappings and the calculation code, because this cannot happen."
            return 1
        # print("learned_context_elements", learned_context_elements)
        # print("referenced_context_elements", referenced_context_elements)
        return len(set(learned_context_elements).intersection(set(referenced_context_elements))) / len(learned_context_elements)
    
    def __str__(self):
        return "LocalTaxonomyMappingBasedPrecision"
    
class LocalTaxonomyMappingBasedRecall(Metric):
    def __init__(self):
        super(LocalTaxonomyMappingBasedRecall, self).__init__()

    def score(self, schema_element, learned_ontology: Mapping, referenced_ontology: Mapping) -> float:
        learned_ontology.set_eq_strategy(classes=False)
        referenced_ontology.set_eq_strategy(classes=False)
        schema_element_in_learned = list(filter(lambda x: x == schema_element, learned_ontology.classes + learned_ontology.relations))[0]
        learned_context_elements = learned_ontology.get_context_elements(schema_element_in_learned)
        referenced_context_elements = referenced_ontology.get_context_elements(schema_element)
        learned_ontology.set_eq_strategy(classes=True)
        referenced_ontology.set_eq_strategy(classes=True)
        if len(learned_context_elements) == 0:
            assert len(referenced_context_elements) == 0, "Something wrong with mappings and the calculation code, because this cannot happen."
            return 1
        # print("learned_context_elements", learned_context_elements)
        # print("referenced_context_elements", referenced_context_elements)
        return len(set(learned_context_elements).intersection(set(referenced_context_elements))) / len(referenced_context_elements)
    
    def __str__(self):
        return "LocalTaxonomyMappingBasedRecall"