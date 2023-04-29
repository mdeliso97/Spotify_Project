# Spotify Featuring Artists Analysis
Here you can find an explanation of the different files in the project folder.

```main.py```
Main file of the project from which all the other functions are called.

```data_reduction.py```
Functions to reduce the number of artists to be considered in computation. This reduction is related to the number of 
collaborations that an artist did: if they are below a certain threshold that we defined, we drop the artist.

```data_enrichment.py```
Combine the Spotify featuring dataset with the Spotify songs dataset to perform some additional analysis on the songs 
produced by artists in different clusters.

```data_expansion.py```
Based on the data that we already have, we are able to compute and add additional information for each artist. 
This information was condensed in two additional columns in the nodes dataframe.

```data_visualization.py```
It contains all the functions producing visual outputs and plots.

```cluster_metrics.py```
Functions to compute the metrics of a given cluster.

```CommonEdges.py```
This class takes as inputs 2 communities (lists of nodes) and the graph itself and outputs the edges in common between
the two communities.

```LouvainScratch.py```
Our chosen Analytic was Community Detection, hence the Louvain clustering algorithm from scratch. This class implements
the Louvain algorithm seen in class.

```LabelConverter.py```
This small program can be used to convert the dataset into integers and mapped through a dictionary to keep track of 
them.

```NodeImportance.py```
This class takes as inputs a graph G and a list of lists of communities. It is responsible to find for each community
the best/worst nodes in each centrality measure: degree centrality, closeness centrality and betweenness centrality.
Finally, the algorithm outputs a dictionary of dictionaries, which holds a dictionary of indexed clusters (following the 
order of the input) with inside 3 dictionaries of the best node for each centrality category.

```SimulationNetwork.py```
This is just a sample of a network of which we previously calculated the solution. It is a reference to compare the 
louvain algorithm implemented from scratch.

```Timer.py```
This class implements the Timer method which has three main methods: start(), checkpoint() and end(). Start() and End()
are used to start and stop the timer, whereas checkpoint is used to output the current time elapsed.

```cluster_counter.py```
This class gives us a list of tuples as output, each one of this has as first element the count of nodes and the second
the count of clusters with that specific node count.

```data_importance.py```
This class plots the data produced in the class NodeImportance.py and plots the centrality measures grouped per each
different centrality having as values the minimum and maximum of the specific centrality measure. In addition, in the
x-axis is also given the artist that corresponds to the best or worst centrality.