from CalFreeSpace import calfreespace
import pdb  # what is this??????????????


class FreeSpaceGraph:
    def __init__(self, g1, g2, epsilon):
        self.g1 = g1  # g1, g2 are Graph objects
        self.g2 = g2
        self.e = epsilon
        self.cell_boundaries = {}
        '''get these dynamically, for each --> given one fsbound print the adjacent'''
        # Horizontal boundaries
        for v in self.g2.nodes.keys():
            for e in self.g1.edges.keys():
                self.cell_boundaries[(v, e, g1, g2)] = CellBoundary(
                    v, e, g1, g2, self.e)
        # Verticle boundaries
        for v in self.g1.nodes.keys():
            for e in self.g2.edges.keys():
                self.cell_boundaries[(v, e, g2, g1)] = CellBoundary(
                    v, e, g2, g1, self.e)

    def print_cbs(self):
        print("-- Cell Boundaries --\n", print(self.cell_boundaries), "\n")

    def DFS(self, cb, path_dists, curr_path_len):
        cb.print_cellboundary()
        cb.visited = True

        # go thru neighboring edges from given vertexID
        for neighbor in cb.g_verts.nodeLink[cb.vertexID]:
            # get neighboring edges' nodes
            left_vertexID, right_vertexID = cb.g_edges.edges[cb.edgeID]
            for V in [left_vertexID, right_vertexID]:
                new_edgeID = cb.g_verts.edgeHash[(V, neighbor)]
                # creating new cell boundary from "flipping" horiz --> vertical
                newCB = self.cell_boundaries[(
                    V, new_edgeID, cb.g_verts, cb.g_edges)]

                # recursive call on the edge that hasn't been called yet
                if newCB.visited == False:
                    self.DFS(newCB, path_dists, curr_path_len + 1)
                else:
                    path_dists += [curr_path_len]

            # connect v's of same type
            newCB = self.cell_boundaries[(
                neighbor, cb.edgeID, cb.g_edges, cb.g_verts)]
            # recursive call on the edge that hasn't been called yet
            if newCB.visited == False:
                self.DFS(newCB, path_dists, curr_path_len + 1)
            else:
                path_dists += [curr_path_len]

    def DFSTraversalDist(self, cb):
        '''get traversal distance using dfs search -->  given one free space boundary, compute all adjacent free space boundaries'''
        for i in self.cell_boundaries.values():  # mark all bounds in graph false --> incase this has been ran before
            i.visited = False
        self.DFS(cb, [], 0)
        #
        # or would we want to just track a minimum path distance? instead of tracking all of them?
        #
        print("\n done DFS traversal dist fxn")


class CellBoundary:
    def __init__(self, vertexID, edgeID, g_edges, g_verts, eps):
        # use ID's consistant with Erfan's code
        self.vertexID = vertexID
        self.edgeID = edgeID
        self.g_edges = g_edges
        self.g_verts = g_verts
        self.visited = False

        edge = g_edges.edges[self.edgeID]
        # inputs for CFS
        x1 = g_edges.nodes[edge[0]][1]  # --> id of vertex, x-coord
        y1 = g_edges.nodes[edge[0]][0]
        x2 = g_edges.nodes[edge[1]][1]
        y2 = g_edges.nodes[edge[1]][0]
        xa = g_verts.nodes[vertexID][0]
        ya = g_verts.nodes[vertexID][1]
        # call CFS and return tuple --> compute from free space by traversing the free space
        self.start, self.end = calfreespace(
            x1, y1, x2, y2, xa, ya, eps)

    def print_cellboundary(self):
        print("Cell Boundary: ", self.vertexID, self.edgeID)
        # print("Start: ", self.start)
        # print("End: ", self.end)


'''in the beginning when you visit, print each cb for dubugging purposes'''
