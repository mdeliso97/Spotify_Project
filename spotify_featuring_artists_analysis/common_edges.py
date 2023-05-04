import itertools


def CommonEdges(graph, community0, community1):
    # Create sets for each list
    common_edges = []

    # Find all nodes in one set in the other
    pairs = [(x, y) for x, y in itertools.product(community0, community1) if x != y]

    for i in pairs:
        if i in graph.edges:
            common_edges.append(i)
    return common_edges
