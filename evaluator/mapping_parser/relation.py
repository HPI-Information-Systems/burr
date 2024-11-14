from evaluator.mapping_parser.sql_elements import SQLAttribute, Join, Condition
from evaluator.mapping_parser.classmap import ClassMap
from evaluator.mapping_parser.utils import parse_condition
from evaluator.utils.get_jinja_env import get_jinja_env
import re
class Relation:
    mapping_id: str
    property: str
    belongsToClassMap: ClassMap
    refersToClassMap: ClassMap
    join: str
    column: str

    def __init__(self, prefix, mapping_id, property, belongsToClassMap, constantValue=None, sqlExpression=None, column=None, join=None, condition=None, datatype=None,refersToClassMap=None, inverse_of=None, translate_with=None) -> None:
        #print(constantValue, sqlExpression, column)
        #assert (constantValue is None and sqlExpression is None and column is not None) or (constantValue is not None and sqlExpression is None and column is None) or (constantValue is None and sqlExpression is not None and column is None)
        self.mapping_id = mapping_id
        self.property = property
        self.belongsToClassMap = belongsToClassMap
        self.refersToClassMap = refersToClassMap
        self.join = join
        self.column = column
        self.condition = condition
        self.datatype = datatype
        self.inverse_of = inverse_of
        self.prefix = prefix
        self.translate_with = translate_with
        self.constantValue = constantValue
        self.set_eq_strategy(classes=False)
        self.sql_expression = sqlExpression
        self.sql_sql_expression = self.parse_sql_expression(sqlExpression) if sqlExpression is not None else None
        if isinstance(join, list):
            self.sql_join = [self.parse_join(j) for j in join]
        else:
            self.sql_join = [self.parse_join(join)] if self.join is not None else None
        if isinstance(condition, list):
            self.sql_condition = [self.parse_condition(j) for j in condition]
        else:
            self.sql_condition = [self.parse_condition(condition)] if self.condition is not None else None    
        self.sql_column = self.parse_column(column) if self.column is not None else None

    def parse_sql_expression(self,sqlExpression):
        match = re.search(r'\((.*)\)', sqlExpression)
        if match:
            attributes = []
            arguments = match.group(1)
            for arg in arguments.split(','):
                arg = arg.strip()
                pattern = r"(?<!['\"])\b\w+\.\w+\b(?!['\"])"
                attributes = attributes + re.findall(pattern, arg)
            return list(map(lambda attr: SQLAttribute(attr.split(".")[0].lower(), attr.split(".")[1].lower()), attributes))
        return []

    def parse_join(self, join):
        join = join.replace(" ", "").replace(">", "").replace("<", "")
        join = join.split("=")
        left = join[0].split(".")
        right = join[1].split(".")
        return Join(SQLAttribute(left[0].lower(), left[1].lower()), SQLAttribute(right[0], right[1]))
    
    def parse_condition(self, condition):
        return parse_condition(condition)

    def parse_column(self, column):
        column = column.split(".")
        return SQLAttribute(column[0].lower(), column[1].lower())

    def get_d2rq_mapping(self):
        return  get_jinja_env() \
                .get_template('propertybridge.j2') \
                .render(
                prefix = self.prefix,
                mapping_name = self.mapping_id,
                property=self.property,
                belongs_to_class_map=self.belongsToClassMap.mapping_id if type(self.belongsToClassMap) == ClassMap else self.belongsToClassMap,
                refers_to_class_map=self.refersToClassMap.mapping_id if type(self.refersToClassMap) == ClassMap else self.refersToClassMap,
                joins=self.sql_join,
                conditions=self.sql_condition,
                column=self.column,
                sqlExpression = self.sql_expression.lower() if self.sql_expression is not None else None,
                datatype=self.datatype,
                inverse_of=self.inverse_of,
                constant_value = self.constantValue if self.constantValue is not None else None,
            )

    def __eq__(self, other):
        if not isinstance(other, Relation):
            return False
        return self._eq_strategy(self, other)
    
    def set_eq_strategy(self, classes=False, name_based=False):
        if classes:
            self._eq_strategy = equality_by_edge_query_and_classes
            self._hash_strategy = hash_by_edge_query_and_classes
        elif name_based:
            self._eq_strategy = equality_by_property_name
            self._hash_strategy = hash
        else:
            self._eq_strategy = equality_by_edge_query
            self._hash_strategy = hash_by_edge_query
        #self._eq_strategy = equality_by_edge_query_and_classes if classes else equality_by_edge_query

    def __hash__(self) -> int:
        joins_hash = hash(frozenset(self.sql_join)) if self.sql_join is not None else 0
        columns_hash = hash(self.sql_column) if self.sql_column is not None else 0
        return hash((joins_hash, columns_hash))
    
    def __str__(self):
        return self.get_d2rq_mapping()

    def __repr__(self):
        return f"Relation(property={self.property}, belongsToClassMap={self.belongsToClassMap}, refersToClassMap={self.refersToClassMap}, eq_strategy={self._eq_strategy})"
    
def equality_by_property_name(edge1: Relation, edge2: Relation) -> bool:
    #print(edge1.property, edge2.property)
    return edge1.property.strip().lower() == edge2.property.strip().lower()

def equality_by_edge_query(edge1: Relation, edge2: Relation) -> bool:
    if not isinstance(edge2, Relation):
        return False
    joins_not_none = edge1.sql_join is not None and edge2.sql_join is not None
    joins_none = edge1.sql_join is None and edge2.sql_join is None
    sql_expressions_not_none = edge1.sql_sql_expression is not None and edge2.sql_sql_expression is not None
    sql_expressions_none = edge1.sql_sql_expression is None and edge2.sql_sql_expression is None
    columns_not_none = edge1.sql_column is not None and edge2.sql_column is not None
    columns_none = edge1.sql_column is None and edge2.sql_column is None
    if joins_not_none:
        joins_equal = set(edge1.sql_join) == set(edge2.sql_join)
    elif joins_none:
        joins_equal = True
    else:
        return False

    if columns_not_none:
        columns_equal = edge1.sql_column == edge2.sql_column
    elif columns_none and sql_expressions_not_none:
        columns_equal = set(edge1.sql_sql_expression) == set(edge2.sql_sql_expression)
    elif columns_none and sql_expressions_none:
        columns_equal = True
    else:
        return False
    return joins_equal and columns_equal

def hash_by_edge_query(edge: Relation) -> int:
    joins_hash = hash(frozenset(edge.sql_join)) if edge.sql_join is not None else 0
    columns_hash = hash(edge.sql_column) if edge.sql_column is not None else 0
    return hash((joins_hash, columns_hash))

def equality_by_edge_query_and_classes(edge1: Relation, edge2: Relation) -> bool:
    ingoing_class_equal = edge1.belongsToClassMap == edge2.belongsToClassMap
    outgoing_class_equal = edge1.refersToClassMap == edge2.refersToClassMap
    return equality_by_edge_query(edge1, edge2) and outgoing_class_equal and ingoing_class_equal

def hash_by_edge_query_and_classes(edge: Relation) -> int:
    joins_hash = hash(frozenset(edge.sql_join)) if edge.sql_join is not None else 0
    columns_hash = hash(edge.sql_column) if edge.sql_column is not None else 0
    belongs_to_class_map_hash = hash(edge.belongsToClassMap)
    refers_to_class_map_hash = hash(edge.refersToClassMap)
    return hash((joins_hash, columns_hash, belongs_to_class_map_hash, refers_to_class_map_hash))
