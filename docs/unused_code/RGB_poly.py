
'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

import numpy as np

from colorspace import diverging_hcl
from colorspace.colorlib import hexcols
pal = hexcols(diverging_hcl()(11))
pal.to("HCL")
def colormap(pal):
    cols = pal.colors()
    from matplotlib import pyplot as plt
    from matplotlib.patches import Rectangle
    import numpy as np
    fig, ax = plt.subplots(figsize = [0.3,2])
    ax.set_xlim([0, 1])
    ax.set_ylim([0, len(cols)])
    for i in range(0, len(cols)):
        rect = Rectangle((0,i), 1, 1, color = cols[i])
        ax.add_patch(rect)

    fig.subplots_adjust(left = 0., bottom = 0., right  = 1.,
                        top  = 1., wspace = 0., hspace = 0.)
    ax.patch.set_visible(False)
    fig.patch.set_visible(False)
    ax.axis('off')
    fig.savefig("_cbar.png")
    plt.close(fig)



def HCL_to_XYZ(x):
    from numpy import sin, cos, pi
    angle  = x.get("H") / 180. * pi
    return [x.get("C") * sin(angle), x.get("C") * cos(angle), x.get("L")]

def append_polygons(verts, side, n = 2):
    """append_polygons(verts, side,n = 2):

    Parameters
    ----------
    verts : list
        can be an empty list. All polygons will be appended, the
        extended verts list will be returned.
    side : int
        a cube has three sides, this is simply one of 1, 2, 3.
    n : int
        number of segments along each axis. n = 3 yields
        6 timex 3 times 3 (54) polygons.

    Returns
    -------
    list
        An extended list ``verts`` with new polygons and colors.
        Each list element is a dict with a color and one polygon
        with four corners.
    """
    # Check
    if not side in [1,2,3]:
        raise ValueError("side must be 1,2,3 (for now).")
    # Helper fun
    def append(verts, A, B, C):
        from colorspace.colorlib import sRGB
        HCL = sRGB(A, B, C); HCL.to("HCL")
        [X,Y,Z] = HCL_to_XYZ(HCL)
        # Face color
        from numpy import mean
        facecol = sRGB(mean(A), mean(B), mean(C))
        facecol = str(facecol.colors()[0])
        verts.append({"color": facecol, "coords": [zip(X,Y,Z)]})
        return verts

    # Looping over a seq x seq grid
    from numpy import linspace
    seq = linspace(0, 1, n+1)
    for i in range(0,n):
        for j in range(0,n):
            A = [seq[i], seq[i+1], seq[i+1], seq[i]]
            B = [seq[j], seq[j], seq[j+1], seq[j+1]]
            if side == 1:
                verts = append(verts, A, B, [0,0,0,0])
                verts = append(verts, A, B, [1,1,1,1])
            elif side == 2:
                verts = append(verts, A, [0,0,0,0], B)
                verts = append(verts, A, [1,1,1,1], B)
            elif side == 3:
                verts = append(verts, [0,0,0,0], A, B)
                verts = append(verts, [1,1,1,1], A, B)
    # Return
    return verts


# Helper function to add dimension in Hue
def add_circle(ax, L):
    from numpy import linspace, pi, sin, cos, repeat
    r = linspace(0, 2*pi, 360)
    x = sin(r) * L
    y = cos(r) * L
    z = repeat(0, len(r))
    ax.plot(xs = x, ys = y, zs = z, c = "#CACACA")

# Helper function to add labels for Hue
def add_hue_labels(ax, L):
    from numpy import arange, pi, sin, cos, repeat
    r = arange(0, 360, 45, dtype = float)
    x = sin(r / 180. * pi) * L
    y = cos(r / 180. * pi) * L
    for i in range(0, len(r)):
        ax.text(x[i], y[i], 0., "H = {:.0f}".format(r[i]),
                color = "black", ha = "center", va = "center")


# Creating the polygons first
n = 20
verts = []
verts = append_polygons(verts, 1, n = n)
verts = append_polygons(verts, 2, n = n)
verts = append_polygons(verts, 3, n = n)


# Plotting
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import art3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize = (5,5))
ax  = fig.add_subplot(111, projection='3d')

# Adding polygons to 3d plot
for rec in verts:
    tri = art3d.Poly3DCollection(rec["coords"], alpha = 0.3)
    tri.set_color(rec["color"])
    tri.set_edgecolor(None)
    ax.add_collection3d(tri)

# Adding circles
from numpy import arange, sin, cos, pi
for L in arange(20, 161, 20):
    add_circle(ax, L)

# Adding HUE lines (radial lines)
for H in arange(0, 360, 45, dtype = float):
    print(H)
    x = sin(H / 180. * pi) * 160
    y = cos(H / 180. * pi) * 160
    c = "#CCCCCC" if not (H % 90) == 0 else "#CECECE"
    ax.plot([0,x], [0,y], [0,0], color = c, ls = "--") #"#CACACA")

# Adding HUE dimension labels
add_hue_labels(ax, L + 30)

# Adding the "Doener Spiess" (C = 0)
ax.plot(xs = [0,0], ys = [0,0], zs = [-5,105], c = "#CACACA")
ax.text(0, 0,  -5, "L = 0",   va = "top",    ha = "center")
ax.text(0, 0, 105, "L = 100", va = "bottom", ha = "center")
ax.scatter([0.,0.], [0.,0.], [0.,100.], c = "black") 


# Adding diverging palette
from colorspace import diverging_hcl
from colorspace.colorlib import hexcols
pal = hexcols(diverging_hcl()(11))
pal.to("HCL")
[X, Y, Z] = HCL_to_XYZ(pal)
ax.plot(xs = X, ys = Y, zs = Z, c = "black")
ax.scatter(X, Y, Z, c = pal.colors())#"black")

# Plot colormap (once)
colormap(pal)

# Axis stuff
ax.set_axis_off()
ax.set_xlim([-120,120])
ax.set_ylim([-120,120])
ax.set_zlim([   0, 70])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Remove the axis and stuff
def disable_axis(ax):
    for a in (ax.w_xaxis, ax.w_yaxis, ax.w_zaxis):
        for t in a.get_ticklines()+a.get_ticklabels():
            t.set_visible(False)
        a.pane.set_visible(False)

plt.tight_layout()

from numpy import arange, sin, pi
from matplotlib.pyplot import savefig
for azim in arange(0, 360, 2, dtype = float):
    print("Plotting: {:03.0f}".format(azim))
    elev = 28 + sin(azim / 180. * pi) * 17
    ax.view_init(elev = elev, azim = azim)
    savefig("_fig_{:03.0f}.png".format(azim), bbox_inches='tight')

from glob import glob
import subprocess as sub
import re

# Adding color map on top of each image
for file in glob("_fig*.png"):
    if not re.match("^_fig_[0-9]{3}\.png$", file): continue
    print("Converting {:s}".format(file))
    sub.Popen(["convert", file, "_cbar.png", "-geometry", "+8+8",
               "-quality", "70", "-composite", file])

# Create animatet Gif (it's a G!)
p = sub.Popen(["convert","-delay","7","_fig*.png","hcl.gif"],
               stdout = sub.PIPE, stderr = sub.PIPE)
out,err = p.communicate()
if p.returncode == 0:
    print("All fine, hcl.gif created")
    import os
    for file in glob("*.png"):
        if not re.match("^(_cmap.png|_fig_[0-9]{3}\.png)$", file): continue
        os.remove(file)
else:
    print("Uiui, problems with convert")
    print err


