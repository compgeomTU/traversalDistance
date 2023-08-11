from FreeSpaceGraph import FreeSpaceGraph
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math

class Visualize(FreeSpaceGraph):

    def __init__(self, g1, g2, epsilon, filename1=None, filename2=None, log=False):
        super().__init__(g1, g2, epsilon, filename1, filename2, log)

    def plot(self, g1_ids=None, g2_ids=None):

        axs = plt.gca()
        axs.set_aspect('equal', 'datalim')
        
        ########### plotting graphs ##################

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

        ########### plotting freespace ##################

        if g1_ids is None and g1_ids is None:
            g1_edges, g2_edges = self.g1.edges, self.g2.edges

        else: 
            g1_edges = {id: self.g1.edges[id] for id in g1_ids}
            g2_edges = {id: self.g2.edges[id] for id in g2_ids}
        
        # cell iteration
        for g2_id, g2_edge in g2_edges.items():
            for g1_id, g1_edge in g1_edges.items():
                
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

        ########## end plotting freespace component ################

        g1_label = mpatches.Patch(color='black', label=self.filename1)
        g2_label = mpatches.Patch(color='grey', label=self.filename2)

        plt.legend(handles=[g1_label, g2_label], loc='upper left')
        plt.show()