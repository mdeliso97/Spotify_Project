
from pyvis.network import Network
import networkx as nx
import pandas as pd

nodes_df = pd.read_csv("nodes.csv")
edges_df = pd.read_csv("edges.csv")

# Create a NetworkX graph object
G = nx.Graph()

counter = 0
# Add nodes to the graph
for _, node in nodes_df.iterrows():
    if counter != 100:
         G.add_node(node["spotify_id"])
         counter += 1
    else:
         break


counter = 0
# Add edges to the graph
for _, edge in edges_df.iterrows():
    if counter != 10000:
        G.add_edge(edge["id_0"], edge["id_1"])
        counter += 1
    else:
        break

#graph = nx.from_pandas_edgelist(df,source = "Source" , target = "Target", edge_attr =['weight','book'] )

nx.draw(G, pos=nx.circular_layout(G),with_labels=True)
nt = Network(height="750px", width="100%", bgcolor="#222222", font_color="white") #filter_menu=True




nt.barnes_hut()

nt.from_nx(G)
#nt.show_buttons(filter_=['physics'])
nt.show('nx.html')

