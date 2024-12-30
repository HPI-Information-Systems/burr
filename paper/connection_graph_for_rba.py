import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.DiGraph()  # Directed graph

# Add nodes with fixed positions (grid layout)
positions = {
    1: (0, 2),  # Top row
    2: (1, 2),
    3: (2, 2),
    4: (3, 2),
    5: (0, 1),  # Bottom row
    6: (1, 1),
    7: (2, 1),
    8: (3, 1)
}

# Edge configuration (start, end, weight, direction)
# Direction: 'uni' for unidirectional, 'bi' for bidirectional
edges = [
    (1, 2, 1.0, 'uni'),  # Unidirectional edge
    (2, 3, 2.5, 'uni'),
    (3, 4, 1.2, 'bi'),   # Bidirectional edge
    (5, 6, 0.8, 'uni'),
    (6, 7, 1.5, 'bi'),
    (7, 8, 2.0, 'uni'),
    (1, 5, 1.8, 'bi'),
    (4, 8, 3.0, 'uni'),
    (2, 6, 1.0, 'uni'),
    (3, 7, 1.2, 'uni')
]

# Add nodes and edges to the graph
for u, v, weight, direction in edges:
    G.add_edge(u, v, weight=weight)
    if direction == 'bi':
        G.add_edge(v, u, weight=weight)  # Add reverse edge for bidirectional

# Extract edge weights and labels
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
edge_labels = {(u, v): f"{G[u][v]['weight']}" for u, v in G.edges()}

# Define custom rectangle node drawing
def draw_nodes_with_labels(ax, pos, labels):
    for node, (x, y) in pos.items():
        ax.add_patch(plt.Rectangle((x - 0.3, y - 0.15), 0.6, 0.3, color="lightblue"))
        ax.text(x, y, str(labels[node]), fontsize=10, ha='center', va='center')

# Create the plot
fig, ax = plt.subplots(figsize=(8, 6))

# Draw the graph layout (edges first)
nx.draw_networkx_edges(
    G,
    pos=positions,
    ax=ax,
    width=edge_weights,
    edge_color='black',
    connectionstyle="arc3,rad=0.0",  # Ensures straight edges
    arrowsize=15
)

# Draw the edge labels
nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=edge_labels, ax=ax, font_color='red')

# Draw custom rectangle nodes with labels
node_labels = {n: f"Node {n}" for n in G.nodes()}
draw_nodes_with_labels(ax, positions, node_labels)

# Set plot limits and remove axes
plt.xlim(-1, 4)
plt.ylim(0, 3)
plt.axis('off')
plt.title("Graph with Rectangular Nodes, Edge Thickness, Labels, and Directions")
plt.show()
