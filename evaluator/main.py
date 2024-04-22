from evaluator.database.sql_engine.sql import SQLEngine

engine = SQLEngine("test_database_naive", "public") #schem selection does not work I guess
print(engine)

