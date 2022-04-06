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

    def DFS(self, cb):  # , paths, curr_path):
        cb.visited = True
        # go thru neighboring edges from given vertexID
        for neighbor in cb.g_verts.nodeLink[cb.vertexID]:
            # Find max/min coords of cb's ellipse
            G1, G2 = cb.g_verts, cb.g_edges
            edge1 = [G1.nodes[cb.vertexID],
                     G1.nodes[neighbor]]
            x, y = G2.edges[cb.edgeID]  # pair of vertex ids
            edge2 = [G2.nodes[x], G2.nodes[y]]
            print("edge1=", edge1, "   edge2=", edge2)
            min1, max1, min2, max2 = find_ellipse_max_min_points(
                line1=edge1, line2=edge2, epsilon=self.e)

            # get neighboring edge nodes
            left_vertexID, right_vertexID = cb.g_edges.edges[cb.edgeID]
            for V in [left_vertexID, right_vertexID]:
                """ CASE 1 """
                if (cb.vertexID, neighbor) in cb.g_verts.edgeHash:
                    new_edgeID = cb.g_verts.edgeHash[(cb.vertexID, neighbor)]
                    newCB = self.cell_boundaries[(
                        V, new_edgeID, cb.g_verts, cb.g_edges)]  # creating new cell boundary from "flipping" horiz --> vertical
                    print("start + end values: ",
                          newCB.start_fs, " ", newCB.end_fs)

                    if newCB.visited == False and newCB.start_fs < newCB.end_fs:
                        # print("DFS -- add ", end="")
                        # newCB.print_cellboundary()
                        newCB.start_p = min1  # from block calling ellipse
                        newCB.end_p = max1
                        # , paths, curr_path+(newCB.add_cd_str()))
                        self.DFS(newCB)
                    # else:
                    #     print("DFS -- basecase -> dont return path")
                    #     paths += [curr_path]
                """ CASE 2 """
                newCB = self.cell_boundaries[(
                    neighbor, cb.edgeID, cb.g_edges, cb.g_verts)]  # connect v's of same type

                print("start + end values: ", newCB.start_fs, " ", newCB.end_fs)
                if newCB.visited == False and newCB.start_fs < newCB.end_fs:
                    print("DFS -- add ", end="")
                    newCB.print_cellboundary()
                    newCB.start_p = min2  # from block calling ellipse
                    newCB.end_p = max2
                    # recursive call on the edge that hasn't been called yet
                    self.DFS(newCB)  # , curr_path+(newCB.add_cd_str()))
                # else:
                #     print("DFS -- basecase -> dont return path")
                #     paths += [curr_path]
            # end for thru L,R
        # end for iterating thru Vi

        """ check_projection here """

        return " success "

    def DFSTraversalDist(self, cb):
        for i in self.cell_boundaries.values():  # mark all bounds in graph false --> incase this has been ran before
            i.visited = False
        # given one free space boundary, compute all adjacent free space boundaries
        self.DFS(cb)
        # paths = self.DFS(cb, [], "")
        # print("\n -- PATHS --  R=rectangle graph X=other")
        # for p in paths:
        #     print(p)

    def check_projection(self, g1, g2):
        """ assumes g1 is horiz and g2 is vert """
        union = {}
        for cb in self.cell_boundaries:
            if cb.edgeID in g1:
                if cb.edgeID in union:
                    localMin = min(union[(cb.edgeID[0], cb.start_p)])
                    localMax = max(union[(cb.edgeID[1], cb.end_p)])
                    union[cb.edgeID] = (localMin, localMax)
                else:
                    union[cb.edgeID] = (cb.start_p, cb.end_p)
        for pairs in union:
            if pairs[0] != 0 or pairs[1] != 1:
                """ should this be > or < ?? """
                return False

        return True

    # TODO: 4/5
    # comment out all the path code --> not ultimately returning them , j creating the structures
    # - write this function .... erfan: do as you are making the cb's so you dont have to do it later ...
    #  ... needs to go after we call dfs (not recursive), post everything
    #  ... will return True or False to check projection ....
    # * go thru cb's dict and make another dictionary for that and then each key will be corrospondant to the edge id of the edges in graph 1
    #  ... (only care about graph 1) then just go thru cbs, look at min/max and find local minima/maxima and update the cb's attribute
    # dict maps edge_it to the global min/max in respect to e
    # for all edges in g1's cbs: == all cb's where edges belong to g1
    #     if edge has edge_id(e) in common
    #         # find the union of all those e common in g1
    #         take min of all mins  --? minX
    #         max of all maxsw --> maxX
    #
    # - going to go thry all cb's and make an array of all edge ids and then assign
    # the min and maxs of all the things we have
    # - how to init??


class CellBoundary:
    def __init__(self, vertexID, edgeID, g_edges, g_verts, eps):
        # use ID's consistant with Erfan's code
        self.vertexID = vertexID
        self.edgeID = edgeID
        self.g_edges = g_edges
        self.g_verts = g_verts
        self.visited = False
        self.start_p = -1
        self.end_p = -1

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
