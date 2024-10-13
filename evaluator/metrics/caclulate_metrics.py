from evaluator.metrics.mapping_based import MappingBasedPrecision, MappingBasedRecall
from evaluator.metrics.taxonomy_mapping_based import TaxonomyMappingBasedPrecision, TaxonomyMappingBasedRecall
from evaluator.metrics.metric import F1Score

def calculate(reference_mapping, learned_mapping):
    # metrics for concepts
    precision = MappingBasedPrecision()(learned_mapping.get_classes(), reference_mapping.get_classes())
    recall = MappingBasedRecall()(learned_mapping.get_classes(), reference_mapping.get_classes())
    f1 = F1Score()(precision, recall)
    # metrics for relations
    precision = MappingBasedPrecision()(learned_mapping.get_relations(), reference_mapping.get_relations())
    recall = MappingBasedRecall()(learned_mapping.get_relations(), reference_mapping.get_relations())
    f1 = F1Score()(precision, recall)
    # metrics for attributes
    precision = MappingBasedPrecision()(learned_mapping.get_attributes(), reference_mapping.get_attributes())
    recall = MappingBasedRecall()(learned_mapping.get_attributes(), reference_mapping.get_attributes())
    f1 = F1Score()(precision, recall)

