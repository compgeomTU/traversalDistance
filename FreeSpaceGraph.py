from calfreespace import calfreespace 
#make file for it

class FreeSpaceGraph: # get this dynamically, for each --> given one fsbound print the adgacent
  def __init__(self, g1, g2): # g1, g2 are Graph objects
    self.g1 = g1
    self.g2 = g2
    self.cell_boundaries = {}

    # Horizontal boundaries
    for e, v in self.g1.edges, self.g2.nodes:
      self.cell_boundaries[(e,v,True)] = CellBoundary(v,e,True)
    # verticle boundaries
    for e, v in self.g2.edges, self.g1.nodes:
      self.cell_boundaries[(e,v,False)] = CellBoundary(v,e,False)

  
  class CellBoundary:
    def _init_(self, vertexID, edgeID, node, isHoriz):
      # use ID's consistant with Erfan's code
      self.vertexID = vertexID
      self.edgeID = edgeID
      self.node = node
      self.isHoriz = isHoriz # True if the edge is from G1
      
      edge = self.g1.edges[self.edgeID]
      # inputs for CFS
      x1 = self.g1.nodes[edge[0]][1] # --> id of vertex, x-coord
      y1 = self.g1.nodes[edge[0]][0]
      x2 = self.g1.nodes[edge[1]][1]
      y2 = self.g1.nodes[edge[1]][0]
      xa = self.g2.nodes[vertexID][0]
      ya = self.g2.nodes[vertexID][1]
      # call CFS and return tuple
      self.start, self.end = calFreeSpace(x1, y1, x2, y2, xa, ya) # compute from free space by traversing the free space
