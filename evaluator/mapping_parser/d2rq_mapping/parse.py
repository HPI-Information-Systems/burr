import os
import json
import os
from rdflib import Graph

from evaluator.mapping_parser.classmap import ClassMap
from evaluator.mapping_parser.relation import Relation
from evaluator.utils.get_jinja_env import get_jinja_env


class JsonMappingParser:
    def __init__(self, mapping_file) -> None:
        self.classes = []
        self.relations = []
        self.parse_mapping_file(mapping_file)


    def parse_mapping_file(self, directory, database):
        meta_file = os.path.join(directory, "meta.json")
        meta_file = meta_file if os.path.exists(meta_file) else './evaluator/mapping_parser/d2rq_mapping/base_meta.json'
        with open(meta_file, 'r') as f:
            meta = json.load(f)
        output = ""
        for file in [directory] if os.path.isfile(directory) else os.listdir(directory):
            if file.endswith(".json") and file != "meta.json":
                with open(os.path.join(directory, file), 'r') as f:
                    data = json.load(f)
                    output += self.create_ttl_string(data, meta, database)
        return output

    def write_to_file(self, output, output_file):
        graph = Graph().parse(data=output, format="turtle")
        graph.serialize(destination=output_file, format="turtle")
    
                
    def create_ttl_string(self, data, meta, database):
        output = ""
        prefixes = meta["prefixes"]
        output+= self.build_meta_data(prefixes, database)
        for _cls in data["classes"]:
            cls_map = self.parse_class_entry(_cls)
            for cls_ in cls_map:
                output += cls_
        for data_prop in data["data_properties"]:
            output += self.parse_property_bridge_entry(data_prop, meta["relation_prefix"])
        for obj_prop in data["object_properties"]:
            output += self.parse_property_bridge_entry(obj_prop, meta["relation_prefix"])
        for translation_table in data["translation_tables"] if "translation_tables" in data else []:
            output += self.parse_translation_table(translation_table)
        return output

    def build_meta_data(self, prefixes, database): return get_jinja_env().get_template('meta.j2').render(prefixes=prefixes, database=database, database_username="lukaslaskowski") 

    def parse_translation_table(self, table): return get_jinja_env().get_template('translationtable.j2').render(mapping_name = table["name"], translations=table["translations"])

    def parse_class_entry(self, entry):
        mapping_name = entry["name"] if "name" in entry else entry["class"]
        cls_ = entry["class"]
        uri_pattern = entry["id"].lower()
        prefix = entry["prefix"].lower() if "prefix" in entry else "base"
        conditions = entry["condition"] if "condition" in entry else None
        joins = entry["join"] if "join" in entry else None
        translate_with = entry["translateWith"] if "translateWith" in entry else None
        parent_classes = entry["subclassOf"] if "subclassOf" in entry else None
        print(parent_classes)
        datastorage = "database"
        return ClassMap(mapping_id=mapping_name, prefix=prefix, class_uri=cls_, uriPattern=uri_pattern, condition=conditions, join=joins, datastorage=datastorage, parent_classes=parent_classes, translate_with=translate_with).get_d2rq_mapping()

    def parse_property_bridge_entry(self, entry, prefix):
        refers_to_class_map = None
        if "refersToClass" in entry or "refersToClassMap" in entry:
            refers_to_class_map = entry["refersToClass"] if "refersToClass" in entry else entry["refersToClassMap"]
        belongs_to_class_map = entry["belongsToClass"] if "belongsToClass" in entry else entry["belongsToClassMap"]
        index = entry["index"] if "index" in entry else None
        mapping_name = f"{entry['property']}_{belongs_to_class_map}_{refers_to_class_map}" + (f"_{index}" if index else "")
        property = entry["property"]
        if property in ["longitude", "latitude"]:
            return ""
        joins = entry["join"] if "join" in entry else None
        conditions = entry["condition"] if "condition" in entry else None
        column = entry["column"].lower() if "column" in entry else None
        datatype = entry["datatype"] if "datatype" in entry else None
        inverse_of = entry["inverseOf"] if "inverseOf" in entry else None
        sqlExpression = entry["sqlExpression"] if "sqlExpression" in entry else None
        translate_with = entry["translateWith"] if "translateWith" in entry else None
        constant_value = entry["constantValue"] if "constantValue" in entry else None
        return Relation(prefix=prefix, mapping_id=mapping_name, property=property, constantValue=constant_value,belongsToClassMap=belongs_to_class_map, refersToClassMap=refers_to_class_map, join=joins, condition=conditions, column=column, datatype=datatype, inverse_of=inverse_of, translate_with=translate_with, sqlExpression=sqlExpression).get_d2rq_mapping()

# parse_mapping_file("/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/real-world/mondial/mappings", "sap", "sap")
# parse_mapping_file("/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/real-world/mondial/mappings", "mondialfk", "mondialtest")
parse_mapping_file("/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/train_data/denormalized/boolean_relation/beverages/mapping.json", "denormalized__boolean_relation__beverages", "denormalized__boolean_relation__beverages")
# path = "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto"
# for file in os.listdir(path):
#     #print(os.path.splitext(os.path.basename(os.path.join(path, file)))[0])
#     # if file == "basic__attributes__person.json" and not file == "mappings":
#     #     print("Ha")
#     parse_mapping_file(os.path.join(path, file), database=os.path.splitext(os.path.basename(os.path.join(path,file)))[0], output_name=os.path.splitext(os.path.basename(os.path.join(path, file)))[0])

# base_path = "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/train_data"

# for folder in os.listdir(base_path):
#     base_scenarios = os.listdir(os.path.join(base_path, folder))
#     if folder == "reviewer_1_hierarchy" or os.path.isfile(os.path.join(base_path, folder)):
#         continue
#     for scenario in base_scenarios:
#         for sub_scenario in os.listdir(os.path.join(base_path, folder, scenario)):
#             parse_mapping_file(os.path.join(base_path, folder, scenario, sub_scenario, "mapping.json"), database=f"{folder}__{scenario}__{sub_scenario}", output_name=f"{folder}__{scenario}__{sub_scenario}")
    