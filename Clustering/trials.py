import pandas as pd
from data_reduction import *
from Graph_Vis import *

nodes_df = pd.read_csv('nodes_with_community_id.csv')
# nodes_df.drop(['community'])

#loading nodes
nodes = nodes_df[nodes_df['community_id'].notna()]
#loading edges
edges = pd.read_csv('reduced_edges.csv')

#selecting specific nodes to be visualized
popularity_score = 85  # minimum popularity score required
artists_to_keep, _ = get_artists_popularity_larger_or_equal_than_n(nodes, popularity_score)
nodes = filter_nodes_on_ids(nodes, artists_to_keep)
edges = filter_edges_on_ids(edges, artists_to_keep)

print("number of nodes is : ", len(nodes), "number of edges is : ", len(edges))

#calling the function that returns the network graph
graph = drawGraph_Louvain(nodes, edges)

# showing the graph in a html page
graph.show("graph.html")
