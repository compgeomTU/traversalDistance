# ext file in command line:
# python3 sample_3d_visualizer.py

# Considering the way that planes are constructed using np.meshgrid,
# I have realized a solution to stitching ajacent planes together in matplotlib
# might by building the planes using equations in polar coods.
#
# These planes will be translated into rectangular coords before being plotted
# inorder to keep the general space in rectangular coords. Because of the
# limited precision of Floating Point numbers, translation from
# (r, 0, z) ~> (x, y, z) will force irrational numebers stored in trigometric
# funtions/pi notation to be tranclated to rational numbers.
#
# This facts is seemily irrevlevent consdering the NumPy engine must
# imput all values into the matplotlib engine using rectangular coords, however,
# this translation will cause coord points to diverge from their true orgin
# (there where problems finding duplicate points beccause of this is the
# Frechet lib).
#
# Once planes exits in general space, their free space can be plotted using
# liniar transformation functions such that (u, v, w) -> (x, y, z) for an
# ellipse (will actually be a polygon) planes cordionding cell plane.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from mpl_toolkits.mplot3d import Axes3D
import io
from PIL import Image
import matplotlib.image as image
import math
from Graph import Graph

def example_cells():
    ax = plt.subplot(projection='3d')

    cell = np.linspace(0, 1, 10)

    y, z = np.meshgrid(cell, cell)

    x = y * 0
    S1 = (x, y, z)

    x = y * -0.5
    S2 = (x, y, z)

    x = y * 0.5
    S3 = (x, y, z)

    ax.plot_surface(S1[0], S1[1], S1[2], color="lightgray")
    ax.plot_surface(S2[0], S2[1], S2[2], color="lightgray")
    ax.plot_surface(S3[0], S3[1], S3[2], color="lightgray")

    xLabel = ax.set_xlabel('X')
    yLabel = ax.set_ylabel('Y')
    zLabel = ax.set_zlabel('Z')

    plt.show()

def polar_degree(n):

    # spine of cells ranging from 0 <= theda <= pi
    # theda is in radian form
    theta = np.linspace(0, 1, n) * np.pi

    # costant lenght of cells
    r = np.full(shape=n, fill_value=1, dtype=np.float)

    # converting polar coordiantes to cartesian coordiantes
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    plt.scatter(x, y)

    plt.show()

def texture_map():

    # sample figure
    plt.figure(figsize=(10, 10), dpi=20)
    ax = plt.axes()
    ax.set_facecolor("grey")

    freespace_struct = np.array([[0, 0], [0, 0.25], [0.25, 0],
                                 [0, 1], [0.25, 1], [0, 0.75],
                                 [1, 1], [1, 0.75], [0.75, 1],
                                 [1, 0], [0.75, 0], [1, 0.25]
                                ])

    freespace_poly_0 = plt.Polygon(freespace_struct[:3, :], color='white')
    plt.gca().add_patch(freespace_poly_0)

    freespace_poly_1 = plt.Polygon(freespace_struct[3:6, :], color='white')
    plt.gca().add_patch(freespace_poly_1)

    freespace_poly_2 = plt.Polygon(freespace_struct[6:9, :], color='white')
    plt.gca().add_patch(freespace_poly_2)

    freespace_poly_3 = plt.Polygon(freespace_struct[9:, :], color='white')
    plt.gca().add_patch(freespace_poly_3)
    # write figure to memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.clf()
    buf.seek(0)

    # read figure from buffer
    im = image.imread(buf)


    xp, yp, __ = im.shape

    x = np.arange(0, xp, 1)
    y = np.arange(0, yp, 1)
    Y, X = np.meshgrid(y, x)
    Z = X * 0.5

    ax = plt.gca(projection='3d')
    ax.plot_surface(X, Y, Z, facecolors=im)
    plt.show()

def graph_2d_plot():

    # edges
    # e: dict of edge {e_n: (x_n, y_n)}
    e = {1: (1.5, 1.5),
        2: (3.5, 4),
        3: (4.5, 6),
        4: (4.5, 10),
        5: (8, 8),
        6: (10, 13),
        7: (9, 15),
        }

    # verticies
    # v: list of edge pairs (e1 ,e2) that make up verticies
    v = [(1 ,2), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (4, 7)]

    for i in v:
        e1 = e[i[0]]
        e2 = e[i[1]]
        plt.plot([e1[0], e2[0]], [e1[1], e2[1]], color ='blue', linewidth=3)

    for k, v_ in e.items():
        plt.scatter([v_[0]], [v_[1]], s=200, c='red')

        plt.annotate(f"e_{k}", v_, textcoords="offset points", xytext=(25,0), ha='center')

    plt.show()

def graph_3d_plot():
    # build graph and then add z-axis to the matplotlib engine
    # paramitization will build verticies as cells
    # once graph is in 3d, example images can be transformed to the cell meshgrids

    # edges
    # e: dict of edge {e_n: (x_n, y_n)}
    e = {1: (1.5, 1.5, 0.5),
        2: (3.5, 4, 0.5),
        3: (4.5, 6, 1),
        4: (4.5, 10, 1.5),
        5: (8, 8, 2),
        6: (10, 13, 2),
        7: (9, 15, 3),
        }

    # verticies
    # v: list of edge pairs (e1 ,e2) that make up verticies
    v = [(1 ,2), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (4, 7)]

    ax = plt.gca(projection='3d')

    for i in v:
        x0 = e[i[0]][0]
        y0 = e[i[0]][1]
        z0 = e[i[0]][2]

        x1 = e[i[1]][0]
        y1 = e[i[1]][1]
        z1 = e[i[1]][2]

        ax.plot([x0, x1], [y0, y1], [z0, z1], color ='blue', linewidth=3)

    mp = [[], [], []]

    for value, item in e.items():
        mp[0].append(item[0])
        mp[1].append(item[1])
        mp[2].append(item[2])

        ax.scatter(item[0], item[1], item[2], s=100, c='green')

    mp_x = sum(mp[0]) / len(e)
    mp_y = sum(mp[1]) / len(e)
    mp_z = sum(mp[2]) / len(e)

    ax.scatter(mp_x, mp_y, mp_z, s=200, c='red')

    plt.show()

def graph_2d_parameterization():

    # edges
    # e: dict of edge {e_n: (x_n, y_n)}
    e = {1: (1.5, 1.5),
        2: (3.5, 4),
        3: (4.5, 6),
        4: (4.5, 10),
        5: (8, 8),
        6: (10, 13),
        7: (9, 15),
        }

    # verticies
    # v: list of edge pairs (e1 ,e2) that make up verticies
    v = [(1 ,2), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (4, 7)]

    ax = plt.gca(projection='3d')


    for i in  v:

        x0 = e[i[0]][0]
        y0 = e[i[0]][1]

        x1 = e[i[1]][0]
        y1 = e[i[1]][1]

        xs = np.linspace(x0, x1, 10)
        zs = np.linspace(0, 1, 10)

        X, Z = np.meshgrid(xs, zs)
        Y = np.linspace(y0, y1, 10)
        ax.plot_surface(X, Y, Z, color='grey')

    plt.show()

def Graph_Class_Plot():



if __name__ == "__main__":
    graph_2d_parameterization()
