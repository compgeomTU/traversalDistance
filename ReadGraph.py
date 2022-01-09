import geojson
from geojson import LineString, Feature, FeatureCollection
from Graph import Graph
from CalFreeSpace import calfreespace
import FreeSpaceGraph

def FreeSpaceGraph():
    g = Graph("sample_graphs/G")
    h = Graph("sample_graphs/H")
    e = 2
    fsg = FreeSpaceGraph.FreeSpaceGraph(g,h,e)
    cb = fsg.cell_boundaries(0,0,False)
    fsg.DFSTraversalDist(cb)
    #prints graph objects with no print override
    #print(g)
    #print(h)

<<<<<<< HEAD
def PlotGraph():
=======
def PlotGraph()
>>>>>>> 8ee4ee966470caee2a0c464fcced4b831c1c1b49
    #plots graph to matplotlib
    r = Graph("sample_graphs/R")
    r.Plot2MatPlotLib()

if __name__ == "__main__":
    pass
