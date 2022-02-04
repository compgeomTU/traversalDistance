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
    print(g)
    print(h)

    fsg = FreeSpaceGraph(g, h, e)
    # get random cell boundary
    cb = fsg.cell_boundaries[(0, 0, g, h)]

    fsg.DFSTraversalDist(cb)


def PlotGraph():
    # plots graph to matplotlib
    r = Graph("sample_graphs/R")
    r.Plot2MatPlotLib()


if __name__ == "__main__":
    testFreeSpaceGraph()
