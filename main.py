#from evaluator.database.sql_engine.sql import SQLEngine
#from evaluator.validator.base_validator import get_validator
#from evaluator.mapping_parser.mapping import Mapping
from evaluator.mapping_parser.mapping import Mapping
from evaluator.metrics.mapping_based import MappingBasedPrecision, MappingBasedRecall
from evaluator.metrics.taxonomy_mapping_based import TaxonomyMappingBasedPrecision, TaxonomyMappingBasedRecall
from evaluator.metrics.metric import F1Score
#engine = SQLEngine("test_database_naive", "public") #schem selection does not work I guess
ontology = None

# mapping_file ="./mapping.ttl"
#mapping_file ="/Users/lukaslaskowski/Downloads/RODI_benchmark/data/cmt_mixed/mapping.ttl"
mapping_file_2 ="/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/mondial.ttl"
mapping_file_1 ="/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/mondial_rdb2onto.ttl"
mapping_file_1 ="/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/groundtruths/sap_groundtruth.ttl"
mapping_file_2 ="/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/groundtruths/sap_rdb2onto.ttl"





print("TAKING care of goldstandard")
mapping_1 = Mapping(mapping_file_1)
print("TAKING care of learned")
mapping_2 = Mapping(mapping_file_2)

precision = MappingBasedPrecision()(mapping_1, mapping_2)
recall = MappingBasedRecall()(mapping_1, mapping_2)
print(precision)
print(recall)
f1 = F1Score()(precision, recall)
tr = TaxonomyMappingBasedRecall().score(mapping_2, mapping_1)
tp = TaxonomyMappingBasedPrecision()(mapping_2, mapping_1)
tf1 = F1Score()(tp, tr)

print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1: {f1}")
print(f"Taxonomy Precision: {tp}")
print(f"Taxonomy Recall: {tr}")
print(f"Taxonomy F1: {tf1}")

print("REMINDER: I do not consider subclasses because they do not have a mapping but are indirectly covered by")
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
