import json
import pygraphviz as pgv

# Load the JSON file
json_file_path = "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/real-world/mondial/mappings/country.json"

with open(json_file_path, 'r') as file:
    ontology_data = json.load(file)

# Create a new graph for visualization
graph = pgv.AGraph(directed=True)

# Customize graph attributes
graph.graph_attr.update(size="8,8!", dpi=600, ranksep="1.5", nodesep="1.0")

# Customize node and edge attributes
graph.node_attr.update(shape="ellipse", style="filled", fillcolor="#add8e6", fontname="Helvetica", fontsize="12")
graph.edge_attr.update(color="#7a7a7a", fontname="Helvetica", fontsize="10")

# Add class nodes (using "class" as the label) and merge nodes with the same name
class_names = {cls["class"]: cls["class"] for cls in ontology_data.get("classes", [])}
for class_name in class_names:
    graph.add_node(class_name)

# Add edges for object properties
for obj_prop in ontology_data.get("object_properties", []):
    belongs_to = obj_prop.get("belongsToClassMap")
    refers_to = obj_prop.get("refersToClassMap")
    property_label = obj_prop.get("property")

    # Only add the edge if both classes exist
    if belongs_to in class_names and refers_to in class_names:
        graph.add_edge(belongs_to, refers_to, label=property_label)

# Use the 'neato' layout algorithm for a balanced visualization
graph.layout(prog="neato")

# Output file path for the visualization
output_path = "ontology_visualization.png"

# Export the graph as a PNG file
graph.draw(output_path)

print(f"Ontology visualization saved to {output_path}")
