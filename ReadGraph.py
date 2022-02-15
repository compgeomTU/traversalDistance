import geojson
from geojson import LineString, Feature, FeatureCollection
from Graph import Graph
from CalFreeSpace import calfreespace
from FreeSpaceGraph import FreeSpaceGraph


def testFreeSpaceGraph():
    g = Graph("sample_graphs/G")
    h = Graph("sample_graphs/H")
    e = 2
    # print("-- G: ", g, " -- H: ", h, " -- eps ", e, "")

    fsg = FreeSpaceGraph(g, h, e)
    print("-- created FSG")

    #cbs = fsg.cell_boundaries.keys()

    cb = fsg.cell_boundaries[(0, 0, g, h)]
    print("-- take test cell bound:   ", end="")
    cb.print_cellboundary()

    fsg.DFSTraversalDist(cb)
    print("-- ran DFS")
    '''are we just going to traverse the whole thing? or have an end?'''


def PlotGraph():
    # plots graph to matplotlib
    r = Graph("sample_graphs/R")
    r.Plot2MatPlotLib()


if __name__ == "__main__":
    testFreeSpaceGraph()
