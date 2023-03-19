from data_reduction import *
from data_expansion import *


if __name__ == '__main__':

    # path to data
    nodes_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/nodes.csv'
    edges_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/edges.csv'

    # import data
    nodes = pd.read_csv(nodes_path)
    edges = pd.read_csv(edges_path)

    # drop duplicates
    nodes, edges = drop_duplicates(nodes, edges)

    # remove artists with few featuring
    n_featuring = 10  # minimum number of featuring we want to consider
    artists_to_keep, _ = get_artists_more_than_n_featuring(edges, n_featuring)
    nodes = filter_nodes(nodes, artists_to_keep)
    edges = filter_edges(edges, artists_to_keep)

    # add columns to nodes with number of featuring and hits
    count_collaborations(nodes, edges)
    count_chart_hits(nodes)
