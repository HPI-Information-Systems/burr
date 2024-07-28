import os
import json
import pytest
from evaluator.metrics.mapping_based import MappingBasedPrecision, MappingBasedRecall
from evaluator.mapping_parser.mapping import Mapping
from evaluator.metrics.taxonomy_mapping_based import TaxonomyMappingBasedPrecision, TaxonomyMappingBasedRecall
from evaluator.metrics.metric import F1Score

@pytest.fixture(scope="module")
def test_dir():
    return "tests"

def load_test_case(case_dir):
    files = {}
    for filename in os.listdir(case_dir):
        file_path = os.path.join(case_dir, filename)
        with open(file_path, 'r') as file:
            if filename == 'expected_metrics.json':
                files['expected'] = json.load(file)
            else:
                files[filename] = file_path
    return files

@pytest.fixture(scope="module")
def generate_test_cases(test_dir):
    test_cases = []
    for test_case in os.listdir(test_dir):
        test_case_dir = os.path.join(test_dir, test_case)
        if os.path.isdir(test_case_dir):
            files = load_test_case(test_case_dir)
            test_cases.append((test_case, files))
    return test_cases

@pytest.mark.parametrize("test_case, files", generate_test_cases(test_dir()))
def test_metrics(test_case, files):
    mapping_learned = Mapping(files['mapping_learned.ttl'])
    mapping_reference = Mapping(files['mapping_reference.ttl'])
    precision = MappingBasedPrecision()(mapping_learned, mapping_reference)
    recall = MappingBasedRecall()(mapping_learned, mapping_reference)
    f1 = F1Score()(precision, recall)
    tp = TaxonomyMappingBasedPrecision()(mapping_learned, mapping_reference)
    tr = TaxonomyMappingBasedRecall().score(mapping_learned, mapping_reference)
    tf1 = F1Score()(tp, tr)
    result = {
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "f1": round(f1, 2),
        "taxonomy_precision": round(tp, 2),
        "taxonomy_recall": round(tr, 2),
        "taxonomy_f1": round(tf1, 2)
    }
    assert result == files['expected'], f"Failed on {test_case}"
