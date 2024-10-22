import rdflib
import pygraphviz as pgv
from rdflib.namespace import split_uri

# File path to the user's ontology
file_path = "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/groundtruths/denormalized__boolean_relation__beverages.ttl"

# Load the ontology
g = rdflib.Graph()
g.parse(file_path, format="turtle")

# Function to get the local name from a URI using rdflib's split_uri()
def get_local_name(uri):
    try:
        return split_uri(uri)[1]
    except:
        return uri  # Fallback to the original URI if splitting fails

# Create a new graph for visualization
graph = pgv.AGraph(directed=True)

# Customize graph attributes
graph.graph_attr.update(size="8,8!", dpi=600, ranksep="2.0", nodesep="1.0")

# Customize node and edge attributes
graph.node_attr.update(shape="ellipse", style="filled", fillcolor="#add8e6", fontname="Helvetica", fontsize="12")
graph.edge_attr.update(color="#7a7a7a", fontname="Helvetica", fontsize="10")

# Add nodes and edges to the graph with shortened labels
for s, p, o in g:
    s_label = get_local_name(str(s))
    o_label = get_local_name(str(o))
    p_label = get_local_name(str(p))
    
    # Add nodes only if labels are not empty
    if s_label and o_label:
        graph.add_node(s_label)
        graph.add_node(o_label)
        graph.add_edge(s_label, o_label, label=p_label)

# Use the 'neato' layout algorithm for a more balanced visualization
graph.layout(prog="neato")

# Output file path
output_path = "ontology_visualization.png"

# Export the graph as a PNG file
graph.draw(output_path)
