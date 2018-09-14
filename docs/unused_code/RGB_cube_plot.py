
'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

from colorspace.colorlib import sRGB, hexcols
from colorspace import *
import numpy as np

n = 2
seq  = np.linspace(0., 1., n)
#seq  = np.linspace(0., 1. - 1./n, n)
grid = np.meshgrid(seq, seq)

colors = {"R": [], "G": [], "B": []}
def append_colors(colors, R, G, B):
    colors["R"] += list(R)
    colors["G"] += list(G)
    colors["B"] += list(B)
    return colors

x = grid[0].flatten()
y = grid[1].flatten()
null = np.repeat(0., len(x))
full = np.repeat(1., len(x))

append_colors(colors, x, y, null)
append_colors(colors, x, y, full)
append_colors(colors, x, null, y)
append_colors(colors, x, full, y)
append_colors(colors, null, x, y)
append_colors(colors, full, x, y)

alpha = np.repeat(0.2, len(colors["R"]))
cols = sRGB(colors["R"], colors["G"], colors["B"], alpha = alpha)
cols.to("HCL")

pal = hexcols(diverging_hcl("Blue-Yellow 3")(200)) #sequential_hcl()(200)) #diverging_hcl()(200))
pal.to("HCL")


def HCL_to_XYZ(x):
    from numpy import sin, cos, pi
    angle  = x.get("H") / 180. * pi
    return [x.get("C") * sin(angle), x.get("C") * cos(angle), x.get("L")]

# Plotting
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax  = fig.add_subplot(111, projection='3d')

X = [0,40,40,0]
Y = [0,0,40,40]
Z = [0,40,60,0]
verts = [zip(X, Y, Z)]
tri = art3d.Poly3DCollection(verts, alpha = 0.2)
tri.set_color("#ff0000") #colors.rgb2hex(sp.rand(3)))
tri.set_edgecolor('k')
ax.add_collection3d(tri)

#[X, Y, Z] = HCL_to_XYZ(cols)
#ax.scatter(X, Y, Z, c = cols.colors(), marker = "o")

[X, Y, Z] = HCL_to_XYZ(pal)
ax.plot(xs = X, ys = Y, zs = Z)

ax.plot(xs = [0,0], ys = [0,0], zs = [0,100], c = "b")

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
