from rdflib import Graph, Namespace, RDF
from typing import List

from evaluator.mapping_parser.classmap import ClassMap
from evaluator.mapping_parser.relation import Relation
from evaluator.mapping_parser.mapping.BaseMapping import BaseMapping

RR = Namespace("http://www.w3.org/ns/r2rml#")
EX = Namespace("http://example.com/ns#")
class R2RMLMapping(BaseMapping):
    def __init__(self, mapping_content, database, meta) -> None:
        super().__init__(mapping_content, database, meta)

    def parse_mapping(self, mapping_content):
        self.graph = Graph()
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
        for triples_map in self.graph.subjects(RDF.type, RR.TriplesMap):
            logicalTable = self.graph.value(subject=triples_map, predicate=RR.logicalTable)
            subject_map = self.graph.value(subject=triples_map, predicate=RR.subjectMap)
            template = self.graph.value(subject=subject_map, predicate=RR.template)
            class_uri = self.shorten_uri(str(self.graph.value(subject=subject_map, predicate=RR["class"])))
            table_name = self.graph.value(subject=logicalTable, predicate=RR.tableName)
            uri_pattern = template.replace("{", f"@@{table_name}.").replace("}", "@@")
            classes.append(ClassMap(
                prefix="base",
                datastorage="database",
                translate_with=None,
                mapping_id=str(triples_map),
                uriPattern=uri_pattern,
                class_uri=class_uri,
                join=None,
                condition=None,
                parent_classes=None
            )) 
        return classes    

    def get_class_uri_for_mapping_id(self, mapping_id):
        for triples_map in self.graph.subjects(RDF.type, RR.TriplesMap):
            subject_map = self.graph.value(subject=triples_map, predicate=RR.subjectMap)
            class_uri = self.shorten_uri(str(self.graph.value(subject=subject_map, predicate=RR["class"])))
            if str(triples_map) == mapping_id:
                return class_uri

    def parse_relations(self):
        relations = []
        for triples_map in self.graph.subjects(RDF.type, RR.TriplesMap):
            mapping_id = self.shorten_uri(triples_map)
            logicalTable = self.graph.value(subject=triples_map, predicate=RR.logicalTable)
            subject_map = self.graph.value(subject=triples_map, predicate=RR.subjectMap)
            class_uri = self.shorten_uri(self.graph.value(subject=subject_map, predicate=RR["class"]))
            table_name = self.graph.value(subject=logicalTable, predicate=RR.tableName)
            for pred_obj_map in self.graph.objects(subject=triples_map, predicate=RR.predicateObjectMap):
                predicate = self.graph.value(subject=pred_obj_map, predicate=RR.predicate)
                property = self.shorten_uri(predicate) if predicate else None
                belongs_to_class_map = self.shorten_uri(class_uri)
                object_map = self.graph.value(subject=pred_obj_map, predicate=RR.objectMap)
                column = self.graph.value(subject=object_map, predicate=RR.column)
                if column:
                    column = f"{table_name}.{column}" if column else None
                else:
                    column = None
                    parentTriplesMap = self.graph.objects(subject=object_map, predicate=RR.parentTriplesMap)
                    joinCondition = self.graph.objects(subject=object_map, predicate=RR.joinCondition)
                    if parentTriplesMap:
                        refers_to_class_map = self.shorten_uri(self.get_class_uri_for_mapping_id(str(parentTriplesMap)))
                    if joinCondition:
                        join = []
                        for join in joinCondition:
                            parent = self.graph.value(subject=join, predicate=RR.parent)
                            child = self.graph.value(subject=join, predicate=RR.child)
                            join.append(f"{table_name}.{parent}={table_name}.{child}")

            relations.append(Relation(
                    prefix="base",
                    mapping_id=mapping_id, #not unique
                    property=property,
                    belongsToClassMap=belongs_to_class_map,
                    refersToClassMap=refers_to_class_map,
                    #sqlExpression=#property_bridge["d2rq:sqlExpression"] if "d2rq:sqlExpression" in property_bridge.keys() else None,
                    join=join,
                    column=column
                ))
        return relations