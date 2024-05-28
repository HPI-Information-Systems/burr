#from evaluator.database.sql_engine.sql import SQLEngine
#from evaluator.validator.base_validator import get_validator
#from evaluator.mapping_parser.mapping import Mapping
from evaluator.mapping_parser.mapping import Mapping
from evaluator.metrics.mapping_based import MappingBasedPrecision, MappingBasedRecall
from evaluator.metrics.taxonomy_mapping_based import TaxonomyMappingBasedPrecision, TaxonomyMappingBasedRecall
from evaluator.metrics.metric import F1Score
#engine = SQLEngine("test_database_naive", "public") #schem selection does not work I guess
ontology = None

#mapping_file ="./mapping_.ttl"
#mapping_file ="/Users/lukaslaskowski/Downloads/RODI_benchmark/data/cmt_mixed/mapping.ttl"
mapping_1 = Mapping("./mapping_test_2.ttl")
mapping_2 = Mapping("./mapping_test_1.ttl")

precision = MappingBasedPrecision()(mapping_1, mapping_2)
recall = MappingBasedRecall()(mapping_1, mapping_2)
f1 = F1Score()(precision, recall)
tp = TaxonomyMappingBasedPrecision()(mapping_1, mapping_2)
tr = TaxonomyMappingBasedRecall()(mapping_1, mapping_2)
tf1 = F1Score()(tp, tr)

print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1: {f1}")
print(f"Taxonomy Precision: {tp}")
print(f"Taxonomy Recall: {tr}")
print(f"Taxonomy F1: {tf1}")

print("REMINDER: I have not considered subclasses yet. How should they be incorporated?")
print("REMINDER: I have not looked at attributes yet.")
# for table in engine.get_tables():
#     for attribute in engine.get_attributes(table):
#         context = engine.get_context(engine.get_schema_element_type(attribute, table), attribute)
#         validator = get_validator(context)(ontology, context)
#         #all necessary parts covered by ontology?
#         validator.validate(attribute, table, context)
#         #das ist dann eine nm tabelle oder 
        
#         #check if part of nm-table
#         #check if (part of) primary key
#         #parse and compare to ontology
#         pass
#     for foreign_key in engine.tables[table].foreign_keys:
#         pass

# #Welche Schemaelemente habe ich?
# #Attribute, FK (n1 attributes), PK, nm tables, 

# engine.get_context()
# # wir haben das geparste mapping
# # wir haben das geparste grountruth mapping
# # wir haben das geparste datenbankschema

# # wir iterieren über die geparste grountruth mapping
# # schaue die beziehung zur datenbank nach. Evaluieren den schema type
