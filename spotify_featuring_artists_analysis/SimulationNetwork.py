import networkx as nx


'''
Expected solution:

First Iteration:
C1 = {0, 3},
C2 = {1, 2, 4},
C3 = {5, 7},
C4 = {6},
C5 = {11},
C6 = {9, 12, 14},
C7 = {10, 13},
C8 = {8, 15}.

Fourth Iteration:
C1 = {0, 1, 2, 4, 5},
C2 = {3, 6, 7},
C3 = {11, 13},
C4 = {8, 9, 10, 12, 14, 15}.

Final partitions.
'''


def generate_graph():

    # Example graph for testing
    G = nx.Graph()
    G.add_edges_from({(1, 2), (1, 4), (1, 7)})
    G.add_edges_from({(2, 1), (2, 4), (2, 5), (2, 0), (2, 6)})
    G.add_edges_from({(3, 0), (3, 7)})
    G.add_edges_from({(4, 1), (4, 2), (4, 0), (4, 10)})
    G.add_edges_from({(5, 2), (5, 0), (5, 7), (5, 11)})
    G.add_edges_from({(6, 2), (6, 7), (6, 1)})
    G.add_edges_from({(7, 6), (7, 5), (7, 1), (7, 3)})
    G.add_edges_from({(8, 15), (8, 14), (8, 9), (8, 10), (8, 11)})
    G.add_edges_from({(9, 8), (9, 12), (9, 14)})
    G.add_edges_from({(10, 11), (10, 12), (10, 13), (10, 14), (10, 8), (10, 4)})
    G.add_edges_from({(11, 5), (11, 6), (11, 8), (11, 10), (11, 13)})
    G.add_edges_from({(12, 10), (12, 9)})
    G.add_edges_from({(13, 10), (13, 11)})
    G.add_edges_from({(14, 8), (14, 9), (14, 10)})
    G.add_edges_from({(15, 8)})

    return G
