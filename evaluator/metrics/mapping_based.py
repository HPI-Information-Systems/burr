from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import D2RQMapping

class MappingBasedPrecision(Metric):
    def __init__(self):
        super(MappingBasedPrecision, self).__init__()

    def score(self, el1: D2RQMapping, el2: D2RQMapping) -> float:
        for el in el1:
            el.set_eq_strategy(name_based=False)
        for el in el2:
            el.set_eq_strategy(name_based=False)
        el1 = list(set(el1))
        el2 = list(set(el2))
        shared_elements = [x for x in el2 if x in el1]
        return len(shared_elements) / len(el2) if len(el2) > 0 else 0.0

    def __str__(self):
        return "MappingBasedPrecision"


class MappingBasedRecall(Metric):
    def __init__(self):
        super(MappingBasedRecall, self).__init__()

    def score(self, el1: D2RQMapping, el2: D2RQMapping) -> float:
        for el in el1:
            el.set_eq_strategy(name_based=False)
        for el in el2:
            el.set_eq_strategy(name_based=False)
        el1 = list(set(el1))
        el2 = list(set(el2))
        shared_elements = [x for x in el2 if x in el1]
        return len(shared_elements) / len(el1) if len(el1) > 0 else 0.0

    def __str__(self):
        return "MappingBasedRecall"