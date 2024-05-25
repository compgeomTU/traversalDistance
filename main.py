"""
    Author: 
        Will Rodman 
        wrodman@tulane.edu
"""
# python3 main.py samples/paris/arc_de_triomphe samples/paris/vehicle 5  -g1_ids 0 -g2_ids 0,1,2

import sys
from Graph import Graph
from FreeSpaceGraph import FreeSpaceGraph
from visualize import Visualize

if __name__ == "__main__":

    # argument parse 
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    epsilon = float(sys.argv[3])

    if '-l' in sys.argv:
        log = True
    else:
        log = False

    if '-g1_ids' in sys.argv and '-g2_ids' in sys.argv:
        arg1 = sys.argv[sys.argv.index('-g1_ids')+1]
        arg2 = sys.argv[sys.argv.index('-g2_ids')+1]
        g1_ids = [eval(i) for i in arg1.split(',')]
        g2_ids = [eval(i) for i in arg2.split(',')]

    else:
        g1_ids, g2_ids = None, None

    # class declaration 
    g1 = Graph(filename1)
    g2 = Graph(filename2)

    vis = Visualize(g1, g2, epsilon, filename1=filename1, filename2=filename2, log=log)
    projection_check = vis.DFSTraversalDist()
    vis.plot(g1_ids=g1_ids, g2_ids=g2_ids)

    # print dfs result 
    print("\n-- Epsilon --")
    print(f"     {epsilon}")

    print("\n-- Sample Graphs --")
    print(f"     No. edges in {filename1}:", g1.numberOfEdges)
    print(f"     No. vertices in {filename1}:", g1.numberOfNodes)
    print(f"     No. edges in {filename2}:", g2.numberOfEdges)
    print(f"     No. vertices in {filename2}:", g1.numberOfNodes)

    print("\n -- Running Traversal Distance --")
    print("     DFS Function Calls:", vis.DFS_calls)
    print("     DFS FS CBs computed:", len(vis.cell_boundaries))
    print("     Total Possible CBs:", vis.cb_count)
    print("     DFS Projection Check:", projection_check)
