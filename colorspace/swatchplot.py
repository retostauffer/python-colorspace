

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

    from numpy import all, max, sum, where
    from .palettes import palette, defaultpalette, hclpalette, hclpalettes
    from .colorlib import colorobject
    allowed = (palette, defaultpalette, hclpalette)


    # Helper functiin; return boolean True if this is a list of character
    # strings and all entries are valid hex colors.
    def _check_is_hex_list(vals):
        check = False
        if isinstance(vals, list) and all([isinstance(x, str) for x in vals]):
            from re import match
            check = all([match(u"^#[0-9A-Fa-f]{6}(o-9]{2})?$$", x) is not None for x in vals])
        return check


    # Helper function; Convert whatever we get (and can) into a simple
    # dictionary containing "name" (name of palette, defaults to None)
    # and "colors", a hex-list with colors.
    def _pal_to_dict(x, n):
        # In case argument 'pals' is a list we first check if this is
        # a valid list of hex colors. If so: convert to dictionary.
        if isinstance(x, list) and _check_is_hex_list(x):
            res = {"name": None, "colors": x}
        # Single colorobject (e.g., RGB, HCL, CIELUV, ...)
        elif isinstance(x, colorobject):
            res = {"name": None, "colors": x.colors(n)}
        # Single color hclpalette object (e.g., diverging_hcl, sequential_hcl, ...)
        elif isinstance(x, hclpalette):
            res = {"name": x.name(), "colors": x.colors(n)}
        # Single palette object (custom palette)
        elif isinstance(x, palette):
            res = {"name": x.name(), "colors": x.colors()}
        else:
            raise Exception("Could not convert 'pals', improper input (type {:s}).".format(str(type(x))))
        # Checking length of color list
        if not len(res["colors"]) > 0:
            raise Exception("Got at least one color object/palette with 0 colors.")
        return res


    # If 'pals' is:
    # * a list with proper hex values
    # * a single colorobject (e.g., RGB, HCL, CIELUV, ...)
    # * a single hclpalette object (e.g., diverging_hcl, sequential_hcl, ...)
    # * a single palette object
    # ... convert and put it into a list of length 1.
    if (isinstance(pals, list) and _check_is_hex_list(pals)) or \
       isinstance(pals, colorobject) or isinstance(pals, hclpalette) or \
       isinstance(pals, palette):
        data = [_pal_to_dict(pals, n)]
    # What else? If we have a list we now iterate over the different items
    # and convert each entry into a dict using _pal_to_dict(). Will fail
    # if we have no rule for this.
    elif isinstance(pals, list):
        data = [_pal_to_dict(x, n) for x in pals]
    # If we got a dictionary we keep the keys as names and extract
    # the colors from the object(s) itself.
    elif isinstance(pals, dict):
        data = []
        for key,pal in pals.items():
            tmp = _pal_to_dict(pal, n)
            data.append({"name": key, "colors": tmp["colors"]})


    # Extract number of palettes, number of named palettes,
    # and max number of colors.
    nnamed    = sum([1 if x is None else 0 for x in data])
    npalettes = len(data)
    ncolors   = max([len(x["colors"]) for x in data])



    # ---------------------------------------------------------------
    # Plotting functions
    # ---------------------------------------------------------------
    # Helper function to plot the color palettes
    # Calls "cmap()" function (see below)
    #
    # TODO(Reto): Well, now I lost the possibility to have subtitles.
    # Or titles. Whatever. I will go for 'args' and 'kwargs' instead.

    def _plotcmaps(data, xpos, ypos, xstep, ystep, single_palette = False):
        ####for pal in data:

        ####    # Adding text (only if not single_palette)
        ####    if not single_palette:
        ####        ax.text(xpos + xstep * 0.02, ypos, data["name"], name_args)

        ####    # Getting colors, plotting color bar
        ####    xoff = 0.35 if not single_palette else 0.
        ####    _cmap(ax, data["colors"], len(data["colors"]), ypos - 0.8 * ystep / 2.,
        ####         ypos + 0.8 * ystep / 2., xpos + xoff * xstep, xpos + 0.99 * xstep) 

        ####    ypos -= ystep
        ####    # Start new column
        ####    if ypos < 0:
        ####        ypos = 1. - ystep / 2.; xpos = xpos + xstep


        # Adding text (only if not single_palette)
        if not single_palette:
            ax.text(xpos + xstep * 0.02, ypos, data["name"], name_args)

        # Getting colors, plotting color bar
        xoff = 0.35 if not single_palette else 0.
        _cmap(ax, data["colors"], len(data["colors"]), ypos - 0.8 * ystep / 2.,
             ypos + 0.8 * ystep / 2., xpos + xoff * xstep, xpos + 0.99 * xstep) 

        ypos -= ystep
        # Start new column
        if ypos < 0:
            ypos = 1. - ystep / 2.; xpos = xpos + xstep

        return xpos, ypos

    # Helper function, draw the colormap
    def _cmap(ax, cols, ncols, ylo, yhi, xmin, xmax, boxedupto = 6, frameupto = 9):

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
    if npalettes <= nrow:
        ncol = 1
        nrow = npalettes
    else:
        from numpy import ceil
        ncol = ceil(float(npalettes) / float(nrow))

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
    type_args["size"] = "large" if npalettes > 20 else "xx-large"
    name_args = {"va": "center", "ha": "left"}

    if npalettes == 1:
        xpos, ypos = _plotcmaps(data[0], xpos, ypos, xstep, ystep, True)
    else:
        for pal in data:
            print(pal)
            #ax.text(xpos + xstep * 0.02, ypos, pal["name"], type_args)
            #ypos -= ystep
            # Start new column
            if ypos < 0:
                ypos = 1. - ystep / 2.; xpos = xpos + xstep
            xpos, ypos = _plotcmaps(pal, xpos, ypos, xstep, ystep)

    plt.show()

    return
