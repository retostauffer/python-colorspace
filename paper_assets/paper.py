#!/usr/bin/env python
# ------------------------------------------------------
# Create static images used for paper
# ------------------------------------------------------

# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-chosing-palettes.png"
# ------------------------------------------------------
from colorspace import palette, sequential_hcl, swatchplot

pal1 = sequential_hcl(palette = "viridis")
pal2 = sequential_hcl(h = [300, 75], c = [40, 95], l = [15, 90], power = [1., 1.1])
pal3 = sequential_hcl(palette = "viridis", cmax = 90,  c2 = 20)
pal4 = sequential_hcl(palette = "viridis", h1 = 200)

swatchplot([palette(pal1(7), "By name"),
            palette(pal2(7), "By hand"),
            palette(pal3(7), "With triangular chroma"),
            palette(pal4(7), "With smaller hue range")],
            figsize = (8, 1.75));

# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-hcl-palettes.png"
# ------------------------------------------------------

hcl_palettes(plot = True, figsize = (20, 15))


# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-specplot-hclplot.png"
# ------------------------------------------------------

pal4.specplot(figsize = (5, 5));

pal4.hclplot(n = 7, figsize = (5, 5));



# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-cvd.png"
# ------------------------------------------------------
from colorspace import demoplot, rainbow, sequential_hcl, deutan
from colorspace import diverging_hcl
import matplotlib.pyplot as plt

col1 = rainbow(end = 1/3, rev = True).colors(11)
col2 = sequential_hcl("Blue-Yellow", rev = True).colors(11)

fig, ax = plt.subplots(2, 2, figsize = (10, 5))

demoplot(col1, "Map", ax = ax[0,0], title = "(In-)famous Rainbow palette", ylabel = "original")
demoplot(col2, "Map", ax = ax[0,1], title = "HCL-based Blue-Yellow")
demoplot(deutan(col1), "Map", ax = ax[1,0], ylabel = "deuteranope")
demoplot(deutan(col2), "Map", ax = ax[1,1])


# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-plotting.png"
# ------------------------------------------------------

from colorspace import dataset
import matplotlib.pyplot as plt

df = dataset("HarzTraffic") # Loading data; requires pandas

# Creating new figure
fig = plt.hist2d(df.tempmin, df.tempmax, bins = 20,
                 cmap = pal3.cmap().reversed())

plt.title("Joint density daily min/max temperature")
plt.xlabel("minimum temperature [deg C]")
plt.ylabel("maximum temperature [deg C]")
plt.show()


from colorspace import qualitative_hcl, dataset
import seaborn as sns 

df = dataset("HarzTraffic") # Loading data; requires pandas
pal = qualitative_hcl("Dark 3", h1 = -180, h2 = 100) # Color palette

# Creating plot
g = sns.displot(data = df, x = "tempmax", hue = "season", fill = "season",   
                kind = "kde", rug = True, height = 4, aspect = 1,
                palette = pal.colors(4))
g.set_axis_labels("temperature [deg C]")              
g.set(title = "Distribution of daily maximum temperature given season")
plt.tight_layout()
plt.show()



