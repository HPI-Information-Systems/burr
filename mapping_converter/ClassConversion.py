from dataclasses import dataclass

@dataclass
class ClassMap:
    class_map_name: str
    id: str
    uri_pattern: str
    class_name: str

class ClassConversion:
    def __init__(self, class_properties):
        self.class_properties = class_properties
    
    def convert(self, dict):
        self.class_map = ClassMap()
        if "name" in dict:
            class_map_name = dict["name"]

    