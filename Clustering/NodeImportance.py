
import pandas as pd
import networkx as nx



def Graph():
    G = nx.Graph()

    # Load nodes and edges data from CSV files
    nodes_df = pd.read_csv("nodes.csv")
    edges_df = pd.read_csv("edges.csv")

    # Add edges and nodes to the graph
    for _, edge in edges_df.iterrows():
        G.add_edge(edge["id_0"], edge["id_1"])

    print("# Nodes: %d" % len(G.nodes))
    print("# Edges: %d" % len(G.edges))

    return G


def Utility(betweenness, degree, closeness, alpha, beta, gamma):
    utility = alpha * betweenness + beta * degree + gamma * closeness
    return utility


def CentralityMeasures(G):
    betweenness_centrality = nx.betweenness_centrality(G, k=len(G.nodes))

    degree_centrality = nx.degree_centrality(G)

    closeness_centrality = nx.closeness_centrality(G)

    return betweenness_centrality, degree_centrality, closeness_centrality
