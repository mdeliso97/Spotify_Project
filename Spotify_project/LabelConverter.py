import networkx as nx


def LabelConverter(G):

    # Generate dictionary to map node labels to integers
    node_dict = {node: idx for idx, node in enumerate(G.nodes())}

    # Convert node labels from strings to integers
    G = nx.relabel_nodes(G, node_dict)

    return G, node_dict
