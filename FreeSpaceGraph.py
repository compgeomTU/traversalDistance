from CalFreeSpace import calfreespace
import pdb


class FreeSpaceGraph:
    def __init__(self, g1, g2, epsilon):  # g1, g2 are Graph objects
        self.g1 = g1
        self.g2 = g2
        self.cell_boundaries = {}
        self.epsilon = epsilon

        # get this dynamically, for each --> given one fsbound print the adgacent
        # Horizontal boundaries
        # for e, v in self.g1.edges, self.g2.nodes:
        for v in self.g2.nodes.keys():
            for e in self.g1.edges.keys():
                '''
                use ids to send actual vertices and edges rather than just passing ids
                '''
                self.cell_boundaries[(v, e, True)] = self.CellBoundary(
                    v, e, True)
        # Verticle boundaries
        # for e, v in self.g2.edges, self.g1.nodes:
        for v in self.g1.nodes.keys():
            for e in self.g2.edges.keys():
                self.cell_boundaries[(v, e, False)] = self.CellBoundary(
                    v, e, False)
        print("-- Cell Boundaries --\n", self.cell_boundaries)

        # get traversal distance using dfs search
        # given one free space boundary, compute all adjacent free space boundaries

        def getG1():
            return g1

        def getG2():
            return g2

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
        for i in self.cell_boundaries:
            i.visited = False
        self.DFS(cb)


class CellBoundary:
    '''def __init__(self, vertex, edge, isHoriz):'''

    def __init__(self, vertexID, edgeID, isHoriz):
        # use ID's consistant with Erfan's code
        self.vertexID = vertexID
        self.edgeID = edgeID
        self.isHoriz = isHoriz  # True if the edge is from G1
        self.visited = False

        if isHoriz:  # edge is from G1
            g_edge = super.g1
            g_verts = super.g2
        else:  # edge is from G2
            g_edge = super.g2
            g_verts = super.g1

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
        self.start, self.end = calfreespace(
            x1, y1, x2, y2, xa, ya, super.epsilon)

    def print_cellboundary(self):
        print("Cell Boundary: ", self.vertexID, self.edgeID, self.isHoriz)
        #print("Start: ", self.start)
        #print("End: ", self.end)
