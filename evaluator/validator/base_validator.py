from evaluator.mapping_parser.mapping import Mapping
from evaluator.validator.nm_table_validator import NMTableValidator
from evaluator.context.context import N1RelationContext, NMTableContext

class BaseValidator:
    def __init__(self, mapping: Mapping, context) -> None:
        self.ontology = mapping
        self.context = context

    def validate(self, attribute, table_name, context):
        raise NotImplementedError
    

#todo finish this gem
def get_validator(context):
    if type(context) == NMTableContext:
        return NMTableValidator
    else:
        return None

