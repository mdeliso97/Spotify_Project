import numpy as np
import pandas as pd

df = pd.read_csv("communities.csv")
print(df.head())
communities = df.to_numpy().flatten()
print(len(communities[0]))


# trying to extract each community nodes
'''Cluster_Nodes = []
for j in range(len(C_List[0])):
    if C_List[0][j] not in Symbols :
        Cluster_Nodes.append(C_List[0][j])

Symbols = ['{', '}', '[', ']', ' ', "'"]

Cluster_Nodes = [C_List[0][j] for j in range(len(C_List[0])) if C_List[0][j] not in Symbols]

Cluster1 = [C_List[1][j] for j in range(len(C_List[1])) if C_List[1][j] not in Symbols]

Cluster2 = [C_List[2][j] for j in range(len(C_List[2])) if C_List[2][j] not in Symbols]

Cluster3 = [C_List[3][j] for j in range(len(C_List[3])) if C_List[3][j] not in Symbols]

# print(Cluster_Nodes)
Nodes = ''.join(Cluster_Nodes)
Nodes = Nodes.split(',')

Nodes1 = ''.join(Cluster1)
Nodes1 = Nodes1.split(',')

Nodes2 = ''.join(Cluster2)
Nodes2 = Nodes1.split(',')

Nodes3 = ''.join(Cluster3)
Nodes3 = Nodes1.split(',')

community_id = pd.DataFrame(Nodes, columns=['community_id'])
spotify_id = df['spotify_id']

spotify_id = spotify_id.astype({'spotify_id': 'string'})
community_id = community_id.astype({'community_id': 'string'})

# print(community_id)
community_id_List = community_id['community_id'].values

# map node Id to it's community id
df['Community_id'] = df['spotify_id'].map(lambda x: 1 if x in community_id_List else 0)

# print(df['Community_id'])
# df.drop('community')
df.to_csv('nodes_with_community_id.csv')

#print(community_id['community_id'].head(10))

#print(community_id.iloc[1])'''

# concatenate
'''partitions = open("partition.txt", "r")

partitions_list = partitions.readlines()

copy_ = partitions_list[0].copy()
print(''.join(copy_))'''
