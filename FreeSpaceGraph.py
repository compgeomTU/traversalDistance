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

from CellBoundary import CellBoundary
from LineIntersection import find_ellipse_max_min_points
import logging
from Graph import Graph

class FreeSpaceGraph:

    g1: Graph 
    g2: Graph
    epsilon: float
    cell_boundaries: dict

    def __init__(self, g1, g2, epsilon):
        self.g1 = g1  # g1, g2 are Graph objects
        self.g2 = g2
        self.epsilon = epsilon
        self.cell_boundaries = dict()

    @staticmethod
    def compute_union(intervals, mycb):
        logging.info("INTERVALS: "+str(intervals))
        sx = int(mycb.start_p)
        ex = int(mycb.end_p)
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
                    i +=1
                    flag = 1
            elif exi == -1:
                if ex < intervals[i]:
                    intervals.insert(i,ex)
                    exi = i
                    i +=1
                    flag = 2
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
        intervalsRETUP = []

        #iterate through to reconvert to list of tuples, list comprehension?
        for k in range(0,len(intervals)-2):
            intervalsRETUP.append((intervals[k],intervals[k+1]))
        logging.info("intervalsRETUP: "+str(intervalsRETUP))
        return intervalsRETUP

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

                        # check if CB is empty, if so do not recursivly check adjacent FS cell
                        # if non empty recursive call on the edge that hasn't been called yet
                        if newCB.start_fs != -1 and newCB.end_fs != -1:
                            self.DFS(newCB, f, p, paths,curr_path+(newCB.add_cd_str()))
                    else:
                        paths += [curr_path] 
            # end for thru L, R

            """ VERTICAL Boundary"""  
            newCB = self.get_cell_boundry(cb.g_verts, neighbor, cb.g_edges, cb.edgeID) # connect v's of same type
            f.write("start + end values: " + str(newCB.start_fs) + " " + str(newCB.end_fs)+"\n")
            if newCB.visited == False and newCB.start_fs <= newCB.end_fs:
                f.write("DFS -- add "+str(newCB.print_cellboundary())+"\n")
                print("vertical start_p min2:", min2)
                newCB.start_p = min2  # from block calling ellipse
                print("vertical end_p max2:", max2)
                newCB.end_p = max2 

                # check if CB is empty, if so do not recursivly check adjacent FS cell
                # if non empty recursive call on the edge that hasn't been called yet
                if newCB.start_fs != -1 and newCB.end_fs != -1:
                    self.DFS(newCB, f, p, paths, curr_path+(newCB.add_cd_str()))
            else:
                paths += [curr_path] 

        # end for iterating thru Vi
        f.write("\nDFS success!!!\n")
        p.write("paths: "+str(paths)+"\n")

    def DFSTraversalDistance(self, cb):

        # given one free space boundary, compute all adjacent free space boundaries
        self.cell_boundaries = dict()
        f = open("outputs/fsg_dfs.txt", "w")
        p = open("outputs/fsg_path.txt", "w")
        self.DFS(cb, f, p, [], "")
        projection_check = self.check_projection()
        print("Projection check: ", projection_check)

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
                f.write("\n   mycb:   edgeID="+str(mycb.edgeID) +
                        "   start_p="+str(mycb.start_p)+"   end_p="+str(mycb.end_p))
                logging.info("ALL CBS"+ str(all_cbs[mycb.edgeID]))
                logging.info("MY CB"+ str(mycb))
                logging.info("EDGEID"+ str(mycb.edgeID))
                listTup = all_cbs[mycb.edgeID] 
                listEdges = list(sum(listTup,()))
                logging.info("LISTUP: "+str(listTup))
                logging.info("LISTEDGES: "+str(listEdges))
                temp = self.compute_union(listEdges, mycb)
                logging.info("INTERVAL: " + str(temp))
                listTup = temp
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
                if intervals[0][0] != 0 or intervals[0][1] != 1:
                    f.write(" --> is false")
                    return False
            else:
                return False
            
        # if intervals cover all edges
        return True
    
    def brute_force(self):
        self.cell_boundaries = dict()

        # Horizontal boundaries
        for v in self.g2.nodes.keys():
            for e in self.g1.edges.keys():
                self.set_cell_boundry(self.g2, v, self.g1, e)

        # Verticle boundaries
        for v in self.g1.nodes.keys():
            for e in self.g2.edges.keys():
                self.set_cell_boundry(self.g1, v, self.g2, e)
    
    def get_cell_boundry(self, ga, v, gb, e):
        cb = self.cell_boundaries.get((id(ga), v, id(gb), e))
        if cb is None:
            cb = CellBoundary(ga, v, gb, e, self.epsilon)
            self.cell_boundaries[(id(ga), v, id(gb), e)] = cb
        return cb
    
    def set_cell_boundry(self, ga, v, gb, e):
        self.cell_boundaries[(id(ga), v, id(gb), e)] = CellBoundary(ga, v, gb, e, self.epsilon)

    def __str__(self):
        str_ = str()
        for key, value in self.cell_boundaries.items():
            str_ += f"({key[0]}, {key[1]}, {key[2]}, {key[3]}): {value}\n"
        return str_
