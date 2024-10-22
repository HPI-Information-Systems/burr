
from evaluator.mapping_parser.sql_elements import SQLAttribute, Join, Condition
def parse_condition(condition):
    condition = condition.replace(" ", "")
    operator = list(filter(lambda x: x in condition, ["=", ">", "<", "<=", ">=" "!="]))[0]
    condition = condition.split(operator)
    sql = list(filter(lambda x: "." in x, condition))[0]
    value = list(filter(lambda x: "." not in x, condition))[0]
    return Condition(SQLAttribute(sql.split(".")[0].lower(), sql.split(".")[1].lower()), operator, value)