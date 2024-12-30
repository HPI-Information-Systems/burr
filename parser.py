from rdflib import Graph

g = Graph()
g.parse("/Users/lukaslaskowski/Downloads/RODI_benchmark/data/cmt_naive/mapping.ttl")
print(len(g))