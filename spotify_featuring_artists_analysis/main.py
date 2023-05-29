from data_reduction import *
from data_enrichment import *
from data_enrichment import generate_collaboration_matrix
from cluster_metrics import *
from data_visualization import *
from networkx.algorithms import community
import networkx as nx
from louvain_scratch import louvain_algorithm
from timer import Timer
from cluster_counter import cluster_counter

if __name__ == '__main__':

    # path to data
    nodes_path = 'Data/nodes.csv'
    edges_path = 'Data/edges.csv'
    tracks_path = 'Data/tracks.csv'
    functional_words_path = 'Data/functional_words.txt'
    spotify_img_mask_path = 'Data/spotify_mask.jpg'
    data_visualization_path = 'Data/data_visualization'

    # import data
    nodes = pd.read_csv(nodes_path)
    edges = pd.read_csv(edges_path)
    tracks = pd.read_csv(tracks_path)
    functional_words = read_txt_file(functional_words_path)
    time_elapsed = Timer()

    # create directory for data visualization
    create_plot_directory(data_visualization_path)

    # data cleaning
    tracks = clean_tracks(tracks)

    # drop duplicates
    nodes, edges = drop_duplicates(nodes, edges)

    # remove artists based on popularity
    # popularity_score = 75  # minimum popularity score required
    # artists_to_keep, _ = get_artists_popularity_larger_or_equal_than_n(nodes, popularity_score)
    # nodes = filter_nodes_on_ids(nodes, artists_to_keep)
    # edges = filter_edges_on_ids(edges, artists_to_keep)

    # - remove artists with few featuring
    n_min_featuring = 22  # minimum number of featuring we want to consider
    n_max_featuring = 101  # max number of featuring we want to consider
    artists_to_keep = get_artists_based_on_n_featuring(edges, n_min_featuring, n_max_featuring)
    nodes = filter_nodes_on_ids(nodes, artists_to_keep)
    edges = filter_edges_on_ids(edges, artists_to_keep)
    tracks = filter_tracks_on_ids(tracks, artists_to_keep
                                  )
    # - normalize tracks data in [0;1] range
    tracks = normalize_tracks(tracks)

    # data expansion
    # - add columns to nodes with number of featuring and hits
    # count_collaborations(nodes, edges)
    # count_chart_hits(nodes)

    # Instantiate networkx graph
    G = nx.Graph()
    for _, edge in edges.iterrows():
        G.add_edge(edge['id_0'], edge['id_1'])

    print("\nSpotify Artists Featurings Network")

    print("\nNetwork Data:")
    print(f"> #nodes = {nx.number_of_nodes(G)}")
    print(f"> #edges = {nx.number_of_edges(G)}")

    # Louvain: Implementation from scratch ________________________________________________________

    time_elapsed.start()

    louvain_communities = louvain_algorithm(G)  # generate communities

    print("\nLouvain Scratch Runtime:")

    time_elapsed.stop()

    print("> #communities = %d" % len(louvain_communities))

    counted_clusters = cluster_counter(louvain_communities)
    print(f'> distribution (#nodes, #communities) = \n{counted_clusters}')

    # Louvain: Implementation built-in ____________________________________________________________
    time_elapsed.start()

    # generate communities
    louvain_communities_built_in = list(community.louvain_partitions(G, seed=20))
    louvain_communities_built_in = louvain_communities_built_in[-1]

    print("\nLouvain Built-In Runtime:")

    time_elapsed.stop()

    print("> #communities = %d" % len(louvain_communities_built_in))

    counted_clusters = cluster_counter(louvain_communities_built_in)
    print(f'> distribution (#nodes, #communities) = \n{counted_clusters}')

    # Normalized Mutual Information: Louvain Built-in vs Louvain Scratch __________________________

    nodes = nodes_cluster_labels(nodes, louvain_communities_built_in, louvain_communities)
    nmi = clusters_mutual_information(nodes)

    print("\nLouvain Distributions Comparison - Built-In Vs Scratch:")
    print(f'> normalized mutual information = {nmi}\n')

    # Analyze communities _________________________________________________________________________

    # Generate map cluster_id -> genre
    cluster_genre_map = generate_cluster_genre_map(nodes, louvain_communities)

    # data enrichment & visualization:
    for i, cluster in enumerate(louvain_communities):

        # if cluster is too small don't consider it
        if len(cluster) <= 100:
            continue

        # create directory for data visualization
        cluster_path = f'{data_visualization_path}/{cluster_genre_map[i]}'
        create_plot_directory(cluster_path)

        # - word-cloud = most important words of each cluster
        cluster_word_freq = get_words_frequency(tracks, cluster, functional_words)
        cluster_words_cloud(spotify_img_mask_path, cluster_word_freq, cluster_genre_map[i], cluster_path)

        # - radar-graph = songs qualities and properties
        indexes = cluster_indexes(tracks, cluster)
        generate_indexes_images(indexes, cluster_genre_map[i], cluster_path)

        centralities = highest_centralities_artists(G, cluster)
        plot_influential_artists(nodes, centralities, cluster_genre_map[i], cluster_path)

    # Data visualization and evaluation

    # - collaboration matrix = degree of collaboration between different clusters
    # - clusters visualization = clusters visualization
    min_len = 9  # minimum cluster length for cluster to be considered
    max_len = 357  # # maximum cluster length for cluster to be considered
    generate_collaboration_matrix(nodes, louvain_communities, G, data_visualization_path, min_len, max_len)
