from evaluator.metrics.mapping_based import MappingBasedPrecision, MappingBasedRecall
from evaluator.metrics.name_based import NameBasedPrecision, NameBasedRecall
from evaluator.metrics.taxonomy_mapping_based import TaxonomyMappingBasedPrecision, TaxonomyMappingBasedRecall
from evaluator.metrics.metric import F1Score

def calculate_metrics(reference_mapping, learned_mapping):
    metrics = {
        "mapping_based": {"precision": MappingBasedPrecision, "recall": MappingBasedRecall},
        "name_based": {"precision": NameBasedPrecision, "recall": NameBasedRecall},
        #"taxonomy_mapping_based": {"precision": TaxonomyMappingBasedPrecision, "recall": TaxonomyMappingBasedRecall},
    }
    for key, metric_concept in metrics.items():
        values = calculate_local_metrics(reference_mapping, learned_mapping, metric_concept["precision"], metric_concept["recall"])
        metrics[key] = values
        print("Metrics for", key, ":", values)
    taxonomy_precision = TaxonomyMappingBasedPrecision().score(learned_mapping, reference_mapping)
    taxonomy_recall = TaxonomyMappingBasedRecall().score(learned_mapping, reference_mapping)
    taxonomy_f1 = F1Score()(taxonomy_precision, taxonomy_recall)
    metrics["taxonomy_mapping_based"] = { "precision": taxonomy_precision, "recall": taxonomy_recall, "f1": taxonomy_f1 }
    return metrics

def calculate_local_metrics(reference_mapping, learned_mapping, Precision, Recall):
    # metrics for concepts
    cls_precision = Precision()(learned_mapping.get_classes(), reference_mapping.get_classes())
    cls_recall = Recall()(learned_mapping.get_classes(), reference_mapping.get_classes())
    cls_f1 = F1Score()(cls_precision, cls_recall)
    # metrics for relations
    # print("RELATIONS", learned_mapping.get_relations())
    # print("RELATIONS2", reference_mapping.get_relations())
    rel_precision = Precision()(learned_mapping.get_relations(), reference_mapping.get_relations())
    rel_recall = Recall()(learned_mapping.get_relations(), reference_mapping.get_relations())
    rel_f1 = F1Score()(rel_precision, rel_recall)
    # metrics for attributes
    attr_precision = Precision()(learned_mapping.get_attributes(), reference_mapping.get_attributes())
    attr_recall = Recall()(learned_mapping.get_attributes(), reference_mapping.get_attributes())
    attr_f1 = F1Score()(attr_precision, attr_recall)

    return { "cls_precision": cls_precision, "cls_recall": cls_recall, "cls_f1": cls_f1, "rel_precision": rel_precision, "rel_recall": rel_recall, "rel_f1": rel_f1, "attr_precision": attr_precision, "attr_recall": attr_recall, "attr_f1": attr_f1 }

