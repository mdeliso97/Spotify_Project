from bokeh.plotting import figure, show, from_networkx
from bokeh.models import Range1d, Circle, HoverTool, StaticLayoutProvider
from bokeh.palettes import Spectral8
import networkx as nx

# Define the graph as a NetworkX Graph instance
G = nx.Graph()

# Add nodes and edges to the graph
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])
G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A')])

# Define the plot layout and properties
plot = figure(title="Networkx Integration with Bokeh", x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1),
              tools="", toolbar_location=None)
plot.axis.visible = False
plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None

# Define the node layout as a dictionary of coordinates
node_positions = {node: [i/5, i%5] for i, node in enumerate(G.nodes())}
node_indices = {node: i for i, node in enumerate(G.nodes())}
node_index = [node_indices[node] for node in G.nodes()]

# Define the plot data source from the NetworkX graph
graph_renderer = from_networkx(G, node_positions, scale=1, center=(0,0))

# Define node and edge colors
graph_renderer.node_renderer.fill_color = Spectral8
graph_renderer.edge_renderer.line_alpha = 0.3

# Define node size and edge line width
graph_renderer.node_renderer.size = 20
graph_renderer.edge_renderer.line_width = 2

# Define the node hover tool
hover = HoverTool(tooltips=[("Name", "@index")])
plot.add_tools(hover)

# Define the node layout provider as a StaticLayoutProvider instance
node_layout_provider = StaticLayoutProvider(graph_layout=node_positions)
graph_renderer.layout_provider = node_layout_provider

# Add the graph renderer to the plot and show it
plot.renderers.append(graph_renderer)
show(plot)