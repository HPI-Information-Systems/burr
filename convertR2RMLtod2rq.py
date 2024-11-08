import sys
import getopt
import rdflib
from rdflib import URIRef, BNode, RDF, Literal
from rdflib.namespace import Namespace

# Namespaces
R2RML = Namespace("http://www.w3.org/ns/r2rml#")
D2RQ = Namespace("http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#")

# Initialize graphs
r2rml_graph = rdflib.Graph()
d2rq_graph = rdflib.Graph()

d2rq_graph.bind("d2rq", D2RQ)

inputfile = ''
outputfile = ''

def main(argv):
    global inputfile, outputfile
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('python3 R2RML_to_D2RQ.py -i <R2RML_mapDoc> -o <D2RQ_mapDoc>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python3 R2RML_to_D2RQ.py -i <R2RML_mapDoc> -o <D2RQ_mapDoc>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

def convert_logical_table(subject):
    for a, b, logical_table in r2rml_graph.triples((subject, R2RML.logicalTable, None)):
        #print(a,b,logical_table)
        d2rq_graph.add((subject, RDF.type, D2RQ.ClassMap))
        d2rq_graph.add((subject, D2RQ.uriPattern, Literal(f"@@{logical_table}@@")))

def convert_subject_map(subject):
    for a, b, subject_map in r2rml_graph.triples((subject, R2RML.subjectMap, None)):
        print(a,b,subject_map)
        for _, _, template in r2rml_graph.triples((subject_map, R2RML.template, None)):
            d2rq_graph.add((subject, D2RQ.uriPattern, Literal(template.replace('{', '@@').replace('}', '@@'))))

def convert_predicate_object_map(subject):
    for _, _, pred_obj_map in r2rml_graph.triples((subject, R2RML.predicateObjectMap, None)):
        for _, _, predicate in r2rml_graph.triples((pred_obj_map, R2RML.predicate, None)):
            d2rq_graph.add((subject, D2RQ.property, predicate))
        for _, _, object_map in r2rml_graph.triples((pred_obj_map, R2RML.objectMap, None)):
            for _, _, template in r2rml_graph.triples((object_map, R2RML.template, None)):
                d2rq_graph.add((pred_obj_map, D2RQ.uriPattern, Literal(template.replace('{', '@@').replace('}', '@@'))))
            for _, _, constant in r2rml_graph.triples((object_map, R2RML.constant, None)):
                d2rq_graph.add((pred_obj_map, D2RQ.constantValue, constant))
            for _, _, column in r2rml_graph.triples((object_map, R2RML.column, None)):
                d2rq_graph.add((pred_obj_map, D2RQ.column, Literal(column)))

def convert_triples():
    for subject, predicate, obj in r2rml_graph.triples((None, RDF.type, R2RML.TriplesMap)):
        convert_logical_table(subject)
        convert_subject_map(subject)
        convert_predicate_object_map(subject)

if __name__ == "__main__":
    main(sys.argv[1:])
    r2rml_graph.parse(inputfile, format="turtle")
    convert_triples()
    d2rq_graph.serialize(outputfile, format="turtle")
