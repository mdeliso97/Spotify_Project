from typing import Set
import regex as re
from sklearn.preprocessing import MinMaxScaler
import ast
from cluster_metrics import get_main_n_cluster_genres
from data_visualization import *


def read_txt_file(path: str):
    """
    This function extract words in a txt file
    and put them in a list
    Parameters:
    path (str): path of the file
    Returns:
    List[str]: list of the words in the file
    """
    with open(path, 'r') as f:
        return [word.strip() for word in f]


def get_author_tracks(tracks: pd.DataFrame, artist_id: str):
    """
    This function gets all the ids of the
    songs of the given artist
    Parameters:
    tracks (pd.DataFrame): dataframe containing tracks
    artist_id (str): artist id
    Returns:
    List[str]: the ids of the tracks written by the given author
    """
    unique_tracks = tracks.drop_duplicates(subset='name', keep='first')  # remove duplicate tracks based on title
    tracks_ids = unique_tracks[unique_tracks['id_artists'].str.contains(artist_id)]['id'].values
    return list(tracks_ids)


def get_words_frequency(tracks: pd.DataFrame, cluster_ids: List[str], functional_words: List[str]):
    """
    This function computes the frequencies of all
    the words in the title of the given songs
    Parameters:
    tracks (pd.DataFrame): dataframe containing tracks
    cluster_ids (List[str]): list of artists' ids part of the cluster
    functional_words (List[str]): functional words list
    Returns:
    Counter: dictionary with words' counts
    """
    filtered_tracks = tracks[tracks['id_artists'].isin(cluster_ids)]

    # Normalize and remove words
    all_titles = ' '.join(filtered_tracks['name'].values)  # extract titles and concatenate into a single string
    all_titles = re.sub(r'\b\s+\b', ' ', all_titles)  # remove spaces from word boundaries
    all_titles = re.sub(r'\d+', '', all_titles)  # remove digits
    all_titles = all_titles.lower()  # convert to lowercase
    all_titles = re.sub(r"[^\w\s']+", '', all_titles)  # remove special characters

    # remove functional words
    all_words = all_titles.split()
    all_words = [word for word in all_words if word not in functional_words]
    all_titles = ' '.join(all_words)

    word_freq = Counter(all_titles.split())  # split titles into individual words and count frequencies
    return word_freq


def normalize_tracks(tracks: pd.DataFrame):
    """
    This function normalizes the values of
    tracks columns with indexes
    Parameters:
    tracks (pd.DataFrame): dataframe containing tracks
    Returns:
    pd.DataFrame: dataframe containing normalized tracks
    """
    tracks = tracks.copy()  # copy dataframe

    # name
    tracks = tracks.dropna(subset=['name'])  # drops songs with no title

    # id_artists
    tracks.loc[:, 'id_artists'] = tracks['id_artists'].apply(ast.literal_eval)
    tracks.loc[:, 'id_artists'] = tracks['id_artists'].apply(lambda x: x[0])

    # artists
    tracks.loc[:, 'artists'] = tracks['artists'].apply(ast.literal_eval)
    tracks.loc[:, 'artists'] = tracks['artists'].apply(lambda x: x[0])

    # features
    features = ['danceability', 'energy', 'loudness', 'valence', 'tempo', 'speechiness', 'acousticness',
                'instrumentalness', 'duration_ms', 'liveness']
    tracks_features = tracks[features]
    scaler = MinMaxScaler()
    tracks.loc[:, features] = scaler.fit_transform(tracks_features)

    return tracks


def cluster_indexes(tracks: pd.DataFrame, cluster_ids: Set[str]):
    """
    This function computes the means of the indexes values
    of the songs of the given artists
    Parameters:
    tracks (pd.DataFrame): dataframe containing tracks
    cluster_ids (Set[str]): list of artists' ids part of the cluster
    Returns:
    dict: dictionary with indexes and corresponding means
    """
    filtered_tracks = tracks[tracks['id_artists'].isin(cluster_ids)]
    features = ['danceability', 'energy', 'loudness', 'valence', 'tempo', 'speechiness', 'acousticness',
                'instrumentalness', 'duration_ms', 'liveness']
    indexes = {}
    for f in features:
        indexes[f] = filtered_tracks[f].mean()
    return indexes


def generate_indexes_images(indexes: dict, cluster_name: str, path: str):
    """
    This function plots a radar graph
    with mean indexes
    Parameters:
    indexes (dict): dictionary with indexes and corresponding means
    cluster_name (str): name of the given cluster
    path (str): path where to save images
    """
    features_a = ['danceability', 'energy', 'loudness', 'valence', 'tempo']
    features_b = ['speechiness', 'acousticness', 'instrumentalness']

    indexes_a = dict((f, indexes[f]) for f in indexes if f in features_a)
    indexes_b = dict((f, indexes[f]) for f in indexes if f in features_b)

    generate_radar_graph(indexes_a, cluster_name, 'red', 'properties', path)
    generate_radar_graph(indexes_b, cluster_name, 'green', 'qualities', path)


def normalize_collaborations(results):
    """
    Normalizes the counts of collaborations in the given results
    dictionary to be between 0 and 1, and returns a new dictionary
    with the normalized counts.
    Parameters:
    results (dict): A dictionary where each key is a pair of
    collaborators, and the corresponding value is the number
    of collaborations between those two collaborators.
    Returns:
    A new dictionary with the same keys as the input dictionary, but with the values normalized to be between 0 and 1.
    """
    normalized_results = {}
    counts = [count for pair, count in results.items()]

    # Get the maximum and minimum values of the counts
    min_count = min(counts)
    max_count = max(counts)

    if max_count - min_count == 0:
        # Handle the case where the range is zero
        normalized_results = {pair: 0 for pair, count in results.items()}
    else:
        # Normalize each count between 0 and 1
        for pair, count in results.items():
            normalized_results[pair] = (count - min_count) / (max_count - min_count)
    return normalized_results


def filter_clusters_based_on_size(louvain_communities, n_min, n_max):
    """
    Filters a list of Louvain communities based on their size,
    returning only the communities with sizes between
    the given `n_min` and `n_max` parameters.
    Parameters:
    louvain_communities (list): A list of lists, where each
    inner list contains the indices of nodes
    belonging to the corresponding Louvain community
    n_min (int): The minimum size of a community to be included in the filtered list
    n_max (int): The maximum size of a community to be included in the filtered list
    Returns:
    A tuple containing two lists: the indices of the filtered communities within
    the original `louvain_communities` list, and the corresponding communities themselves.
    """
    clusters_indexes = []
    clusters = []
    for i, c in enumerate(louvain_communities):
        if n_min < len(c) < n_max:
            clusters.append(c)
            clusters_indexes.append(i)
    return clusters_indexes, clusters


def generate_symmetric_collaboration_matrix(normalized_results):
    """
    Creates a symmetric matrix from a dictionary of normalized collaboration counts.
    Parameters:
    normalized_results (dict): A dictionary containing normalized collaboration counts,
    where the keys are tuples representing pairs of collaborators and the values are
    floats between 0 and 1.
    Returns:
    numpy.ndarray: A symmetric matrix of size n x n, where n is the largest value in any
    tuple key in normalized_results plus 1. The diagonal elements of the matrix are all
    1, and the off-diagonal elements correspond to the values in normalized_results
    for the corresponding tuple keys.
    """
    # initialize matrix with zeros
    matrix_size = max([max(k) for k in normalized_results]) + 1  # determine size of the matrix
    symmetric_matrix = np.zeros((matrix_size, matrix_size))

    # loop over dictionary items and update matrix
    for k, v in normalized_results.items():
        symmetric_matrix[k[0], k[1]] = v
        symmetric_matrix[k[1], k[0]] = v

    for i in range(len(symmetric_matrix[0])):
        for j in range(len(symmetric_matrix[0])):
            if i == j:
                symmetric_matrix[i, j] = 1

    return symmetric_matrix


def get_matrix_labels(nodes, clusters_indexes, louvain_communities):
    """
    Returns a list of labels for the rows and columns of a matrix, based on the genres
    of the top node in each cluster.
    Parameters:
    nodes (list): A list of nodes in the graph, where each node is represented as a
    dictionary with various properties including a 'genre' field.
    clusters_indexes (list): A list of integers representing the indexes of clusters to
    include in the labels.
    louvain_communities (list): A list of lists representing the nodes in each cluster.
    Returns:
    list: A list of strings representing the top genre for each cluster. The order of
    the strings corresponds to the order of the clusters in the clusters_indexes list.
    """
    labels = []
    for ci in clusters_indexes:
        top_genres = get_main_n_cluster_genres(nodes, louvain_communities[ci], 1)
        labels.append(top_genres[0])
    return labels


def generate_collaboration_matrix(nodes, louvain_communities: List[str], G, path, lower_bound, upper_bound):
    """
    Generates a collaboration matrix for the given nodes and their corresponding communities.
    Parameters:
    nodes (list): List of node ids
    louvain_communities (List[str]): List of community labels
    G (networkx.Graph): Networkx graph object
    path (str): Path to save the visualization
    lower_bound (int): Minimum size of a community to be considered
    upper_bound (int): Maximum size of a community to be considered
    """
    clusters_indexes, clusters = filter_clusters_based_on_size(louvain_communities, lower_bound, upper_bound)

    results = {}
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):

            edge_count = 0

            for n1 in clusters[i]:
                for n2 in clusters[j]:
                    if G.has_edge(n1, n2):
                        edge_count += 1

            if edge_count > 0:
                results[(i, j)] = edge_count

    normalized_results = normalize_collaborations(results)

    symmetric_matrix = generate_symmetric_collaboration_matrix(normalized_results)

    labels = get_matrix_labels(nodes, clusters_indexes, louvain_communities)

    visualize_collaboration_matrix(symmetric_matrix, labels, path)

    visualize_clusters(clusters, labels, symmetric_matrix, path)
