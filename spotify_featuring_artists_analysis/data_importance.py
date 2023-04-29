import matplotlib.pyplot as plt
import pandas as pd

'''
This class is responsible for plotting the importance of the nodes from the class "NodeImportance.py". The method 
iterates through each community and generates a bar for each centrality measure and binds to it the artists that have
that specific score. The plots are grouped by centrality measure and represent the minimum and maximum of that 
centrality measure.
'''


def data_importance(communities_importance):
    for com in communities_importance:

        # Take first cluster as dictionary
        data = communities_importance[com]

        # Extract node ids
        nodes = list([key for key in data.values() for key in key.keys()])

        # Extract minimum and maximum values for each centrality measure
        btw_max = [data['betweenness_max'][nodes[0]]]
        degree_max = [data['degree_max'][nodes[1]]]
        cls_max = [data['closeness_max'][nodes[2]]]
        btw_min = [data['betweenness_min'][nodes[3]]]
        degree_min = [data['degree_min'][nodes[4]]]
        cls_min = [data['closeness_min'][nodes[5]]]

        # Create a panda dataframe and store the ids and names of artists
        df = pd.read_csv('Data/nodes.csv', header=0)
        sample = df[["spotify_id", "name"]]

        # Storing to each id the corresponding name for the labels
        matching_artist0 = sample[sample['spotify_id'] == nodes[0]]
        specific_artist0 = matching_artist0['name'].values[0]

        matching_artist1 = sample[sample['spotify_id'] == nodes[1]]
        specific_artist1 = matching_artist1['name'].values[0]

        matching_artist2 = sample[sample['spotify_id'] == nodes[2]]
        specific_artist2 = matching_artist2['name'].values[0]

        matching_artist3 = sample[sample['spotify_id'] == nodes[3]]
        specific_artist3 = matching_artist3['name'].values[0]

        matching_artist4 = sample[sample['spotify_id'] == nodes[4]]
        specific_artist4 = matching_artist4['name'].values[0]

        matching_artist5 = sample[sample['spotify_id'] == nodes[5]]
        specific_artist5 = matching_artist5['name'].values[0]

        # Set bar width and x-axis values
        bar_width = 0.2
        x_pos = [0, 1, 2, 3, 4]
        x_pos_label = [x_pos[1] - 0.125, x_pos[1] + 0.125, x_pos[2] - 0.125, x_pos[2] + 0.125, x_pos[3] - 0.125,
                       x_pos[3] + 0.125]
        x_label = [specific_artist0, specific_artist3, specific_artist1, specific_artist4, specific_artist2,
                   specific_artist5]

        # Plot bars for each centrality measure
        plt.figure(figsize=(10, 7))
        plt.bar(x_pos[1] - 0.125, btw_max, width=bar_width, color='#7DD4FF', label='Btw max')
        plt.bar(x_pos[1] + 0.125, btw_min, width=bar_width, color='#0B87C6', label='Btw min')
        plt.bar(x_pos[2] - 0.125, degree_max, width=bar_width, color='#7CFF62', label='Degree max')
        plt.bar(x_pos[2] + 0.125, degree_min, width=bar_width, color='#3FA22B', label='Degree min')
        plt.bar(x_pos[3] - 0.125, cls_max, width=bar_width, color='#FF5858', label='Cls max')
        plt.bar(x_pos[3] + 0.125, cls_min, width=bar_width, color='#942222', label='Cls min')
        plt.xticks(x_pos_label, x_label, rotation=30, ha='right',
                   fontdict={'fontsize': 7, 'fontweight': 'bold', 'fontfamily': 'Arial'})

        plt.legend(loc='upper left')
        plt.title(com)
        plt.savefig('Data/data_visualization/importance_%s.png' % com)
        plt.close()
