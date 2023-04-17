from collections import Counter
from typing import List, Set
import regex as re
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import pandas as pd
import os
import ast


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
    tracks_ids (List[str]): list of songs ids
    functional_words (List[str]): functional words list
    Returns:
    Counter: dictionary with words' counts
    """
    # artist_name_obj = tracks.artists.values

    # artists_set = set()
    # for s in artist_name_obj:
    #     # Extract artist names using regex
    #     artists_names = re.findall(r"'([\w\s]+)'", s)
    #
    #     # Add artist names to set
    #     for artist_names in artists_names:
    #         for name in artist_names.split():
    #             artists_set.add(name.lower())

    filtered_tracks = tracks[tracks['id_artists'].isin(cluster_ids)]

    # Normalize and remove words
    all_titles = ' '.join(filtered_tracks['name'].values)  # extract titles and concatenate into a single string
    all_titles = re.sub(r'\b\s+\b', ' ', all_titles)  # remove spaces from word boundaries
    all_titles = re.sub(r'\d+', '', all_titles)  # remove digits
    all_titles = all_titles.lower()  # convert to lowercase
    all_titles = re.sub(r"[^\w\s']+", '', all_titles)  # remove special characters

    # for name in artists_set:
    #     all_titles = all_titles.replace(name, '')  # remove artist names

    # remove functional words
    all_words = all_titles.split()
    all_words = [word for word in all_words if word not in functional_words]
    all_titles = ' '.join(all_words)

    word_freq = Counter(all_titles.split())  # split titles into individual words and count frequencies
    return word_freq


def cluster_words_cloud(img_mask: str, words: Counter, cluster_name: str):
    """
    This function produces a words' cloud
    of the given cluster words considering
    their frequency
    Parameters:
    shape_path (str): path of the image mask
    words (Counter): dictionary with words' counts
    """
    # if cluster songs titles contain 0 words
    if len(words) == 0:
        return
    mask = np.array(Image.open(img_mask))
    wordcloud = WordCloud(width=800,
                          height=800,
                          background_color='white',
                          # contour_width=0.1,
                          # contour_color='black',
                          # background_color='green',
                          colormap='summer_r',
                          mask=mask).generate_from_frequencies(words)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    if not os.path.exists("./cluster_indexes"):
        os.mkdir("./cluster_indexes")

    plt.savefig(f'./cluster_indexes/{cluster_name}_cluster_words_cloud.png')
    plt.close()


def normalize_tracks(tracks: pd.DataFrame):
    """
    This function normalizes the values of
    tracks columns with indexes
    Parameters:
    tracks (pd.DataFrame): dataframe containing tracks
    Returns:
    pd.DataFrame: dataframe containing normalized tracks
    """
    tracks = tracks.copy()

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
    cluster_artists_ids (List[str]): list of artists ids
    Returns:
    dict: dictionary with indexes and corresponding means
    """
    # filtered_tracks = tracks[tracks['id_artists'].apply(lambda x: any(artist_id in x for artist_id in cluster_ids))]
    filtered_tracks = tracks[tracks['id_artists'].isin(cluster_ids)]
    features = ['danceability', 'energy', 'loudness', 'valence', 'tempo', 'speechiness', 'acousticness',
                'instrumentalness', 'duration_ms', 'liveness']
    indexes = {}
    for f in features:
        indexes[f] = filtered_tracks[f].mean()
    return indexes


def generate_radar_graph(indexes, cluster_name: str, color: str, graph_type: str):
    df = pd.DataFrame(dict(
        r=list(indexes.values()) + [list(indexes.values())[0]],  # add the first value at the end of the `r` array
        theta=list(indexes.keys()) + [list(indexes.keys())[0]]))  # add the first key at the end of the `theta` array

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=df['r'],
        theta=df['theta'],
        fill='toself',
        line=dict(color=color),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        title={
            'text': f'Music {graph_type}: {cluster_name}',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
    fig.write_image(f'./cluster_indexes/{cluster_name}_cluster_{graph_type}.png')


def generate_indexes_images(indexes: dict, cluster_name: str):
    """
    This function plots a radar graph
    with mean indexes
    Parameters:
    indexes (dict): dictionary with indexes and corresponding means
    cluster_name (str): name of the given cluster
    """
    features_a = ['danceability', 'energy', 'loudness', 'valence', 'tempo']
    features_b = ['speechiness', 'acousticness', 'instrumentalness']

    indexes_a = dict((f, indexes[f]) for f in indexes if f in features_a)
    indexes_b = dict((f, indexes[f]) for f in indexes if f in features_b)

    if not os.path.exists("./cluster_indexes"):
        os.mkdir("./cluster_indexes")

    generate_radar_graph(indexes_a, cluster_name, 'red', 'properties')
    generate_radar_graph(indexes_b, cluster_name, 'green', 'qualities')
