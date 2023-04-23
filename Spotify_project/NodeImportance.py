import networkx as nx

'''
This class takes as inputs a graph G and a list of lists of communities. It is responsible to find for each community
the best nodes in each centrality measure: degree centrality, closeness centrality and betweenness centrality. Finally,
the algorithm outputs a dictionary of dictionaries, which holds a dictionary of indexed clusters (following the order of 
the input) with inside 3 dictionaries of the best node for each centrality category.
'''


def Importance(G, communities):
    # Initializing dictionaries
    cluster_dict = {}  # dictionary of dictionaries of the nodes wirth the highest centralities

    # Calculating for each node the three chosen centrality measures: betweenness, closeness and degree centralities
    betweenness_centrality, degree_centrality, closeness_centrality = CentralityMeasures(G)

    for community in communities:

        # initialize dictionaries and cluster index
        id_cluster = communities.index(community)
        betweenness_dict = {}
        degree_dict = {}
        closeness_dict = {}

        # Find the highest values of the centrality measures and the corresponding node in a cluster
        highest_degree = max(degree_centrality[node] for node in community)
        id_node_degree = next(node for node in community if degree_centrality[node] == highest_degree)

        highest_btw = max(betweenness_centrality[node] for node in community)
        id_node_btw = next(node for node in community if betweenness_centrality[node] == highest_btw)

        highest_cls = max(closeness_centrality[node] for node in community)
        id_node_cls = next(node for node in community if closeness_centrality[node] == highest_cls)

        # create dictionaries with the node as key and its measure as value
        betweenness_dict[id_node_btw] = highest_btw
        degree_dict[id_node_degree] = highest_degree
        closeness_dict[id_node_cls] = highest_cls

        # Store everything inside another dictionary
        cluster_dict["community_%d" % id_cluster] = {
            "betweenness": betweenness_dict,
            "degree": degree_dict,
            "closeness": closeness_dict
        }
    return cluster_dict


def CentralityMeasures(G):

    # built-in centrality measures
    betweenness_centrality = nx.betweenness_centrality(G, k=len(G.nodes))

    degree_centrality = nx.degree_centrality(G)

    closeness_centrality = nx.closeness_centrality(G)

    return betweenness_centrality, degree_centrality, closeness_centrality
