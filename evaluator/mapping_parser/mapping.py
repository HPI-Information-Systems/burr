from rdflib import Graph
from typing import List

from evaluator.mapping_parser.sql_mapping import ClassMap, Relation

class Mapping:
    def __init__(self, mapping_file) -> None:
        self.classes: List[ClassMap]
        self.relations: List[Relation]
        self.__parse_mapping(mapping_file)

    def __parse_mapping(self, mapping_file):
        self.graph = Graph()
        self.graph.parse(mapping_file)
        self.classes = self.get_classes()
        self.relations = self.get_relations()
    
    def get_context_elements(self, schema_element):
        if schema_element in self.classes:
            return self.get_classes_connected_to_class(schema_element)
        elif schema_element in self.relations:
            fn = self.get_relations_connected_to_relation
        else:
            raise Exception("Schema element not found in mapping")
        return fn(schema_element)

    def __mapping_id_to_class(self, mapping_id):
        for class_ in self.classes:
            if class_.mapping_id == mapping_id:
                return class_
        return None
    
    def get_classes_connected_to_class(self, class_: ClassMap):
        outgoing_classes = [self.__mapping_id_to_class(relation.refersToClassMap) for relation in self.relations if relation.belongsToClassMap == class_.mapping_id]
        ingoing_classes = [self.__mapping_id_to_class(relation.belongsToClassMap) for relation in self.relations if relation.refersToClassMap == class_.mapping_id]
        return list(set(outgoing_classes + ingoing_classes))

    def get_relations_connected_to_relation(self, relation: Relation):
        def mapping_id_to_relation(mapping_id):
            for rel in self.relations:
                if rel.mapping_id == mapping_id:
                    return rel
            return None
        #für 
        #outgoing_class = self.__mapping_id_to_class(relation.belongsToClassMap)
        #ingoing_class = self.__mapping_id_to_class(relation.refersToClassMap)
        relations = list(set(self.relations) - set([relation]))
        relations_of_outgoing_class = [mapping_id_to_relation(rel.mapping_id) for rel in relations if rel.belongsToClassMap == relation.belongsToClassMap or rel.refersToClassMap == relation.belongsToClassMap]
        relations_of_ingoing_class = [mapping_id_to_relation(rel.mapping_id) for rel in relations if rel.belongsToClassMap == relation.refersToClassMap or rel.refersToClassMap == relation.refersToClassMap]
        print("outgoing", relations_of_outgoing_class)
        print("ingoing", relations_of_ingoing_class)
        # outgoing_relations = [mapping_id_to_relation(relation.refersToClassMap) for relation in self.relations if relation.belongsToClassMap == relation.mapping_id]
        # ingoing_relations = [mapping_id_to_relation(relation.belongsToClassMap) for relation in self.relations if relation.refersToClassMap == relation.mapping_id]
        return list(set(relations_of_outgoing_class + relations_of_ingoing_class))
    
    def get_classes(self) -> List[str]:
        classes = []
        properties = ["d2rq:uriPattern", "d2rq:class", "d2rq:additionalClassDefinitionProperty", "d2rq:condition"]
        class_maps = self.query_properties("ClassMap", properties)
        for class_map in class_maps:
                classes.append(
                        ClassMap(
                            mapping_id=class_map["mapping_id"],
                            uriPattern=class_map["d2rq:uriPattern"] if "d2rq:uriPattern" in class_map.keys() else None,
                            class_uri=class_map["d2rq:class"] if "d2rq:class" in class_map.keys() else None,
                            additionalClassDefinitionProperty=class_map["d2rq:additionalClassDefinitionProperty"] if "d2rq:additionalClassDefinitionProperty" in class_map.keys() else None,
                            join=class_map["d2rq:join"] if "d2rq:join" in class_map.keys() else None,
                            condition=class_map["d2rq:condition"] if "d2rq:condition" in class_map.keys() else None,
                            graph = self.graph
                            ),
                        )
        return classes
    
    def parse_additionalClassDefinitionProperty(self, uri):
        query = f"""             
            SELECT DISTINCT ?class
            WHERE {{ {uri} d2rq:propertyValue ?class. }}
        """
        res = [obj[0].n3() for obj in self.graph.query(query)]
        return res if len(res)>1 else res[0]

    def get_relations(self):
        relations = []
        properties = ["d2rq:property", "d2rq:belongsToClassMap", "d2rq:refersToClassMap", "d2rq:join", "d2rq:column"]
        property_bridges = self.query_properties("PropertyBridge", properties)
        for property_bridge in property_bridges:
            relations.append(
                Relation(
                    mapping_id=property_bridge["mapping_id"],
                    property=property_bridge["d2rq:property"] if "d2rq:property" in property_bridge.keys() else None,
                    belongsToClassMap=property_bridge["d2rq:belongsToClassMap"] if "d2rq:belongsToClassMap" in property_bridge.keys() else None,
                    refersToClassMap=property_bridge["d2rq:refersToClassMap"] if "d2rq:refersToClassMap" in property_bridge.keys() else None,
                    join=property_bridge["d2rq:join"] if "d2rq:join" in property_bridge.keys() else None,
                    column=property_bridge["d2rq:column"] if "d2rq:column" in property_bridge.keys() else None,
                )
            )
        return relations


    def query_properties(self, id, properties):
        result = []
        query = f"""             
            SELECT DISTINCT ?mapping_id
            WHERE {{ ?mapping_id a d2rq:{id}. }}
        """

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
    
    def get_attribute_from_mapping(self, attribute, table):
        for class_ in self.classes:
            if class_.sql_uri_pattern.table == table and class_.sql_uri_pattern.attribute == attribute:
                return class_
        return None