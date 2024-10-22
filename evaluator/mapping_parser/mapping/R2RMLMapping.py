from rdflib import Graph, URIRef
from typing import List

from evaluator.mapping_parser.classmap import ClassMap
from evaluator.mapping_parser.relation import Relation
from evaluator.mapping_parser.mapping.BaseMapping import BaseMapping

class R2RMLMapping(BaseMapping):
    def __init__(self, mapping_content, database, meta) -> None:
        super().__init__(mapping_content, database, meta)

    def parse_mapping(self, mapping_content):
        self.graph = Graph()
        print(mapping_content)
        self.graph.parse(mapping_content, format="turtle")
        self.classes = self.parse_classes()
        print(self.classes)
        # self.relations = self.parse_relations()
        # self.translation_tables = []
        # for class_ in self.get_classes():
        #     self.convert_subclass_to_relations(class_) 
    
    def get_context_elements(self, schema_element):
        if schema_element in self.classes:
            return self.get_classes_connected_to_class(schema_element)
        elif schema_element in self.relations:
            return self.get_relations_connected_to_relation(schema_element)
        else:
            raise Exception("Schema element not found in mapping")
    
    def get_classes_connected_to_class(self, class_: ClassMap):
        outgoing_classes = [relation.refersToClassMap for relation in self.relations if relation.belongsToClassMap == class_]
        ingoing_classes = [relation.belongsToClassMap for relation in self.relations if relation.refersToClassMap == class_]
        return list(set(outgoing_classes + ingoing_classes))
    
    def parse_classes(self) -> List[str]:
        classes = []
        properties = ["rr:class"]
        class_maps = self.query_properties("subjectMap", properties)
        print(class_maps)
        for class_map in class_maps:
                parent_classes = []
                if "d2rq:additionalClassDefinitionProperty" in class_map.keys():
                    if isinstance(class_map["d2rq:additionalClassDefinitionProperty"], list):
                        for el in class_map["d2rq:additionalClassDefinitionProperty"]:
                            parent_classes.append(self.parse_additionalClassDefinitionProperty(el))
                    else:
                        parent_classes = [self.parse_additionalClassDefinitionProperty(class_map["d2rq:additionalClassDefinitionProperty"])]
                classes.append(ClassMap(
                            #fix first three
                            prefix="base",
                            datastorage="database",
                            translate_with=None,
                            mapping_id=self.shorten_uri(class_map["mapping_id"]),
                            uriPattern=class_map["d2rq:uriPattern"] if "d2rq:uriPattern" in class_map.keys() else None,
                            class_uri=self.shorten_uri(class_map["d2rq:class"]) if "d2rq:class" in class_map.keys() else None,
                            #additionalClassDefinitionProperty=class_map["d2rq:additionalClassDefinitionProperty"] if "d2rq:additionalClassDefinitionProperty" in class_map.keys() else None,
                            join=class_map["d2rq:join"] if "d2rq:join" in class_map.keys() else None,
                            condition=class_map["d2rq:condition"] if "d2rq:condition" in class_map.keys() else None,
                            parent_classes=parent_classes,
                            #graph = self.graph
                            ))      
        return classes    

    def parse_relations(self):
        relations = []
        properties = ["d2rq:property", "d2rq:belongsToClassMap", "d2rq:refersToClassMap", "d2rq:join", "d2rq:column", "d2rq:sqlExpression"]
        property_bridges = self.query_properties("PropertyBridge", properties)
        for property_bridge in property_bridges:
            relations.append(Relation(
                    prefix="base",
                    mapping_id=self.shorten_uri(property_bridge["mapping_id"]),
                    property=self.shorten_uri(property_bridge["d2rq:property"]) if "d2rq:property" in property_bridge.keys() else None,
                    belongsToClassMap=self.__mapping_id_to_class(self.shorten_uri(property_bridge["d2rq:belongsToClassMap"])) if "d2rq:belongsToClassMap" in property_bridge.keys() else None,
                    refersToClassMap=self.__mapping_id_to_class(self.shorten_uri(property_bridge["d2rq:refersToClassMap"])) if "d2rq:refersToClassMap" in property_bridge.keys() else None,
                    sqlExpression=property_bridge["d2rq:sqlExpression"] if "d2rq:sqlExpression" in property_bridge.keys() else None,
                    join=property_bridge["d2rq:join"] if "d2rq:join" in property_bridge.keys() else None,
                    column=property_bridge["d2rq:column"] if "d2rq:column" in property_bridge.keys() else None,
                ))
        return relations

    def query_properties(self, id, properties):
        result = []
        query = f"""             
                SELECT DISTINCT ?mapping_id
                WHERE {{ ?mapping_id a ?o . }}
            """
        s = self.graph.query(query)
        print(s)
        ids = [obj[0].n3() for obj in self.graph.query(query)]
        query_properties = lambda uri, property: f"""             
            SELECT DISTINCT ?classes
            WHERE {{ {uri} {property} ?classes. }}
        """
        for id in ids:
            temp = {}
            for property in properties:
                res = self.graph.query(query_properties(id, property))
                if len(res) == 1:
                    for obj in res:
                        temp[property] = obj[0].n3().replace("'", "").replace('"', "")
                elif len(res) > 1:
                    objects_of_property = []
                    for obj in res:
                        objects_of_property.append(obj[0].n3().replace("'", "").replace('"', ""))
                    temp[property] = objects_of_property
            temp["mapping_id"] = id
            result.append(temp)
        return result