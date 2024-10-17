from evaluator.metrics.mapping_based import MappingBasedPrecision, MappingBasedRecall
from evaluator.metrics.taxonomy_mapping_based import TaxonomyMappingBasedPrecision, TaxonomyMappingBasedRecall
from evaluator.metrics.metric import F1Score

def calculate_metrics(reference_mapping, learned_mapping):
    # metrics for concepts
    cls_precision = MappingBasedPrecision()(learned_mapping.get_classes(), reference_mapping.get_classes())
    cls_recall = MappingBasedRecall()(learned_mapping.get_classes(), reference_mapping.get_classes())
    cls_f1 = F1Score()(cls_precision, cls_recall)
    # metrics for relations
    rel_precision = MappingBasedPrecision()(learned_mapping.get_relations(), reference_mapping.get_relations())
    rel_recall = MappingBasedRecall()(learned_mapping.get_relations(), reference_mapping.get_relations())
    rel_f1 = F1Score()(rel_precision, rel_recall)
    # metrics for attributes
    attr_precision = MappingBasedPrecision()(learned_mapping.get_attributes(), reference_mapping.get_attributes())
    attr_recall = MappingBasedRecall()(learned_mapping.get_attributes(), reference_mapping.get_attributes())
    attr_f1 = F1Score()(attr_precision, attr_recall)

    return { "cls_precision": cls_precision, "cls_recall": cls_recall, "cls_f1": cls_f1, "rel_precision": rel_precision, "rel_recall": rel_recall, "rel_f1": rel_f1, "attr_precision": attr_precision, "attr_recall": attr_recall, "attr_f1": attr_f1 }

