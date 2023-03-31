"""
    Will Rodman
    wrodman@tulane.edu
"""

from Graph import Graph
from FreeSpaceGraph import FreeSpaceGraph

print("\n -- TESTING FreeSpaceGraph.py -- ")
graph_g = Graph("sample_graphs/G")
graph_h = Graph("sample_graphs/H")
epsilon = 2
graph_g.Plot2MatPlotLib()
graph_h.Plot2MatPlotLib()
fsg = FreeSpaceGraph(graph_g, graph_h, epsilon)
seed_cb = fsg.get_cell_boundry(graph_g, 0, graph_h, 0)
print("Seed Cell Boundery:", seed_cb)
fsg.DFSTraversalDistance(seed_cb)
print(fsg)