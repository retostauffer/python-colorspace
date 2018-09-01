
import os
import sys

import logging as log
log.basicConfig(format="[%(levelname)s] %(message)s", level=log.DEBUG)


def specplot(hex_, rgb = True, hcl = True, palette = True):
    """Visualization of the RGB and HCL spectrum given a set of
    hex colors.

    Parameters:
        hex_ (:class:`list` or :class`numpy.ndarray`): containing the
            color hex codes.
        rgb (:class:`bool`): whether or not to plot the RGB color spectrum.
            Default is `True`.
        hcl (:class:`bool`): whether or not to plot the HCL color spectrum.
            Default is `True`.
        palette (:class:`bool`): whether or not to plot the colors as a 
            color map. Default is `True`.

    Returns:
        No return, creates an interactive figure.

    Example:
        >>> from colorspace.palettes import rainbow_hcl
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
        import matplotlib.pyplot as plt
    except:
        log.error("Requires matplotlib to be installed!. Stop.")
        sys.exit(9)


    # Support function to draw the color map (the color strip)
    def cmap(ax, hex_):

        from numpy import linspace
        from matplotlib.patches import Rectangle

        n = len(hex_)
        delta = 2 / float(n + 1.)
        x = linspace(-delta / 2., 1. + delta / 2, n + 1)
        for i in range(0,n):
            rect = Rectangle((x[i],0.), delta, 1., color = hex_[i]) 
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
    cols = hexcols(hex_)
    cols.to("RGB")
    if rgb:
        [R, G, B] = [cols.get("R"), cols.get("G"), cols.get("B")]
    if hcl:
        cols.to("HCL")
        [H, C, L] = [cols.get("H"), cols.get("C"), cols.get("L")]

    from colorlib import sRGB
    from palettes import rainbow_hcl

    # Specify the colors for the spectrum plots
    rgbcols = sRGB([0.8, 0, 0], [0, 0.8, 0], [0, 0, 0.8])
    hclcols = rainbow_hcl(3)

    # Create figure
    from numpy import linspace, arange
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    
    # Create plot
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
        ax2 = plt.subplot2grid((1, 1), (0, 0))
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

    # Plotting RGB spectrum
    x = linspace(0., 1., len(hex_))
    if rgb:
        ax1.plot(x, R, color = rgbcols.colors()[0], linestyle = "solid")
        ax1.plot(x, G, color = rgbcols.colors()[1], linestyle = "solid")
        ax1.plot(x, B, color = rgbcols.colors()[2], linestyle = "solid")

    # Plotting the color map
    if palette: cmap(ax2, hex_)

    # Plotting HCL spectrum
    if hcl:
        ax3.plot(x, C, color = hclcols.colors()[1], linestyle = "solid")
        ax3.plot(x, L, color = hclcols.colors()[2], linestyle = "solid")
        ax33.plot(x, H, color = hclcols.colors()[0], linestyle = "solid")
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
        ax3.set_ylabel("Hue")
        ax3.text(0.5,  -10, "HCL Spectrum", horizontalalignment = "center",
                 verticalalignment = "top")
    
    plt.show()
    





























