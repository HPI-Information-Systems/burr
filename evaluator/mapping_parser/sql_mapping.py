from dataclasses import dataclass
import re

class SQLAttribute:
    def __init__(self, table, attribute):
        self.table = table
        self.attribute = attribute

    def __eq__(self, other):
        return isinstance(other, SQLAttribute) and self.table == other.table and self.attribute == other.attribute

    def __hash__(self):
        return hash((self.table, self.attribute))

class Condition:
    def __init__(self, sql_attribute, operator, value):
        self.sql_attribute = sql_attribute
        self.operator = operator
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Condition) and self.sql_attribute == other.sql_attribute and self.operator == other.operator and self.value == other.value

    def __hash__(self):
        return hash((self.sql_attribute, self.operator, self.value))


@dataclass
class Join:
    left_attribute: SQLAttribute
    right_attribute: SQLAttribute

@dataclass
class Query:
    content: set

def sql_attribute_equal(sql_attribute1, sql_attribute2): sql_attribute1.table == sql_attribute2.table and sql_attribute1.attribute == sql_attribute2.attribute
def join_equal(join1, join2): sql_attribute_equal(join1.left_attribute, join2.left_attribute) and sql_attribute_equal(join1.right_attribute, join2.right_attribute) or sql_attribute_equal(join1.left_attribute, join2.right_attribute) and sql_attribute_equal(join1.right_attribute, join2.left_attribute)
def condition_equal(condition1: Condition, condition2: Condition): sql_attribute_equal(condition1.sql_attribute, condition2.sql_attribute) and condition1.operator == condition2.operator and condition1.value == condition2.value

class ClassMap:
    #Todo classmap can also have a join
    uriPattern: str
    class_uri: str
    subclass: str# | list[str]
    condition: str
    graph: str
    def __init__(self, uriPattern, class_uri, additionalClassDefinitionProperty, condition, graph) -> None:
        self.uriPattern = uriPattern
        self.class_uri = class_uri
        self.additionalClassDefinitionProperty = additionalClassDefinitionProperty
        self.condition = condition
        self.subclasses = None
        self.condition = None
        if self.additionalClassDefinitionProperty is not None:
            self.subclasses = []
            if isinstance(additionalClassDefinitionProperty, list):
                for el in additionalClassDefinitionProperty:
                    self.subclasses.append(self.parse_additionalClassDefinitionProperty(el, graph))
            else:
                self.subclasses = self.parse_additionalClassDefinitionProperty(additionalClassDefinitionProperty, graph)
        self.sql_condition = self.parse_condition(condition) if self.condition is not None else None
        self.sql_uri_pattern: SQLAttribute = self.parse_uri_pattern(uriPattern)
        print(self.sql_condition)
        print(self.sql_uri_pattern)
        print(self.subclasses)
    
    def parse_condition(self, condition):
        operator = list(filter(lambda x: x in condition, ["=", ">", "<", "<=", ">=" "!="]))[0]
        condition = condition.replace(" ", "").split(operator)
        sql = list(filter(lambda x: "." in x, condition))[0]
        value = list(filter(lambda x: "." not in x, condition))[0]
        return Condition(SQLAttribute(sql.split(".")[0], sql.split(".")[1]), operator, value)

    def parse_uri_pattern(self, uri_pattern):
        uri_pattern = re.search('@@(.*)@@', uri_pattern).group(1).split(".")
        return SQLAttribute(table=uri_pattern[0], attribute=uri_pattern[1])
        
    def parse_additionalClassDefinitionProperty(self, uri, graph):
        query = f"""             
            SELECT DISTINCT ?class
            WHERE {{ {uri} d2rq:propertyValue ?class. }}
        """
        res = [obj[0].n3() for obj in graph.query(query)]
        return res if len(res)>1 else res[0]
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ClassMap):
            return False
        print("todo add condition for uri\
        todo handle correctly uripattern in equality check")
        return self.sql_condition == other.sql_condition and self.sql_uri_pattern == other.sql_uri_pattern
    
    def __hash__(self) -> int:
        return hash((self.sql_condition, self.sql_uri_pattern))

    def __repr__(self):
        return f"ClassMap(uriPattern={self.uriPattern}, class_uri={self.class_uri})"


class Relation:
    property: str
    belongsToClassMap: str
    refersToClassMap: str
    join: str
    column: str
    def __init__(self, property, belongsToClassMap, refersToClassMap, join, column) -> None:
        self.property = property
        self.belongsToClassMap = belongsToClassMap
        self.refersToClassMap = refersToClassMap
        self.join = join
        self.column = column
        self.sql_join = self.parse_join(join) if self.join is not None else None
        self.sql_column = self.parse_column(column) if self.column is not None else None
    
    def parse_join(self, join):
        join = join.split("=")
        left = join[0].split(".")
        right = join[1].split(".")
        return Join(SQLAttribute(left[0], left[1]), SQLAttribute(right[0], right[1]))
    
    def parse_column(self, column):
        column = column.split(".")
        return SQLAttribute(column[0], column[1])
    
    def __eq__(self, value: object) -> bool:
        #todo is this correct?
        return join_equal(self.sql_join, value.sql_join) if self.sql_join is not None and value.sql_join is not None else True \
                and \
               sql_attribute_equal(self.sql_column, value.sql_column) if self.sql_column is not None and value.sql_column is not None else True

    def __hash__(self) -> int:
        pass