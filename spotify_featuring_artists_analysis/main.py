from data_reduction import *
from data_expansion import *
from data_enrichment import *


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

    # drop duplicates
    nodes, edges = drop_duplicates(nodes, edges)

    # remove very unpopular artists
    popularity_score = 40  # minimum popularity score required
    artists_to_keep, _ = get_artists_popularity_larger_or_equal_than_n(nodes, popularity_score)
    nodes = filter_nodes_on_ids(nodes, artists_to_keep)
    edges = filter_edges_on_ids(edges, artists_to_keep)

    # remove artists with few featuring
    n_featuring = 20  # minimum number of featuring we want to consider
    artists_to_keep, _ = get_artists_more_than_n_featuring(edges, n_featuring)
    nodes = filter_nodes_on_ids(nodes, artists_to_keep)
    edges = filter_edges_on_ids(edges, artists_to_keep)

    # add columns to nodes with number of featuring and hits
    count_collaborations(nodes, edges)
    count_chart_hits(nodes)
