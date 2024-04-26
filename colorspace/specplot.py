

def specplot(x, y = None, hcl = True, palette = True, fix = True, rgb = False, \
             title = None, fig = None, **figargs):
    """Visualization of the RGB and HCL spectrum given a set of hex colors.
    As the hues for low-chroma colors are not (or poorly) identified, by
    default a smoothing is applied to the hues (``fix = TRUE``). Also, to
    avoid jumps from 0 to 360 or vice versa, the hue coordinates are shifted
    suitably.

    No return, creates an interactive figure.

    Args:
        x (list): list of strings (hex colors or standard-names of colors).
        y (None or list): if set it must be a list of strings (see `x`) with the very
            same length as the object provided on argument `x`. Allows to draw
            two sets of colors for comparison. Defaults to `None`.
        hcl (bool): Whether or not to plot the HCL color spectrum.
        palette: bool Whether or not to plot the colors as a color map.
        fix (bool): Should the hues be fixed to be on a smooth(er) curve?
            Details in the method description.
        rgb (bool): Whether or not to plot the RGB color spectrum. Default is
            False.
        title (None or str): title of the figure. Defaults to `None` (no title).
        fig (None, matplotlib.figure.Figure): If `None`, a new
            `matplotlib.figure.Figure` is created. 
        **figargs: forwarded to `matplotlib.pyplot.subplot`. Only has an effect
            if `fig = None`.

    Example:

       >>> from colorspace import rainbow_hcl
       >>> from colorspace import specplot
       >>> pal = rainbow_hcl(100)
       >>> specplot(pal.colors())
       >>> specplot(pal.colors(), rgb = False, hcl = True, palette = False)

    Raises:
        TypeError: If `x` is not a list.
        TypeError: If `y` is neither a list nor `None`.
        ValueError: If `x` contains strings which can not be converted to hex colors.
        ValueError: If `y` contains strings which can not be converted to hex colors.
        ValueError: If `y` is not the same length as `y`. Only checked if `y` is not `None`.
        TypeError: If either `rgb`, `hcl`, or `palette` is not boolean.
        ValueError: If all, `rgb`, `hcl` and `palette` are set to `False` as this would
            result in an empty plot.
        TypeError: If 'title' is neither `None` nor `str`.
    """

    from .utils import check_hex_colors

    # Support function to draw the color map (the color strip)
    def cmap(ax, hex_, ylo = 0):
        """Plotting a color map given a set of colors.

        Args:
            ax (matplotlib.Axis): The axis object on which the color map should be drawn
            hex_ (list): List of hex colors.
            ylo (float): Lower limit where the rectangles are plotted. Height is always
                1, if multiple palettes have to be plotted xlo has to be set to 0, 1, ...
        """

        from numpy import linspace
        from matplotlib.patches import Rectangle

        n = len(hex_)
        w = 1. / float(n - 1)
        x = linspace(-w / 2., 1. + w / 2, n + 1)
        for i in range(0,n):
            rect = Rectangle((x[i], 0. + ylo), w, 1. + ylo, color = hex_[i])
            ax.add_patch(rect)
        if ylo > 0:
            ax.plot([0, 1], [ylo] * 2, ls = "-", c = "0")


    # Checking main arguments 'x' and 'y'
    if not isinstance(x, list): raise TypeError("Argument `x` must be a list.")
    x = check_hex_colors(x) # Checks if all entries are valid

    # Checking y
    if not isinstance(y, (type(None), list)):
        raise TypeError("Argument `x` must be `None` or a list.")
    if not isinstance(y, type(None)):
        y = check_hex_colors(y) # Checks if all entries are valid
        if not len(x) == len(y):
            raise ValueError("If argument `y` is provided it must be of the same length as `x`.")


    # Sanity check for input arguemnts to control the different parts
    # of the spectogram plot. Namely rgb spectrum, hcl spectrum, and the palette.
    if not isinstance(rgb, bool):     raise TypeError("argument 'rgb' must be boolean True or False.")
    if not isinstance(hcl, bool):     raise TypeError("argument 'hcl' must be boolean True or False.")
    if not isinstance(palette, bool): raise TypeError("argument 'palette' must be boolean True or False.")
    if not rgb and not hcl and not palette:
        import inspect
        raise ValueError("disabling rgb, hcl, and palette all at the same time is not possible " + \
                  "when calling \"{:s}\".".format(inspect.stack()[0][3]))

    if not isinstance(title, (type(None), str)):
        raise TypeError("Argument 'title' must be either `None` or `str`.")

    # Import hexcolors: convert colors to hexcolors for the plot if needed.
    from .colorlib import hexcols
    from .palettes import palette

    # TODO Why am I doing it this way? Is this dict required?
    colors = {"x": x, "y": y}

    # If input parameter "fix = True": fixing
    # the hue coordinates to avoid jumping which
    # can occur due to the HCL->RGB transformation.
    def fixcoords(x):

        [H, C, L] = x
        n = len(H) # Number of colors
        # Fixing spikes
        import numpy as np
        for i in range(1,n):
            d = H[i] - H[i - 1]
            if np.abs(d) > 320.:    H[i]   = H[i]       - np.sign(d) * 360.
            if np.abs(H[i]) > 360:  H[0:i+1] = H[0:i+1] - np.sign(H[i]) * 360

        # Smoothing the hue values in batches where chroma is very low
        idx = np.where(C < 8.)[0]
        if len(idx) == n:
            H = np.repeat(np.mean(H), n)
        else:
            # pre-smoothing the hue
            # Running mean
            if n > 49:
                H = 1./3. * (H + np.append(H[0],H[0:-1]) + np.append(H[1:],H[n-1]))

            # TODO Spline smoother not yet implemented

        return [H, C, L]


    # Calculate coordinates
    coords = {}
    for key, vals in colors.items():
        # This happens if 'y' is set to 'None' (default)
        if vals is None: continue

        # Else get HCL and RGB coordinates for all colors
        cols = hexcols(vals)
        cols.to("sRGB")
        coords[key] = {"hex":vals}
        if rgb:
            coords[key]["sRGB"] = [cols.get("R"), cols.get("G"), cols.get("B")]
        if hcl:
            cols.to("HCL")
            coords[key]["HCL"] = [cols.get("H"), cols.get("C"), cols.get("L")]
            if fix: coords[key]["HCL"] = fixcoords(coords[key]["HCL"])


    from .colorlib import sRGB
    from .palettes import rainbow_hcl

    # Specify the colors for the spectrum plots
    rgbcols = sRGB([0.8, 0, 0], [0, 0.8, 0], [0, 0, 0.8])
    hclcols = rainbow_hcl()(4)

    # Create figure
    from numpy import linspace, arange
    import matplotlib.ticker as ticker
    import matplotlib.pyplot as plt

    # Create plot
    import numpy as np

    # Open new figure.
    if not fig:
        hfig = plt.figure()
    else:
        hfig = fig

    if rgb and hcl and palette:
        ax1 = plt.subplot2grid((7, 1), (0, 0), rowspan = 3)
        ax2 = plt.subplot2grid((7, 1), (3, 0))
        ax3 = plt.subplot2grid((7, 1), (4, 0), rowspan = 3)
    elif rgb and hcl:
        ax1 = plt.subplot2grid((2, 1), (0, 0))
        ax3 = plt.subplot2grid((2, 1), (1, 0))
    elif rgb and palette:
        ax1 = plt.subplot2grid((4, 1), (0, 0), rowspan = 3)
        ax2 = plt.subplot2grid((4, 1), (3, 0))
    elif hcl and palette:
        ax2 = plt.subplot2grid((4, 1), (0, 0))
        ax3 = plt.subplot2grid((4, 1), (1, 0), rowspan = 3)
    elif rgb:
        ax1 = plt.subplot2grid((1, 1), (0, 0))
    elif hcl:
        ax3 = plt.subplot2grid((1, 1), (0, 0))
    elif palette:
        # Adjusting outer margins
        ax2 = plt.subplot2grid((1, 1), (0, 0))
        hfig.subplots_adjust(left = 0., bottom = 0., right  = 1.,
                             top  = 1., wspace = 0., hspace = 0.)
    else:
        import inspect
        raise ValueError("Unexpected condition in \"{:s}\". Sorry.".format(inspect.stack()[0][3]))

    # Setting axis properties
    # ax1: RGB
    if rgb:
        ax1.set_xlim(0, 1); ax1.set_ylim(0, 1);
        ax1.get_xaxis().set_visible(False)
    # ax2: color map
    if palette:
        ax2.set_xlim(0, 1); ax2.set_ylim(len(coords), 0);
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)
    # ax3 and ax33: HCL
    if hcl:
        ax3.set_xlim(0,1); ax3.set_ylim(0,100); ax3.get_xaxis().set_visible(False)
        ax33 = ax3.twinx()
        ax33.set_ylim(-360,360)

    # Linestyles (used in case multiple palettes are handed over)
    linestyles = ["-", "--", "-.", ":"]

    # Plotting RGB spectrum
    if rgb:
        count = 0
        for key,val in coords.items():
            [R, G, B] = val["sRGB"]
            x = linspace(0., 1., len(R))
            linestyle = linestyles[count % len(linestyles)] 
            LR, = ax1.plot(x, R, color = rgbcols.colors()[0], linestyle = linestyle)
            LG, = ax1.plot(x, G, color = rgbcols.colors()[1], linestyle = linestyle)
            LB, = ax1.plot(x, B, color = rgbcols.colors()[2], linestyle = linestyle)
            count += 1

    # Plotting the color map
    if palette:
        for i in range(len(coords)):
            cmap(ax2, coords[list(coords.keys())[i]]["hex"], ylo = i)

    # Plotting HCL spectrum
    if hcl:
        count = 0
        for key,val in coords.items():
            [H, C, L] = val["HCL"]

            # Setting limits for left y-axis
            ymax = max(0, max(C), max(L))
            ax3.set_ylim(0, ymax * 1.05)

            x = linspace(0., 1., len(H))
            linestyle = linestyles[count % len(linestyles)] 
            ax3.plot(x,  C, color = hclcols[1], linestyle = linestyle)
            ax3.plot(x,  L, color = hclcols[2], linestyle = linestyle)
            ax33.plot(x, H, color = hclcols[0], linestyle = linestyle)

            # If the minimum of H does not go below 0, set axis to 0, 360
            ax33.set_yticks(arange(-360, 361, 120))
            ax33.set_ylim(-360 if min(H) < 0 else 0, 360)

            count += 1
        ax33.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

    # Labels and annotations
    if rgb:
        ax1.set_ylabel("Red/Green/Blue")
        ax1.xaxis.set_label_position("top")
        ax1.text(0.5, 1.05, "RGB Spectrum", horizontalalignment = "center",
                 verticalalignment = "bottom")
    if hcl:
        ax3.set_ylabel("Chroma/Luminance")
        ax33.set_ylabel("Hue")
        ax3.text(0.5,  -10, "HCL Spectrum", horizontalalignment = "center",
                 verticalalignment = "top")

    if isinstance(title, str):
        plt.gcf().get_axes()[0].set_title(title, va = "top",
                fontdict = dict(fontsize = "large", fontweight = "semibold"))


    # Show figure or return the Axes object (in case `ax` has not been None).
    if not fig: hfig.show()

    return hfig







