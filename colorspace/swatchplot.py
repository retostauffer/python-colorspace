

def swatchplot(pals, nrow = 20, n = 5, *args, **kwargs):
    """Note: ``**kwargs`` can be used to specify the figure size of the resulting
    image by specifying ``figsize = (height, width)`` where both, ``height``
    and ``width`` must be int/float, specifying the height and width in inches.

    Example:

        An example using custom :py:class:`palettes.palette`, once
        named and once unnamed:

        >>> # Single swatchplot (unnamed) for a series of colors
        >>> from colorspace import diverging_hcl, swatchplot
        >>> colors = diverging_hcl()(5)
        >>> swatchplot(colors) 
        >>> # Create three custom palettes for the three dimensions
        >>> # of the Hue-Chroma-Luminance color space
        >>> # H: only hue varies along the palette
        >>> # C: only chroma varies along the palette
        >>> # L: only luminance varies along the palette
        >>> # Create custom HCL colors and convert them to :py:class:`palettes.palette` objects
        >>> from numpy import linspace, repeat
        >>> from colorspace.colorlib import HCL
        >>> from colorspace import palette, swatchplot
        >>> H = palette(HCL(linspace(0, 360, 7), repeat(60, 7), repeat(60, 7))(), "Hue")
        >>> C = palette(HCL(repeat(0, 7), linspace(0, 100, 7), repeat(60, 7))(), "Chroma")
        >>> L = palette(HCL(repeat(0, 7), repeat(0, 7), linspace(0, 100, 7))(), "Luminance")
        >>> # Swatchplot, once unnamed (no title), once named (title will be shown) 
        >>> swatchplot([H, C, L])
        >>> swatchplot({"HCL Dimensions": [H, C, L]})

    .. note:
        Requires the ``matplotlib`` module to be installed.
    """


    # If plot is True: proceed.
    # Requires matpotlib, a suggested package. If not avialable
    # raise an import error.
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        import inspect
        msg = "{:s} requires matplotlib to be installed: {:s}".format(
                inspect.stack()[0][3], str(e))
        raise ImportError(msg)

    # Prepares a list item
    def prepare_listelement(rec, n = 5):
        from numpy import ndarray
        if isinstance(rec, list) or isinstance(rec, ndarray):
            colors = rec
        else:
            raise Exception("problems preparing list item in swatchplot")

        # Check if all hex colors are valid. If not, a
        # ValueError will be raised.
        valid(rec)

        # Return
        return ["custom", colors]

    # Allow the user to specify figure size if needed
    if "figsize" in kwargs:
        figsize = kwargs["figsize"]
        if not isinstance(figsize, tuple) or not len(figsize) == 2:
            raise ValueError("\"figsize\" must be a tuple of length 2.")
        for i in range(0, 1):
            if not isinstance(figsize[i], int) and not isinstance(figsize[i], float):
                raise ValueError("Element {:d} in \"figsize\" not int/float.".format(i))
    else:
        figsize = (5, 4) # default

    from re import match
    from numpy import all, max, sum, where
    from .palettes import palette, defaultpalette, hclpalette, hclpalettes
    allowed = (palette, defaultpalette, hclpalette)

    # ---------------------------------------------------------------
    # In case input 'pals' is a list object:
    # Prepare a list of dicsts with names and colors.
    # ---------------------------------------------------------------
    single_palette = False
    if isinstance(pals, list):

        # Check if a single list of valid hex colors is given
        try:
            check = [match(u"^#[0-9A-Fa-f]{6}(o-9]{2})?$$", x) is not None for x in pals]
            if all(check): single_palette = True
            npals = 1
            ncols = len(pals)
            data  = [{"name": "unnamed", "colors": pals}]
        # Else check whehter or not the list contains valid objects
        except:
            # Check if all types are allowed
            check = [isinstance(x, allowed) for x in pals]
            if not all(check):
                import inspect
                raise ValueError("wrong input to function {:s}".format(inspect.stack()[0][3]))
            # Elxe prepare the objects we need for the plot
            data = []
            for pal in pals:
                data.append({"name": pal.name(), "colors": pal.colors(n)})

            npals = len(data)
            ncols = max([len(x["colors"]) for x in data])

    # ---------------------------------------------------------------
    # In case input 'pals' is a dict
    # Prepare a dict with lists of dicts containing name and colors.
    # ---------------------------------------------------------------
    elif isinstance(pals, dict):

        data = {}
        ncols = 0
        npals = 0
        for key,values in pals.items():
            check = [isinstance(x, allowed) for x in values]
            if not all(check):
                import inspect
                raise ValueError("wrong input to function {:s}".format(inspect.stack()[0][3]))
            # Else prepare the objects we need for the plot
            data[key] = []
            npals += 1 # Increase palette counter for each type
            for pal in values:
                data[key].append({"name": pal.name(), "colors": pal.colors(n)})
                if ncols < len(pal.colors(n)): ncols = len(pal.colors(n))
                npals += 1 # Increase palette counter for each palette

    # ---------------------------------------------------------------
    # Else unknown
    # ---------------------------------------------------------------
    elif isinstance(pals, hclpalettes):
        data  = {}
        ncols = n
        npals = 0
        for type_ in pals.get_palette_types():
            data[type_] = []
            npals += 1 # Increase palette counter for each type
            for pal in pals.get_palettes(type_):
                data[type_].append({"name": pal.name(), "colors": pal.colors(n)})
                npals += 1 # Increase palette counter for each palette

    # ---------------------------------------------------------------
    # Else unknown
    # ---------------------------------------------------------------
    else:
        import inspect
        raise Exception("got {:s} for {:s}: unknown input".format(
            type(pals), inspect.stack()[0][3]))


    # ---------------------------------------------------------------
    # Plotting functions
    # ---------------------------------------------------------------
    # Helper function to plot the color palettes
    # Calls "cmap()" function (see below)
    def plotcmaps(data, xpos, ypos, xstep, ystep, single_palette = False):
        for pal in data:

            # Adding text (only if not single_palette)
            if not single_palette:
                ax.text(xpos + xstep * 0.02, ypos, pal["name"], name_args)

            # Getting colors, plotting color bar
            xoff = 0.35 if not single_palette else 0.
            cmap(ax, pal["colors"], ncols, ypos - 0.8 * ystep / 2.,
                 ypos + 0.8 * ystep / 2., xpos + xoff * xstep, xpos + 0.99 * xstep) 

            ypos -= ystep
            # Start new column
            if ypos < 0:
                ypos = 1. - ystep / 2.; xpos = xpos + xstep

        return xpos, ypos

    # Helper function, draw the colormap
    def cmap(ax, cols, ncols, ylo, yhi, xmin, xmax, boxedupto = 6, frameupto = 9):

        from numpy import linspace
        from matplotlib.patches import Rectangle
        framecol = "#cecece"

        if ncols == 1:
            space     = 0.
            step      = xmax - xmin
            xlo       = [xmin]
            edgecolor = framecol

        elif ncols <= boxedupto:
            # -----------------------------------------
            # For n = 2
            #    |<------------ deltax ------------>|
            #  xmin                                xmax
            #    | -------------------------------- |
            #    |#####COL1#######   ######COL2######
            #    |               >|-|< space        |
            #    |<--- step ------->|               |
            #    |xlo[0]            |xlo[1]         |
            #    |                |xhi[0]           |xhi[1]
            #    
            deltax    = float(xmax - xmin)
            space     = deltax * 0.05 / (ncols - 1)
            step      = (deltax - float(ncols - 1.) * space) / float(ncols)
            xlo       = linspace(xmin, xmax - step + space, ncols)
            edgecolor = framecol

        # Else it is a bit simpler
        else:
            space     = 0.
            step      = float(xmax - xmin) / float(ncols)
            xlo       = linspace(xmin, xmax - float(xmax - xmin) / (ncols), ncols)
            edgecolor = framecol if ncols <= frameupto else None

        # Plotting the rectangles
        for i in range(0, len(cols)):
            rect = Rectangle((xlo[i], ylo), (step - space), yhi - ylo,
                    facecolor = cols[i], edgecolor = edgecolor)
            ax.add_patch(rect)

        # Outer frame
        if ncols > frameupto:
            rect = Rectangle((xmin, ylo), step * len(cols), yhi - ylo,
                             facecolor = "none", edgecolor = framecol)
            ax.add_patch(rect)


    # ---------------------------------------------------------------
    # Plot
    # ---------------------------------------------------------------
    # Initialize new figure
    fig, ax = plt.subplots(figsize = figsize)

    # Compute number of columns needed
    if npals <= nrow:
        ncol = 1
        nrow = npals
    else:
        from numpy import ceil
        ncol = ceil(float(npals) / float(nrow))

    # Plotting the different color maps
    ystep = 1. / float(nrow)
    ypos  = 1. - ystep / 2

    # Starting top left
    xstep  = 1. / float(ncol)
    xpos   = 0.

    # Adjusting outer margins
    fig.subplots_adjust(left = 0., bottom = 0., right  = 1.,
                        top  = 1., wspace = 0., hspace = 0.)
    ax.axis("off")
    # Small white margin around the plot
    ax.set_xlim(-0.01, 1.01); ax.set_ylim(-0.01, 1.01)

    # Styling of the texts
    type_args = {"weight": "bold", "va": "center", "ha": "left"}
    type_args["size"] = "large" if npals > 20 else "xx-large"
    name_args = {"va": "center", "ha": "left"}

    if isinstance(data, list):
        xpos, ypos = plotcmaps(data, xpos, ypos, xstep, ystep, single_palette)
    else:
        for type_,paldata in data.items():
            ax.text(xpos + xstep * 0.02, ypos, type_, type_args)
            ypos -= ystep
            # Start new column
            if ypos < 0:
                ypos = 1. - ystep / 2.; xpos = xpos + xstep
            xpos, ypos = plotcmaps(paldata, xpos, ypos, xstep, ystep)

    plt.show()

    return
