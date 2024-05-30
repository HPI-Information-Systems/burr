from evaluator.mapping_parser.sql_elements import SQLAttribute, Join
from evaluator.mapping_parser.classmap import ClassMap

class Relation:
    mapping_id: str
    property: str
    belongsToClassMap: ClassMap
    refersToClassMap: ClassMap
    join: str
    column: str

    def __init__(self, mapping_id, property, belongsToClassMap, refersToClassMap, join, column) -> None:
        self.mapping_id = mapping_id
        self.property = property
        self.belongsToClassMap = belongsToClassMap
        self.refersToClassMap = refersToClassMap
        self.join = join
        self.column = column
        self.set_eq_strategy(classes=False)
        #check if join is list
        if isinstance(join, list):
            self.sql_join = [self.parse_join(j) for j in join]
        else:
            self.sql_join = [self.parse_join(join)] if self.join is not None else None
        self.sql_column = self.parse_column(column) if self.column is not None else None

    def parse_join(self, join):
        join = join.split("=")
        left = join[0].split(".")
        right = join[1].split(".")
        return Join(SQLAttribute(left[0], left[1]), SQLAttribute(right[0], right[1]))

    def parse_column(self, column):
        column = column.split(".")
        return SQLAttribute(column[0], column[1])

    def __eq__(self, other):
        if not isinstance(other, Relation):
            return False
        return self._eq_strategy(self, other)
    
    def set_eq_strategy(self, classes=False):
        self._eq_strategy = equality_by_edge_query_and_classes if classes else equality_by_edge_query

    def __hash__(self) -> int:
        joins_hash = hash(frozenset(self.sql_join)) if self.sql_join is not None else 0
        columns_hash = hash(self.sql_column) if self.sql_column is not None else 0
        return hash((joins_hash, columns_hash))
    
    def __repr__(self):
        return f"Relation(property={self.property}, belongsToClassMap={self.belongsToClassMap}, refersToClassMap={self.refersToClassMap}, eq_strategy={self._eq_strategy})"
    


def equality_by_edge_query(edge1: Relation, edge2: Relation) -> bool:
    if not isinstance(edge2, Relation):
        return False
    if edge1.sql_join is not None and edge2.sql_join is not None:
        joins_equal = set(edge1.sql_join) == set(edge2.sql_join)
    elif edge1.sql_join is None and edge2.sql_join is None:
        joins_equal = True
    else:
        joins_equal = False
    if edge1.sql_column is not None and edge2.sql_column is not None:
        columns_equal = edge1.sql_column == edge2.sql_column
    elif edge1.sql_column is None and edge2.sql_column is None:
        columns_equal = True
    else:
        columns_equal = False
    #joins_equal = set(edge1.sql_join) == set(edge2.sql_join) if edge1.sql_join is not None and edge2.sql_join is not None else True
    #columns_equal = edge1.sql_column == edge2.sql_column if edge1.sql_column is not None and edge2.sql_column is not None else True
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
