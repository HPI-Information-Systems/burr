from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import Mapping

class MappingBasedPrecision(Metric):
    def __init__(self):
        super(MappingBasedPrecision, self).__init__()

    def score(self, el1: Mapping, el2: Mapping) -> float:
        shared_elements = [x for x in el2.classes if x in el1.classes]
        return len(shared_elements) / (len(el1) + len(el1))
    
    def __str__(self):
        return "MappingBasedPrecision"

class MappingBasedRecall(Metric):
    def __init__(self):
        super(MappingBasedRecall, self).__init__()

    def score(self, el1, el2) -> float:
        shared_elements = [x for x in el2.classes if x in el1.classes]
        return len(shared_elements) / (len(el2) + len(el2))
    
    def __str__(self):
        return "MappingBasedRecall"