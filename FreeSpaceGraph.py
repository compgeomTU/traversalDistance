"""
Author:
    Carola Wenk
    cwenk@tulane.edu

Contributors:
    Rena Repenning
    www.renarepenning.com

    Emily Powers
    epowers3@tulane.edu

    Erfan Hosseini Sereshgi
    shosseinisereshgi@tulane.edu
"""


#from types import NoneType
from CalFreeSpace import calfreespace
from LineIntersection import find_ellipse_max_min_points
import logging

class FreeSpaceGraph:
    def __init__(self, g1, g2, epsilon):
        self.g1 = g1  # g1, g2 are Graph objects
        self.g2 = g2
        self.epsilon = epsilon
        self.cell_boundaries = {}
        self.cb_count = len(g2.nodes) * len(g1.edges) + len(g1.nodes) * len(g2.edges)
        self.DFS_calls = 0
                
    def print_cbs(self):
        print("-- Cell Boundaries --\n", print(self.cell_boundaries), "\n")

    """ DFS Diagram: for all neighbors--> for 2 horizontals and one vertical
        boundaries are lined, vertices are in (), the ellipse boundaries are shown without outlining ellipse

            G2 g_edges
                .
                .
                .
 (right vertex) .________________
                |         |  __ .
                |               .
            cb  |   (ellipse)   .
         edge 2 | __            .
                |    |          .
                |_______________..  .  .  .  . G1 g_verts
              (V)     edge 1    (neighbor)
    (left vertex)
    
    """
    def DFS(self, cb, f, p, paths, curr_path): # f is written to a file, p is written for the path
        #new line in f is a new dfs call
        f.write("\n")
        cb.visited = True
        # go thru neighboring edges from given vertexID
        for neighbor in cb.g_verts.nodeLink[cb.vertexID]:
            # Find max/min coords of cb's ellipse
            G1, G2 = cb.g_verts, cb.g_edges
            edge1 = [G1.nodes[cb.vertexID], G1.nodes[neighbor]]
            x, y = G2.edges[cb.edgeID] # pair of vertex ids
            edge2 = [G2.nodes[x], G2.nodes[y]]
            f.write("edge1=" + str(edge1) + "   edge2=" + str(edge2)+"\n")
            min1, max1, min2, max2 = find_ellipse_max_min_points(line1=edge1, line2=edge2, epsilon=self.epsilon)

            # get neighboring edge nodes
            left_vertexID, right_vertexID = cb.g_edges.edges[cb.edgeID]
            for V in [left_vertexID, right_vertexID]:
                """ HORIZONTAL Boundaries --> left_vertex:bottom, right_vertex:top """ 
                if (cb.vertexID, neighbor) in cb.g_verts.edgeHash: 
                    new_edgeID = cb.g_verts.edgeHash[(cb.vertexID, neighbor)] #on vertex graph
                    ### DYNAMIC STEP ###
                    newCB = self.get_cell_boundry(cb.g_edges, V, cb.g_verts, new_edgeID) # creating new cell boundary from "flipping" horiz --> vertical
                    f.write("start + end values: " +
                            str(newCB.start_fs) + " " + str(newCB.end_fs)+"\n")
                    if newCB.visited == False and newCB.start_fs <= newCB.end_fs:
                        p.write("DFS -- add "+str(newCB.print_cellboundary())+"\n")
                        print("horizontal start_p min1:", min1)
                        newCB.start_p = min1  # from block calling ellipse
                        print("horizontal end_p max1:", max1)
                        newCB.end_p = max1
                        logging.info("START_P, END_P: "+ str(newCB.start_p)+ " " + str(newCB.end_p))
                        self.DFS(newCB, f, p, paths,
                                 curr_path+(newCB.add_cd_str()))
                    else:
                        #p.write("DFS -- basecase -> dont return path\n")
                        paths += [curr_path] 
            # end for thru L,R
            """ VERTICAL Boundary"""  
            ### DYNAMIC STEP ###
            newCB = self.get_cell_boundry(cb.g_verts, neighbor, cb.g_edges, cb.edgeID) # connect v's of same type
            f.write("start + end values: " + str(newCB.start_fs) + " " + str(newCB.end_fs)+"\n")
            if newCB.visited == False and newCB.start_fs <= newCB.end_fs:
                f.write("DFS -- add "+str(newCB.print_cellboundary())+"\n")
                print("vertical start_p min2:", min2)
                newCB.start_p = min2  # from block calling ellipse
                print("vertical end_p max2:", max2)
                newCB.end_p = max2 
                # recursive call on the edge that hasn't been called yet
                self.DFS(newCB, f, p, paths, curr_path+(newCB.add_cd_str()))
            else:
                #p.write("DFS -- basecase -> dont return path\n")
                paths += [curr_path] 
        # end for iterating thru Vi
        f.write("\nDFS success!!!\n")
        p.write("paths: "+str(paths)+"\n")


    def compute_union(self, intervals, mycb):
        logging.info("INTERVALS: "+str(intervals))
        sx = mycb.start_p
        ex = mycb.end_p
        logging.info("SX-Compute union:"+str(sx))
        logging.info("EX-Compute union:"+str(ex))
        i = 0
        sxi = -1
        exi = -1
        while i < len(intervals):
            if sxi == -1:
                if sx < intervals[i]:
                    intervals.insert(i,sx)
                    sxi = i
            elif exi == -1:
                if ex < intervals[i]:
                    intervals.insert(i,ex)
                    exi = i
            i+=1
        if sxi == -1 and exi == -1:
            intervals.append(sx)
            intervals.append(ex)
        if sxi != -1 and exi == -1:
            intervals.append(ex)
    
        if sxi % 2 == 0 and exi % 2 == 1:
            intervals = intervals[0:sxi+1] + intervals[exi:]
        elif sxi % 2 == 0 and exi % 2 == 0:
            intervals = intervals[0:sxi+1] + intervals[exi+1:]
        elif sxi % 2 == 1 and exi % 2 == 0:
            intervals = intervals[0:sxi] + intervals[exi+1:]
        elif sxi % 2 == 1 and exi % 2 == 1:
            intervals = intervals[0:sxi] + intervals[exi:]
        intervalsRETURN = []
        #iterate through to reconvert to list of tuples, list comprehension?
        for k in range(0,len(intervals)//2,2):
            intervalsRETURN.append((intervals[k],intervals[k+1]))
        logging.info("intervalsRETURN: "+str(intervalsRETURN))
        return intervalsRETURN

    def check_projection(self):
        # assumes g1 is horiz and g2 is vert
        f = open("outputs/check_projection.txt", "w")
        # all_cbs = { edgeID : output of compute_union }
        all_cbs = {}
        f.write("self.cell_boundaries:\n ")
        f.write(str(self.cell_boundaries)+"\n")
        f.write("self.G1="+str(self.g1)+"\n")
        f.write("\nfor cb in self.cell_boundaries")
        #pick an edge id and only look at contents of that edge id just for a single edge 
        for cb in self.cell_boundaries:
            mycb = self.cell_boundaries[cb]
            f.write("\nmycb="+str(mycb))
            f.write("\n   g_edges="+str(mycb.g_edges))
            #if mycb.g_edges == self.g1:
            if mycb.edgeID in all_cbs:
                f.write("\n   mycb:   edgeID= "+str(mycb.edgeID) +
                        "   start_p= "+str(mycb.start_p)+"   end_p= "+str(mycb.end_p))
                logging.info("ALL CBS "+ str(all_cbs[mycb.edgeID]))
                logging.info("MY CB "+ str(mycb))
                logging.info("EDGEID "+ str(mycb.edgeID))
                if all_cbs[mycb.edgeID] == [(0.0,1.0)]: #if the union of all the processed ranges already covers [0,1] there's no need to include the new range
                    continue
                if mycb.start_p == 0.0 and mycb.end_p == 1.0: #if the new range covers [0,1], this is our new union so no need to find the union between the new range and the previous union
                    all_cbs[mycb.edgeID] = [(0.0,1.0)]
                    continue
                listEdges = list(sum(all_cbs[mycb.edgeID],()))
                logging.info("LISTUP: "+str(all_cbs[mycb.edgeID]))
                logging.info("LISTEDGES: "+str(listEdges))
                all_cbs[mycb.edgeID] = self.compute_union(listEdges, mycb)
                logging.info("INTERVAL: " + str(all_cbs[mycb.edgeID]))
            else:
                # adds first (single white interval)
                # map --> [pairs] --- sorted list of (s,e) pairs will be the val
                all_cbs[mycb.edgeID] = [(mycb.start_p, mycb.end_p)]
        f.write("\n\n for pairs in union:")
        for key in all_cbs:
            intervals = all_cbs[key]
            f.write("\n intervals="+str(intervals))
            # we want intervals to be start=0 and end=1
            if len(intervals) == 1:
                if intervals[0][0] != 0.0 or intervals[0][1] != 1.0:
                    f.write(" --> is false")
                    return False
            else:
                return False
        # if intervals cover all edges
        return True

    def DFSTraversalDist(self):
        # given one free space boundary, compute all adjacent free space boundaries
        f = open("outputs/fsg_dfs.txt", "w")
        p = open("outputs/fsg_path.txt", "w")

        # Horizontal boundaries
        for v in self.g2.nodes.keys():
            for e in self.g1.edges.keys():
                seed_cb = self.get_cell_boundry(self.g2, v, self.g1, e)
                ### check visted 
                if not seed_cb.visited:
                    logging.info("v: " + str(v) + " e: " + str(e) + " seed_cb: " + str(seed_cb))
                    print("DFS", self.DFS(seed_cb, f, p, [], ""))
                    check_projection = self.check_projection()
                    print("Projection check: ", check_projection)
                    self.DFS_calls += 1
                    if check_projection:
                        return True

        # Verticle boundaries
        for v in self.g1.nodes.keys():
            for e in self.g2.edges.keys():
                seed_cb = self.get_cell_boundry(self.g1, v, self.g2, e)
                ### check visited
                if not seed_cb.visited:
                    logging.info("v: " + str(v) + " e: " + str(e) + " seed_cb: " + str(seed_cb))
                    print("DFS", self.DFS(seed_cb, f, p, [], ""))
                    check_projection = self.check_projection()
                    print("Projection check: ", check_projection)
                    self.DFS_calls += 1
                    if check_projection:
                        return True
                
        return False
   
    def get_cell_boundry(self, ga, v, gb, e):
        cb = self.cell_boundaries.get((id(ga), v, id(gb), e))
        if cb is None:
            cb = CellBoundary(ga, v, gb, e, self.epsilon)
            self.cell_boundaries[(id(ga), v, id(gb), e)] = cb
        return cb
    
    def set_cell_boundry(self, ga, v, gb, e):
        self.cell_boundaries[(id(ga), v, id(gb), e)] = CellBoundary(ga, v, gb, e, self.epsilon)

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

        edge = g_edges.edges[self.edgeID]
        # inputs for CFS
        x1 = g_edges.nodes[edge[0]][0]  # --> id of vertex, x-coord
        y1 = g_edges.nodes[edge[0]][1]
        x2 = g_edges.nodes[edge[1]][0]
        y2 = g_edges.nodes[edge[1]][1]
        xa = g_verts.nodes[vertexID][0]
        ya = g_verts.nodes[vertexID][1]

        # call CFS and return tuple --> compute from free space by traversing the free space
        self.start_fs, self.end_fs = calfreespace(
            x1, y1, x2, y2, xa, ya, eps)  # start/end of freespace

    def print_cellboundary(self):
        print("V_ID: " + str(self.vertexID) + " E_ID: " + str(self.edgeID) + " start: " + str(self.start_p) + " end: " + str(self.end_p))

    def add_cd_str(self):
        if self.g_verts.nodes[0][0] == 0 and self.g_verts.nodes[0][1] == -3:
            isRectangleGraph = "v"
        else:
            isRectangleGraph = "u"
        return isRectangleGraph+str(self.vertexID) + "," + str(self.edgeID)+" -> "
