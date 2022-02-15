import geojson
from geojson import LineString, Feature, FeatureCollection
from Graph import Graph
from CalFreeSpace import calfreespace
from FreeSpaceGraph import FreeSpaceGraph


def testFreeSpaceGraph():
    g = Graph("sample_graphs/G")
    h = Graph("sample_graphs/H")
    e = 2
    # prints graph objects with no print override
    print("-- G: ", g, " -- H: ", h, " -- eps ", e, "")

    fsg = FreeSpaceGraph(g, h, e)
    print("-- created FSG")

    # from g_edges: 0,0,1
    cb = fsg.cell_boundaries[(0, 1, g, h)]
    print("-- created test cell boundary: ", cb.print_cellboundary())

    fsg.DFSTraversalDist(cb)
    print("-- ran DFS")
    '''are we just going to traverse the whole thing? or have an end?'''


def PlotGraph():
    # plots graph to matplotlib
    r = Graph("sample_graphs/R")
    r.Plot2MatPlotLib()


if __name__ == "__main__":
    testFreeSpaceGraph()
