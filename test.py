"""
    Will Rodman
    wrodman@tulane.edu
"""

from Graph import Graph
from FreeSpaceGraph import FreeSpaceGraph

graph_a = Graph("sample_graphs/arc_de_triomphe")
graph_b = Graph("sample_graphs/vehicle_path")
#graph_a = Graph("sample_graphs/G")
#graph_b = Graph("sample_graphs/H")
epsilon = 10
graph_a.Plot2MatPlotLib()
graph_b.Plot2MatPlotLib()
fsg = FreeSpaceGraph(graph_a, graph_b, epsilon)

print("-- Graph sample sizes -- ")
print("     No. edges is arc_de_triomphe:", graph_a.numberOfEdges)
print("     No. edges vehicle_path :", graph_b.numberOfEdges)

seed_cb = fsg.get_cell_boundry(graph_a, 0, graph_b, 0)
fsg.DFSTraversalDist(seed_cb)

print("\n -- TESTING FreeSpaceGraph DFS Memorization -- ")
print("     Seed Cell Boundery:", seed_cb)
print("     DFS Memorization FS CBs computed:", len(fsg.cell_boundaries))
print(fsg)

print("\n -- TESTING FreeSpaceGraph Brute Force -- ")
fsg.brute_force()
print("     Brute Force FS CBs computed:", len(fsg.cell_boundaries))