from evaluator.validator.base_validator import BaseValidator

class NMTableValidator(BaseValidator):
    def __init__(self, mapping, context) -> None:
        super().__init__(mapping=mapping, context=context)
        mapping

    def validate(self, context):
        pass

    def get_attribute_from_ontology(self, attribute, table):
        pass
    