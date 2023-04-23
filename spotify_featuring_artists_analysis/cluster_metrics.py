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


def generate_cluster_genre_map(nodes: pd.DataFrame, louvain_communities: List[List[str]]):
    """
    This functions generates a map linking each cluster
    with its main genre
    Parameters:
    nodes (pd.DataFrame): dataframe containing the network nodes
    louvain_communities (List[List[str]]): list of clusters
    Returns:
    Map[str,str]: map linking each cluster with its main genre
    """
    cluster_genre_map = {}
    no_genre_count = 0

    # iterate over each cluster
    for i, cluster in enumerate(louvain_communities):

        top_genres = get_main_n_cluster_genres(nodes, cluster, 1)  # compute top-n cluster genre

        # if no top-genre assign 'no_genre' placeholder
        if len(top_genres) == 0:
            top_genres = [f'no_genre_{no_genre_count}']
            no_genre_count += 1

        cluster_genre_map[i] = top_genres[0]

    return cluster_genre_map
