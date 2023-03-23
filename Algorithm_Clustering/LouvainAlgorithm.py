import pandas as pd
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
import scipy

# Load nodes and edges data from CSV files
nodes_df = pd.read_csv("nodes.csv")
edges_df = pd.read_csv("edges.csv")
counter = 0

# Create a NetworkX graph object
G = nx.Graph()

# Add nodes to the graph
# for _, node in nodes_df.iterrows():
#     if counter != 100:
#         G.add_node(node["spotify_id"])
#         counter += 1
#     else:
#         break

counter = 0
# Add edges to the graph
for _, edge in edges_df.iterrows():
    if counter != 1000:
        G.add_edge(edge["id_0"], edge["id_1"])
        counter += 1
    else:
        break


# Apply the Louvain Algorithm
partition = list(community.louvain_partitions(G, weight='genres'))
partition = list(partition[0])
# Add community assignments to nodes dataframe
nodes_df["community"] = pd.Series(partition)

# Output the community assignments to a separate CSV file
nodes_df.to_csv("nodes_with_community.csv", index=False)

# Plot the network divided into clusters
pos = nx.spring_layout(G, k=5)  # Gives a cluster shape to the network
size = len(partition)
count = 0.
list_nodes = []
list_pos = {}
list = []

# for x in pos:
#     tuple_0 = (float(x[0]), float(x[1]))
#     # tuple_1 = tuple(partition[com])  # TODO: check this
#     list.clear()
#     count = count + 1.
#     list_nodes.append(x)
#     list_pos[x] = tuple_0
# nx.draw_networkx_nodes(G, list_pos, list_nodes, node_size=20, node_color=str(count / size))
# nx.draw_networkx_edges(G, pos, alpha=0.5)
# plt.savefig('Louvain_Network.png')
# plt.show()
