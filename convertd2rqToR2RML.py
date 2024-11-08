import sys
import getopt
import rdflib
import re
import time
import datetime
from rdflib import URIRef, BNode, RDF, Literal
from rdflib.namespace import XSD

g = rdflib.Graph()
newg = rdflib.Graph()

newg.bind("rr", URIRef("http://www.w3.org/ns/r2rml#"))
newg.bind("dc", URIRef("http://purl.org/dc/elements/1.1/"))
newg.bind("dcterms", URIRef("http://purl.org/dc/terms/"))
newg.bind("xsd", URIRef("http://www.w3.org/2001/XMLSchema#"))
newg.bind("owl", URIRef("http://www.w3.org/2002/07/owl#"))
newg.bind("rdf", URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
newg.bind("rdfs", URIRef("http://www.w3.org/2000/01/rdf-schema#"))
newg.bind("foaf", URIRef("http://xmlns.com/foaf/0.1/"))

inputfile = ''
outputfile = ''

def main(argv):
    global inputfile, outputfile
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('python3 D2RQ_to_R2RML.py -i <D2RQ_mapDoc> -o <R2RML_mapDoc>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python3 D2RQ_to_R2RML.py -i <D2RQ_mapDoc> -o <R2RML_mapDoc>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

def LogicalTable(subject):
    logicalTableNode = f"{subject}_LogicalTable"
    newg.add((subject, URIRef('http://www.w3.org/ns/r2rml#logicalTable'), URIRef(logicalTableNode)))
    newg.add((URIRef(logicalTableNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#LogicalTable')))
    return logicalTableNode

def SubjectMap(subject, pattern, logicalTableNode):
    subjectNode = f"{subject}_subjectMap"
    newg.add((subject, URIRef('http://www.w3.org/ns/r2rml#subjectMap'), URIRef(subjectNode)))
    newg.add((URIRef(subjectNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#SubjectMap')))
    if pattern != "null":
        newg.add((subject, RDF.type, URIRef('http://www.w3.org/ns/r2rml#TriplesMap')))
        newg.add((URIRef(subjectNode), URIRef('http://www.w3.org/ns/r2rml#template'), Literal(pattern)))
    else:
        for subject, predicate, obj in g.triples((subject, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriPattern'), None)):
            tableName = re.search('(.+?)\\.', re.search('@@(.+?)@@', obj).group(1)).group(1)
            newg.add((URIRef(logicalTableNode), URIRef('http://www.w3.org/ns/r2rml#tableName'), Literal(tableName)))
            new_obj = re.sub('@@(.+?)@@', r'{\1}', obj.replace("|urlencode", "").replace("|urlify", ""))
            reference = new_obj.replace(re.search(r'{(.+?)\.', new_obj).group(1) + ".", "")
            newg.add((URIRef(subjectNode), URIRef('http://www.w3.org/ns/r2rml#template'), Literal(reference)))
        for subject, predicate, obj in g.triples((subject, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#class'), None)):
            newg.add((URIRef(subjectNode), URIRef('http://www.w3.org/ns/r2rml#class'), URIRef(obj)))

def RefObjectMap(subject, preObj, pre, obj):
    objNode = f"{preObj}_ObjMap"
    newg.add((preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), URIRef(objNode)))
    newg.add((URIRef(objNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#RefObjectMap')))
    newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#parentTriplesMap'), obj))
    numJoins = 0
    for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#join'), None)):
        joinNode = f"{objNode}_JoinMap_{numJoins}"
        numJoins += 1
        newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#joinCondition'), URIRef(joinNode)))
        table = re.split(' |=', obj)
        newg.add((URIRef(joinNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#Join')))
        for subj, pred, tableName in newg.triples((subject, URIRef('http://www.w3.org/ns/r2rml#logicalTable'), None)):
            for obj, predd, tab in newg.triples((obj, URIRef('http://www.w3.org/ns/r2rml#tableName'), None)):
                mm = re.search('(.+?)\\.', table[0])
                if str(mm.group(1)) == str(tab):
                    reference = table[-1].replace(re.search('(.+?)\\.', table[-1]).group(1) + ".", "")
                    newg.add((URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#parent'), Literal(reference)))
                    reference = table[0].replace(re.search('(.+?)\\.', table[0]).group(1) + ".", "")
                    newg.add((URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#child'), Literal(reference)))
                else:
                    reference = table[0].replace(re.search('(.+?)\\.', table[0]).group(1) + ".", "")
                    newg.add((URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#parent'), Literal(reference)))
                    reference = table[-1].replace(re.search('(.+?)\\.', table[-1]).group(1) + ".", "")
                    newg.add((URIRef(joinNode), URIRef('http://www.w3.org/ns/r2rml#child'), Literal(table[-1])))

if __name__ == "__main__":
    main(sys.argv[1:])

g.parse(inputfile, format="turtle")

for subject, predicate, obj in g.triples((None, RDF.type, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#ClassMap'))):
    logicalTableNode = LogicalTable(subject)
    subjectNode = f"{subject}_subjectMap"
    newg.add((subject, RDF.type, URIRef('http://www.w3.org/ns/r2rml#TriplesMap')))
    SubjectMap(subject, "null", logicalTableNode)
    for preObj, predicate, obj in g.triples((None, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#belongsToClassMap'), subject)):
        newg.add((subject, URIRef('http://www.w3.org/ns/r2rml#predicateObjectMap'), URIRef(preObj)))
        newg.add((preObj, RDF.type, URIRef('http://www.w3.org/ns/r2rml#PredicateObjectMap')))
        for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#property'), None)):
            newg.add((preObj, URIRef('http://www.w3.org/ns/r2rml#predicate'), obj))
        for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#dynamicProperty'), None)):
            preNode = f"{obj}_PreMap"
            newg.add((preObj, URIRef('http://www.w3.org/ns/r2rml#predicateMap'), URIRef(preNode)))
            newg.add((URIRef(preNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#PredicateMap')))
            newg.add((URIRef(preNode), URIRef('http://www.w3.org/ns/r2rml#constant'), Literal(obj)))
            newg.add((URIRef(preNode), URIRef('http://www.w3.org/ns/r2rml#termType'), URIRef('http://www.w3.org/ns/r2rml#IRI')))
        for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriPattern'), None)):
            objNode = f"{preObj}_ObjMap"
            new_obj = re.sub('@@(.+?)@@', r'{\1}', obj.replace("|urlencode", "").replace("|urlify", ""))
            reference = new_obj.replace(re.search(r'{(.+?)\.', new_obj).group(1) + ".", "")
            newg.add((preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), URIRef(objNode)))
            if tableName != re.search(r'{(.+?)\.', new_obj).group(1):
                obj = f"{preObj}_RefObjMap"
                RefObjectMap(subject, preObj, pre, obj)
                SubjectMap(obj, reference, logicalTableNode)
                tableName = re.search(r'{(.+?)\.', new_obj).group(1)
                logicalTable = f"{preObj}_RefObjMap_LogicalTable"
                newg.add((obj, URIRef('http://www.w3.org/ns/r2rml#logicalTable'), URIRef(logicalTable)))
                newg.add((URIRef(logicalTable), URIRef('http://www.w3.org/ns/r2rml#tableName'), Literal(tableName)))
            else:
                newg.add((URIRef(objNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')))
                newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#template'), Literal(reference)))
        for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#pattern'), None)):
            objNode = f"{preObj}_ObjMap"
            newg.add((preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), URIRef(objNode)))
            newg.add((URIRef(objNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')))
            new_obj = re.sub('@@(.+?)@@', r'{\1}', obj.replace("|urlencode", "").replace("|urlify", ""))
            reference = new_obj.replace(re.search(r'{(.+?)\.', new_obj).group(1) + ".", "")
            newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#template'), Literal(reference)))
            newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#termType'), URIRef('http://www.w3.org/ns/r2rml#Literal')))
        for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#constantValue'), None)):
            objNode = f"{preObj}_ObjMap"
            newg.add((preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), URIRef(objNode)))
            newg.add((URIRef(objNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')))
            newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#constant'), URIRef(obj.replace("|urlencode", ""))))
        for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#column'), None)):
            objNode = f"{preObj}_ObjMap"
            newg.add((preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), URIRef(objNode)))
            newg.add((URIRef(objNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')))
            reference = obj.replace(re.search(r'(.+?)\.', obj).group(1) + ".", "")
            newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#column'), Literal(reference)))
            for preObj, pre, datatype in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#datatype'), None)):
                newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#datatype'), datatype))
            for preObj, pre, lang in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#lang'), None)):
                newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#language'), lang))
        for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriColumn'), None)):
            objNode = f"{preObj}_ObjMap"
            newg.add((preObj, URIRef('http://www.w3.org/ns/r2rml#objectMap'), URIRef(objNode)))
            newg.add((URIRef(objNode), RDF.type, URIRef('http://www.w3.org/ns/r2rml#ObjectMap')))
            reference = obj.replace(re.search(r'(.+?)\.', obj).group(1) + ".", "")
            newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#column'), Literal(reference)))
            newg.add((URIRef(objNode), URIRef('http://www.w3.org/ns/r2rml#termType'), URIRef('http://www.w3.org/ns/r2rml#IRI')))
        for preObj, pre, obj in g.triples((preObj, URIRef('http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#refersToClassMap'), None)):
            RefObjectMap(subject, preObj, pre, obj)

now = datetime.datetime.now()
newg.add((BNode(), URIRef("http://purl.org/dc/elements/1.1/created"), Literal(f"{now.year}-{now.month}-{now.day}")))
newg.serialize(outputfile, format='turtle')
