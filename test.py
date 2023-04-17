"""
    Will Rodman
    wrodman@tulane.edu
"""

import sys
from Graph import Graph
from FreeSpaceGraph import FreeSpaceGraph

#graph_a = Graph("sample_graphs/arc_de_triomphe")
#graph_b = Graph("sample_graphs/vehicle_path")
graph_a = Graph("sample_graphs/G")
graph_b = Graph("sample_graphs/H")
epsilon = float(sys.argv[1])
#graph_a.Plot2MatPlotLib()
#graph_b.Plot2MatPlotLib()
fsg = FreeSpaceGraph(graph_a, graph_b, epsilon)
pg = fsg.DFSTraversalDist()

print("-- Graph sample sizes -- ")
print("     No. edges is arc_de_triomphe:", graph_a.numberOfEdges)
print("     No. edges vehicle_path :", graph_b.numberOfEdges)

print("\n -- TESTING FreeSpaceGraph DFS Memorization -- ")
print("     DFS FS CBs computed:", len(fsg.cell_boundaries))
print("     DFS Projection Check:", pg)
print("     DFS Function Calls:", fsg.DFS_calls)

print("\n -- TESTING FreeSpaceGraph Brute Force -- ")
print("     Brute Force FS CBs computed:", fsg.cb_count)