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

    Will Rodman
    wrodman@tulane.edu
"""

from CalFreeSpace import calfreespace
from LineIntersection import find_ellipse_max_min_points
import logging
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import math

sys.setrecursionlimit(10000)

class FreeSpaceGraph:
    def __init__(self, g1, g2, epsilon, filename1=None, filename2=None, log=False):
        self.g1 = g1  # g1, g2 are Graph objects
        self.g2 = g2
        self.epsilon = epsilon
        self.cell_boundaries = {}
        self.cb_count = len(g2.nodes) * len(g1.edges) + len(g1.nodes) * len(g2.edges)
        self.DFS_calls = 0
        self.filename1 = filename1
        self.filename2 = filename2
        self.log = log

        # logging setup
        if self.log:
            self.traversal_logger = logging.getLogger('traversal')
            self.dfs_logger = logging.getLogger('dfs')
            self.path_logger = logging.getLogger('path')
            self.projection_logger = logging.getLogger('projection')

            self.traversal_logger.setLevel(logging.INFO)
            self.dfs_logger.setLevel(logging.INFO)
            self.path_logger.setLevel(logging.INFO)
            self.projection_logger.setLevel(logging.INFO)

            traversal_log_handler = logging.FileHandler('logs/traversal.log', mode='w')
            dfs_log_handler = logging.FileHandler('logs/dfs.log', mode='w')
            path_log_handler = logging.FileHandler('logs/path.log', mode='w')
            projection_log_handler = logging.FileHandler('logs/projection.log', mode='w')

            traversal_log_handler.setLevel(logging.INFO)
            dfs_log_handler.setLevel(logging.INFO)
            path_log_handler.setLevel(logging.INFO)
            projection_log_handler.setLevel(logging.INFO)

            log_format = logging.Formatter('%(message)s')

            traversal_log_handler.setFormatter(log_format)
            dfs_log_handler.setFormatter(log_format)
            path_log_handler.setFormatter(log_format)
            projection_log_handler.setLevel(logging.INFO)

            self.traversal_logger.addHandler(traversal_log_handler)
            self.dfs_logger.addHandler(dfs_log_handler)
            self.path_logger.addHandler(path_log_handler)
            self.projection_logger.addHandler(projection_log_handler)
              
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
    def DFS(self, cb, paths, curr_path): # f is written to a file, p is written for the path
        #new line in f is a new dfs call
        if self.log: self.dfs_logger.info("\n")
        cb.visited = True
        # go thru neighboring edges from given vertexID
        for neighbor in cb.g_verts.nodeLink[cb.vertexID]:
            # Find max/min coords of cb's ellipse
            G1, G2 = cb.g_verts, cb.g_edges
            edge1 = [G1.nodes[cb.vertexID], G1.nodes[neighbor]]
            x, y = G2.edges[cb.edgeID] # pair of vertex ids
            edge2 = [G2.nodes[x], G2.nodes[y]]
            if self.log: self.dfs_logger.info("edge1=" + str(edge1) + "   edge2=" + str(edge2)+"\n")
            min1, max1, min2, max2 = find_ellipse_max_min_points(line1=edge1, line2=edge2, epsilon=self.epsilon)

            # get neighboring edge nodes
            left_vertexID, right_vertexID = cb.g_edges.edges[cb.edgeID]
            for V in [left_vertexID, right_vertexID]:
                """ HORIZONTAL Boundaries --> left_vertex:bottom, right_vertex:top """ 
                if (cb.vertexID, neighbor) in cb.g_verts.edgeHash: 
                    new_edgeID = cb.g_verts.edgeHash[(cb.vertexID, neighbor)] #on vertex graph
                    newCB = self.get_cell_boundry(cb.g_edges, V, cb.g_verts, new_edgeID) # creating new cell boundary from "flipping" horiz --> vertical
                    if self.log: self.dfs_logger.info("start + end values: " + str(newCB.start_fs) + " " + str(newCB.end_fs)+"\n")
                    if newCB.visited == False and newCB.start_fs <= newCB.end_fs:
                        newCB.start_p = min1  # from block calling ellipse
                        newCB.end_p = max1
                        if self.log:
                            self.path_logger.info("DFS -- add "+str(newCB.print_cellboundary())+"\n")
                            self.traversal_logger.info("START_P, END_P: "+ str(newCB.start_p)+ " " + str(newCB.end_p))
                        self.DFS(newCB, paths, curr_path+(newCB.add_cd_str()))
                    else:
                        if self.log: self.path_logger.info("DFS -- basecase -> dont return path\n")
                        paths += [curr_path] 
            # end for thru L,R
            """ VERTICAL Boundary"""  
            newCB = self.get_cell_boundry(cb.g_verts, neighbor, cb.g_edges, cb.edgeID) # connect v's of same type
            if self.log: self.dfs_logger.info("start + end values: " + str(newCB.start_fs) + " " + str(newCB.end_fs)+"\n")
            if newCB.visited == False and newCB.start_fs <= newCB.end_fs:
                if self.log: self.dfs_logger.info("DFS -- add "+str(newCB.print_cellboundary())+"\n")
                newCB.start_p = min2  # from block calling ellipse
                newCB.end_p = max2 
                # recursive call on the edge that hasn't been called yet
                self.DFS(newCB, paths, curr_path+(newCB.add_cd_str()))
            else:
                if self.log: self.path_logger.info("DFS -- basecase -> dont return path\n")
                paths += [curr_path] 
        # end for iterating thru Vi
        if self.log:
            self.dfs_logger.info("\nDFS success!!!\n")
            self.path_logger.info("paths: "+str(paths)+"\n")

    def compute_union(self, intervals, mycb):
        sx = mycb.start_p
        ex = mycb.end_p
        if self.log:
            self.traversal_logger.info("INTERVALS: "+str(intervals))
            self.traversal_logger.info("SX-Compute union:"+str(sx))
            self.traversal_logger.info("EX-Compute union:"+str(ex))
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
        if self.log: self.traversal_logger.info("intervalsRETURN: "+str(intervalsRETURN))
        return intervalsRETURN

    def check_projection(self):
        # assumes g1 is horiz and g2 is vert
        all_cbs = {}
        if self.log:
            self.projection_logger.info("self.cell_boundaries:\n ")
            self.projection_logger.info(str(self.cell_boundaries)+"\n")
            self.projection_logger.info("self.G1="+str(self.g1)+"\n")
            self.projection_logger.info("\nfor cb in self.cell_boundaries")
        #pick an edge id and only look at contents of that edge id just for a single edge 
        for cb in self.cell_boundaries:
            mycb = self.cell_boundaries[cb]
            if self.log:
                self.projection_logger.info("\nmycb="+str(mycb))
                self.projection_logger.info("\n   g_edges="+str(mycb.g_edges))
            if mycb.edgeID in all_cbs:
                if self.log:
                    self.projection_logger.info("\n   mycb:   edgeID= "+str(mycb.edgeID) + "   start_p= "+str(mycb.start_p)+"   end_p= "+str(mycb.end_p))
                    self.traversal_logger.info("ALL CBS "+ str(all_cbs[mycb.edgeID]))
                    self.traversal_logger.info("MY CB "+ str(mycb))
                    self.traversal_logger.info("EDGEID "+ str(mycb.edgeID))
                if all_cbs[mycb.edgeID] == [(0.0,1.0)]: #if the union of all the processed ranges already covers [0,1] there's no need to include the new range
                    continue
                if mycb.start_p == 0.0 and mycb.end_p == 1.0: #if the new range covers [0,1], this is our new union so no need to find the union between the new range and the previous union
                    all_cbs[mycb.edgeID] = [(0.0,1.0)]
                    continue
                listEdges = list(sum(all_cbs[mycb.edgeID],()))
                all_cbs[mycb.edgeID] = self.compute_union(listEdges, mycb)

                if self.log:
                    self.traversal_logger.info("LISTUP: "+str(all_cbs[mycb.edgeID]))
                    self.traversal_logger.info("LISTEDGES: "+str(listEdges))
                    self.traversal_logger.info("INTERVAL: " + str(all_cbs[mycb.edgeID]))
            else:
                # adds first (single white interval)
                # map --> [pairs] --- sorted list of (s,e) pairs will be the val
                all_cbs[mycb.edgeID] = [(mycb.start_p, mycb.end_p)]
        if self.log: self.projection_logger.info("\n\n for pairs in union:")
        for key in all_cbs:
            intervals = all_cbs[key]
            #self.projection_logger.info("\n intervals="+str(intervals))
            # we want intervals to be start=0 and end=1
            if len(intervals) == 1:
                if intervals[0][0] != 0.0 or intervals[0][1] != 1.0:
                    if self.log: self.projection_logger.info(" --> is false")
                    return False
            else:
                return False
        # if intervals cover all edges
        return True

    def DFSTraversalDist(self):
        # given one free space boundary, compute all adjacent free space boundaries

        # Horizontal boundaries
        for v in self.g2.nodes.keys():
            for e in self.g1.edges.keys():
                seed_cb = self.get_cell_boundry(self.g2, v, self.g1, e)
                ### check visted 
                if not seed_cb.visited:
                    if self.log: self.traversal_logger.info("v: " + str(v) + " e: " + str(e) + " seed_cb: " + str(seed_cb))
                    self.DFS(seed_cb, [], "")
                    check_projection = self.check_projection()
                    self.DFS_calls += 1
                    if check_projection:
                        return True

        # Verticle boundaries
        for v in self.g1.nodes.keys():
            for e in self.g2.edges.keys():
                seed_cb = self.get_cell_boundry(self.g1, v, self.g2, e)
                ### check visited
                if not seed_cb.visited:
                    if self.log: self.traversal_logger.info("v: " + str(v) + " e: " + str(e) + " seed_cb: " + str(seed_cb))
                    self.DFS(seed_cb, [], "")
                    check_projection = self.check_projection()
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
        self.cell_boundaries[(ga, v, gb, e)] = CellBoundary(ga, v, gb, e, self.epsilon)

    def plot(self):
        axs = plt.gca()
        axs.set_aspect('equal', 'datalim')

        G_n = list()

        for id, edge in self.g1.edges.items():
            n1_id, n2_id = edge[0], edge[1]
            n1, n2 = self.g1.nodes[n1_id], self.g1.nodes[n2_id]

            if n1 not in G_n: G_n.append(n1)
            if n2 not in G_n: G_n.append(n2)

            plt.plot([n1[0], n2[0]], [n1[1], n2[1]], color='black', linewidth=1.5)

        lons, lats = map(list, zip(*G_n))
        plt.scatter(lons, lats, s=12, c='black')

        for id, edge in self.g2.edges.items():
            n1_id, n2_id = edge[0], edge[1]
            n1, n2 = self.g2.nodes[n1_id], self.g2.nodes[n2_id]
            plt.plot([n1[0], n2[0]], [n1[1], n2[1]], color='grey', linewidth=1.5)

        ########### plotting freespace component ##################

        # single cell condition
        g1_id, g2_id = 0, 1
        g1_edge, g2_edge = self.g1.edges[g1_id], self.g2.edges[g2_id]

        # cell iteration
        #for g2_id, g2_edge in self.g2.edges.items():
            #for g1_id, g1_edge in self.g1.edges.items():

        # dummy ittr
        for i in [0]:
                
                # horizonal lower CB
                cb_1 = self.get_cell_boundry(self.g2, g2_edge[0], self.g1, g1_id)

                # vertical right CB
                cb_2 = self.get_cell_boundry(self.g1, g1_edge[0], self.g2, g2_id)

                # horizonal upper CB
                cb_3 = self.get_cell_boundry(self.g2, g2_edge[1], self.g1, g1_id)

                # vetical left CB
                cb_4 = self.get_cell_boundry(self.g1, g1_edge[1], self.g2, g2_id)

                g1_n1_id, g1_n2_id = g1_edge[0], g1_edge[1]
                g1_n1_x, g1_n2_x = self.g1.nodes[g1_n1_id][0], self.g1.nodes[g1_n2_id][0]
                g1_n1_y, g1_n2_y = self.g1.nodes[g1_n1_id][1], self.g1.nodes[g1_n2_id][1]

                g2_n1_id, g2_n2_id = g2_edge[0], g2_edge[1]
                g2_n1_x, g2_n2_x = self.g2.nodes[g2_n1_id][0], self.g2.nodes[g2_n2_id][0]
                g2_n1_y, g2_n2_y = self.g2.nodes[g2_n1_id][1], self.g2.nodes[g2_n2_id][1]

                # map normal square to quadralateral
                points = list()

                # map horizonal lower CB (1)
                cb_1_x = lambda cb: (g2_n2_x - g2_n1_x) * cb + g2_n1_x
                cb_1_y = lambda cb: (g2_n2_y - g2_n1_y) * cb + g2_n1_y

                if cb_1:
                    if cb_1.start_fs != -1.0:
                        point = (cb_1_x(cb_1.start_fs), cb_1_y(cb_1.start_fs))
                        points.append(point)

                    if cb_1.end_fs != -1.0:
                        point = (cb_1_x(cb_1.end_fs), cb_1_y(cb_1.end_fs))
                        points.append(point)

                # map vert right CB (2)
                cb_2_x = lambda cb: (g1_n1_x - g2_n1_x) * cb + g2_n1_x
                cb_2_y = lambda cb: (g1_n1_y - g2_n1_y) * cb + g2_n1_y

                if cb_2:
                    if cb_2.start_fs != -1.0:
                        point = (cb_2_x(cb_2.start_fs), cb_2_y(cb_2.start_fs))
                        points.append(point)

                    if cb_2.end_fs != -1.0:
                        point = (cb_2_x(cb_2.end_fs), cb_2_y(cb_2.end_fs))
                        points.append(point)

                # map horizonal upper CB (3)
                cb_3_x = lambda cb: (g1_n2_x - g1_n1_x) * cb + g1_n1_x
                cb_3_y = lambda cb: (g1_n2_y - g1_n1_y) * cb + g1_n1_y

                if cb_3:
                    if cb_3.start_fs != -1.0:
                        point = (cb_3_x(cb_3.start_fs), cb_3_y(cb_3.start_fs))
                        points.append(point)

                    if cb_3.end_fs != -1.0:
                        point = (cb_3_x(cb_3.end_fs), cb_3_y(cb_3.end_fs))
                        points.append(point)
                
                # map vert right CB (2)
                cb_4_x = lambda cb: (g1_n2_x - g2_n2_x) * cb + g2_n2_x
                cb_4_y = lambda cb: (g1_n2_y - g2_n2_y) * cb + g2_n2_y

                if cb_4:
                    if cb_4.start_fs != -1.0:
                        point = (cb_4_x(cb_4.start_fs), cb_4_y(cb_4.start_fs))
                        points.append(point)

                    if cb_4.end_fs != -1.0:
                        point = (cb_4_x(cb_4.end_fs), cb_4_y(cb_4.end_fs))
                        points.append(point)

                # verify polygon (not line)
                if len(points) > 2: 

                    # sorting coords 
                    cent=(sum([p[0] for p in points])/len(points),sum([p[1] for p in points])/len(points))
                    points.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))

                    xs, ys = list(zip(*points))    
                    axs.fill(xs, ys, alpha=0.3, fc='r', ec='none')

        # python3 main.py samples/paris/arc_de_triomphe samples/paris/vehicle 5 -p
        ########## end plotting freespace component ################

        g1_label = mpatches.Patch(color='black', label=self.filename1)
        g2_label = mpatches.Patch(color='grey', label=self.filename2)

        plt.legend(handles=[g1_label, g2_label], loc='upper left')
        plt.show()

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
        return "V_ID: " + str(self.vertexID) + " E_ID: " + str(self.edgeID) + " start: " + str(self.start_p) + " end: " + str(self.end_p)

    def add_cd_str(self):
        return f"({self.vertexID}, {self.edgeID}) -> "

