from rdflib import Graph, Namespace, RDF
from typing import List

from evaluator.mapping_parser.classmap import ClassMap
from evaluator.mapping_parser.relation import Relation
from evaluator.mapping_parser.mapping.BaseMapping import BaseMapping
from evaluator.mapping_parser.mapping.D2RQMapping import D2RQMapping
RR = Namespace("http://www.w3.org/ns/r2rml#")
EX = Namespace("http://example.com/ns#")
class R2RMLMapping(BaseMapping):
    def __init__(self, mapping_content, database, meta) -> None:
        super().__init__(mapping_content, database, meta)

    def parse_mapping(self, mapping_content):
        self.graph = Graph()
        print("mappingcontent",mapping_content)
        self.graph.parse(data=mapping_content, format="ttl")
        self.classes = self.parse_classes()
        print(self.classes)
        self.relations = self.parse_relations()
        self.translation_tables = []
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
        triples = self.graph.subjects(RDF.type, RR.TriplesMap)
        for idx, triples_map in enumerate(triples):
            print("triples_map", triples_map)
            mapping_id = f"{idx}{str(triples_map).split('/')[-1].replace('#', '')}_CLS"
            logicalTable = self.graph.value(subject=triples_map, predicate=RR.logicalTable)
            subject_map = self.graph.value(subject=triples_map, predicate=RR.subjectMap)
            if self.graph.value(subject=subject_map, predicate=RR["class"]) is None:
                print("WARNING - Class not found for triples map: ", triples_map, " - skipping")
                continue
            template = self.graph.value(subject=subject_map, predicate=RR.template)
            class_uri = self.shorten_uri(str(self.graph.value(subject=subject_map, predicate=RR["class"])))
            table_name = self.graph.value(subject=logicalTable, predicate=RR.tableName)
            uri_pattern = template.replace("{", f"@@{table_name}.").replace("}", "@@")
            print("class", class_uri)
            print(str(self.graph.value(subject=subject_map, predicate=RR["class"])))
            classes.append(ClassMap(
                prefix="base",
                datastorage="database",
                translate_with=None,
                mapping_id=mapping_id,
                uriPattern=uri_pattern,
                class_uri=class_uri,
                join=None,
                condition=None,
                parent_classes=None,
                bNodeIdColumns=None
            )) 
        return classes
    
    def get_attributes(self):
        return list(filter(lambda rel: rel.refersToClassMap is None, self.relations))
    
    def get_relations(self):
        return list(filter(lambda rel: rel.refersToClassMap is not None, self.relations))
        
    def to_D2RQ_Mapping(self):
        #print(self.create_ttl_string(self.database))
        x = self.create_ttl_string(self.database)
        print(x)
        return D2RQMapping(x, self.database, self.meta)
    
    def get_class_uri_for_mapping_id(self, mapping_id):
        for triples_map in self.graph.subjects(RDF.type, RR.TriplesMap):
            subject_map = self.graph.value(subject=triples_map, predicate=RR.subjectMap)
            class_uri = self.shorten_uri(str(self.graph.value(subject=subject_map, predicate=RR["class"])))
            if str(triples_map) == mapping_id:
                return class_uri
    
    def get_mapping_id_from_class_uri(self, class_uri):    
        for cls in self.classes:
            if cls.class_uri == class_uri:
                return cls.mapping_id
    def match_class_uri_by_uri(self, uri):
        for cls in self.classes:
            if cls.uriPattern == uri:
                return cls
        return None

    def parse_relations(self):
        relations = []
        triples = self.graph.subjects(RDF.type, RR.TriplesMap)
        for triples_map in triples:
            logicalTable = self.graph.value(subject=triples_map, predicate=RR.logicalTable)
            subject_map = self.graph.value(subject=triples_map, predicate=RR.subjectMap)
            table_name = self.graph.value(subject=logicalTable, predicate=RR.tableName)
            if self.graph.value(subject=subject_map, predicate=RR["class"]) is None:
                print("WARNING - Class not found for triples map: ", triples_map, " - Trying to match by URI")
                template = self.graph.value(subject=subject_map, predicate=RR.template)
                uri_pattern = template.replace("{", f"@@{table_name}.").replace("}", "@@")
                class_uri = self.match_class_uri_by_uri(uri_pattern)
                if class_uri is None:
                    print("WARNING - Class not found for triples map: ", triples_map, " - skipping")
                    continue
            else:
                class_uri = self.shorten_uri(self.graph.value(subject=subject_map, predicate=RR["class"]))
            for idx, pred_obj_map in enumerate(self.graph.objects(subject=triples_map, predicate=RR.predicateObjectMap)):
                mapping_id = f"{idx}{str(triples_map).split('/')[-1].replace('#', '')}_REL"
                predicate = self.graph.value(subject=pred_obj_map, predicate=RR.predicate)
                property = self.shorten_uri(predicate) if predicate else None
                belongs_to_class_map = self.get_mapping_id_from_class_uri(self.shorten_uri(class_uri))
                object_map = self.graph.value(subject=pred_obj_map, predicate=RR.objectMap)
                column = self.graph.value(subject=object_map, predicate=RR.column)
                if column:
                    column = f"{table_name}.{column}" if column else None
                else:
                    column = None
                parentTriplesMap = self.graph.value(subject=object_map, predicate=RR.parentTriplesMap)
                joinCondition = self.graph.objects(subject=object_map, predicate=RR.joinCondition)
                
                refers_to_class_map = self.get_mapping_id_from_class_uri(self.shorten_uri(self.get_class_uri_for_mapping_id(str(parentTriplesMap)))) if parentTriplesMap else None
                if joinCondition:
                    join = []
                    for j in joinCondition:
                        parent = self.graph.value(subject=j, predicate=RR.parent)
                        child = self.graph.value(subject=j, predicate=RR.child)
                        join.append(f"{table_name}.{parent}={table_name}.{child}")
                else:   
                    join = None

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