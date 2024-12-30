import json
import os

folder_to_jsons = "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/real-world/mondial/mappings/"

attributes = []
#{"name": NAME, "belongsToClass": , "belongsToClassMap"}

for file in os.listdir(folder_to_jsons):
    if file == "meta.json":
        continue
    with open(folder_to_jsons+file) as json_file:
        data = json.load(json_file)
    for el in data["object_properties"]:
        print(el)
        attributes.append(el)        #

print(len(attributes))
    