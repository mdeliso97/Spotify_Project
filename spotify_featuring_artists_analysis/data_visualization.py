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


def create_visualization_directory(path):
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
                          # contour_width=0.1,
                          # contour_color='black',
                          # background_color='green',
                          colormap='summer_r',
                          mask=mask).generate_from_frequencies(words)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig(f'{path}/{cluster_name}_cluster_words_cloud.png')
    plt.close()


def visualize_clusters(clusters: List[str], labels: List[str], symmetric_matrix, path):

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
    fig = px.scatter(df, x='x', y='y', size='cluster_size', color='cluster_label', text='cluster_label', hover_name='cluster_size', size_max=60)

    fig.update_layout(showlegend=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(title="Clusters")

    # Show the plot
    fig.write_image(f'{path}/clusters.png')


def visualize_collaboration_matrix(symmetric_matrix, labels, path):

    # Create a figure and axis
    # fig, ax = plt.subplots()
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