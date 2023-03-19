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
    pd.DataFrame: dataframe without duplicates
    pd.DataFrame: dataframe without duplicates
    """
    return nodes.drop_duplicates(), edges.drop_duplicates()


def get_artists_more_than_n_featuring(edges: pd.DataFrame, n: int):
    """
    This function creates a list with ids of artists
    with more than n featuring
    Parameters:
    edges (pd.DataFrame): dataframe containing network edges
    n (int): minimum number of featuring
    Returns:
    List[str]: id of the artists with >= than n collaborations
    List[str]: id of the artists with < than n collaborations
    """
    n_featuring = pd.concat([edges['id_0'], edges['id_1']]).value_counts()
    more_than_n = n_featuring[n_featuring >= n]
    less_than_n = n_featuring[n_featuring < n]
    artists_more_than_n_featuring = more_than_n.index.tolist()
    return artists_more_than_n_featuring, less_than_n


def filter_nodes(nodes: pd.DataFrame, nodes_to_keep: List[str]):
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


def filter_edges(edges: pd.DataFrame, nodes_to_keep: List[str]):
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
    return edges[edges['id_0'].isin(nodes_to_keep) | edges['id_1'].isin(nodes_to_keep)]