import numpy as np

from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import D2RQMapping
from evaluator.mapping_parser.relation import Relation
from evaluator.mapping_parser.classmap import ClassMap

class TaxonomyMappingBasedPrecision(Metric):
    def __init__(self):
        super(TaxonomyMappingBasedPrecision, self).__init__()

    def score(self, learned_ontology: D2RQMapping, referenced_ontology: D2RQMapping) -> float:
        shared_classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        learned_ontology.classes = list(shared_classes)
        referenced_ontology.classes = list(shared_classes)
        learned_ontology.set_eq_strategy(classes=False)
        referenced_ontology.set_eq_strategy(classes=False)
        shared_relations_referenced = set(set(learned_ontology.relations).intersection(set(referenced_ontology.relations)))
        shared_relations_learned = set(referenced_ontology.relations).intersection(set(learned_ontology.relations))
        learned_ontology.relations, edges_to_remove = filter_edges_with_missing_classes(list(shared_relations_learned), learned_ontology.classes)
        shared_relations_learned = list(set(shared_relations_learned) - set(edges_to_remove))
        referenced_ontology.relations, edges_to_remove = filter_edges_with_missing_classes(list(shared_relations_referenced), referenced_ontology.classes)
        shared_relations_referenced = list(set(shared_relations_referenced) - set(edges_to_remove))
        shared_elements = shared_relations_referenced
        return np.mean(list(map(lambda el: LocalTaxonomyMappingBasedPrecision().score(el, learned_ontology, referenced_ontology), shared_elements)))
    
    def __str__(self):
        return "TaxonomyMappingBasedPrecision"

class TaxonomyMappingBasedRecall():
    # def __init__(self):
    #     super(TaxonomyMappingBasedRecall, self).__init__()

    def score(self, learned_ontology: D2RQMapping, referenced_ontology: D2RQMapping) -> float:
        #intersect ontology
        #todo alle gemeinsamen konzepte, basierend auf uripattern, sqljoin, sqlconiditon -> check sql column!
        shared_classes = set(learned_ontology.classes).intersection(set(referenced_ontology.classes))
        learned_ontology.classes = list(shared_classes)
        referenced_ontology.classes = list(shared_classes)
        learned_ontology.set_eq_strategy(classes=False)
        referenced_ontology.set_eq_strategy(classes=False)

        #gleiche mit relationen -> alle gleichen relationen aber ohne domain und range
        # was ist mit denen die keinen join oder so haben? -> wie werden die behandelt?
        shared_relations_referenced = set(set(learned_ontology.relations).intersection(set(referenced_ontology.relations)))
        shared_relations_learned = set(referenced_ontology.relations).intersection(set(learned_ontology.relations))

        #shared classes that are at edges but not in the class list are removed
        # es wird nur noch der subgraph betrachtet, der auch in den klassen vorkommt
        # print(shared_relations_learned)
        learned_ontology.relations, edges_to_remove = filter_edges_with_missing_classes(list(shared_relations_learned), learned_ontology.classes)
        # print("edges to remove", edges_to_remove)
        shared_relations_learned = list(set(shared_relations_learned) - set(edges_to_remove))
        referenced_ontology.relations, edges_to_remove = filter_edges_with_missing_classes(list(shared_relations_referenced), referenced_ontology.classes)
        shared_relations_referenced = list(set(shared_relations_referenced) - set(edges_to_remove))
        shared_elements = shared_relations_referenced
        # print("shared_classes", shared_classes)
        # auf diesen subgraphen wird nun precision und recall berechnet
        for el in shared_elements:
            # print("el", el)
            # print("learned",learned_ontology)
            # print("referenced",referenced_ontology)
            print(LocalTaxonomyMappingBasedRecall().score(el, learned_ontology, referenced_ontology))
        res = list(map(lambda el: LocalTaxonomyMappingBasedRecall().score(el, learned_ontology, referenced_ontology), shared_elements))
        return np.mean(res)
    
    def __str__(self):
        return "TaxonomyMappingBasedRecall"
    
class TaxonomyMappingBasedF1(Metric):
    def __init__(self):
        super(TaxonomyMappingBasedF1, self).__init__()

    def score(self, learned_ontology: D2RQMapping, referenced_ontology: D2RQMapping) -> float:
        precision = TaxonomyMappingBasedPrecision().score(learned_ontology, referenced_ontology)
        recall = TaxonomyMappingBasedRecall().score(learned_ontology, referenced_ontology)
        return 2 * (precision * recall) / (precision + recall)
    
    def __str__(self):
        return "TaxonomyMappingBasedF1"
    
class LocalTaxonomyMappingBasedPrecision():
    # def __init__(self):
    #     super(LocalTaxonomyMappingBasedPrecision, self).__init__()

    def score(self, schema_element, learned_ontology: D2RQMapping, referenced_ontology: D2RQMapping) -> float:
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
    
class LocalTaxonomyMappingBasedRecall():
    # def __init__(self):
    #     super(LocalTaxonomyMappingBasedRecall, self).__init__()

    def score(self, schema_element, learned_ontology: D2RQMapping, referenced_ontology: D2RQMapping) -> float:
        learned_ontology.set_eq_strategy(classes=False)
        #print(learned_ontology.relations)
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
        #print("schema el", schema_element)
        # if schema_element.property == "<http://cmt#writtenBy>":
        #     print(schema_element_in_learned)
        #     print("learned", len(learned_context_elements))
        #     print("referenced", len(referenced_context_elements))
        #     print("score", len(set(learned_context_elements).intersection(set(referenced_context_elements))) / len(referenced_context_elements))
        return len(set(learned_context_elements).intersection(set(referenced_context_elements))) / len(referenced_context_elements)
    
    def __str__(self):
        return "LocalTaxonomyMappingBasedRecall"
    
def filter_edges_with_missing_classes(edges: list[Relation], classes: list[ClassMap]):
    #I do not deal with attributes (dataproperties) as I filter everything that has not a range. Does this make sense?
    return list(filter(lambda edge: edge.belongsToClassMap in classes and edge.refersToClassMap in classes and edge.refersToClassMap is not None, edges)), list(filter(lambda edge: edge.belongsToClassMap not in classes or edge.refersToClassMap not in classes or edge.refersToClassMap is None, edges))
    #return list(filter(lambda edge: edge.ref in classes and edge[1] in classes, edges))