import networkx as nx

'''
This class takes as inputs a graph G and a list of lists of communities. It is responsible to find for each community
the best/worst nodes in each centrality measure: degree centrality, closeness centrality and betweenness centrality.
Finally, the algorithm outputs a dictionary of dictionaries, which holds a dictionary of indexed clusters (following the 
order of the input) with inside 3 dictionaries of the best node for each centrality category.
'''


def Importance(G, communities):
    # Initializing dictionaries
    cluster_dict = {}  # dictionary of dictionaries of the nodes wirth the highest centralities

    # Calculating for each node the three chosen centrality measures: betweenness, closeness and degree centralities
    betweenness_centrality, degree_centrality, closeness_centrality = CentralityMeasures(G)

    for community in communities:

        # if cluster is too small don't consider it
        if len(community) <= 100:
            continue

        # initialize dictionaries and cluster index
        id_cluster = communities.index(community)
        betweenness_max_dict = {}
        degree_max_dict = {}
        closeness_max_dict = {}
        betweenness_min_dict = {}
        degree_min_dict = {}
        closeness_min_dict = {}

        # Find the highest/lowest values of the centrality measures and the corresponding node in a cluster
        highest_degree = max(degree_centrality[node] for node in community)
        id_node_degree = next(node for node in community if degree_centrality[node] == highest_degree)

        lowest_degree = min(degree_centrality[node] for node in community)
        id_node_lw_degree = next(node for node in community if degree_centrality[node] == lowest_degree)

        highest_btw = max(betweenness_centrality[node] for node in community)
        id_node_btw = next(node for node in community if betweenness_centrality[node] == highest_btw)

        lowest_btw = min(betweenness_centrality[node] for node in community)
        id_node_lw_btw = next(node for node in community if betweenness_centrality[node] == lowest_btw)

        highest_cls = max(closeness_centrality[node] for node in community)
        id_node_cls = next(node for node in community if closeness_centrality[node] == highest_cls)

        lowest_cls = min(closeness_centrality[node] for node in community)
        id_node_lw_cls = next(node for node in community if closeness_centrality[node] == lowest_cls)

        # create dictionaries with the node as key and its measure as value
        betweenness_max_dict[id_node_btw] = highest_btw
        degree_max_dict[id_node_degree] = highest_degree
        closeness_max_dict[id_node_cls] = highest_cls

        betweenness_min_dict[id_node_lw_btw] = lowest_btw
        degree_min_dict[id_node_lw_degree] = lowest_degree
        closeness_min_dict[id_node_lw_cls] = lowest_cls

        # Store everything inside another dictionary
        cluster_dict["community_%d" % id_cluster] = {
            "betweenness_max": betweenness_max_dict,
            "degree_max": degree_max_dict,
            "closeness_max": closeness_max_dict,
            "betweenness_min": betweenness_min_dict,
            "degree_min": degree_min_dict,
            "closeness_min": closeness_min_dict
        }
    return cluster_dict


def CentralityMeasures(G):

    # built-in centrality measures
    betweenness_centrality = nx.betweenness_centrality(G, k=len(G.nodes))

    degree_centrality = nx.degree_centrality(G)

    closeness_centrality = nx.closeness_centrality(G)

    return betweenness_centrality, degree_centrality, closeness_centrality
