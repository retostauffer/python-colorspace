
import os
import sys

from cslogger import cslogger
log = cslogger(__name__)


def specplot(hex_, rgb = True, hcl = True, palette = True, **kwargs):
    """specplot(hex_, rgb = True, hcl = True, palette = True, **kwargs)
    
    Visualization of the RGB and HCL spectrum given a set of hex colors.

    Parameters
    ----------
    hex_ : list or numpy.ndarray
        hex color codes.
    rgb : bool
        whether or not to plot the RGB color spectrum.
    hcl : bool
        whether or not to plot the HCL color spectrum.
    palette : bool
        whether or not to plot the colors as a color map.
    kwargs : ...
        Currently not used.

    Returns
    -------
    No return, creates an interactive figure.

    Example
    -------
    >>> from colorspace import rainbow_hcl
    >>> from colorspace import specplot
    >>> pal = rainbow_hcl(100)
    >>> specplot(pal.colors())
    >>> specplot(pal.colors(), rgb = False, hcl = True, palette = False)

    .. todo::
        Implement the smoothings to improve the look of the plots.
    """

    # Check if matplotlib is installed or not (as it is not
    # a package requirement but a suggested package).
    try:
        import matplotlib
    except:
        log.error("Requires matplotlib to be installed!. Stop.")
        sys.exit(9)


    # Support function to draw the color map (the color strip)
    def cmap(ax, hex_):

        from numpy import linspace
        from matplotlib.patches import Rectangle

        n = len(hex_)
        w = 1. / float(n - 1)
        x = linspace(-w / 2., 1. + w / 2, n + 1)
        for i in range(0,n):
            rect = Rectangle((x[i],0.), w, 1., color = hex_[i]) 
            ax.add_patch(rect)

    # Try to convert inputs to boolean.
    # raise exception if not possible.
    try:
        rgb = bool(rgb); hcl = bool(hcl); palette = bool(palette)
    except Exception as e:
        log.error(e); sys.exit(9)

    # This would yield an empty plot: raise an error.
    if not rgb and not hcl and not palette:
        import inspect
        log.error("Disabling rgb, hcl, and palette all at the same time is not possible " + \
                  "when calling \"{:s}\".".format(inspect.stack()[0][3]))
        sys.exit(9)


    from colorlib import hexcols
    coords = {} 
    if not isinstance(hex_, dict):
        hex_ = {"colors": hex_}

    # Calculate coordinates
    coords = {}
    for key,vals in hex_.items():
        cols = hexcols(vals)
        cols.to("sRGB")
        coords[key] = {"hex":vals}
        if rgb:
            coords[key]["sRGB"] = [cols.get("R"), cols.get("G"), cols.get("B")]
        if hcl:
            cols.to("HCL")
            coords[key]["HCL"] = [cols.get("H"), cols.get("C"), cols.get("L")]

    # If we have multiple color maps: disable palette
    if len(coords) > 1:
        palette = False


    from colorlib import sRGB
    from palettes import rainbow_hcl

    # Specify the colors for the spectrum plots
    rgbcols = sRGB([0.8, 0, 0], [0, 0.8, 0], [0, 0, 0.8])
    hclcols = rainbow_hcl(3)

    # Create figure
    from numpy import linspace, arange
    import matplotlib.ticker as ticker
    import matplotlib.pyplot as plt
    from matplotlib import pyplot as plt
    
    # Create plot
    fig = plt.figure() 
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
        fig.subplots_adjust(left = 0., bottom = 0., right  = 1.,
                            top  = 1., wspace = 0., hspace = 0.)
    else:
        import inspect
        log.error("Unexpected condition in \"{:s}\". Sorry.".format(inspect.stack()[0][3]))
        sys.exit(9)

    # Setting axis properties
    # ax1: RGB
    if rgb:
        ax1.set_xlim(0,1); ax1.set_ylim(0,1);
        ax1.get_xaxis().set_visible(False)
    # ax2: color map
    if palette:
        ax2.set_xlim(0,1); ax2.set_ylim(0,1);
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
            print B
            x = linspace(0., 1., len(R))
            linestyle = linestyles[count % len(linestyles)] 
            LR, = ax1.plot(x, R, color = rgbcols.colors()[0], linestyle = linestyle)
            LG, = ax1.plot(x, G, color = rgbcols.colors()[1], linestyle = linestyle)
            LB, = ax1.plot(x, B, color = rgbcols.colors()[2], linestyle = linestyle)
            count += 1
        #ax1.legend([LR, LG, LB], ["R", "G", "B"],
        #    bbox_to_anchor = (0., 1., .3, 0.), ncol = 3, frameon = False)

    # Plotting the color map
    if palette:
        cmap(ax2, coords[coords.keys()[0]]["hex"])

    # Plotting HCL spectrum
    if hcl:
        count = 0
        for key,val in coords.items():
            [H, C, L] = val["HCL"]
            x = linspace(0., 1., len(H))
            linestyle = linestyles[count % len(linestyles)] 
            ax3.plot(x,  C, color = hclcols.colors()[1], linestyle = linestyle)
            ax3.plot(x,  L, color = hclcols.colors()[2], linestyle = linestyle)
            ax33.plot(x, H, color = hclcols.colors()[0], linestyle = linestyle)
            count += 1
        ax33.set_yticks(arange(-360, 361, 120))
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
    
    plt.show()
    





