from CalFreeSpace import calfreespace
import pdb


class FreeSpaceGraph:
    def __init__(self, g1, g2):  # g1, g2 are Graph objects
        self.g1 = g1
        self.g2 = g2
        self.cell_boundaries = {}

        # get this dynamically, for each --> given one fsbound print the adgacent
        # Horizontal boundaries
        for e, v in self.g1.edges, self.g2.nodes:
            self.cell_boundaries[(v, e, True)] = CellBoundary(v, e, True)
        # Verticle boundaries
        for e, v in self.g2.edges, self.g1.nodes:
            self.cell_boundaries[(v, e, False)] = CellBoundary(v, e, False)
        print("-- Cell Boundaries --\n", self.cell_boundaries)

        # get traversal distance using dfs search
        # given one free space boundary, compute all adjacent free space boundaries
    
    def DFSTraversalDist(self, cb):
        def DFS(cb):
            # Mark the current node as visited
            cb.visited = True
            # call recursively for all nodes adjacent
            #take vertex id and look at all neighbors 
            if cb.isHoriz == False:
                for neighbour in self.g1.nodeLink[cb.vertexID]: 
                        #for the top
                        vertexID = g2.edges[cb.edgeID][0] #gets the next vertex
                        #get next edge id
                        edgeID = g1.edgeHash[(vertexID, neighbour)] #NOT DONE YET JUST A PSEUDOCODE OUTLINE
                        #for the right traversal
                        newCB = cell_boundaries[(vertexID, edgeID, True)]
                        if newCB.visited == False:
                            self.DFS(newCB)
                        
                        #for the bottom
                        vertexID = g2.edges[cb.edgeID][1] #gets the next vertex
                        #get next edge id
                        edgeID = g1.edgeHash[(vertexID, neighbour)] #NOT DONE YET JUST A PSEUDOCODE OUTLINE
                        newCB = cell_boundaries[(vertexID, edgeID, True)]
                        if newCB.visited == False:
                            self.DFS(newCB)

                        #for the right traversal
                        newCB = cell_boundaries[(neighbour, cb.edgeID, False)]
                        if newCB.visited == False:
                            self.DFS(newCB)

            else: #horizontal need to repeat all the steps ^ but flipped g1 and g2
                for neighbour in self.g2.nodeLink[cb.vertexID]: 
                        #for the top
                        vertexID = g1.edges[cb.edgeID][0] #gets the next vertex
                        #get next edge id
                        edgeID = g2.edgeHash[(vertexID, neighbour)] #NOT DONE YET JUST A PSEUDOCODE OUTLINE
                        #for the right traversal
                        newCB = cell_boundaries[tuple(vertexID, edgeID, False)]
                        if newCB.visited == False:
                            self.DFS(newCB)
                        
                        #for the bottom
                        vertexID = g1.edges[cb.edgeID][1] #gets the next vertex
                        #get next edge id
                        edgeID = g2.edgeHash[(vertexID, neighbour)] #NOT DONE YET JUST A PSEUDOCODE OUTLINE
                        newCB = cell_boundaries[tuple(vertexID, edgeID, False)]
                        if newCB.visited == False:
                            self.DFS(newCB)
                        
                        #for the right traversal
                        newCB = cell_boundaries[tuple(neighbour, cb.edgeID, True)]
                        if newCB.visited == False:
                            self.DFS(newCB)

        # call recursive dfs function
        #for i in self.cell_boundaries:
        #    i.visited = False
        #self.DFS(cb)

    class CellBoundary:
        def _init_(self, vertexID, edgeID, node, isHoriz):
            # use ID's consistant with Erfan's code
            self.vertexID = vertexID
            self.edgeID = edgeID
            self.isHoriz = isHoriz  # True if the edge is from G1
            self.visited = False

            if isHoriz:  # edge is from G1
                g_edge = self.g1
                g_verts = self.g2
            else:  # edge is from G2
                g_edge = self.g2
                g_verts = self.g1

            edge = g_edge.edges[self.edgeID]
            # inputs for CFS
            x1 = g_edge.nodes[edge[0]][1]  # --> id of vertex, x-coord
            y1 = g_edge.nodes[edge[0]][0]
            x2 = g_edge.nodes[edge[1]][1]
            y2 = g_edge.nodes[edge[1]][0]
            xa = g_verts.nodes[vertexID][0]
            ya = g_verts.nodes[vertexID][1]
            # call CFS and return tuple
            # compute from free space by traversing the free space
            self.start, self.end = calFreeSpace(x1, y1, x2, y2, xa, ya)
