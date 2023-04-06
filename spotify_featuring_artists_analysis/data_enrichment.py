from collections import Counter
from typing import List
import pandas as pd
import regex as re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


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


def get_words_frequency(tracks: pd.DataFrame, tracks_ids: List[str], functional_words: List[str]):
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
    filtered_track = tracks[tracks['id'].isin(tracks_ids)]
    artist_name_obj = filtered_track.artists.values

    artists_set = set()
    for s in artist_name_obj:
        # Extract artist names using regex
        artists_names = re.findall(r"'([\w\s]+)'", s)

        # Add artist names to set
        for artist_names in artists_names:
            for name in artist_names.split():
                artists_set.add(name.lower())

    # Normalize and remove words
    all_titles = ' '.join(filtered_track['name'].values)  # extract titles and concatenate into a single string
    all_titles = re.sub(r'\b\s+\b', ' ', all_titles)  # remove spaces from word boundaries
    all_titles = re.sub(r'\d+', '', all_titles)  # remove digits
    all_titles = all_titles.lower()  # convert to lowercase
    all_titles = re.sub(r"[^\w\s']+", '', all_titles)  # remove special characters

    for name in artists_set:
        all_titles = all_titles.replace(name, '')  # remove artist names

    # remove functional words
    all_words = all_titles.split()
    all_words = [word for word in all_words if word not in functional_words]
    all_titles = ' '.join(all_words)

    word_freq = Counter(all_titles.split())  # split titles into individual words and count frequencies
    return word_freq


def cluster_words_frequency(tracks: pd.DataFrame, cluster_artists_ids: List[str], functional_words: List[str]):
    """
    This function gets all the ids of the
    songs of the given artist
    Parameters:
    tracks (pd.DataFrame): dataframe containing tracks
    cluster_artists_ids (str): ids of the artists in a cluster
    functional_words (List[str]): functional words list
    Returns:
    Counter: dictionary with words' counts
    """
    words_freq = Counter()
    for artist_id in cluster_artists_ids:
        artist_tracks_ids = get_author_tracks(tracks, artist_id)
        artist_words_freq = get_words_frequency(tracks, artist_tracks_ids, functional_words)
        words_freq += artist_words_freq
    return words_freq


def cluster_words_cloud(img_mask: str, words: Counter):
    """
    This function produces a words' cloud
    of the given cluster words considering
    their frequency
    Parameters:
    shape_path (str): path of the image mask
    words (Counter): dictionary with words' counts
    """
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
    plt.show()
