from calfreespace import calfreespace 

class FreeSpaceGraph:
  def __init__(self, g1, g2): # g1, g2 are Graph objects
    self.g1 = g1
    self.g2 = g2
    self.cell_boundaries = {}

    ## get this dynamically, for each --> given one fsbound print the adgacent
    # Horizontal boundaries
    for e, v in self.g1.edges, self.g2.nodes:
      self.cell_boundaries[(e,v,True)] = CellBoundary(v,e,True)
    # Verticle boundaries
    for e, v in self.g2.edges, self.g1.nodes:
      self.cell_boundaries[(e,v,False)] = CellBoundary(v,e,False)
    print("-- Cell Boundaries --\n", self.cell_boundaries)
    
    
    ## get traversal distance
    # searching algorithm?
  
  class CellBoundary:
    def _init_(self, vertexID, edgeID, node, isHoriz):
      # use ID's consistant with Erfan's code
      self.vertexID = vertexID
      self.edgeID = edgeID
      self.node = node
      self.isHoriz = isHoriz # True if the edge is from G1
      
      if isHoriz: # edge is from G1
        g_edge = self.g1
        g_verts = self.g2
      else: # edge is from G2
        g_edge = self.g2
        g_verts = self.g1
        
      edge = g_edge.edges[self.edgeID]
      # inputs for CFS
      x1 = g_edge.nodes[edge[0]][1] # --> id of vertex, x-coord
      y1 = g_edge.nodes[edge[0]][0]
      x2 = g_edge.nodes[edge[1]][1]
      y2 = g_edge.nodes[edge[1]][0]
      xa = g_verts.nodes[vertexID][0]
      ya = g_verts.nodes[vertexID][1]
      # call CFS and return tuple
      self.start, self.end = calFreeSpace(x1, y1, x2, y2, xa, ya) # compute from free space by traversing the free space

      
      
