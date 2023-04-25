"""
    Author: 
        Will Rodman 
        wrodman@tulane.edu
"""

import sys
from Graph import Graph
from FreeSpaceGraph import FreeSpaceGraph

if __name__ == "__main__":
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    epsilon = float(sys.argv[3])

    if '-l' in sys.argv:
        log = True
    else:
        log = False

    if '-p' in sys.argv:
        plot = True
    else:
        plot = False

    g1 = Graph(filename1)
    g2 = Graph(filename2)

    fsg = FreeSpaceGraph(g1, g2, epsilon, filename1=filename1, filename2=filename2, log=log)

    if plot:
        fsg.plot()

    projection_check = fsg.DFSTraversalDist()

    print("\n-- Epsilon --")
    print(f"     {epsilon}")

    print("\n-- Sample Graphs --")
    print(f"     No. edges in {filename1}:", g1.numberOfEdges)
    print(f"     No. vertices in {filename1}:", g1.numberOfNodes)
    print(f"     No. edges in {filename2}:", g2.numberOfEdges)
    print(f"     No. vertices in {filename2}:", g1.numberOfNodes)

    print("\n -- Running Traversal Distance --")
    print("     DFS Function Calls:", fsg.DFS_calls)
    print("     DFS FS CBs computed:", len(fsg.cell_boundaries))
    print("     Total Possible CBs:", fsg.cb_count)
    print("     DFS Projection Check:", projection_check)
