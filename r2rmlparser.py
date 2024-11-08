from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

# Define R2RML and custom namespaces
RR = Namespace("http://www.w3.org/ns/r2rml#")
EX = Namespace("http://example.org/")
def shorten_uri(g, uri):
        uri = str(URIRef(uri)).replace("<", "").replace(">", "").replace(" ", "")
        for prefix, namespace in g.namespaces():
            print(namespace)
            if str(uri).startswith(namespace):
                return str(uri)[len(namespace):]
        return uri
def extract_concepts(r2rml_file):
    g = Graph()
    g.parse(r2rml_file, format="ttl")

    concepts = []

    for triples_map in g.subjects(RDF.type, RR.TriplesMap):
        concept = {}
        concept['mapping_id'] = str(triples_map)

        subject_map = g.value(subject=triples_map, predicate=RR.subjectMap)

        if subject_map:
            uri_pattern = g.value(subject=subject_map, predicate=RR.template)
            concept['uriPattern'] = str(uri_pattern) if uri_pattern else None

            class_uri = g.value(subject=subject_map, predicate=RR["class"])
            concept['class_uri'] = shorten_uri(g,str(class_uri)) if class_uri else None
            print("Class URI", concept['class_uri'])

        class_uri = g.value(subject=triples_map, predicate=RR["class"])
        concept['class_uri'] = shorten_uri(g,str(class_uri)) if class_uri else None

        joins = []
        for join in g.objects(subject=triples_map, predicate=RR.joinCondition):
            join_details = {
                'parent': str(g.value(subject=join, predicate=RR.parent)),
                'child': str(g.value(subject=join, predicate=RR.child))
            }
            joins.append(join_details)
        concept['used_joins'] = joins if joins else None

        # This part assumes any custom condition is provided as part of a `rr:logicalTable` or `rr:sqlQuery`
        conditions = []
        logical_table = g.value(subject=triples_map, predicate=RR.logicalTable)
        print("Logical table", logical_table)
        if logical_table:
            sql_query = g.value(subject=logical_table, predicate=RR.sqlQuery)
            if sql_query:
                print("ds", sql_query)
                conditions.append(str(sql_query))
            table_name = g.value(subject=logical_table, predicate=RR.tableName)
            print("Table name", table_name)

        concept['used_conditions'] = conditions if conditions else None

        concepts.append(concept)

    return concepts


def extract_properties_with_local_ids(r2rml_file):
    g = Graph()
    g.parse(r2rml_file, format="ttl")

    properties = []

    for triples_map in g.subjects(RDF.type, RR.TriplesMap):
        mapping_id = shorten_uri(triples_map)

        for pred_obj_map in g.objects(subject=triples_map, predicate=RR.predicateObjectMap):
            property_map = {}
            property_map['prefix'] = "base"
            property_map['mapping_id'] = mapping_id

            predicate = g.value(subject=pred_obj_map, predicate=RR.predicate)
            property_map['property'] = shorten_uri(predicate) if predicate else None

            object_map = g.value(subject=pred_obj_map, predicate=RR.objectMap)
            if object_map:
                belongs_to_class_map = g.value(subject=object_map, predicate=RR.parentTriplesMap)
                property_map['belongsToClassMap'] = shorten_uri(belongs_to_class_map) if belongs_to_class_map else None

                refers_to_class_map = g.value(subject=object_map, predicate=RR.refersToClassMap)
                property_map['refersToClassMap'] = shorten_uri(refers_to_class_map) if refers_to_class_map else None

                sql_expression = g.value(subject=object_map, predicate=RR.sqlQuery)
                property_map['sqlExpression'] = str(sql_expression) if sql_expression else None

                join = g.value(subject=object_map, predicate=RR.joinCondition)
                property_map['join'] = str(join) if join else None

                column = g.value(subject=object_map, predicate=RR.column)
                property_map['column'] = str(column) if column else None

            properties.append(property_map)

    return properties

# Usage
r2rml_file = "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/r2rmloutput.ttl"  # Replace with your R2RML file path
r2rml_file = "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/r2rml.ttl"
concepts = extract_concepts(r2rml_file)
for concept in concepts:
    print(concept)
