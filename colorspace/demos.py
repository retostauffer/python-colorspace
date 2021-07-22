# -------------------------------------------------------------------
# - NAME:        demos.py
# - AUTHOR:      Reto Stauffer
# - DATE:        2018-09-15
# -------------------------------------------------------------------
# - DESCRIPTION:
# -------------------------------------------------------------------
# - EDITORIAL:   2018-09-15, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2018-09-17 16:30 on marvin
# -------------------------------------------------------------------


def demoplot(colors, type_, n = 7, ax = None, **kwargs):
    """Create demo plots.

    Arguments:
        type_ (str): Name of the demoplot; name of the demo function to be called.
            Not case sensitive.
        n (int): Positive integer, number of colors for the plot. Only used
            if argument ``colors`` is a palette where a dedicated number of
            colors must be drawn first. Defaults to 7.
        title (None or str): used to draw the figure title if specified (str).
            Forwarded to different plot types.
        ax (None or matplotlib.axes.Axes): If `None` a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
            Forwarded to different plot types.
        **kwargs: Forwarded to the corresponding demo plot functions.

    Examples:

        >>> # Custom list of hex colors (n = 5)
        >>> hexlist    = ["#BCBE57", "#DEDFC0", "#F1F1F1", "#F7D3E7", "#FB99D7"]
        >>> hexlist
        >>> # A (HCL based) colorobject with (n = 3)
        >>> colorobj = HCL([0, 90, 180], [60, 60, 60], [60, 60, 60])
        >>> colorobj
        >>> # Default diverging HCL palette
        >>> hclpalette = diverging_hcl()
        >>> hclpalette
        >>> # Default color palette shipped with the package
        >>> defaultpalette = hcl_palettes(name = "Berlin").get_palettes()[0]
        >>> defaultpalette
        >>> # Demoplots
        >>> demoplot(hexlist,        "Bar")
        >>> demoplot(colorobj,       "Lines")
        >>> demoplot(hclpalette,     "Pie", n = 4)
        >>> demoplot(defaultpalette, "Matrix", n = 11)
        >>>
        >>> # Using custom subplots and plot titles
        >>> from matplotlib import pyplot as plt
        >>> from colorspace import protan, deutan, desaturate
        >>> fig, axes = plt.subplots(2, 2)
        >>> colors = diverging_hcl("Green-Orange").colors(7)
        >>> demoplot(colors,             "Bar",
        >>>          title = "Original",           ax = axes[0, 0])
        >>> demoplot(protan(colors),     "Bar",
        >>>          title = "Protanope vision",   ax = axes[0, 1])
        >>> demoplot(deutan(colors),     "Bar",
        >>>          title = "Deuteranope vision", ax = axes[1, 0])
        >>> demoplot(desaturate(colors), "Bar",
        >>>          title = "Desaturated",        ax = axes[1, 1])
        >>> fig.show()


    Raises:
        TypeError: If `type_` is not a string.
        ValueError: If `type_` is not an available demo plot type.
        TypeError: If `n`` is not integer.
        ValueError: `n` must be a positive integer.
    """
    from . import demos
    from re import match, compile, IGNORECASE

    # Sanity checks
    if not isinstance(type_, str):
        raise TypeError("Argument 'type_' must be string.")
    if not isinstance(n, int):
        raise TypeError("Argument 'n' must be integer.")
    if not n > 0:
        raise ValueError("Argument 'n' must be a positive integer (number of colors).")

    # Now let's deal with the color input.
    # In case it is a list of strings we assume it is a list of hex colors.
    # To handle it we will convert it into a palette (which is checking that
    # all colors are valid hex colors). The argument 'colors' also allowes
    # for a series of other types.
    from numpy import all
    from .palettes import palette, hclpalette, defaultpalette
    from .colorlib import colorobject
    if isinstance(colors, list) and all([isinstance(x, str) for x in colors]):
        colors = palette(colors, "demoplot color palette").colors()
    elif isinstance(colors, (hclpalette, defaultpalette)):
        colors = colors(n)
    elif isinstance(colors, colorobject):
        colors = colors.colors()
    else:
        raise TypeError("No rule to handle argument ``colors`` of type {:s}.".format(str(type(colors))))


    # Loading available demo plot types (functions)
    available_types = []
    for rec in dir(demos):
        if not rec == "demoplot" and match("^[A-Za-z]*$", rec):
            available_types.append(rec)

    # Is the user asking for an available demo plot?
    fun   = None
    check = compile("^{:s}$".format(type_), IGNORECASE)
    for avtype in available_types:
        if not check.match(avtype): continue
        fun = avtype

    # Not found?
    if fun is None:
        raise ValueError("No demoplot available for {:s} (Available: {:s}).".format(
                type_, ", ".join(available_types)))

    # Calling the required plotting function
    fun = getattr(demos, fun)
    return fun(colors, ax = ax, **kwargs)


def _demoplot_set_labels(ax, **kwargs):
    """Setting axis and labels for demoplots.

    Args:
        **kwargs: named arguments to set different labels of the demoplots.
            Considered are `title`, `xlable`, and `ylabel` only.

    Returns:
        No return.
    """

    from matplotlib import pyplot as plt

    # Hide axis ticks and frame (box)
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    ax.set_frame_on(False)

    # In case the user specified title, xlabel, or ylabel as a string
    # we will call ax.set_title, ax.set_xlabel, and ax.set_ylabel respectively.
    # For the title boldface font will be used.
    for x in ["title", "xlabel", "ylabel"]:
        if x in kwargs.keys():
            if isinstance(kwargs[x], str):
                fn = getattr(ax, "set_{:s}".format(x))
                fn(kwargs[x], fontweight = "bold" if x == "title" else "regular")

    plt.tight_layout()


def Bar(colors, ax = None, **kwargs):
    """Plotting the barplot example.

    Args:
        colors (list of str): List of hex colors.
        ax (None or matplotlib.axes.Axes): If none a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
        **kwargs: optional. Strings can be set for `title = "My title"`, 
            `xlabel = "My x label"` and `ylabel = "My y label"`. 

    Returns:
        Returns a new figure object if `ax` equals `None`, else the
        same object as provided on `ax` is returned.

    Raises:
        ValueError: If `ax` is neither none nor an object which inherits from
            `matplotlib.axes.Axes`.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.axes import Axes

    if not isinstance(ax, (Axes, type(None))):
        raise ValueError("Wrong input: ax must be None or inherit from matplotlib.axes.Axes.")

    # Open new figure in case the user has not specified the `ax`
    # input argument (matplotlib.axes.Axes) but use `ax = None` (default).
    # In this case this function will also auto-show the image at the end
    # of the function.
    if ax is None:
        fig = plt.figure()
        ax  = plt.gca()
        showfig = True
    else:
        showfig = False

    # Get random data
    np.random.seed(1)
    width = 0.9 / len(colors)

    lower  = [1.1, 1.9, 0.7, 0.3]
    offset = [0.5, 1.1, 1.5, 0.8]

    # Creating the plot
    for i in range(0, len(lower)):
        x = i + np.arange(0, len(colors)) * width
        y = lower[i] + np.abs(np.sin(offset[i] + 1 + \
            np.arange(0, len(colors), dtype = float))) / 3
        ax.bar(x, y, color = colors, width = width)


    # Set and draw axis and labels for the demoplots
    _demoplot_set_labels(ax, **kwargs)

    if not showfig:
        return ax
    else:
        fig.show()
        return fig


def Pie(colors, ax = None, **kwargs):
    """Plotting pie chart example.

    Args:
        colors (list of str): List of hex colors.
        ax (None or matplotlib.axes.Axes): If none a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
        **kwargs: optional. Strings can be set for `title = "My title"`,
            `xlabel = "My x label"` and `ylabel = "My y label"`.

    Returns:
        Returns a new figure object if `ax` equals `None`, else the
        same object as provided on `ax` is returned.

    Raises:
        ValueError: If `ax` is neither none nor an object which inherits from
            `matplotlib.axes.Axes`.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.axes import Axes

    if not isinstance(ax, (Axes, type(None))):
        raise ValueError("Wrong input: ax must be None or inherit from matplotlib.axes.Axes.")

    # Open new figure in case the user has not specified the `ax`
    # input argument (matplotlib.axes.Axes) but use `ax = None` (default).
    # In this case this function will also auto-show the image at the end
    # of the function.
    if ax is None:
        fig = plt.figure()
        ax  = plt.gca()
        showfig = True
    else:
        showfig = False

    # Generate pie plot
    x = 0.01 + np.abs(np.sin(1.5 + np.arange(0, len(colors))))
    ax.pie(x, colors = colors)

    # Set and draw axis and labels for the demoplots
    _demoplot_set_labels(ax, **kwargs)

    if not showfig:
        return ax
    else:
        fig.show()
        return fig


def Spine(colors, ax = None, **kwargs):
    """Plotting spine plot example.

    Args:
        colors (list of str): List of hex colors.
        ax (None or matplotlib.axes.Axes): If none a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
        **kwargs: optional. Strings can be set for `title = "My title"`,
            `xlabel = "My x label"` and `ylabel = "My y label"`.

    Returns:
        Returns a new figure object if `ax` equals `None`, else the
        same object as provided on `ax` is returned.

    Raises:
        ValueError: If `ax` is neither none nor an object which inherits from
            `matplotlib.axes.Axes`.
    """

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import numpy as np
    from matplotlib.axes import Axes

    if not isinstance(ax, (Axes, type(None))):
        raise ValueError("Wrong input: ax must be None or inherit from matplotlib.axes.Axes.")

    # Open new figure in case the user has not specified the `ax`
    # input argument (matplotlib.axes.Axes) but use `ax = None` (default).
    # In this case this function will also auto-show the image at the end
    # of the function.
    if ax is None:
        fig = plt.figure()
        ax  = plt.gca()
        showfig = True
    else:
        showfig = False

    # Data
    offset  = 0.015
    widths  = [0.05, 0.1, 0.15, 0.1, 0.2, 0.08, 0.12, 0.16, 0.04]
    k       = len(widths)
    n       = len(colors)
    heights = [np.power(np.arange(1, n + 1, dtype = float) / n, 1. / p) for p in \
              [2.5, 1.2, 2.7, 1, 1.3, 0.7, 0.4, 0.2, 1.7]]

    # Plot
    x = 0.
    for i in range(0,k):
        y = 0.
        heights[i] = heights[i] / sum(heights[i]) # Scale
        for j in range(0,n):
            rect = Rectangle((x,y), widths[i], heights[i][j], color = colors[j])
            ax.add_patch(rect)
            y += heights[i][j]
        x += offset + widths[i]

    # Set and draw axis and labels for the demoplots
    _demoplot_set_labels(ax, **kwargs)

    if not showfig:
        return ax
    else:
        fig.show()
        return fig


def Heatmap(colors, ax = None, **kwargs):
    """Plotting heatmap example.

    Dataset source: Digitized from a topographic map by Ross Ihaka. These data
    should not be regarded as accurate.

    Dataset description: Maunga Whau (Mt Eden) is one of about 50
    volcanos in the Auckland volcanic field. This data set gives topographic
    information for Maunga Whau on a 10m by 10m grid.  A matrix with 87 rows
    and 61 columns, rows corresponding to grid lines running east to west and
    columns to grid lines running south to north.

    Todo:
        Add source/link.

    Args:
        colors (list of str): List of hex colors.
        ax (None or matplotlib.axes.Axes): If none a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
        **kwargs: optional. Strings can be set for `title = "My title"`,
            `xlabel = "My x label"` and `ylabel = "My y label"`.

    Returns:
        Returns a new figure object if `ax` equals `None`, else the
        same object as provided on `ax` is returned.

    Raises:
        ValueError: If `ax` is neither none nor an object which inherits from
            `matplotlib.axes.Axes`.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.axes import Axes

    from matplotlib.colors import LinearSegmentedColormap
    from .colorlib import hexcols

    if not isinstance(ax, (Axes, type(None))):
        raise ValueError("Wrong input: ax must be None or inherit from matplotlib.axes.Axes.")

    # Open new figure in case the user has not specified the `ax`
    # input argument (matplotlib.axes.Axes) but use `ax = None` (default).
    # In this case this function will also auto-show the image at the end
    # of the function.
    if ax is None:
        fig = plt.figure()
        ax  = plt.gca()
        showfig = True
    else:
        showfig = False

    # Get coordinates
    cobj = hexcols(colors)
    cobj.to("sRGB")
    r = cobj.get("R"); g = cobj.get("G"); b = cobj.get("B")

    # Create cmap
    pos = np.linspace(0, 1, len(colors), dtype = float)
    cdict = {'red':[], 'green':[], 'blue':[]}
    for i in range(0, len(colors)):
        cdict['red'].append(   (pos[i], r[i], r[i]) )
        cdict['green'].append( (pos[i], g[i], g[i]) )
        cdict['blue'].append(  (pos[i], b[i], b[i]) )
    cmap = LinearSegmentedColormap("custom", cdict, len(colors))

    # Loading vulcano
    data = get_volcano_data()

    # Plotting data
    ax.imshow(data, cmap = cmap, aspect = "auto")

    #ax.axis("off")
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    ax.set_frame_on(False)

    # Set and draw axis and labels for the demoplots
    _demoplot_set_labels(ax, **kwargs)

    if not showfig:
        return ax
    else:
        fig.show()
        return fig



def Matrix(colors, ax = None, **kwargs):
    """Plotting matrix example.

    Args:
        colors (list of str): List of hex colors.
        ax (None or matplotlib.axes.Axes): If none a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
        **kwargs: optional. Strings can be set for `title = "My title"`,
            `xlabel = "My x label"` and `ylabel = "My y label"`.

    Returns:
        Returns a new figure object if `ax` equals `None`, else the
        same object as provided on `ax` is returned.

    Raises:
        ValueError: If `ax` is neither none nor an object which inherits from
            `matplotlib.axes.Axes`.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.axes import Axes

    from matplotlib.colors import LinearSegmentedColormap
    from .colorlib import hexcols

    if not isinstance(ax, (Axes, type(None))):
        raise ValueError("Wrong input: ax must be None or inherit from matplotlib.axes.Axes.")

    # Open new figure in case the user has not specified the `ax`
    # input argument (matplotlib.axes.Axes) but use `ax = None` (default).
    # In this case this function will also auto-show the image at the end
    # of the function.
    if ax is None:
        fig = plt.figure()
        ax  = plt.gca()
        showfig = True
    else:
        showfig = False

    # Get coordinates
    cobj = hexcols(colors)
    cobj.to("sRGB")
    r = cobj.get("R"); g = cobj.get("G"); b = cobj.get("B")

    # Create cmap
    pos = np.linspace(0, 1, len(colors), dtype = float)
    cdict = {'red':[], 'green':[], 'blue':[]}
    for i in range(0, len(colors)):
        cdict['red'].append(   (pos[i], r[i], r[i]) )
        cdict['green'].append( (pos[i], g[i], g[i]) )
        cdict['blue'].append(  (pos[i], b[i], b[i]) )
    cmap = LinearSegmentedColormap("custom", cdict, len(colors))

    # Get random data
    np.random.seed(1)
    data = np.random.uniform(0., float(len(colors)), 100).reshape((10,10))

    # Plotting data
    ax.imshow(data, cmap = cmap)

    # Set and draw axis and labels for the demoplots
    _demoplot_set_labels(ax, **kwargs)

    if not showfig:
        return ax
    else:
        fig.show()
        return fig

#def Scatter(colors, fig = None):
#
#    import matplotlib.pyplot as plt
#    import numpy as np
#
#    # Open figure if input "fig" is None, else use
#    # input "fig" handler.
#    if fig is None:
#        fig = plt.figure()
#        showfig = True
#    else:
#        showfig = False
#
#    # Data
#    x0 = np.sin(np.pi * np.arange(1,61) / 30) / 5
#    y0 = np.cos(np.pi * np.arange(1,61) / 30) / 5
#    xr = [0.1, -0.6, -0.7, -0.9,  0.4,  1.3, 1.0]
#    yr = [0.3,  1.0,  0.1, -0.9, -0.8, -0.4, 0.6]
#
#    # Requires scipy
#
#    x = 0.01 + np.abs(np.sin(1.5 + np.arange(0, len(colors))))
#    plt.pie(x, colors = colors)
#    plt.axis("off")
#    plt.tight_layout()
#
#    if not showfig:  return fig
#    else:            fig.show()

def Lines(colors, ax = None, **kwargs):
    """Plotting lineplot example.

    Args:
        colors (list of str): List of hex colors.
        ax (None or matplotlib.axes.Axes): If none a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
        **kwargs: optional. Strings can be set for `title = "My title"`,
            `xlabel = "My x label"` and `ylabel = "My y label"`.

    Returns:
        Returns a new figure object if `ax` equals `None`, else the
        same object as provided on `ax` is returned.

    Raises:
        ValueError: If `ax` is neither none nor an object which inherits from
            `matplotlib.axes.Axes`.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.axes import Axes

    if not isinstance(ax, (Axes, type(None))):
        raise ValueError("Wrong input: ax must be None or inherit from matplotlib.axes.Axes.")

    # Open new figure in case the user has not specified the `ax`
    # input argument (matplotlib.axes.Axes) but use `ax = None` (default).
    # In this case this function will also auto-show the image at the end
    # of the function.
    if ax is None:
        fig = plt.figure()
        ax  = plt.gca()
        showfig = True
    else:
        showfig = False

    # Data
    n = len(colors)
    s = range(2, n + 2)

    lwd = 6
    if n > 5:  lwd -= 1
    if n > 15: lwd -= 1
    if n > 25: lwd -= 1

    for i in range(0, len(colors)):
        j = n - 1 - i
        # Plotting two lines to get the overlays correctly
        ax.plot([1 / s[i], 2. + 1. / s[j]],
                [s[i], s[j]],
                color = colors[i], linewidth = lwd,
                solid_capstyle = "round")
        ax.plot([2. + 1. / s[i], 4. - 1. / s[i], 6. - 1 / s[i]],
                [s[i], s[i], s[j]],
                color = colors[j], linewidth = lwd,
                solid_capstyle = "round")

    # Set and draw axis and labels for the demoplots
    _demoplot_set_labels(ax, **kwargs)

    if not showfig:
        return ax
    else:
        fig.show()
        return fig


def Map(colors, ax = None, **kwargs):
    """Plotting map example.

    Args:
        colors (list of str): List of hex colors.
        ax (None or matplotlib.axes.Axes): If none a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
        **kwargs: optional. Strings can be set for `title = "My title"`,
            `xlabel = "My x label"` and `ylabel = "My y label"`. In addition
            `edgecolor = <color>` can be used to specify custom edge color of the
            polygons.

    Returns:
        Returns a new figure object if `ax` equals `None`, else the
        same object as provided on `ax` is returned.

    Raises:
        ValueError: If `ax` is neither none nor an object which inherits from
            `matplotlib.axes.Axes`.
    """

    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.axes import Axes

    if not isinstance(ax, (Axes, type(None))):
        raise ValueError("Wrong input: ax must be None or inherit from matplotlib.axes.Axes.")

    # Open new figure in case the user has not specified the `ax`
    # input argument (matplotlib.axes.Axes) but use `ax = None` (default).
    # In this case this function will also auto-show the image at the end
    # of the function.
    if ax is None:
        fig = plt.figure()
        ax  = plt.gca()
        showfig = True
    else:
        showfig = False


    # Returns a PatchCollection with the polygons for the map and
    # a numpy array with the values used for the color coding.
    collection,vals = get_map_data()

    # Convert the numeric values into integers [0, n-1] to pick
    # the correct colors for each polygon given the user input
    # object `colors`.
    n    = len(colors)
    vals = np.floor((vals - np.min(vals)) / (np.max(vals) - np.min(vals)) * (n - 1))
    vals = np.fmin(vals, n - 1)
    cols = [colors[int(x)] for x in vals]

    # Setting facecolor of the polygons
    collection.set_facecolor(cols)
    edgecolor = "black" if not "edgecolor" in kwargs.keys() else kwargs["edgecolor"]
    collection.set_edgecolor(edgecolor)

    # Draw map
    ax.add_collection(collection)
    ax.autoscale_view()
    ax.set_aspect("equal")

    # Set and draw axis and labels for the demoplots
    _demoplot_set_labels(ax, **kwargs)

    if not showfig:
        return ax
    else:
        fig.show()
        return fig




def Spectrum(*args, **kwargs):
    """Plotting example. Simply interfaces the specplot function.

    Args:
        colors (list of str): List of hex colors.
    """

    from colorspace import specplot
    specplot(rgb = True, *args, **kwargs)


def get_volcano_data(array = False):
    """Loading vulcano data set

    Args:
        array (bool): should the return be a list (default) or 2d
            numpy array?

    Returns:
        Returns a list of length 67 where each entry is a list of integers
        of lenth 87 if `asarray = False` (default). If `asarray = True`
        an integer numpy array of shape `(67, 87)` will be returned.

    Raises:
        ValueError: If input `asarray` is not boolean.
    """

    import os
    from numpy import asarray

    if not isinstance(array, bool):
        raise ValueError("Input 'asarray' must be boolean.")

    # Loading the data set
    resource_package = os.path.dirname(__file__)
    volcano = os.path.join(resource_package, "data", "volcano.dat")

    # Reading the data set; create recursive list
    data = []
    with open(volcano, "r") as fid:
        for line in fid.readlines():
            data.append([int(x) for x in line.split()])

    # Return data
    if array:
        return asarray(data)
    else:
        data.reverse()
        return(data)

def get_map_data():
    """Loading map data for demoplot.

    Reading a file called `map.json` shipped with the package which
    contains the definition of the different areas (polygons) and 
    values to draw the map.

    Returns
    -------
        List of length `2`. The first entry is a `PatchCollection` object
        (`matplotlib.collections`) which sonsists of a series of `Polygon`s
        for the different districts. The second entry is a `numpy.ndarray`
        (float) containing the values used to color-code the areas.
    """
    import os
    import json

    from matplotlib import pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Polygon
    from colorspace.demos import get_map_data
    from numpy import column_stack, asarray


    # Loading the data set
    resource_package = os.path.dirname(__file__)
    mapdata = os.path.join(resource_package, "data", "map.json")

    with open(mapdata, "r") as fid: mapdata = json.loads(fid.readline())

    patches = []
    values  = []

    # Prepare the data for return
    for key,vals in mapdata.items():
        polygon = Polygon(column_stack((vals["x"], vals["y"])))
        patches.append(polygon)
        values.append(vals["value"][0])

    return [PatchCollection(patches), asarray(values)]
