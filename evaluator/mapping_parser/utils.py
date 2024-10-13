
from evaluator.mapping_parser.sql_elements import SQLAttribute, Join, Condition
def parse_condition(condition):
    print("condition", condition)
    condition = condition.replace(" ", "")
    print("condition", condition)
    operator = list(filter(lambda x: x in condition, ["=", ">", "<", "<=", ">=" "!="]))[0]
    condition = condition.split(operator)
    print("condition", condition)
    sql = list(filter(lambda x: "." in x, condition))[0]
    value = list(filter(lambda x: "." not in x, condition))[0]
    print("value", value)
    print(condition)
    return Condition(SQLAttribute(sql.split(".")[0].lower(), sql.split(".")[1].lower()), operator, value)