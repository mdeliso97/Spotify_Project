import networkx as nx
import copy


def louvain_algorithm(G):
    # Initialize the partition with each node in its own community
    partition = [[node] for node in G.nodes()]
    ht = {}

    # Initialize the maximum modularity
    max_modularity = -1

    count = 0

    # maps each node to its position in new_partition
    for el in partition:
        ht[el[0]] = count
        count += 1

    # Loop until there are no more improvements in modularity
    while True:

        # Initialize the new partition
        new_partition = copy.deepcopy(partition)

        # Loop over each node and its neighbors
        for node in sorted(G.nodes()):

            # Step 1: remove node from its community
            pos = ht[node]
            new_partition[pos].remove(node)

            neighbors = list(nx.neighbors(G, node))

            # Calculate the modularity gain for each community
            community_gains = {}
            for neighbor in neighbors:
                pos_neighbor = ht[neighbor]

                # Calculate the gain in modularity if node was moved to community c
                new_modularity = modularity_gain(G, new_partition[pos_neighbor], node)
                community_gains["%s" % str(new_partition[pos_neighbor])] = new_modularity

            # Move the node to the community with the maximum modularity gain
            best_community = max(community_gains, key=community_gains.get)

            com_pos = best_community
            com_pos_list = eval(com_pos)
            result = com_pos_list[0]
            com_pos = ht[result]

            new_partition[com_pos].append(node)
            ht[node] = com_pos

        # If there is no improvement in modularity, stop looping
        new_modularity = modularity(G, new_partition)
        if new_modularity == max_modularity:
            break

        # Update the partition and maximum modularity
        partition = new_partition
        max_modularity = new_modularity

    # Return the final partition
    partition_final = [partition[int(pos)] for pos in set(ht.values())]

    return partition_final


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
        q += (2 * l_c - ((k_c ** 2) / (2 * m)))

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
    delta_q = (1/(2 * m)) * (2 * d_ij - ((d_i * d_j) / m))

    return delta_q
