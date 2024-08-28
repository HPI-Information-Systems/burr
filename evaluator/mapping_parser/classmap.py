from evaluator.mapping_parser.sql_elements import SQLAttribute, Join, Condition
from evaluator.utils.get_jinja_env import get_jinja_env

from functools import reduce
import re

class ClassMap:
    mapping_id: str
    uriPattern: str
    join: str
    class_uri: str
    subclass: str# | list[str]
    condition: str
    def __init__(self, mapping_id, uriPattern, class_uri, join, parent_classes, condition, prefix, datastorage, translate_with) -> None:
        self.uriPattern = uriPattern
        self.mapping_id = mapping_id
        self.class_uri = class_uri
        self.prefix = prefix
        self.datastorage = datastorage
        self.condition = condition
        self.join = join
        self.parent_classes = parent_classes
        self.translate_with = translate_with
            
        if isinstance(join, list):
            self.sql_join = [self.parse_join(j) for j in join]
        else:
            self.sql_join = [self.parse_join(join)] if self.join is not None else None
        if isinstance(condition, list):
            self.sql_condition = [self.parse_condition(s) for s in condition]
        else:
            self.sql_condition = [self.parse_condition(condition)] if self.condition is not None else None
        #self.sql_condition = self.parse_condition(condition) if self.condition is not None else None
        self.sql_uri_pattern: SQLAttribute = self.parse_uri_pattern(uriPattern)
    
    def parse_condition(self, condition):
        operator = list(filter(lambda x: x in condition, ["=", ">", "<", "<=", ">=" "!="]))[0]
        condition = condition.replace(" ", "").split(operator)
        sql = list(filter(lambda x: "." in x, condition))[0]
        value = list(filter(lambda x: "." not in x, condition))[0]
        return Condition(SQLAttribute(sql.split(".")[0], sql.split(".")[1]), operator, value)

    def parse_uri_pattern(self, uri_pattern):
        uri_patterns = re.findall('@@(.*?)@@', uri_pattern)#.group(1).split(".") #!TODO This does not work when having more than one database access
        return [SQLAttribute(table=pattern.split(".")[0], attribute=pattern.split(".")[1]) for pattern in uri_patterns]

    def parse_join(self, join):
        join = join.split("=")
        left = join[0].split(".")
        right = join[1].split(".")
        return Join(SQLAttribute(left[0], left[1]), SQLAttribute(right[0], right[1]))
    
    def get_d2rq_mapping(self):
        return  get_jinja_env() \
                .get_template('classmap.j2') \
                .render(
                    class_name=self.class_uri,
                    mapping_name = self.mapping_id,
                    uri_patterns=self.sql_uri_pattern,
                    #additional_property=self.additional_property,
                    conditions=self.sql_condition,
                    parent_class=self.parent_classes,
                    joins = self.sql_join,
                    datastorage=self.datastorage,
                    prefix = self.prefix,
                    translate_with=self.translate_with
                )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ClassMap):
            return False
        return self.sql_condition == other.sql_condition and self.sql_uri_pattern == other.sql_uri_pattern and self.sql_join == other.sql_join
    
    def __hash__(self) -> int:
        return hash((tuple(self.sql_condition) if isinstance(self.sql_condition, list) else self.sql_condition, self.sql_uri_pattern, self.sql_join))
        #return hash((self.sql_condition, self.sql_uri_pattern, self.sql_join))

    def __repr__(self):
        return f"ClassMap(uriPattern={self.uriPattern}, class_uri={self.class_uri})"