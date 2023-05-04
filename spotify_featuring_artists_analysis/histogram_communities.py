from matplotlib import pyplot as plt

'''
This class is responsible for the plots of the two Louvain algorithms which represent the amount of clusters sharing the 
same count of artists. It generates two histograms.
'''


def histogram_communities():
    scratch = [(4, 11), (48, 1), (2, 74), (3, 35), (6, 11), (20, 3), (25, 2), (8, 5), (170, 1), (90, 1), (35, 1),
               (198, 1), (96, 1), (12, 1), (5, 7), (22, 2), (775, 1), (95, 1), (18, 2), (167, 1), (51, 1), (52, 1),
               (7, 6), (67, 1), (100, 1), (9, 1), (132, 1), (144, 1), (156, 1), (19, 1), (97, 1), (49, 1), (240, 1),
               (11, 1), (138, 1), (103, 1), (41, 1), (10, 1), (13, 2), (36, 1), (39, 1), (21, 1), (154, 1), (222, 1),
               (53, 1)]
    built_in = [(123, 1), (119, 1), (700, 1), (51, 1), (135, 1), (62, 1), (2, 10), (346, 1), (3, 3), (25, 1), (109, 1),
                (28, 1), (113, 1), (5, 1), (4, 4), (95, 1), (93, 1), (8, 2), (820, 1), (7, 1), (64, 1), (67, 1), (9, 1),
                (377, 1), (34, 1), (195, 1), (174, 1), (262, 1), (138, 1), (102, 1), (12, 1)]

    sorted_scratch = sorted(scratch, key=lambda x: x[1], reverse=True)
    sorted_built_in = sorted(built_in, key=lambda x: x[1], reverse=True)

    nodes_scratch = [X for X, Y in sorted_scratch]
    nodes_built_in = [X for X, Y in sorted_built_in]

    communities_scratch = [Y for X, Y in sorted_scratch]
    communities_built_in = [Y for X, Y in sorted_built_in]

    plt.bar(nodes_scratch, communities_scratch, width=5)
    plt.ylabel('# of communities')
    plt.xlabel('# of artists')
    plt.title('communities artists distribution')
    plt.savefig(f'histogram_scratch_communities_5.png')
    plt.show()

    plt.bar(nodes_built_in, communities_built_in, width=5)
    plt.ylabel('# of communities')
    plt.xlabel('# of artists')
    plt.title('communities artists distribution')
    plt.savefig(f'histogram_builtin_communities_5.png')
    plt.show()


if __name__ == '__main__':
    histogram_communities()


