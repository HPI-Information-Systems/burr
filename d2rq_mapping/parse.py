import os
import json

from d2rq_mapping.ClassMap import ClassMap
from d2rq_mapping.PropertyBridge import PropertyBridge

def parse_mapping_file(directory):
    meta_file = os.path.join(directory, "meta.json")
    with open(meta_file, 'r') as f:
        meta = json.load(f)
        base_uri = meta["base_uri"]
        namespace = meta["namespace"]
    meta = build_meta_data(base_uri, namespace)
    for file in os.listdir(directory):
        if file.endswith(".json") and file != "meta.json":
            with open(os.path.join(directory, file), 'r') as f:
                data = json.load(f)
                for _cls in data["classes"]:
                    parse_class_entry(_cls)
                for data_prop in data["data_properties"]:
                    parse_property_bridge_entry(data_prop)
                for obj_prop in data["object_properties"]:
                    parse_property_bridge_entry(obj_prop)
                #todo parse translations

def build_meta_data(base_uri, namespace):
    pass

def parse_class_entry(entry):
    mapping_name = entry["name"] if "name" in entry else entry["Class"]
    cls_ = entry["Class"]
    uri_pattern = entry["id"]
    prefix = entry["prefix"]
    conditions = entry["condition"] if "condition" in entry else None
    datastorage = "database"
    mapping = ClassMap(prefix=prefix, class_name=cls_, mapping_name=mapping_name, uri_pattern=uri_pattern, condition=conditions, datastorage=datastorage).get_d2rq_mapping()
    return mapping

def parse_property_bridge_entry(entry):
    if "refersToClass" in entry or "refersToClassMap" in entry:
        refers_to_class_map = entry["refersToClass"] if "refersToClass" in entry else entry["refersToClassMap"]
    belongs_to_class_map = entry["belongsToClass"] if "belongsToClass" in entry else entry["belongsToClassMap"]
    mapping_name = f"{entry["property"]}_{refers_to_class_map}_{belongs_to_class_map}"
    property = entry["property"],
    joins = entry["join"] if "join" in entry else None
    conditions = entry["condition"] if "condition" in entry else None
    column = entry["column"] if "column" in entry else None
    datatype = entry["datatype"] if "datatype" in entry else None
    inverse_of = entry["inverseOf"] if "inverseOf" in entry else None
    prefix = entry["prefix"]
    return PropertyBridge(prefix=prefix, belongsToClassMap=belongs_to_class_map, property=property, mapping_name=mapping_name, refersToClassMap=refers_to_class_map, joins=joins, conditions=conditions, column=column, datatype=datatype, inverseOf=inverse_of).get_d2rq_mapping()