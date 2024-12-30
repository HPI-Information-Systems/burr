from dataclasses import dataclass
from typing import List

@dataclass
class ForeignKeyRelation:
    name: str = ""
    origin_table: str = ""
    origin_attribute: str = ""
    reference_table: str = ""
    reference_attribute: str = ""

class TableContext:
    table_name = ""
    attributes = []
    foreign_keys: List[ForeignKeyRelation] = []
    primary_keys = []

    def __init__(self, table_name, attributes, foreign_keys, primary_keys) -> None:
        self.table_name = table_name
        self.attributes = attributes
        self.foreign_keys = foreign_keys
        self.primary_keys = primary_keys

    def stringify(self):    
        return f"{self.table_name} {' '.join(self.attributes)} {' '.join(map(lambda x: x.name, self.foreign_keys))} {' '.join(self.primary_keys)}"