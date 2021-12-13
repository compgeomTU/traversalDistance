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
    plt.figure()
    plt.plot([1, 2], linewidth=10.0)
    plt.plot([2, 1], linewidth=10.0)

    # write figure to memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.clf()
    buf.seek(0)

    # read figure from buffer
    im = image.imread(buf)

    xp, yp = im.shape

    x = np.arange(0, xp, 1)
    y = np.arange(0, yp, 1)
    Y, X = np.meshgrid(y, x)
    Z = X * 0.5

    ax = plt.gca(projection='3d')
    ax.plot_surface(X, Y, Z, facecolors=im)
    plt.show()


if __name__ == "__main__":
    texture_map()
