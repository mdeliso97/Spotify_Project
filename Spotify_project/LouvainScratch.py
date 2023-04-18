# Define the Louvain algorithm
def louvain_algorithm(G):
    # Initialize the partition with each node in its own community
    partition = {node: i for i, node in enumerate(G.nodes())}
    # Initialize the maximum modularity
    max_modularity = -1

    # Loop until there are no more improvements in modularity
    while True:
        # Get the communities in the current partition
        # ToDo: Infinite loop here
        communities = {c: [n for n in partition if partition[n] == c] for c in set(partition.values())}
        # Initialize the new partition
        new_partition = partition.copy()

        # Loop over each node and its neighbors
        for node in G.nodes():
            neighbors = list(G.neighbors(node))

            # Calculate the modularity gain for each community
            community_gains = {}
            for c in set(partition.values()):
                # Calculate the gain in modularity if node was moved to community c
                new_modularity = modularity_gain(G, communities, c, node, neighbors)
                community_gains[c] = new_modularity

            # Move the node to the community with the maximum modularity gain
            best_community = max(community_gains, key=community_gains.get)
            new_partition[node] = best_community

        # If there is no improvement in modularity, stop looping
        new_modularity = modularity(G, new_partition)
        if new_modularity == max_modularity:
            break

        # Update the partition and maximum modularity
        partition = new_partition
        max_modularity = new_modularity

    # Return the final partition
    return partition


# Define the modularity function
def modularity(G, partition):
    m = G.number_of_edges()
    q = 0

    for c in set(partition.values()):
        nodes = [n for n in partition if partition[n] == c]
        subgraph = G.subgraph(nodes)
        lc = subgraph.number_of_edges()
        dc = sum(G.degree(nodes).values())
        q += (lc / m) - ((dc / (2 * m)) ** 2)

    return q


# Define the modularity gain function
def modularity_gain(G, communities, c, node, neighbors):
    m = G.number_of_edges()
    lc = sum([1 for neighbor in neighbors if neighbor in communities[c]])
    dc = sum(G.degree(communities[c]).values())
    k = G.degree(node)
    q = (lc / m) - (((dc + k) / (2 * m)) ** 2) - ((dc / (2 * m)) ** 2)
    return q