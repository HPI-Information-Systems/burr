from evaluator.validator.base_validator import BaseValidator

class AttributeValidator(BaseValidator):
    def __init__(self, mapping, context) -> None:
        super().__init__(mapping=mapping, context=context)
        mapping

    def validate(self, attribute, table_name): self.mapping.get_attribute_from_mapping(attribute, table_name) if self.mapping.get_attribute_from_mapping(attribute, table_name) else None
    



