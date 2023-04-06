from pyvis.network import Network
import networkx as nx
from data_reduction import *
import pandas as pd


def drawGraph_Louvain(nodes, edges):
    # Create a NetworkX graph object
    G = nx.Graph()

    # adding graph nodes
    for _, node in nodes.iterrows():
        G.add_node(node["spotify_id"], color=node['node color'], size=15)

    # adding edges nodes
    for _, edge in edges.iterrows():
        G.add_edge(edge["id_0"], edge["id_1"])

    print("graph is constructed!")

    nx.draw(G, pos=nx.circular_layout(G), with_labels=True)

    # initializing the graph layout
    nt = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", filter_menu=True)
    nt.barnes_hut()
    print("network is graphed")

    # transforming the graph from networkx object to pyvis.network object
    nt.from_nx(G)
    print("transformation is done")

    # returns network object
    return nt
