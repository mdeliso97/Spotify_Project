# Spotify Featuring Artists Analysis
Here you can find an explaination of the different files in the project folder.

```main.py```
Main file of the project from which all the other functions are called.

```data_reduction.py```
Functions to reduce the number of artists to be considered in computation. This reduction is related to the number of collaborations that an artist did: if they are below a certain threshold that we defined, we drop the artist.

```data_expansion.py```
Based on the data that we already have, we are able to compute and add additional information for each artist. These information are condensed in two additional columns in the nodes dataframe. 