from typing import List

import pandas as pd
import regex as re


def count_collaborations(nodes: pd.DataFrame, edges: pd.DataFrame):
    """
    This function adds a new column to the nodes dataframe with
    the number of edges each node has in the edges dataframe
    Parameters:
    nodes (pd.DataFrame): dataframe containing the network nodes
    edges (pd.DataFrame): dataframe containing edges between network nodes
    """
    counts = pd.concat([edges['id_0'], edges['id_1']]).value_counts()
    nodes['n_featuring'] = nodes['spotify_id'].map(counts).fillna(0).astype(int)


def count_chart_hits(nodes: pd.DataFrame):
    """
    This function adds a new column to the nodes dataframe with
    the number of chart hits the artist produced in total
    Parameters:
    nodes (pd.DataFrame): dataframe containing the network nodes
    """
    nodes['n_hits'] = nodes['chart_hits'].astype(str).apply(count_chart_hits_auxiliary)


def count_chart_hits_auxiliary(chart_hits: List[str]):
    """
    This function extracts and sum up the number of chart
    hits songs from the given chart_hits list of hits
    divided by countries
    Parameters:
    chart_hits (List[str]): list containing the number
    of chart hits divided by nations
    Returns:
    int: the count of chart hits
    """
    numbers = []
    for hit in chart_hits:
        match = re.search(r'\d+', hit)
        if match:
            numbers.append(int(match.group()))
    return sum(numbers)
