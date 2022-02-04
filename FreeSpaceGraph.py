from CalFreeSpace import calfreespace
import pdb


class FreeSpaceGraph:
    def __init__(self, g1, g2, epsilon):
        self.g1 = g1  # g1, g2 are Graph objects
        self.g2 = g2
        self.e = epsilon
        self.cell_boundaries = {}

        # get this dynamically, for each --> given one fsbound print the adgacent
        # Horizontal boundaries
        for v in self.g2.nodes.keys():
            for e in self.g1.edges.keys():
                '''myKey = v, e, g1, g2'''
                #### self.cell_boundaries[(myKey)] = self.CellBoundary(myKey)
                self.cell_boundaries[(v, e, g1, g2)] = CellBoundary(
                    v, e, g1, g2, self.e)
        # Verticle boundaries
        for v in self.g1.nodes.keys():
            for e in self.g2.edges.keys():
                self.cell_boundaries[(v, e, g2, g1)] = CellBoundary(
                    v, e, g2, g1, self.e)

        '''print("-- Cell Boundaries --\n", print(self.cell_boundaries))'''

        # get traversal distance using dfs search
        # given one free space boundary, compute all adjacent free space boundaries

    def DFSTraversalDist(self, cb):
        def DFS(cb):
            cb.print_cellboundary()
            # Mark the current node as visited
            cb.visited = True
            # call recursively for all nodes adjacent
            # take vertex id and look at all neighbors
            if cb.isHoriz == False:
                for neighbour in self.g1.nodeLink[cb.vertexID]:
                    # for the top
                    # gets the next vertex
                    vertexID = self.g2.edges[cb.edgeID][0]
                    # get next edge id
                    # NOT DONE YET JUST A PSEUDOCODE OUTLINE
                    edgeID = self.g1.edgeHash[(vertexID, neighbour)]
                    # for the right traversal
                    newCB = self.cell_boundaries[(vertexID, edgeID, True)]
                    if newCB.visited == False:
                        self.DFS(newCB)

                    # for the bottom
                    # gets the next vertex
                    vertexID = self.g2.edges[cb.edgeID][1]
                    # get next edge id
                    # NOT DONE YET JUST A PSEUDOCODE OUTLINE
                    edgeID = self.g1.edgeHash[(vertexID, neighbour)]
                    newCB = self.cell_boundaries[(vertexID, edgeID, True)]
                    if newCB.visited == False:
                        self.DFS(newCB)

                    # for the right traversal
                    newCB = self.cell_boundaries[(neighbour, cb.edgeID, False)]
                    if newCB.visited == False:
                        self.DFS(newCB)

            else:  # horizontal need to repeat all the steps ^ but flipped g1 and g2
                for neighbour in self.g2.nodeLink[cb.vertexID]:
                    # for the left
                    # gets the next vertex
                    vertexID = self.g1.edges[cb.edgeID][0]
                    # get next edge id
                    # NOT DONE YET JUST A PSEUDOCODE OUTLINE
                    edgeID = self.g2.edgeHash[(vertexID, neighbour)]
                    # for the right traversal
                    newCB = self.cell_boundaries[tuple(
                        vertexID, edgeID, False)]
                    if newCB.visited == False:
                        self.DFS(newCB)

                    # for the right
                    # gets the next vertex
                    vertexID = self.g1.edges[cb.edgeID][1]
                    # get next edge id
                    # NOT DONE YET JUST A PSEUDOCODE OUTLINE
                    edgeID = self.g2.edgeHash[(vertexID, neighbour)]
                    newCB = self.cell_boundaries[tuple(
                        vertexID, edgeID, False)]
                    if newCB.visited == False:
                        self.DFS(newCB)

                    # for the top traversal
                    newCB = self.cell_boundaries[tuple(
                        neighbour, cb.edgeID, True)]
                    if newCB.visited == False:
                        self.DFS(newCB)

        # call recursive dfs function (this is now the DFSTraversalDist function)
        for i in self.cell_boundaries.values():
            i.visited = False
        self.DFS(cb)

        print("\ndone DFS traversal dist fxn")


class CellBoundary:

    def __init__(self, vertexID, edgeID, g_edge, g_verts, eps):
        # use ID's consistant with Erfan's code
        self.vertexID = vertexID
        self.edgeID = edgeID
        self.visited = False

        edge = g_edge.edges[self.edgeID]
        # inputs for CFS
        x1 = g_edge.nodes[edge[0]][1]  # --> id of vertex, x-coord
        y1 = g_edge.nodes[edge[0]][0]
        x2 = g_edge.nodes[edge[1]][1]
        y2 = g_edge.nodes[edge[1]][0]
        xa = g_verts.nodes[vertexID][0]
        ya = g_verts.nodes[vertexID][1]
        # call CFS and return tuple --> compute from free space by traversing the free space
        self.start, self.end = calfreespace(
            x1, y1, x2, y2, xa, ya, eps)

    def print_cellboundary(self):
        print("Cell Boundary: ", self.vertexID, self.edgeID, self.isHoriz)
        #print("Start: ", self.start)
        #print("End: ", self.end)
