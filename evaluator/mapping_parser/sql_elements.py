from dataclasses import dataclass
@dataclass
class SQLAttribute:
    table: str
    attribute: str

    def __post_init__(self):
        # Convert table and attribute to lowercase
        self.table = self.table.lower()
        self.attribute = self.attribute.lower()

    def __eq__(self, other):
        return isinstance(other, SQLAttribute) and self.table == other.table and self.attribute == other.attribute

    def __hash__(self):
        return hash((self.table, self.attribute))
    
    def __str__(self):
        return f"{self.table.lower()}.{self.attribute.lower()}"

@dataclass
class Condition:
    sql_attribute: SQLAttribute
    operator: str
    value: str
    
    def __eq__(self, other):
        return isinstance(other, Condition) and self.sql_attribute == other.sql_attribute and self.operator == other.operator and self.value == other.value

    def __hash__(self):
        return hash((self.sql_attribute, self.operator, self.value))
    
    def __str__(self):
        return f"{self.sql_attribute} {self.operator} {self.value}"


@dataclass
class Join:
    left_attribute: SQLAttribute
    right_attribute: SQLAttribute

    def __eq__(self, other):
        if not isinstance(other, Join):
            return False
        return (self.left_attribute == other.left_attribute and self.right_attribute == other.right_attribute) or \
               (self.left_attribute == other.right_attribute and self.right_attribute == other.left_attribute)

    def __hash__(self):
        return hash(frozenset([self.left_attribute, self.right_attribute]))
    
    def __str__(self):
        return f"{self.left_attribute} = {self.right_attribute}"
@dataclass
class Query:
    content: set