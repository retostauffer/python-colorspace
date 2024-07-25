#!/usr/bin/env python
# ------------------------------------------------------
# Create static images used for paper
# ------------------------------------------------------

import matplotlib.pyplot as plt

# helper function to combine 2 or more images horizontally
def stack_images(files, output):
    import numpy as np
    import os

    assert isinstance(files, list)
    assert np.all(isinstance(files, str) for f in files)
    assert np.all(os.path.isfile(f) for f in files)
    assert isinstance(output, str)

    import PIL
    from PIL import Image

    imgs = [Image.open(f) for f in files]
    # pick the image which is the smallest hehg, and resize the others to match
    # it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    print(f"{min_shape=}")
    imgs_comb = np.hstack([i.resize(min_shape) for i in imgs])
    
    # save that beautiful picture
    imgs_comb = Image.fromarray(imgs_comb)
    print(f"Saving combined imate to {output}")
    imgs_comb.save(output)

# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-chosing-palettes.png"
# ------------------------------------------------------
from colorspace import palette, sequential_hcl, swatchplot

pal1 = sequential_hcl(palette = "viridis")
pal2 = sequential_hcl(h = [300, 75], c = [40, 95], l = [15, 90], power = [1., 1.1])
pal3 = sequential_hcl(palette = "viridis", cmax = 90,  c2 = 20)
pal4 = sequential_hcl(palette = "viridis", h1 = 200)

fig = swatchplot([palette(pal1(7), "By name"),
            palette(pal2(7), "By hand"),
            palette(pal3(7), "With triangular chroma"),
            palette(pal4(7), "With smaller hue range")],
            figsize = (8, 1.75));
fig.savefig("fig-chosing-palettes.png", transparent = False, dpi = 200)
plt.close()


# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-hcl-palettes.png"
# ------------------------------------------------------
from colorspace import hcl_palettes

fig = hcl_palettes(plot = True, figsize = (20, 15))
fig.savefig("fig-hcl-palettes.png", transparent = False, dpi = 150)
plt.close()



# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-specplot-hclplot.png"
# ------------------------------------------------------
from tempfile import NamedTemporaryFile
png1 = NamedTemporaryFile(suffix = ".png")
png2 = NamedTemporaryFile(suffix = ".png")

fig1 = pal4.specplot(figsize = (6, 5));
fig1.savefig(png1.name, dpi = 150)

fig2 = pal4.hclplot(n = 7, figsize = (6, 5));
fig2.savefig(png2.name, dpi = 150)

stack_images([png1.name, png2.name], "fig-specplot-hclplot.png")

png1.close()
png2.close()
plt.close()


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

fig.savefig("fig-cvd.png", dpi = 150)
plt.close() # Importante


# ------------------------------------------------------
# Chosing/defining palettes
# - Creates "fig-plotting.png"
# ------------------------------------------------------
from tempfile import NamedTemporaryFile
png1 = NamedTemporaryFile(suffix = ".png")
png2 = NamedTemporaryFile(suffix = ".png")

from colorspace import dataset
import matplotlib.pyplot as plt

df = dataset("HarzTraffic") # Loading data; requires pandas

fig = plt.Figure()

# Creating new figure
fig = plt.hist2d(df.tempmin, df.tempmax, bins = 20,
                 cmap = pal3.cmap().reversed())

plt.title("Joint density daily min/max temperature")
plt.xlabel("minimum temperature [deg C]")
plt.ylabel("maximum temperature [deg C]")
plt.savefig(png1.name, dpi = 150)


from colorspace import qualitative_hcl, dataset
import seaborn as sns 

df = dataset("HarzTraffic") # Loading data; requires pandas
pal = qualitative_hcl("Dark 3", h1 = -180, h2 = 100) # Color palette

# Creating plot
g = sns.displot(data = df, x = "tempmax", hue = "season", fill = "season",   
                kind = "kde", rug = True, height = 5, aspect = 1,
                palette = pal.colors(4))
g.set_axis_labels("temperature [deg C]")              
g.set(title = "Distribution of daily maximum temperature given season")
plt.tight_layout()
plt.savefig(png2.name, dpi = 150)

stack_images([png1.name, png2.name], "fig-plotting.png")

png1.close()
png2.close()
plt.close()

