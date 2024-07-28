import unittest
import os
import json
from evaluator.metrics.mapping_based import MappingBasedPrecision, MappingBasedRecall
from evaluator.mapping_parser.mapping import Mapping
from evaluator.metrics.taxonomy_mapping_based import TaxonomyMappingBasedPrecision, TaxonomyMappingBasedRecall
from evaluator.metrics.metric import F1Score
class TestMetrics(unittest.TestCase):

    def setUp(self):
        self.test_dir = "tests"

    def load_test_case(self, case_dir):
        files = {}
        for filename in os.listdir(case_dir):
            file_path = os.path.join(case_dir, filename)
            with open(file_path, 'r') as file:
                if filename == 'expected_metrics.json':
                    files['expected'] = json.load(file)
                else:
                    files[filename] = file_path
        return files

    def generate_test_cases(self):
        test_cases = []
        for test_case in os.listdir(self.test_dir):
            test_case_dir = os.path.join(self.test_dir, test_case)
            if os.path.isdir(test_case_dir):
                files = self.load_test_case(test_case_dir)
                test_cases.append((test_case, files))
        return test_cases

    def test_metrics(self):
        for test_case, files in self.generate_test_cases():
            with self.subTest(test_case=test_case):
                mapping_learned = Mapping(files['mapping_learned.ttl'])
                mapping_reference = Mapping(files['mapping_reference.ttl'])
                precision = MappingBasedPrecision()(mapping_learned, mapping_reference)
                recall = MappingBasedRecall()(mapping_learned, mapping_reference)
                f1 = F1Score()(precision, recall)
                tp = TaxonomyMappingBasedPrecision()(mapping_learned, mapping_reference)
                tr = TaxonomyMappingBasedRecall().score(mapping_learned, mapping_reference)
                tf1 = F1Score()(tp, tr)
                result = {
                    "precision": round(precision,2),
                    "recall": round(recall,2),
                    "f1": round(f1,2),
                    "taxonomy_precision": round(tp,2),
                    "taxonomy_recall": round(tr,2),
                    "taxonomy_f1": round(tf1,2)
                }
                self.assertEqual(result, files['expected'], f"Failed on {test_case}")

if __name__ == '__main__':
    unittest.main()