"""
    Author: 
        Will Rodman 
        wrodman@tulane.edu
"""

from Graph import Graph
from FreeSpaceGraph import FreeSpaceGraph

graph_a = Graph("sample_graphs/sample_1/arc_de_triomphe")
graph_b = Graph("sample_graphs/sample_1/vehicle_path")
graph_a = Graph("sample_graphs/sample_2/athens_small_1")
graph_b = Graph("sample_graphs/sample_2/athens_small_2")
epsilon = 1000
fsg = FreeSpaceGraph(graph_a, graph_b, epsilon)
fsg.plot()

pg = fsg.DFSTraversalDist()

print("-- Graph sample sizes -- ")
print("     No. edges is graph 1:", graph_a.numberOfEdges)
print("     No. edges graph 2 :", graph_b.numberOfEdges)

print("\n -- TESTING FreeSpaceGraph DFS Memorization -- ")
print("     DFS FS CBs computed:", len(fsg.cell_boundaries))
print("     DFS Projection Check:", pg)
print("     DFS Function Calls:", fsg.DFS_calls)

print("\n -- TESTING FreeSpaceGraph Brute Force -- ")
print("     Brute Force FS CBs computed:", fsg.cb_count)