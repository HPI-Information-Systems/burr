from evaluator.mapping_parser.sql_elements import SQLAttribute, Join, Condition
from evaluator.mapping_parser.classmap import ClassMap, name_based_equality
from evaluator.mapping_parser.utils import parse_condition, parse_pattern
from evaluator.utils.get_jinja_env import get_jinja_env
import re
class Relation:
    mapping_id: str
    property: str
    belongsToClassMap: ClassMap
    refersToClassMap: ClassMap
    join: str
    column: str

    def __init__(self, prefix, mapping_id, property, belongsToClassMap, pattern=None, constantValue=None, sqlExpression=None, column=None, join=None, condition=None, datatype=None,refersToClassMap=None, inverse_of=None, translate_with=None) -> None:
        #print(constantValue, sqlExpression, column)
        #assert (constantValue is None and sqlExpression is None and column is not None) or (constantValue is not None and sqlExpression is None and column is None) or (constantValue is None and sqlExpression is not None and column is None)
        self.mapping_id = mapping_id
        self.property = property
        self.belongsToClassMap = belongsToClassMap
        self.refersToClassMap = refersToClassMap
        self.join = join
        self.pattern = pattern
        self.sql_pattern = self.parse_pattern(pattern) if pattern is not None else None
        self.column = column
        self.condition = condition
        self.datatype = datatype
        self.inverse_of = inverse_of
        self.prefix = prefix
        self.translate_with = translate_with
        self.constantValue = constantValue
        self.set_eq_strategy(classes=False)
        self.sql_expression = sqlExpression
        self.translate_with = translate_with
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

    def parse_pattern(self, pattern):
        return parse_pattern(pattern)

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
        return get_jinja_env() \
                .get_template('propertybridge.j2') \
                .render(
                prefix = self.prefix,
                mapping_name = self.mapping_id,
                property=self.property,
                belongs_to_class_map=self.belongsToClassMap.mapping_id if type(self.belongsToClassMap) == ClassMap else self.belongsToClassMap,
                refers_to_class_map=self.refersToClassMap.mapping_id if type(self.refersToClassMap) == ClassMap else self.refersToClassMap,
                joins=self.sql_join,
                conditions=self.sql_condition,
                translate_with=self.translate_with,
                column=self.column,
                pattern = self.pattern,
                sqlExpression = self.sql_expression.lower() if self.sql_expression is not None else None,

                datatype=self.datatype,
                inverse_of=self.inverse_of,
                constant_value = self.constantValue if self.constantValue is not None else None,
            )

    def __eq__(self, other):
        if not isinstance(other, Relation):
            return False
        return self._eq_strategy(self, other)
    
    def set_eq_strategy(self, classes=False, name_based=False, distinct=False):
        if classes:
            self._eq_strategy = equality_by_edge_query_and_classes
            self._hash_strategy = hash_by_edge_query_and_classes
        elif name_based:
            self._eq_strategy = equality_by_property_name_and_classes
            self._hash_strategy = hash_by_property_name
        elif distinct:
            self._eq_strategy = equality_by_property_name_and_classes
            self._hash_strategy = hash
        else:
            self._eq_strategy = equality_by_edge_query
            self._hash_strategy = hash_by_edge_query
        #self._eq_strategy = equality_by_edge_query_and_classes if classes else equality_by_edge_query

    def __hash__(self) -> int:
        return self._hash_strategy(self)
    
    def __str__(self):
        return self.get_d2rq_mapping()

    def __repr__(self):
        return f"Relation(property={self.property}, belongsToClassMap={self.belongsToClassMap}, refersToClassMap={self.refersToClassMap}, eq_strategy={self._eq_strategy}, joins={self.sql_join}, column={self.sql_column}, condition={self.sql_condition}, sql_expression={self.sql_expression})"

def equality_by_property_name(edge1: Relation, edge2: Relation) -> bool:
    def clean_property_name(property):
        fillers = [" ", "_", "-", "has", "is", "of", "the"]
        #work with fillers "a" or "an" only when they follow a capital letter
        for filler in fillers:
            property = property.replace(filler, "")
        property = re.sub(r"\b(a|an)\s+(?=[A-Z])", "", property)
        return property.strip().lower()
    cleaned_equality = clean_property_name(edge1.property) == clean_property_name(edge2.property)
    regular_equality = edge1.property.strip().lower() == edge2.property.strip().lower()
    return cleaned_equality or regular_equality

def equality_by_property_name_and_classes(edge1: Relation, edge2: Relation) -> bool:
    same_property = equality_by_property_name(edge1, edge2)
    ingoing_class_equal = name_based_equality(edge1.belongsToClassMap, edge2.belongsToClassMap)
    if edge1.refersToClassMap is not None and edge2.refersToClassMap is not None:
        outgoing_class_equal = name_based_equality(edge1.refersToClassMap, edge2.refersToClassMap) 
    elif edge1.refersToClassMap is not None and edge2.refersToClassMap is None or edge1.refersToClassMap is None and edge2.refersToClassMap is not None:
        outgoing_class_equal = False
    else:
        outgoing_class_equal = True
    return same_property and outgoing_class_equal and ingoing_class_equal

def equality_by_edge_query(edge1: Relation, edge2: Relation) -> bool:
    if not isinstance(edge2, Relation):
        return False
    joins_not_none = edge1.sql_join is not None and edge2.sql_join is not None
    joins_none = edge1.sql_join is None and edge2.sql_join is None
    sql_expressions_not_none = edge1.sql_sql_expression is not None and edge2.sql_sql_expression is not None
    sql_expressions_none = edge1.sql_sql_expression is None and edge2.sql_sql_expression is None
    columns_not_none = edge1.sql_column is not None and edge2.sql_column is not None
    columns_none = edge1.sql_column is None and edge2.sql_column is None
    constant_values_not_none = edge1.constantValue is not None and edge2.constantValue is not None
    constant_values_none = edge1.constantValue is None and edge2.constantValue is None
    pattern_not_none = edge1.pattern is not None and edge2.pattern is not None
    pattern_none = edge1.pattern is None and edge2.pattern is None
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
    
    if constant_values_not_none:
        constant_values_equal = edge1.constantValue == edge2.constantValue
    elif constant_values_none:
        constant_values_equal = True
    else:
        return False
    
    if pattern_not_none:
        pattern_equal = set(edge1.sql_pattern) == set(edge2.sql_pattern)
    elif pattern_none:
        pattern_equal = True
    else:
        return False
    
    #here check für constantbalue einbae
    return joins_equal and columns_equal and constant_values_equal and pattern_equal

def hash_by_edge_query(edge: Relation) -> int:
    joins_part = frozenset(edge.sql_join) if edge.sql_join else frozenset()
    column_part = edge.sql_column
    sql_expr_part = frozenset(edge.sql_sql_expression) if edge.sql_sql_expression else frozenset()
    pattern_part = frozenset(edge.sql_pattern) if edge.sql_pattern else frozenset()
    constant_part = edge.constantValue
    return hash((joins_part, column_part, sql_expr_part, pattern_part, constant_part))


def hash_by_property_name(edge: Relation) -> int:
    property_hash = hash(edge.property)
    belongs_to_class_map_hash = hash(edge.belongsToClassMap)
    refers_to_class_map_hash = hash(edge.refersToClassMap) if edge.refersToClassMap is not None else 0
    return hash((property_hash, belongs_to_class_map_hash, refers_to_class_map_hash))

def equality_by_edge_query_and_classes(edge1: Relation, edge2: Relation) -> bool:
    ingoing_class_equal = edge1.belongsToClassMap == edge2.belongsToClassMap
    outgoing_class_equal = edge1.refersToClassMap == edge2.refersToClassMap
    return equality_by_edge_query(edge1, edge2) and outgoing_class_equal and ingoing_class_equal

def hash_by_edge_query_and_classes(edge: Relation) -> int:
    # The same parts from hash_by_edge_query:
    joins_part = frozenset(edge.sql_join) if edge.sql_join else frozenset()
    column_part = edge.sql_column
    sql_expr_part = frozenset(edge.sql_sql_expression) if edge.sql_sql_expression else frozenset()
    sql_pattern_part = frozenset(edge.sql_pattern) if edge.sql_pattern else frozenset()
    const_part = edge.constantValue

    # Plus class maps:
    belongs_to_hash = hash(edge.belongsToClassMap)
    refers_to_hash = hash(edge.refersToClassMap) if edge.refersToClassMap else 0

    return hash(
        (joins_part,
         column_part,
         sql_expr_part,
         sql_pattern_part,
         const_part,
         belongs_to_hash,
         refers_to_hash)
    )