from typing import List

import pandas as pd


def drop_duplicates(nodes: pd.DataFrame, edges: pd.DataFrame):
    """
    This function drops eventual duplicates in both nodes
    and edges dataframes
    Parameters:
    nodes (pd.DataFrame): dataframe containing the network nodes
    edges (pd.DataFrame): dataframe containing network edges
    Returns:
    pd.DataFrame: nodes dataframe without duplicates
    pd.DataFrame: edges dataframe without duplicates
    """
    return nodes.drop_duplicates(), edges.drop_duplicates()


def get_artists_based_on_n_featuring(edges: pd.DataFrame, n_min: int, n_max: int):
    """
    This function creates a list with ids of artists
    with more than n featuring
    Parameters:
    edges (pd.DataFrame): dataframe containing network edges
    n_min (int): minimum number of featuring
    n_max (int): maximum number of featuring
    Returns:
    List[str]: id of the artists with n_min < #collaborations < n_max
    """
    n_featuring = pd.concat([edges['id_0'], edges['id_1']]).value_counts()
    filtered_nodes = n_featuring[(n_min < n_featuring) & (n_featuring < n_max)]
    filtered_nodes_ids = filtered_nodes.index.tolist()
    return filtered_nodes_ids


def get_artists_popularity_larger_or_equal_than_n(nodes: pd.DataFrame, n: int):
    """
    This function removes artists with popularity less than n
    Parameters:
    nodes (pd.DataFrame): dataframe containing the network nodes
    n (int): minimum popularity score
    Returns:
    List[str]: id of the artists with >= than popularity n
    List[str]: id of the artists with < than popularity n
    """
    if 0 <= n <= 100:
        return nodes[nodes['popularity'] >= n]['spotify_id'].tolist(), nodes[nodes['popularity'] < n]['spotify_id'].tolist()
    else:
        return nodes['spotify_id'], None


def filter_nodes_on_ids(nodes: pd.DataFrame, nodes_to_keep: List[str]):
    """
    This function cuts all the nodes that are not present
    inside the nodes_to_keep list
    Parameters:
    nodes (pd.DataFrame): dataframe containing the network nodes
    nodes_to_keep (List[str]): list of nodes ids to keep
    Returns:
    pd.DataFrame: filtered dataframe with only nodes in the nodes_to_keep list
    """
    return nodes[nodes['spotify_id'].isin(nodes_to_keep)]


def filter_edges_on_ids(edges: pd.DataFrame, nodes_to_keep: List[str]):
    """
    This function cuts all the edges that are not related
    to nodes in the nodes_to_keep list
    Parameters:
    edges (pd.DataFrame): dataframe containing network edges
    nodes_to_keep (List[str]): list of nodes ids to keep
    Returns:
    pd.DataFrame: filtered dataframe with only edges related
    to nodes in the nodes_to_keep list
    """
    filtered_edges = edges[edges['id_0'].isin(nodes_to_keep)]
    filtered_edges = filtered_edges[filtered_edges['id_1'].isin(nodes_to_keep)]
    return filtered_edges
