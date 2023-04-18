import networkx as nx
from bokeh.models import GraphRenderer, Circle, StaticLayoutProvider
from bokeh.palettes import Spectral8
from bokeh.plotting import figure, show


def Visualization(communities, edges, G):

    # Define the colors for the communities
    community_colors = Spectral8[:len(communities)]

    # Create the graph renderer and add the nodes and edges
    graph = GraphRenderer()

    node_indices = []
    community_colors_list = []
    for i, community in enumerate(communities):
        community_colors_list.extend([community_colors[i]] * len(community))
        node_indices.extend(community)

    graph.node_renderer.data_source.add(node_indices, 'index')
    graph.node_renderer.data_source.add(community_colors_list, 'color')

    graph.edge_renderer.data_source.data = dict(
        start=[edge[0] for edge in edges],
        end=[edge[1] for edge in edges])

    pos = nx.spring_layout(G)

    # Define the layout provider
    layout_provider = StaticLayoutProvider(graph_layout={node: node.value for node in pos})

    # Create the plot
    plot = figure(title='Community Graph with Bokeh', x_range=(-1.1,1.1), y_range=(-1.1,1.1),
                  tools='', toolbar_location=None)

    # Add the nodes and edges to the plot
    graph.node_renderer.glyph = Circle(height=0.1, width=0.2, fill_color='color')
    graph.edge_renderer.glyph.line_alpha = 0.2

    plot.renderers.append(graph)

    # Set the layout provider
    graph.layout_provider = layout_provider

    # Show the plot
    show(plot)
