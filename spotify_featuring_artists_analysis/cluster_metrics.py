import ast
from collections import Counter
from typing import List
import pandas as pd


def get_main_n_cluster_genres(nodes: pd.DataFrame, cluster_nodes_ids: List[str], n: int):
    """
    This functions outputs the n predominant genres
    in a cluster of artists
    Parameters:
    nodes (pd.DataFrame): dataframe containing the network nodes
    cluster_nodes_ids (List[str]): list of nodes in the same cluster
    n (int): number of predominant genres to output
    Returns:
    List[str]: list with top n genres
    """
    nodes = nodes.drop(nodes[nodes['genres'] == '[]'].index)  # drop artists with no genres
    nodes_to_consider = nodes[nodes['spotify_id'].isin(cluster_nodes_ids)]  # extract cluster nodes information
    genres_lists = nodes_to_consider['genres'].tolist()  # extract in a list the genres produced by each artist
    genres_lists = [ast.literal_eval(x) for x in genres_lists]  # safely consider the string as a list
    genres = [genre for genres_list in genres_lists for genre in genres_list]  # flatten the list of lists into a single list of genres
    genres_count = Counter(genres)
    genre_list = [genre[0] for genre in genres_count.most_common(n)]
    return genre_list
