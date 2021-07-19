

from colorspace import max_chroma
from numpy import linspace

H = linspace(0, 360, 7)
C = max_chroma(H, L = 50)
print(H)
print(C)


import sys; sys.exit(3)


from colorspace import palette, swatchplot, lighten, darken
oi = ["#61A9D9", "#ADD668", "#E6D152", "#CE6BAF", "#797CBA"]

swatchplot([palette(lighten(oi, 0.4), "-40%"),
            palette(lighten(oi, 0.2), "-20%"),
            palette(oi, "0%"),
            palette(darken(oi, 0.2), "+20%"),
            palette(darken(oi, 0.4), "+40%")])



from matplotlib import pyplot as plt
from colorspace import rainbow, rainbow_hcl, desaturate
import numpy as np

col     = rainbow()(8)
col_hcl = rainbow_hcl()(8)

fig, axes = plt.subplots(2, 2)
axes[0, 0].pie(np.repeat(1, len(col)),
               colors = col,
               labels = range(len(col)))
axes[0, 1].pie(np.repeat(1, len(col)),
               colors = desaturate(col),
               labels = range(len(col)))
axes[1, 0].pie(np.repeat(1, len(col_hcl)),
               colors = col_hcl,
               labels = range(len(col_hcl)))
axes[1, 1].pie(np.repeat(1, len(col_hcl)),
               colors = desaturate(col_hcl),
               labels = range(len(col_hcl)))


fig.tight_layout()
fig.show()

import sys; sys.exit(3)

from colorspace import sequential_hcl

print(sequential_hcl()(3))

print("'#023FA5', '#A1A6C8', '#E2E2E2']")
import sys; sys.exit(3)

from colorspace.colorlib import *

x = hexcols("#CC99A3")
print(x)
x.to("HLS")
print(x)
x.to("hex")
print(x)

import sys; sys.exit(3)

from colorspace import *

pcol  = diverging_hcl()(4)
pcol2 = diverging_hcl()(7)

rcol  = ["#023FA5", "#BEC1D4", "#D6BCC0", "#8E063B"]
rcol2 = ["#023FA5", "#7D87B9", "#BEC1D4", "#E2E2E2", "#D6BCC0", "#BB7784", "#8E063B"]

swatchplot({"R1": rcol, "Py1": pcol, "R2": rcol2, "Py2": pcol2})

import sys; sys.exit(3)

from colorspace import *
from colorspace.colorlib import HSV

x = HSV(100, 0.5, 0.5)
x.to("RGB")
x.to("sRGB")
#x.to("RGB")
x.to("HLS")
print(x)
import sys; sys.exit(3)

from colorspace import *

import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 2)

from colorspace import *

p = palette(["#330033", "#123123"], "foo")

print(deutan(p))

import sys; sys.exit(3)


import sys
from colorspace import diverging_hcl, sequential_hcl
from colorspace import hcl_palettes, specplot, swatchplot, palette
from colorspace import *

p = qualitative_hcl("Set 2")(100)

specplot(p)

sys.exit(3)

pal1 = sequential_hcl("YlGnBu")(5)
pal2 = sequential_hcl("Viridis")(5)

#@savefig palette_visualization_cvd_option.png width=60% align=center
swatchplot([palette(pal1, "YlGnBu"),
            palette(pal2, "Viridis")],
            cvd = ["protan", "desaturate"],
            nrow = 4)



import sys; sys.exit(3)

pals = hcl_palettes(5, "diverging")

for pal in pals.get_palettes():
    #print(pal)
    #print(pal.get_settings())
    #print(type(pal))
    print(pal.colors(5))


#pal = diverging_hcl("Vik") #Blue-Red 3")
#print(pal(5))
#print('[1] "#002F70" "#879FDB" "#F6F6F6" "#DA8A8B" "#5F1415"')
#specplot(pal(5))
#import sys; sys.exit(0)

hcl_palettes(type_ = "diverging", plot = True, ncol = 1)

print(" \n\n ----------- VIK -------------- \n\n")
diverging_hcl("Vik")(5)
import sys; sys.exit(0)



print(pal(7))

import sys; sys.exit(0)

pal = diverging_hcl("Tofino")
R = ["#D6E0FF", "#666E9A", "#111111", "#557A47", "#C2EFB4"] # Tofino

#pal = sequential_hcl("Blues 3")
#R = ["#00366C", "#0072B4", "#79ABE2", "#C3DBFD", "#F9F9F9"] # Blues 3

#pal = sequential_hcl("Blues 2")
#R = ["#023FA5", "#6A76B2", "#A1A6C8", "#CBCDD9", "#E2E2E2"] # Blues 2

print(pal.show_settings())

P = pal(5)


b = []
for i in range(0, len(P)):
    print(" {:s}  {:s}  {:s}".format(R[i], P[i],
          "" if P[i] == R[i] else "False"))

import sys; sys.exit(3)


from colorspace import demoplot
from colorspace import *
from colorspace.colorlib import HCL

hexlist    = ["#BCBE57", "#DEDFC0", "#F1F1F1", "#F7D3E7", "#FB99D7"]
hexlist

colorobj = HCL([0, 90, 180], [60, 60, 60], [60, 60, 60])
colorobj

hclpalette = diverging_hcl()
hclpalette

defaultpalette = hcl_palettes(name = "Berlin").get_palettes()[0]
defaultpalette


demoplot(hexlist,        "Bar")
demoplot(colorobj,       "Lines")
demoplot(hclpalette,     "Pie", n = 4)
demoplot(defaultpalette, "Matrix", n = 11)

import sys; sys.exit(3)

from colorspace.colorlib import *
x = RGB(1, 0.5, 0, alpha = 0.3)
assert x.get("R")[0] == 1
assert x.get("G")[0] == 0.5
assert x.get("B")[0] == 0
assert x.get("alpha")[0] == 0.3

x.set(R = 0.2)
x.set(G = 0.2, B = 0.2, alpha = 0.2)
assert x.get("R")[0] == 0.2
assert x.get("G")[0] == 0.2
assert x.get("B")[0] == 0.2
assert x.get("alpha")[0] == 0.2

import sys; sys.exit()


from colorspace import hclpalettes
#print(hclpalettes().get_palettes("Sequential"))
#print(hclpalettes().get_palettes("Qualitative"))
from colorspace import qualitative_hcl
print(qualitative_hcl("Dark 3"))

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
data = sm.datasets.elnino.load(as_pandas=False)


from colorspace import sequential_hcl
pal = sequential_hcl("Purples").cmap()

fig = plt.figure()
ax = fig.add_subplot(111)
res = sm.graphics.rainbowplot(data.raw_data[:, 1:], ax=ax, cmap = pal)
ax.set_xlabel("Month of the year")
ax.set_ylabel("Sea surface temperature (C)")
ax.set_xticks(np.arange(13, step=3) - 1)
ax.set_xticklabels(["", "Mar", "Jun", "Sep", "Dec"])
ax.set_xlim([-0.2, 11.2])
plt.show()

#import matplotlib.pyplot as plt
#from matplotlib.colors import BoundaryNorm
#from matplotlib.ticker import MaxNLocator
#import numpy as np
#
#from colorspace import diverging_hcl
#pal = diverging_hcl("Blue-Red 3")
#
#np.random.seed(19680801)
#Z = np.random.rand(6, 10)
#x = np.arange(-0.5, 10, 1)  # len = 11
#y = np.arange(4.5, 11, 1)  # len = 7
#
#fig, ax = plt.subplots()
#ax.pcolormesh(x, y, Z, cmap = pal.cmap())
#
#fig.show()

### Loading package
##from colorspace import *
##from colorspace.colorlib import *
##
##import numpy as np
##
### Generate a set of colors
##cols = hexcols(["#023FA5", "#A1A6C8", "#E2E2E2", "#CA9CA4", "#8E063B"])
##
### Convert colors
##cols.to("HCL")
##print(cols)
##
##cols.to("hex")
##print(cols)
##
##H = sequential_hcl(h = [0, 300], c = [60, 60], l = 65)
##C = sequential_hcl(h = 0, c = [100, 0], l = 65, rev = True, power = 1)
##L = sequential_hcl(h = 260, c = [25, 25], l = [25, 90], rev = True, power = 1)
##
##swatchplot([palette(H(5), "Hue"),
##            palette(C(5), "Chroma"),
##            palette(L(5), "Luminance")])
##
##
