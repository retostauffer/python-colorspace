


from colorspace import sequential_hcl

pal = sequential_hcl("Blues 3")
print(pal.show_settings())

P = pal(5)
R = ["#00366C", "#0072B4", "#79ABE2", "#C3DBFD", "#F9F9F9"]

print(P)
print(R)


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
