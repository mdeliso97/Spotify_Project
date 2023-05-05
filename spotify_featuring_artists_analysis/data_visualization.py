import os
from collections import Counter
from typing import List
import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import plotly.graph_objects as go
from sklearn import manifold
import plotly.express as px
import matplotlib.patches as mpatches


def create_plot_directory(path):
    """
    Create a directory in the given path if it does not already exist
    Parameters:
    path (str): The path of the directory to create
    """
    if not os.path.exists(path):
        os.mkdir(path)


def cluster_words_cloud(img_mask: str, words: Counter, cluster_name: str, path: str):
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
                          colormap='summer_r',
                          mask=mask).generate_from_frequencies(words)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(f'Most Influential Words: {cluster_name}', fontsize=20)
    plt.tight_layout(pad=0)
    plt.subplots_adjust(top=0.9)  # adjust the top margin
    plt.savefig(f'{path}/{cluster_name}_cluster_words_cloud.png')
    plt.close()


def visualize_clusters(clusters: List[str], labels: List[str], symmetric_matrix, path):
    """
    Creates a bubble chart visualization of the clusters using the MDS algorithm to reduce the dimensions of the
    similarity matrix to 2D, then plots the size of each cluster as the size of the bubbles and the label of the
    cluster as the color of the bubbles. The resulting plot is saved to the given path.
    Params:
    clusters (List[str]): The list of cluster names
    labels (List[str]): The list of cluster labels
    symmetric_matrix (numpy.ndarray): The similarity matrix
    path (str): The path to save the resulting plot
    """
    cluster_sizes = [len(c) for c in clusters]

    # Calculate the x and y coordinates based on the distance matrix
    mds = manifold.MDS(n_components=2, dissimilarity="euclidean", random_state=42, normalized_stress='auto')
    coordinates = mds.fit_transform(symmetric_matrix)

    # Create a dataframe with the coordinates, cluster sizes, and cluster labels
    df = pd.DataFrame({
        'x': coordinates[:, 0],
        'y': coordinates[:, 1],
        'cluster_size': cluster_sizes,
        'cluster_label': labels
    })

    # Create the bubble chart
    fig = px.scatter(df, x='x', y='y', size='cluster_size', color='cluster_label', text='cluster_label',
                     hover_name='cluster_size', size_max=60)

    fig.update_layout(showlegend=False)
    fig.update_xaxes(showticklabels=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, zeroline=False)
    fig.update_layout(title="Clusters")

    # Show the plot
    fig.write_image(f'{path}/clusters.png')


def visualize_collaboration_matrix(symmetric_matrix, labels, path):
    """
    Visualizes the collaboration matrix as an image with labeled
    axes and a colorbar. Saves the resulting image to a file.
    Params:
    symmetric_matrix: A 2D numpy array representing the symmetric collaboration matrix
    labels: A list of strings representing the labels for the rows and columns of the matrix
    path: A string representing the path to the directory where the resulting image should be saved
    """
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(12, 12))

    # Plot the data
    im = ax.imshow(symmetric_matrix)

    # Add x-axis and y-axis labels
    ax.set_xticks(np.arange(symmetric_matrix.shape[1]))
    ax.set_yticks(np.arange(symmetric_matrix.shape[0]))

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    # Rotate the x-axis labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Add a colorbar
    cbar = ax.figure.colorbar(im, ax=ax)

    # Adjust the margins of the plot
    plt.subplots_adjust(left=0.15, bottom=0.3, right=0.95, top=0.9)

    ax.set_title("Clusters Collaboration Matrix")

    # Show the plot
    plt.savefig(f'{path}/collaboration_matrix.png')
    plt.close()


def generate_radar_graph(indexes, cluster_name: str, color: str, graph_type: str, path: str):
    """
    The generate_radar_graph function generates a radar graph using the plotly
    library based on the given indexes, cluster name, color, graph type, and path.
    Parameters:
    indexes (dictionary): A dictionary containing the values and labels for each axis of the radar graph.
    cluster_name (str): The name of the cluster to be used in the title of the graph.
    color (str): The color of the graph line.
    graph_type (str): The type of graph being generated, e.g., similarity, dissimilarity.
    path (str): The file path to save the generated graph.
    """
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
    fig.write_image(f'{path}/{cluster_name}_cluster_{graph_type}.png')


def plot_influential_artists(nodes, centralities, cluster_name, path):
    values = [c[1] for c in centralities]
    artist_ids = [c[0] for c in centralities]
    labels = [nodes[nodes['spotify_id'] == artist_id].name.values[0] for artist_id in artist_ids]
    colors = ['r', 'b', 'g']
    names = ['betweenness', 'degree', 'closeness']

    plt.figure(figsize=(8, 5))
    plt.bar(names, values, color=colors)
    plt.title(f'Most Influential Artists: {cluster_name}')
    plt.xticks(rotation=0)

    for i in range(len(values)):
        plt.text(i, values[i] + 0.05, round(values[i], 2), ha='center')

    plt.ylim(0, 1)

    plt.subplots_adjust(bottom=0.2, top=0.9)

    patches = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, labels)]
    plt.legend(handles=patches, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=len(labels))
    plt.savefig(f'{path}/{cluster_name}_cluster_most_influential_artists.png', dpi=300)  # save the image to a file
