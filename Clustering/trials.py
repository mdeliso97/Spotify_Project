'''C_List = [[5,6,4,3,6,3,6,'}','[',']',' ',]]


Symbols = ['{','}','[',']',' ',"'"]


Cluster_Nodes = [C_List[0][j] for j in range(len(C_List[0])) if C_List[0][j] not in Symbols]

print(Cluster_Nodes)

Nodes = ''.join(Cluster_Nodes).split(',')

print(Nodes)'''
