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


def demoplot(colors, type_, n = 7, fig = None):
    """Create demo plots.

    Arguments:
        type_ (str): Name of the demoplot; name of the demo function to be called.
        fig: None (default) or a matplotlib figure object, forwarded to the
            plotting function.
        n (int): Positive integer, number of colors for the plot. Only used
            if argument ``colors`` is a palette where a dedicated number of
            colors must be drawn first. Defaults to 7.

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

    Raises:
        TypeError: If ``type_`` is not a string.
        ValueError: If ``type_`` is not an available demo plot.
        TypeError: If ``n`` is not integer.
        ValueError: ``n`` must be a positive integer.
    """
    from . import demos
    from re import match

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
    if not type_ in available_types:
        raise ValueError("No demoplot available for {:s} (Available: {:s}).".format(
                type_, ", ".join(available_types)))

    # Calling the required plotting function
    fun = getattr(demos, type_)
    fun(colors, fig = fig)



def Bar(colors, fig = None):
    """Plotting the barplot example.

    Args:
        colors (list of str): List of hex colors.
        fig (None or a matplotlib.pyplot.figure):
            If None, a figure will be initialized internally. If input ``fig`` is
            already a figure object the data will be plotted using this data handler.

    Returns:
        None or a same as input ``fig``
        If input ``fig = None`` nothing will be returned, else the input figure
        handler will be returned at the end containing a new axis object with
        the demo plot.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Get random data
    np.random.seed(1)
    width = 0.9 / len(colors)

    lower  = [1.1, 1.9, 0.7, 0.3]
    offset = [0.5, 1.1, 1.5, 0.8]

    ax = plt.subplot2grid((1, 1), (0, 0))
    for i in range(0, len(lower)):
        x = i + np.arange(0, len(colors)) * width
        y = lower[i] + np.abs(np.sin(offset[i] + 1 + \
            np.arange(0, len(colors), dtype = float))) / 3
        ax.bar(x, y, color = colors, width = width)

    # Plot
    #ax.bar(range(0, len(colors)), x, color = colors)
    plt.axis("off")
    plt.tight_layout()

    if not showfig:
        return fig
    else:
        fig.show()


def Pie(colors, fig = None):
    """Plotting pie chart example.

    Args:
        colors (list of str): List of hex colors.
        fig (None or a matplotlib.pyplot.figure):
            If None, a figure will be initialized internally. If input ``fig`` is
            already a figure object the data will be plotted using this data handler.

    Returns:
        None or a same as input ``fig``
        If input ``fig = None`` nothing will be returned, else the input figure
        handler will be returned at the end containing a new axis object with
        the demo plot.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Axis
    ax = plt.subplot2grid((1, 1), (0, 0))

    # Data
    x = 0.01 + np.abs(np.sin(1.5 + np.arange(0, len(colors))))
    plt.pie(x, colors = colors)
    plt.axis("off")
    plt.tight_layout()

    if not showfig:  return fig
    else:            fig.show()


def Spine(colors, fig = None):
    """Plotting spine plot example.

    Args:
        colors (list of str): List of hex colors.
        fig (None or a matplotlib.pyplot.figure):
            If None, a figure will be initialized internally. If input ``fig`` is
            already a figure object the data will be plotted using this data handler.

    Returns:
        None or a same as input ``fig``
        If input ``fig = None`` nothing will be returned, else the input figure
        handler will be returned at the end containing a new axis object with
        the demo plot.
    """

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
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

    # Axis
    ax = plt.subplot2grid((1, 1), (0, 0))

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

    plt.axis("off")
    plt.tight_layout()

    if not showfig:  return fig
    else:            fig.show()


def Heatmap(colors, fig = None):
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
        fig (None or a matplotlib.pyplot.figure):
            If None, a figure will be initialized internally. If input ``fig`` is
            already a figure object the data will be plotted using this data handler.

    Returns:
        None or a same as input ``fig``
        If input ``fig = None`` nothing will be returned, else the input figure
        handler will be returned at the end containing a new axis object with
        the demo plot.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Create custom cmap
    from matplotlib.colors import LinearSegmentedColormap
    from .colorlib import hexcols
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
    import os
    resource_package = os.path.dirname(__file__)
    volcano = os.path.join(resource_package, "data", "volcano.dat")

    data = []
    with open(volcano, "r") as fid:
        for line in fid.readlines():
            data.append([int(x) for x in line.split()])

    # Plotting
    ax = plt.subplot2grid((1, 1), (0, 0))
    ax.imshow(data, cmap = cmap)
    plt.axis("off")
    plt.tight_layout()

    if not showfig: return fig
    else:           fig.show()



def Matrix(colors, fig = None):
    """Plotting matrix example.

    Args:
        colors (list of str): List of hex colors.
        fig (None or a matplotlib.pyplot.figure):
            If None, a figure will be initialized internally. If input ``fig`` is
            already a figure object the data will be plotted using this data handler.

    Returns:
        None or a same as input ``fig``
        If input ``fig = None`` nothing will be returned, else the input figure
        handler will be returned at the end containing a new axis object with
        the demo plot.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Create custom cmap
    from matplotlib.colors import LinearSegmentedColormap
    from .colorlib import hexcols
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

    # Plotting
    ax = plt.subplot2grid((1, 1), (0, 0))
    ax.imshow(data, cmap = cmap)
    plt.axis("off")
    plt.tight_layout()

    if not showfig: return fig
    else:           fig.show()

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

def Lines(colors, fig = None):
    """Plotting lineplot example.

    Args:
        colors (list of str): List of hex colors.
        fig (None or a matplotlib.pyplot.figure):
            If None, a figure will be initialized internally. If input ``fig`` is
            already a figure object the data will be plotted using this data handler.

    Returns:
        None or a same as input ``fig``
        If input ``fig = None`` nothing will be returned, else the input figure
        handler will be returned at the end containing a new axis object with
        the demo plot.
    """

    import matplotlib.pyplot as plt
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
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

    ax = plt.subplot2grid((1, 1), (0, 0))
    for i in range(0, len(colors)):
        j = n - 1 - i
        ax.plot([1 / s[i], 2. + 1. / s[j]],
                [s[i], s[j]],
                color = colors[i], linewidth = lwd)
        ax.plot([2. + 1. / s[i], 4. - 1. / s[i], 6. - 1 / s[i]],
                [s[i], s[i], s[j]],
                color = colors[j], linewidth = lwd)
    plt.axis("off")
    plt.tight_layout()

    if not showfig:  return fig
    else:            fig.show()


def Spectrum(*args, **kwargs):
    """Plotting example. Simply interfaces the specplot function.

    Args:
        colors (list of str): List of hex colors.
        fig (None or a matplotlib.pyplot.figure):
            If None, a figure will be initialized internally. If input ``fig`` is
            already a figure object the data will be plotted using this data handler.

    Returns:
        None or a same as input ``fig``
        If input ``fig = None`` nothing will be returned, else the input figure
        handler will be returned at the end containing a new axis object with
        the demo plot.
    """

    from colorspace import specplot
    specplot(rgb = True, *args, **kwargs)

