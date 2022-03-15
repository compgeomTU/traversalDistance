"""
Author:
    Carola Wenk
    cwenk@tulane.edu

Contributors:
    Rena Repenning
    www.renarepenning.com

    Emily Powers
    epowers3@tulane.edu
"""


from CalFreeSpace import calfreespace
from LineIntersection import find_ellipse_max_min_points


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

    """
    - when in dfs want to see prinout where we are, don't care about ...
    - computing boundaries with each run 
    """

    def DFS(self, cb, paths, curr_path):
        cb.visited = True
        # go thru neighboring edges from given vertexID
        for neighbor in cb.g_verts.nodeLink[cb.vertexID]:
            # get neighboring edges' nodes
            left_vertexID, right_vertexID = cb.g_edges.edges[cb.edgeID]
            for V in [left_vertexID, right_vertexID]:
                # or (V, neighbor) in cb.g_verts.edgeHash:
                if (cb.vertexID, neighbor) in cb.g_verts.edgeHash:
                    new_edgeID = cb.g_verts.edgeHash[(cb.vertexID, neighbor)]
                    # creating new cell boundary from "flipping" horiz --> vertical
                    newCB = self.cell_boundaries[(
                        V, new_edgeID, cb.g_verts, cb.g_edges)]

                    # recursive call on the edge that hasn't been called yet
                    if newCB.visited == False:
                        print("DFS -- add ", end="")
                        newCB.print_cellboundary()  # print visited cb'''
                        self.DFS(newCB, paths, curr_path+(newCB.add_cd_str()))

                    else:
                        print("DFS -- basecase -> dont return path")
                        paths += [curr_path]
                    """ else:
                        print("DFS -- basecase -> return path")
                        
                        # return paths"""

                # connect v's of same type
                newCB = self.cell_boundaries[(
                    neighbor, cb.edgeID, cb.g_edges, cb.g_verts)]
                # recursive call on the edge that hasn't been called yet
                if newCB.visited == False:
                    print("DFS -- add ", end="")
                    newCB.print_cellboundary()  # print visited cb'''
                    self.DFS(newCB, paths, curr_path+(newCB.add_cd_str()))
                else:
                    print("DFS -- basecase -> dont return path")
                    paths += [curr_path]
                    # return paths

        return paths

    def DFSTraversalDist(self, cb):
        '''get traversal distance using dfs search -->  given one free space boundary, compute all adjacent free space boundaries'''
        for i in self.cell_boundaries.values():  # mark all bounds in graph false --> incase this has been ran before
            i.visited = False
        paths = self.DFS(cb, [], "")
        print("\n -- PATHS --  R=rectangle graph X=other")
        for p in paths:
            print(p)
        #
        # or would we want to just track a minimum path distance? instead of tracking all of them?
        #


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
        self.start_fs, self.end_fs = calfreespace(
            x1, y1, x2, y2, xa, ya, eps)  # start/end of freespace

        self.start_p, self.end_p = find_ellipse_max_min_points([], [], eps)

    def print_cellboundary(self):
        print("Cell Boundary: ", self.vertexID, self.edgeID)
        # print("Start: ", self.start)
        # print("End: ", self.end)

    def add_cd_str(self):
        if self.g_verts.nodes[0][0] == 0 and self.g_verts.nodes[0][1] == -3:
            isRectangleGraph = "v"
        else:
            isRectangleGraph = "u"
        return isRectangleGraph+str(self.vertexID) + "," + str(self.edgeID)+" -> "
        """possibly want to add a flag for which graph is first ..."""
