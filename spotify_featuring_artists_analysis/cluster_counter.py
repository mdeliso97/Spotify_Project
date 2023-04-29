"""
This class is responsible for counting the amount of communities that have a specific length
"""


def cluster_counter(louvain_communities):
    # initialize a dictionary to count the number of lists with each length
    counts = {}

    # loop through each list and count the number of lists with the same length
    for lst in louvain_communities:
        length = len(lst)
        if length not in counts:
            counts[length] = 1
        else:
            counts[length] += 1

    # convert the dictionary to a list of tuples
    result = list(counts.items())

    return result
