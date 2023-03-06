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
from math import sqrt

class CellBoundary:
    def __init__(self, g_verts, vertexID, g_edges, edgeID, eps):

        # use ID's consistant with Erfan's code
        self.vertexID = vertexID
        self.edgeID = edgeID
        self.g_edges = g_edges
        self.g_verts = g_verts
        self.visited = False
        self.start_p = 0
        self.end_p = 0

        # inputs for CFS
        edge = g_edges.edges[self.edgeID]
        x1 = g_edges.nodes[edge[0]][0]  # --> id of vertex, x-coord
        y1 = g_edges.nodes[edge[0]][1]
        x2 = g_edges.nodes[edge[1]][0]
        y2 = g_edges.nodes[edge[1]][1]
        xa = g_verts.nodes[vertexID][0]
        ya = g_verts.nodes[vertexID][1]

        # call CFS and return tuple --> compute from free space by traversing the free space
        self.start_fs, self.end_fs = self.calfreespace(x1, y1, x2, y2, xa, ya, eps)  # start/end of freespace

    @staticmethod
    def calfreespace(x1, y1, x2, y2, xa, ya, Epsilon):
        xdiff = x2-x1
        ydiff = y2-y1
        divisor = xdiff * xdiff + ydiff * ydiff
        if divisor == 0:
            print("divisor =", divisor, "x1 =", x1, "x2 =", x2, "y1 =", y1, "y2 =", y2)
        b = (xa-x1) * xdiff + (ya-y1) * ydiff
        q = (x1 * x1 + y1 * y1 + xa * xa + ya * ya - 2 * x1 * xa - 2 * y1 * ya - Epsilon * Epsilon) * divisor
        root = b * b - q 
        if root < 0:
            start=end=-1 
            return (start, end)
        root = sqrt(root)
        t2 = (b + root) / divisor
        t1 = (b - root) / divisor
        if t1 < 0:
            t1=0
        if t2 < 0:
            t2=0
        if t1 > 1:
            t1=1
        if t2 > 1:
            t2=1
        start = t1
        end = t2
        if start == end:
            start=-1
            end=-1
        return (start, end)
    
    def add_cd_str(self):
        if self.g_verts.nodes[0][0] == 0 and self.g_verts.nodes[0][1] == -3:
            isRectangleGraph = "v"
        else:
            isRectangleGraph = "u"
        return isRectangleGraph+str(self.vertexID) + "," + str(self.edgeID)+" -> "
      
    def print_cellboundary(self):
        print("V_ID: " + str(self.vertexID) + " E_ID: " + str(self.edgeID) + " start: " + str(self.start_p) + " end: " + str(self.end_p))

    def __str__(self):
        return f"|{round(self.start_fs, 3)} --- {round(self.end_fs, 3)}|"