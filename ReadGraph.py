import geojson
from geojson import LineString, Feature, FeatureCollection
from Graph import Graph
from CalFreeSpace import calfreespace
from FreeSpaceGraph import FreeSpaceGraph


def testFreeSpaceGraph():
    print("n\ -- TESTING FreeSpaceGraph.py -- ")
    g = Graph("sample_graphs/G")
    h = Graph("sample_graphs/H")
    e = 2
    # print("-- G: ", g, " -- H: ", h, " -- eps ", e, "")

    fsg = FreeSpaceGraph(g, h, e)
    print("-- created FSG")

    cb = fsg.cell_boundaries[(0, 0, g, h)]
    print("-- take test cell bound:   ", end="")
    cb.print_cellboundary()

    fsg.DFSTraversalDist(cb)
    print("-- END -- \n")

    '''are we just going to traverse the whole thing? or have an end?'''


def PlotGraph():
    # plots graph to matplotlib
    g = Graph("sample_graphs/G")
    g.Plot2MatPlotLib()
    h = Graph("sample_graphs/H")
    h.Plot2MatPlotLib()
    print("-- Graph Plotted --")


if __name__ == "__main__":
    testFreeSpaceGraph()
    # PlotGraph()
