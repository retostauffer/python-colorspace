
# Visualizing 6-day precipitation amount GFS forecasts initialized
# September 12, 2018 few days before the landfall of Hurricane
# Florence.
def demo(lev, *colormaps, **kwargs):

    import numpy as np

    # --------------------------
    # Reading the data set first
    # --------------------------
    file = "ncdc_tempanomaly_072018.dat"
    lons = np.linspace(235, 294, 237, dtype = float)
    lats = np.linspace( 24,  50, 105, dtype = float)
    lons, lats = np.meshgrid(lons, lats)
    
    with open("GFS_tp_201809120000_000_144.dat", "r") as fid:
        data = np.ndarray(lons.shape, dtype = float)
        i = 0
        for line in fid.readlines():
            if line.strip()[0] == "#": continue
            data[i,:] = np.asarray([float(x) for x in line.split()])
            i += 1

    # --------------------------
    # Setting up the figure
    # --------------------------
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    fig = plt.figure()
    nsubplots = len(colormaps)

    # Do we have titles?
    titles = None
    if "titles" in kwargs.keys():
        if not len(kwargs["titles"]) == len(colormaps):
            raise ValueError("length of titles has to match the number of colormaps")
        titles = kwargs["titles"]

    # Extra arg
    if "ncol" in kwargs.keys():
        ncol = kwargs["ncol"]
    else:
        ncol = 2
    # Calculcate grid size needed
    if nsubplots <= ncol:
        ncol = nsubplots
        nrow = 1
    else:
        nrow = np.ceil(float(nsubplots) / float(ncol))

    for i,colors in enumerate(colormaps):

        ax = fig.add_subplot(nrow, ncol, i + 1)

        # Setting up the projection
        m = Basemap(projection = "merc",
            llcrnrlat = np.min(lats), urcrnrlat = np.max(lats),
            llcrnrlon = np.min(lons), urcrnrlon = np.max(lons),
            rsphere=6371200., resolution='l', area_thresh=10000, lat_ts = 20)
        xi,  yi  = m(lons, lats)
        
        # Plot data in inches
        zlim = np.max(data)
        cc = m.contourf(xi, yi, data * 0.03937008, levels = lev, colors = colors)
        
        # Add Grid Lines
        m.drawparallels(np.arange(-80., 81., 20.))
        m.drawmeridians(np.arange(-180., 181., 20.))
        
        # Add Coastlines, States, and Country Boundaries
        m.drawcoastlines()
        m.drawstates()
        m.drawcountries()
        
        # Add Colorbar
        cbar = m.colorbar(cc, location='bottom', pad="10%")
        cbar.set_label("Precipitation Sum [inch over 6 days]")

        # Add Title
        title = "GFS Precipitation Amount Forecast\n2018-09-12 00UTC to 2018-09-18 00UTC"
        if titles: title += "\n{:s}".format(titles[i])
        plt.title(title)

    fig.tight_layout()
    plt.show()


