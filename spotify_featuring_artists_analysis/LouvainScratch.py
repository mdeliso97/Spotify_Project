import networkx as nx


def louvain_algorithm(G):
    # Initialize the partition with each node in its own community
    partition = [[node] for node in G.nodes()]

    # Initialize the maximum modularity
    max_modularity = -1

    # Loop until there are no more improvements in modularity
    while True:
        # Get the communities in the current partition
        # communities = {community: [node for node in partition if partition[node] == community] for community in set(partition.values())}
        # Initialize the new partition
        new_partition = partition.copy()

        # Loop over each node and its neighbors
        for node in G.nodes():

            neighbors = list(nx.neighbors(G, node))

            # Calculate the modularity gain for each community
            community_gains = {}
            for community in partition:
                for neighbor in neighbors:
                    if neighbor in community:
                        in_bool = True
                    else:
                        in_bool = False
                    if in_bool:

                        # Calculate the gain in modularity if node was moved to community c
                        new_modularity = modularity_gain(G, community, node)
                        community_gains["%s" % str(community)] = new_modularity

            # Move the node to the community with the maximum modularity gain
            best_community = max(community_gains, key=community_gains.get)
            count = 0
            for com in new_partition:
                if str(com) == best_community:
                    new_partition[count].append(node)
                    for com_search in new_partition:
                        if node in com_search and str(com_search) != best_community:
                            com_search.remove(node)
                            if len(com_search) == 0:
                                new_partition.remove(com_search)
                            break
                    break
                else:
                    count += 1

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
    m = len(G.edges)
    q = 0
    k_c = 0

    for c in partition:
        nodes = [n for n in c]
        subgraph = G.subgraph(nodes)
        l_c = len(subgraph.edges)
        for x in nodes:
            k_c += G.degree(x)
        q += (2 * l_c - (k_c ** 2) / m)

        q *= (1/(2 * m))

    return q


# Define the modularity gain function
def modularity_gain(G, community, target):
    # initialize parameters
    d_j = 0
    d_ij = 0

    m = len(G.edges)
    d_i = G.degree(target)
    for node in community:
        d_j += G.degree(node)
        if (node, target) in G.edges or (target, node) in G.edges:
            d_ij += 1
    delta_q = (1/(2 * m)) * (2 * d_ij - (d_i * d_j) / m)

    return delta_q
