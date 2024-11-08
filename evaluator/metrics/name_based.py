from evaluator.metrics.metric import Metric
from evaluator.mapping_parser.mapping import D2RQMapping
from evaluator.mapping_parser.classmap import ClassMap
from evaluator.mapping_parser.relation import Relation
from evaluator.metrics import Precision, Recall

class NameBasedPrecision(Metric):
    def __init__(self):
        super(NameBasedPrecision, self).__init__()

    def score(self, el1: ClassMap | Relation, el2: ClassMap | Relation) -> float:
        el1.set_eq_strategy(name_based=True)
        el2.set_eq_strategy(name_based=True)
        return Precision()(el1, el2)

    def __str__(self):
        return "NameBasedPrecision"


class NameBasedRecall(Metric):
    def __init__(self):
        super(NameBasedRecall, self).__init__()

    def score(self, el1: ClassMap | Relation, el2: ClassMap | Relation) -> float:
        el1.set_eq_strategy(name_based=True)
        el2.set_eq_strategy(name_based=True)
        return Recall()(el1, el2)

    def __str__(self):
        return "NameBasedRecall"