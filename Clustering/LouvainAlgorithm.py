import pandas as pd
import networkx as nx
from networkx.algorithms import community
import Timer
import matplotlib.pyplot as plt
import scipy

# Load nodes and edges data from CSV files
nodes_df = pd.read_csv("nodes.csv")
edges_df = pd.read_csv("edges.csv")

# Create a NetworkX graph object
G = nx.Graph()

# Add nodes to the graph
# for _, node in nodes_df.iterrows():
#     if counter != 100:
#         G.add_node(node["spotify_id"])
#         counter += 1
#     else:
#         break

timer_elapse = Timer.Timer()
timer_elapse.start()

counter = 0
# Add edges to the graph
for _, edge in edges_df.iterrows():
    if counter != 10000:
        G.add_edge(edge["id_0"], edge["id_1"])
        counter += 1
    else:
        break

print("# Nodes: %d" % len(G.nodes))
print("# Edges: %d" % len(G.edges))

# Apply the Louvain Algorithm
partition0 = list(community.louvain_partitions(G, resolution=0.01, seed=50))
print("Lovain Partitions: %d " % len(partition0))
print(len(partition0[0]))

# TODO: try to figure out why louvain keeps outputting lists of list as result, even giving multiple variations of
#  clusters.

a = sum(len(X) for X in partition0[0])
b = max(len(X) for X in partition0[0])
print(a)
print(b)
partition00 = list(community.louvain_communities(G, resolution=0.01, seed=50))
print("Lovain Partitions: %d " % len(partition00))
sub_graph0 = nx.Graph()

# for X in partition0[0]:
#     sub_graph0.add_edge(X[0], X[1])
#
# partition0_0 = list(community.louvain_partitions(sub_graph0))
# partition0_1 = list(community.louvain_partitions(sub_graph1))
# partition0_2 = list(community.louvain_partitions(sub_graph2))
# partition0_3 = list(community.louvain_partitions(sub_graph3))

# partition1 = list(community.girvan_newman(G))
# print("Girvan Newman: %d" % len(partition1))



# # Add community assignments to nodes dataframe
# nodes_df["community"] = pd.Series(partition0)
#
# node_list = [X for X in G.nodes]
#
# # Output the community assignments to a separate CSV file
# nodes_df.to_csv("nodes_with_community.csv", index=False)
#
# # Plot the network divided into clusters
# pos = nx.spring_layout(G, k=10, seed=10)  # Gives a cluster shape to the network
# size = len(partition0)
# count = 0.
# list_nodes = []
# list_pos = {}
# coord_list = []
#
# timer_elapse.checkpoint()
#
# for X in G.nodes:
#     if X in pos:
#         list_pos[X] = pos[X]
#         # tuple_0 = (float(X[0]), float(X[1]))
#         # tuple_1 = tuple(partition[com])  # TODO: check this
#         count = count + 1.
# nx.draw_networkx_nodes(G, list_pos, node_list, node_size=20)
# # nx.draw_networkx_nodes(G, list_pos, node_list, node_size=20, node_color=str(count / size))
# nx.draw_networkx_edges(G, pos, alpha=0.5)
# plt.savefig('Louvain_Network.png')
# plt.show()
#
# timer_elapse.stop()