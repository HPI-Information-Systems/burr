import os
import json

from evaluator.mapping_parser.classmap import ClassMap as MappingParserClassMap
from evaluator.mapping_parser.relation import Relation
from evaluator.utils.get_jinja_env import get_jinja_env

def parse_mapping_file(directory):
    meta_file = os.path.join(directory, "meta.json")
    with open(meta_file, 'r') as f:
        meta = json.load(f)
        prefixes = meta["prefixes"]
    with open("Output.ttl", "w", encoding="utf-8") as text_file:
        text_file.write(build_meta_data(prefixes))
        for file in os.listdir(directory):
            if file.endswith(".json") and file != "meta.json":
                with open(os.path.join(directory, file), 'r') as f:
                    data = json.load(f)
                    for _cls in data["classes"]:
                        text_file.write(parse_class_entry(_cls))
                    for data_prop in data["data_properties"]:
                        text_file.write(parse_property_bridge_entry(data_prop))
                    for obj_prop in data["object_properties"]:
                        text_file.write(parse_property_bridge_entry(obj_prop))
                    for translation_table in data["translation_tables"] if "translation_tables" in data else []:
                        text_file.write(parse_translation_table(translation_table))

def build_meta_data(prefixes): return get_jinja_env().get_template('meta.j2').render(prefixes=prefixes, database="mondial", database_username="lukaslaskowski") 

def parse_translation_table(table): return get_jinja_env().get_template('translationtable.j2').render(mapping_name = table["name"], translations=table["translations"])

def parse_class_entry(entry):
    mapping_name = entry["name"] if "name" in entry else entry["class"]
    cls_ = entry["class"]
    uri_pattern = entry["id"].lower()
    prefix = entry["prefix"].lower()
    conditions = entry["condition"] if "condition" in entry else None
    joins = entry["join"] if "join" in entry else None
    translate_with = entry["translateWith"] if "translateWith" in entry else None
    parent_class = entry["subclassOf"][0] if "subclassOf" in entry else None
    parent_class=None
    datastorage = "database"
    return MappingParserClassMap(mapping_id=mapping_name, prefix=prefix, class_uri=cls_, uriPattern=uri_pattern, condition=conditions, join=joins, datastorage=datastorage, parent_classes=parent_class, translate_with=translate_with).get_d2rq_mapping()

def parse_property_bridge_entry(entry):
    refers_to_class_map = None
    if "refersToClass" in entry or "refersToClassMap" in entry:
        refers_to_class_map = entry["refersToClass"] if "refersToClass" in entry else entry["refersToClassMap"]
    belongs_to_class_map = entry["belongsToClass"] if "belongsToClass" in entry else entry["belongsToClassMap"]
    mapping_name = f"{entry['property']}_{belongs_to_class_map}_{refers_to_class_map}"
    property = entry["property"]
    if property in ["longitude", "latitude"]:
        return ""
    joins = entry["join"] if "join" in entry else None
    conditions = entry["condition"] if "condition" in entry else None
    column = entry["column"].lower() if "column" in entry else None
    datatype = entry["datatype"] if "datatype" in entry else None
    inverse_of = entry["inverseOf"] if "inverseOf" in entry else None
    translate_with = entry["translateWith"] if "translateWith" in entry else None

    return Relation(prefix="mondial", mapping_id=mapping_name, property=property, belongsToClassMap=belongs_to_class_map, refersToClassMap=refers_to_class_map, join=joins, condition=conditions, column=column, datatype=datatype, inverse_of=inverse_of, translate_with=translate_with).get_d2rq_mapping()

parse_mapping_file("/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/real-world/mondial/mapping")