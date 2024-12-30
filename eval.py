import os
from evaluator.mapping_parser.mapping import Mapping
from evaluator.metrics.mapping_based import MappingBasedPrecision, MappingBasedRecall
from evaluator.metrics.taxonomy_mapping_based import TaxonomyMappingBasedPrecision, TaxonomyMappingBasedRecall
from evaluator.metrics.metric import F1Score

# Define paths for generated mappings and groundtruth mappings
generated_mappings_folder = '/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/mappings'
groundtruth_mappings_folder = '/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/groundtruths'

# Initialize metrics
def evaluate_mappings(generated_mapping_file, groundtruth_mapping_file):
    mapping_1 = Mapping(groundtruth_mapping_file)
    # print("mapping1", mapping_1)
    mapping_2 = Mapping(generated_mapping_file)
    # print("mapping2", mapping_2)

    precision = MappingBasedPrecision()(mapping_1, mapping_2)
    recall = MappingBasedRecall()(mapping_1, mapping_2)
    f1 = F1Score()(precision, recall)

    tr = TaxonomyMappingBasedRecall().score(mapping_2, mapping_1)
    tp = TaxonomyMappingBasedPrecision()(mapping_2, mapping_1)
    tf1 = F1Score()(tp, tr)

    return {
        'Precision': precision,
        'Recall': recall,
        'F1': f1,
        'Taxonomy Precision': tp,
        'Taxonomy Recall': tr,
        'Taxonomy F1': tf1
    }

# Group results by experiment
results = {}

# Iterate through generated mappings and find corresponding groundtruth mappings
for generated_mapping_file in os.listdir(generated_mappings_folder):
    if generated_mapping_file == "attributes__cryptic_attribute_name__person.ttl" or generated_mapping_file == "denormalized__same_concept_multiple_tables__library.ttl" or "boolean_relation" in generated_mapping_file:
        continue
    if generated_mapping_file != "denormalized__composite_attributes__person.ttl":
        continue
    print("experiment", generated_mapping_file)
    if generated_mapping_file.endswith('.ttl'):
        # Extract experiment details from file name
        parts = generated_mapping_file.split('__')
        if len(parts) != 3:
            continue
        superexperiment, experiment, scenario = parts

        # Construct file paths
        generated_mapping_path = os.path.join(generated_mappings_folder, generated_mapping_file)
        groundtruth_mapping_path = os.path.join(groundtruth_mappings_folder, generated_mapping_file)

        # Check if corresponding groundtruth mapping exists
        if os.path.exists(groundtruth_mapping_path):
            # Evaluate mappings
            metrics = evaluate_mappings(generated_mapping_path, groundtruth_mapping_path)

            # Group results by experiment
            if experiment not in results:
                results[experiment] = []
            results[experiment].append({
                'Scenario': scenario,
                'Metrics': metrics
            })

# Print results grouped by experiment
for experiment, experiment_results in results.items():
    print(f"Experiment: {experiment}")
    total_f1 = 0
    num_scenarios = len(experiment_results)
    for result in experiment_results:
        scenario = result['Scenario']
        metrics = result['Metrics']
        total_f1 += metrics['F1']
        print(f"  Scenario: {scenario}")
        print(f"    Precision: {metrics['Precision']}")
        print(f"    Recall: {metrics['Recall']}")
        print(f"    F1: {metrics['F1']}")
        print(f"    Taxonomy Precision: {metrics['Taxonomy Precision']}")
        print(f"    Taxonomy Recall: {metrics['Taxonomy Recall']}")
        print(f"    Taxonomy F1: {metrics['Taxonomy F1']}")
    average_f1 = total_f1 / num_scenarios if num_scenarios > 0 else 0
    print(f"  Average F1 Score: {average_f1}")
    print()