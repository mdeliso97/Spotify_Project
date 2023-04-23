import networkx as nx


def LabelConverter(G):

    # Generate dictionary to map node labels to integers
    node_dict = {node: idx for idx, node in enumerate(G.nodes())}

    # Convert node labels from strings to integers
    G = nx.relabel_nodes(G, node_dict)

    # Update edges with new node labels
    # new_edges = [(node_dict[u], node_dict[v]) for u, v in G.edges()]

    # Update graph with new edges
    # G.clear()
    # G.add_nodes_from(node_dict.values())
    # G.add_edges_from(new_edges)

    return G, node_dict
