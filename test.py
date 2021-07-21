

from colorspace.colorlib import HCL
from colorspace import max_chroma
import matplotlib.pyplot as plt
import numpy as np


# ----------------------------------------
# Setting up the plot
# ----------------------------------------
fig, [ax1, ax2] = plt.subplots(1, 2, figsize = (9, 4))

# ----------------------------------------
# C vs. H plot
# ----------------------------------------
H = np.linspace(0, 360, 37, endpoint = True, dtype = "int")
L = np.linspace(30, 90, 4, endpoint = True, dtype = "int")

C = []; Cmax = 0
for i in range(len(L)):
    C.append(max_chroma(H, float(L[i])))
    Cmax = max(Cmax, max(C[i]))

for i in range(len(L)):
    colors = HCL(H, C[i], np.repeat(L[i], len(H))).colors()
    ax1.plot(H, C[i], color = "0.5", zorder = 1)
    ax1.scatter(H, C[i], c = colors, zorder = 2)

ax1.set_xlim(0, 360)
ax1.set_ylim(0, Cmax * 1.05)
yr = ax1.secondary_yaxis("right")
yr.set_ticks([x[len(x) - 1] for x in C])
yr.set_yticklabels(["L = {:d}".format(x) for x in L])
ax1.set_xlabel("Hue (H)")
ax1.set_ylabel("Maximum chroma (C)")


# ----------------------------------------
# L vs. C plot
# ----------------------------------------
L = np.linspace(0, 100, 21, endpoint = True, dtype = "int")
H = np.asarray([0, 60, 120, 250, 330], dtype = "int")

C = []; Cmax = 0
for i in range(len(H)):
    C.append(max_chroma(float(H[i]), L))
    Cmax = max(Cmax, max(C[i]))

for i in range(len(H)):
    colors = HCL(np.repeat(H[i], len(L)), C[i], L).colors()
    ax2.plot(C[i], L, color = "0.5", zorder = 1)
    ax2.scatter(C[i], L, c = colors, zorder = 2)
    # Setting label
    idx = int(np.where(C[i] == max(C[i]))[0])
    ax2.text(C[i][idx] + Cmax / 15, L[idx], "H = {:d}".format(H[i]),
             color = colors[idx], va = "center")


ax2.set_xlim(0, Cmax * 1.20)
ax2.set_ylim(0, 100)
ax2.set_xlabel("Maximum chroma (C)")
ax2.set_ylabel("Luminance (L)")

fig.tight_layout()
plt.show()


import sys; sys.exit(3)


from colorspace.colorlib import hexcols

x1 = hexcols(["#ff00ff", "#00ff00", "#0000ff"])
print(x1)
x2 = hexcols(["#f0f", "#00ff00", "#0000ff"])
print(x2)
import sys; sys.exit(3)

from colorspace import check_hex_colors

#check_hex_colors("#ff003311")
#check_hex_colors("#ff0033")
#check_hex_colors("#f03")
#check_hex_colors(["#f0f", "#00F", "#00FFFF", "#ff003311"])
#import sys; sys.exit(3)


from colorspace.palettes import palette
colors = ["#070707", "#690056", "#C30E62", "#ED8353", "#FDF5EB"]
custom_pal = palette(colors, "test palette")
print(custom_pal)

## Testing different input types (str, list, colorobject)
from colorspace.colorlib import hexcols
from colorspace import palette
hexcols = hexcols(colors)

pal1 = palette("#ff0033")
pal2 = palette("#ff0033", name = "custom name")
pal3 = palette(colors, name = "custom 1.1")
pal4 = palette(hexcols, name = "custom 1.2")
print(pal1)
print(pal2)
print(pal3)
print(pal4)

from colorspace import swatchplot
swatchplot([pal3, pal4])


