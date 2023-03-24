## Clustering Algorithms

### Louvain Algorithm

This algorithm is known for its speed and scalability, making it an ideal choice for large networks.
It is a hierarchical clustering method that optimizes modularity, a measure of the strength of the 
connections between nodes within clusters.

**Advantages**: Fast and scalable, can handle networks with millions of nodes and edges. Produces 
high-quality clusters with high modularity scores.

**Disadvantages**: May not find the optimal clustering solution, as it uses a greedy optimization 
algorithm.

Given *m* # of edges and *n* # of nodes:

1. **Time complexity**: *O(m log n)*. This is due to the algorithm's iterative process of merging 
adjacent communities while optimizing modularity.

2. **Space complexity**: *O(n)*. This is due to the storage of community assignments for each node.

### Girvan-Newman Algorithm

This algorithm is based on edge betweenness, which measures the number of the shortest paths that pass
through an edge. It works by recursively removing edges with the highest betweenness until the network 
is divided into the desired number of clusters.

**Advantages**: Works well for detecting communities with a clear separation between clusters. Does not 
require the number of clusters to be specified beforehand.

**Disadvantages**: Can be computationally expensive for large networks. May not perform well for networks 
with overlapping clusters.

Given *m* # of edges and *n* # of nodes:

1. **Time complexity**: *O(m^2 n)*. This is due to the recursive removal of edges with the highest 
betweenness centrality.

2. **Space complexity**: *O(m)*. This is due to the storage of the betweenness centrality scores for 
each edge.

### Infomap Algorithm

This algorithm is based on the idea that information flows through the network in the form of random walks.
It partitions the network by minimizing the expected description length of a random walk through the 
network.

**Advantages**: Can detect overlapping and hierarchical clusters. Performs well for networks with strong 
modular structure.

**Disadvantages**: Can be sensitive to noise and small fluctuations in the network structure. Can be 
computationally expensive for large networks.

Given *m* # of edges and *n* # of nodes:

1. **Time complexity**: *O(m log n)*. This is due to the algorithm's iterative process of minimizing the 
expected description length.
    
2. **Space complexity**: *O(m)*. This is due to the storage of transition probabilities between nodes.

### Spectral Clustering Algorithm

This algorithm uses the eigenvalues and eigenvectors of the adjacency matrix to partition the network into 
clusters. It is particularly useful for networks with a community structure, where clusters are densely 
connected internally and sparsely connected externally.

**Advantages**: Can handle networks with non-convex and irregular shapes. Works well for networks with a clear 
community structure.

**Disadvantages**: Can be computationally expensive for large networks. Requires knowledge of the number of 
clusters beforehand.

Given *m* # of edges and *n* # of nodes:

1. **Time complexity**: *O(n^2 log n)*. This is due to the computation of the eigenvalues and eigenvectors 
of the adjacency matrix.
   
2. **Space complexity**: *O(n^2)*. This is due to the storage of the adjacency matrix and the eigenvectors.

## Time Complexity summarized (best to worst)

1. Infomap Algorithm: O(m log n)
2. Louvain Algorithm: O(m log n)
3. Spectral Clustering Algorithm: O(n^2 log n)
4. Girvan-Newman Algorithm: O(m^2 n)

look for Pruning cliques







