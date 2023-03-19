import pandas as pd
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
import scipy

# Load nodes and edges data from CSV files
nodes_df = pd.read_csv("nodes.csv")
edges_df = pd.read_csv("edges.csv")

# Create a NetworkX graph object
G = nx.Graph()

# Add nodes to the graph
for _, node in nodes_df.iterrows():
    G.add_node(node["spotify_id"])

# Add edges to the graph
for _, edge in edges_df.iterrows():
    G.add_edge(edge["id_0"], edge["id_1"])

# Apply the Louvain Algorithm
partition = community.louvain_partitions(G, weight='genres')

# Add community assignments to nodes dataframe
nodes_df["community"] = pd.Series(partition)

# Output the community assignments to a separate CSV file
nodes_df.to_csv("nodes_with_community.csv", index=False)

# Plot the network divided into clusters
pos = nx.spring_layout(G)
size = float(len(set(partition.values())))
count = 0.
for com in set(partition.values()):
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20, node_color=str(count / size))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.show()
