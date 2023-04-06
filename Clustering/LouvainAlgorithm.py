import itertools
from data_reduction import *
import pandas as pd
import networkx as nx
from networkx.algorithms import community
from networkx.algorithms.community import modularity

import Timer
import matplotlib.pyplot as plt
import scipy


def louvain_partitions_k(G, k, weight="weight", resolution=1, threshold=0.0000001, seed=None):
    """Returns the partition of the graph G into k communities using Louvain community detection algorithm."""
    partitions = list(community.louvain_partitions(G, weight, resolution, threshold, seed))
    while len(partitions) > k:
        partition = partitions.pop()
        m = modularity(G, partition, resolution=resolution, weight=weight)
        mod = m
        best_partition = partition
        for com in partition:
            subgraph = G.subgraph(com)
            new_partition = list(community.louvain_partitions(subgraph, weight, resolution, threshold, seed))
            new_m = modularity(subgraph, new_partition, resolution=resolution, weight=weight)
            if new_m > mod:
                best_partition = new_partition
                mod = new_m
        partitions.append(best_partition)
    return partitions[-1]


def Louvain(G, k):
    louvain_list = []
    comp = community.louvain_communities(G)
    for communities in itertools.islice(comp, k):
        louvain_list += [c for c in communities]

    return louvain_list


def louvain(G, k):
    louvain_list = []
    comp = community.louvain_communities(G)
    communities = {}
    for node, comm_id in comp.items():
        if comm_id not in communities:
            communities[comm_id] = [node]
        else:
            communities[comm_id].append(node)
    for comm_id, nodes in communities.items():
        if len(louvain_list) == k:
            break
        louvain_list.append(sorted(nodes))
    return louvain_list


if __name__ == "__main__":
    # Load nodes and edges data from CSV files
    nodes_df = pd.read_csv("nodes.csv")
    edges_df = pd.read_csv("edges.csv")

    # Create a NetworkX graph object
    G = nx.Graph()
    timer_elapse = Timer.Timer()
    timer_elapse.start()

    # Perform data reduction

    # drop duplicates
    nodes, edges = drop_duplicates(nodes_df, edges_df)

    # remove very unpopular artists
    popularity_score = 40  # minimum popularity score required
    artists_to_keep, _ = get_artists_popularity_larger_or_equal_than_n(nodes, popularity_score)
    nodes = filter_nodes_on_ids(nodes, artists_to_keep)
    edges = filter_edges_on_ids(edges, artists_to_keep)

    # remove artists with few featuring
    n_featuring = 20  # minimum number of featuring we want to consider
    artists_to_keep, _ = get_artists_more_than_n_featuring(edges, n_featuring)
    nodes = filter_nodes_on_ids(nodes, artists_to_keep)
    edges = filter_edges_on_ids(edges, artists_to_keep)

    counter = 0
    # Add edges to the graph
    for _, edge in edges.iterrows():
        if counter != 1000000:
            G.add_edge(edge["id_0"], edge["id_1"])
            counter += 1
        else:
            break

    print("# Nodes: %d" % len(G.nodes))
    print("# Edges: %d" % len(G.edges))

    # Apply the Louvain Algorithm
    # louvain_communities = louvain_partitions_k(G, k=10)
    louvain_communities = list(community.louvain_partitions(G, seed=20))
    louvain_communities = louvain_communities[-1]

    louvain_communities_list = []

    for X in louvain_communities:
        louvain_communities_list0 = []
        for Y in X:
            louvain_communities_list0.append(Y)
        louvain_communities_list.append(louvain_communities_list0)

    # Add community assignments to nodes dataframe
    df = pd.Series(louvain_communities_list)
    nodes_df["community"] = pd.Series(louvain_communities_list)

    print("There were found %d communities in Louvain" % len(louvain_communities))
    print("Length of each community: ", sorted(len(a) for a in louvain_communities))
    count = sum(1 for X in louvain_communities if len(X) < 20)
    print("# of communities that we can get rid of since smaller then 20: ", count)

    # Output the community assignments to a separate CSV file
    df.to_csv("communities.csv", index=False)
    nodes_df.to_csv("nodes_with_community.csv", index=False)




    # Plot the network divided into clusters
    # pos = nx.spring_layout(G, k=10, seed=10)  # Gives a cluster shape to the network
    # size = len(partition)
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