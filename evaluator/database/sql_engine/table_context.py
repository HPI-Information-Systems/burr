from dataclasses import dataclass
from typing import List

@dataclass
class ForeignKeyRelation:
    name: str = ""
    origin_table: str = ""
    origin_attribute: str = ""
    reference_table: str = ""
    reference_attribute: str = ""

@dataclass
class TableContext:
    table_name = ""
    attributes = []
    foreign_keys: List[ForeignKeyRelation] = []
    primary_keys = []