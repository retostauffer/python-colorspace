

#from colorspace import *
#
#res = max_chroma(10, 10)
#print(res)
#import sys; sys.exit(3)

import numpy as np
L = np.arange(start = 30, stop = 91, step = 20)

H = np.linspace(0, 360, 37, endpoint = True, dtype = "int")
L = np.linspace(30, 90, 5, endpoint = True, dtype = "int")

#par(mfrow = c(1, 2), xaxs = "i", yaxs = "i", mar = c(5, 4, 1, 5), las = 1)
#plot(0, 0, type = "n", xlim = c(0, 360), ylim = c(0, 165),
#  xlab = "Hue (H)", ylab = "Maximum chroma (C)")
#axis(4, at = C[37, ], labels = paste("L =", L))
from colorspace.colorlib import HCL
from colorspace import max_chroma

import matplotlib.pyplot as plt

C = []; Cmax = 0
for i in range(len(L)):
    C.append(max_chroma(H, float(L[i])))
    Cmax = max(Cmax, max(C[i]))


fig, ax = plt.subplots()
ax.set_xlim(0, 360)
ax.set_ylim(0, Cmax)

for i in range(len(L)):
    ax.plot(H, C[i])

fig.show()

print(C)
#for(i in seq_along(L)) {
#  lines(H, C[, i])
#  points(H, C[, i], col = hex(polarLUV(L[i], C[, i], H)), pch = 19, cex = 1.5, xpd = TRUE)
#}


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


