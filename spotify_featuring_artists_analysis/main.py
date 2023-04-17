from data_reduction import *
from data_expansion import *
from data_enrichment import *
from cluster_metrics import *
from networkx.algorithms import community
import networkx as nx


if __name__ == '__main__':

    # path to data
    nodes_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/nodes.csv'
    edges_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/edges.csv'
    tracks_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/tracks.csv'
    functional_words_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/functional_words.txt'
    spotify_img_mask_path = '/Users/caratja/Desktop/Benefri/Semester2/Social Media Analytics/Project/Data/spotify_mask2.jpg'

    # import data
    nodes = pd.read_csv(nodes_path)
    edges = pd.read_csv(edges_path)
    tracks = pd.read_csv(tracks_path)
    functional_words = read_txt_file(functional_words_path)

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

    # data enrichment:
    # - word-cloud = most important words of each cluster
    # - radar-graph = qualities and properties extraction
    no_genre_count = 0
    for cluster in louvain_communities:
        if len(cluster) <= 100:
            continue
        top_genres = get_main_n_cluster_genres(nodes, cluster, 1)

        if len(top_genres) == 0:
            top_genres = [f'no_genre_{no_genre_count}']
            no_genre_count += 1

        # word-cloud
        cluster_word_freq = get_words_frequency(tracks, cluster, functional_words)
        cluster_words_cloud(spotify_img_mask_path, cluster_word_freq, top_genres[0])

        # radar-graph
        indexes = cluster_indexes(tracks, cluster)
        generate_indexes_images(indexes, top_genres[0])
