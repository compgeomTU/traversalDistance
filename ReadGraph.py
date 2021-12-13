import geojson
from geojson import LineString, Feature, FeatureCollection
from Graph import Graph
from CalFreeSpace import calfreespace
import FreeSpaceGraph

g = Graph("G")
h = Graph("H")

fsg = FreeSpaceGraph.FreeSpaceGraph(g,h)
cb = fsg.cell_boundaries(0,0,False)
fsg.DFSTraversalDist(cb)
#prints graph objects with no print override 
#print(g)
#print(h)

#gives 2 empty files
#g.Dump2txt("out_g")


