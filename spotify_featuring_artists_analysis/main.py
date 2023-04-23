from data_reduction import *
from data_expansion import *
from data_enrichment import *
from data_enrichment import generate_collaboration_matrix
from cluster_metrics import *
from data_visualization import *
from networkx.algorithms import community
import networkx as nx

if __name__ == '__main__':

    # path to data
    nodes_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/nodes.csv'
    edges_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/edges.csv'
    tracks_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/tracks.csv'
    functional_words_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/functional_words.txt'
    spotify_img_mask_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/spotify_mask2.jpg'
    data_visualization_path = '/Users/caratja/Desktop/data_visualization'

    # import data
    nodes = pd.read_csv(nodes_path)
    edges = pd.read_csv(edges_path)
    tracks = pd.read_csv(tracks_path)
    functional_words = read_txt_file(functional_words_path)

    # create directory for data visualization
    create_visualization_directory(data_visualization_path)

    # normalize tracks data in [0;1] range
    tracks = normalize_tracks(tracks)

    # drop duplicates
    nodes, edges = drop_duplicates(nodes, edges)

    # remove very unpopular artists
    # popularity_score = 60  # minimum popularity score required
    # artists_to_keep, _ = get_artists_popularity_larger_or_equal_than_n(nodes, popularity_score)
    # nodes = filter_nodes_on_ids(nodes, artists_to_keep)
    # edges = filter_edges_on_ids(edges, artists_to_keep)

    # remove artists with few featuring
    # n_featuring = 60  # minimum number of featuring we want to consider
    # artists_to_keep, _ = get_artists_more_than_n_featuring(edges, n_featuring)
    # nodes = filter_nodes_on_ids(nodes, artists_to_keep)
    # edges = filter_edges_on_ids(edges, artists_to_keep)

    # add columns to nodes with number of featuring and hits
    # count_collaborations(nodes, edges)
    # count_chart_hits(nodes)

    # instantiate networkx graph
    G = nx.Graph()
    for _, edge in edges.iterrows():
        G.add_edge(edge['id_0'], edge['id_1'])

    # clustering algorithm
    louvain_communities = list(community.louvain_partitions(G, seed=20))
    louvain_communities = louvain_communities[-1]

    # generate map cluster_id->genre
    cluster_genre_map = generate_cluster_genre_map(nodes, louvain_communities)

    # data enrichment & data visualization:
    for i, cluster in enumerate(louvain_communities):

        if len(cluster) <= 100:
            continue

        # word-cloud = most important words of each cluster
        # cluster_word_freq = get_words_frequency(tracks, cluster, functional_words)
        # cluster_words_cloud(spotify_img_mask_path, cluster_word_freq, cluster_genre_map[i], data_visualization_path)

        # radar-graph = songs qualities and properties
        # indexes = cluster_indexes(tracks, cluster)
        # generate_indexes_images(indexes, cluster_genre_map[i], data_visualization_path)

    # - collaboration matrix = degree of collaboration between different clusters
    # - clusters visualization = clusters visualization
    generate_collaboration_matrix(nodes, louvain_communities, G, data_visualization_path, 500, 1000)
