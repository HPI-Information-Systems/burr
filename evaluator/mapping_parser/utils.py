
import re

from evaluator.mapping_parser.sql_elements import SQLAttribute, Join, Condition

def parse_condition(condition):
    condition = condition.replace(" ", "")
    operator = list(filter(lambda x: x in condition, ["=", ">", "<", "<=", ">=" "!=", "<>"]))[0]
    condition = condition.split(operator)
    sql = list(filter(lambda x: "." in x, condition))[0]
    value = list(filter(lambda x: "." not in x, condition))[0]
    return Condition(SQLAttribute(sql.split(".")[0].lower(), sql.split(".")[1].lower()), operator, value)

def parse_pattern(uri_pattern):
    if uri_pattern is None:
            return None
    uri_pattern = uri_pattern[0] if isinstance(uri_pattern, list) else uri_pattern # !TODO This is quickfix for the book scenario
    uri_patterns = re.findall('@@(.*?)@@', uri_pattern)#.group(1).split(".") #!TODO This does not work when having more than one database access
    # replace |urlify with ""
    uri_patterns = [pattern.replace("|urlify", "") for pattern in uri_patterns]
    uri_patterns = [pattern.replace("|encode", "") for pattern in uri_patterns]
    return [SQLAttribute(table=pattern.split(".")[0].lower(), attribute=pattern.split(".")[1].lower()) for pattern in uri_patterns]