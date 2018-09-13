
    
def hcl_palettes(n = 5, type_ = None, name = None, plot = False, custom = None):
    """hcl_palettes(n = 7, type_ = None, names = None, plot = False, custom = None)
    
    Gives access to the default color palettes of the colorspace package.

    The method can be used to display the default color palettes or subsets or
    to get a :py:class:`palettes.hclpalettes` object. 
    The inputs ``type_`` and ``name`` can be used to retrieve a custom subset,
    ``custom`` can be used to add custom :py:class:`palettes.defaultpalette`
    objects if needed.

    Parameters
    ----------
    n : int
        number of colors to be plotted, default is 7. Only used
            if plot = True.
    type_ : None, str, list of str
        given a string or a list of strings only a subset of all available
        default color maps will be displayed. If not set, all default
        palettes will be returned/plotted. Can be used in combination with
        input argument ``name``.
    name : None, str, list of str
        similar to ``type_``. If not specified all palettes will be returned.
        Can be set to a string or a list of strings containing the names
        of the palettes which should be returned/plotted.
    plot : bool
        if ``False`` (default) a hclpalettes object will be returned
        containing the (subset) of default color palettes.
        Note that matplotlib has to be installed if plot is set to True.
    custom : :py:class:`palettes.defaultpalette`
        one or multiple defaultpalettes can be provided in addition.
    args : ...
        currently unused.

    Examples
    --------
    >>> # Basic usage
    >>> from colorspace.hcl_palettes import hcl_palettes
    >>>
    >>> print hcl_palettes()
    >>> print hcl_palettes(type_ = "Diverging")
    >>> print hcl_palettes(name = ["Oranges", "Tropic"]) 
    >>>
    >>> print hcl_palettes(type_ = "Diverging", plot = True)
    >>> print hcl_palettes(name = ["Oranges", "Tropic"], plot = True) 
    >>> 
    >>> # Loading all available palettes (just to make custom palettes)
    >>> from colorspace.palettes import hclpalettes
    >>> pal = hclpalettes()
    >>> c1 = pal.get_palette("Oranges")
    >>> c2 = pal.get_palette("Greens")
    >>> 
    >>> # Modify the custom palettes
    >>> c1.set(h1 = 99, l2 = 30, l1 = 30)
    >>> c1.rename("Retos custom 1")
    >>> c2.set(h1 = -30, l1 = 40, l2 = 30, c1 = 30, c2 = 40)
    >>> c2.rename("Retos custom 1")
    >>>
    >>> hcl_palettes(type_ = "Custom", custom = [c1, c2], plot = True)
    """
    
    # Loading pre-defined palettes from within the package
    from . import hclpalettes
    pals = hclpalettes()                    # Loading palettes

    # If custom palettes have been added: add them as well (if
    # the types are correct, of course).
    if not custom is None:
        from numpy import all
        from palettes import defaultpalette
        def customerror():
            import inspect
            str = "list with custom palettes provided to {:s}".format(inspect.stack()[0][3])
            str += " but not all elements are of type defaultpalette"
            raise ValueError(str)

        if isinstance(custom, defaultpalette):
            pals._palettes_["Custom"] = [custom]
        # Check if all inputs are of correct type
        elif isinstance(custom, list):
            if not all([isinstance(x, defaultpalette) for x in custom]):
                    customerror()
            pals._palettes_["Custom"] = custom
        # Else append pals._palettes_["Custom"] = custom
        else:
            raise ValueError("input custom to {:s} misspecified".format(self.__class__.__name__))


    if not type_ is None:
        if isinstance(type_, str): type_ = [type_]
        
        # Drop palettes from hclpalettes object not requested
        # by the user.
        for t in pals.get_palette_types():
            if not t.upper() in [x.upper() for x in type_]:
                del pals._palettes_[t]
    else:
        type_ = pals.get_palette_types()

    # Now dropping all color maps not matching a name, if the
    # user has set a name.
    if not name is None:
        if isinstance(name, str): name = [name]
        # Looping over palette types
        for t in pals.get_palette_types():
            palettenames = [p.name() for p in pals.get_palettes(t)]
            drop = []
            for i in range(0, len(palettenames)):
                if not palettenames[i] in name: drop.append(i)
            # Drop all?
            if len(drop) == len(palettenames):
                del pals._palettes_[t]
            else:
                drop.sort(reverse = True)
                for i in drop: del pals._palettes_[t][i]

    # No palettes survived?
    if len(pals.get_palettes()) == 0:
        import inspect
        raise Exception("no palettes found in {:s} matching one of: {:s}".format(
                inspect.stack()[0][3], ", ".join(type_)))

    # Return if plot is not required
    if not plot:
        return pals
    else:
        swatchplot(pals, n = n)
        return



def swatchplot(pals, nrow = 20, n = 5, *args, **kwargs):
    """


    Examples
    --------

    An example using custom :py:class:`palettes.palette`, once
    named and once unnamed:

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
                inspect.stack()[0][3], e)
        raise ImportError(msg)

    # Prepares a list item
    def prepare_listelement(rec, n = 5):
        from numpy import ndarray
        if isinstance(rec, list) or isinstance(rec, ndarray):
            colors = rec
        else:
            print type(rec)
            sys.exit("--exit in parpare list item--")

        # Check if all hex colors are valid. If not, a
        # ValueError will be raised.
        valid(rec)

        # Return
        return ["custom", colors]

    from numpy import all, max, sum
    from palettes import palette, defaultpalette, hclpalette, hclpalettes
    allowed = (palette, defaultpalette, hclpalette)

    # ---------------------------------------------------------------
    # In case input 'pals' is a list object:
    # Prepare a list of dicsts with names and colors.
    # ---------------------------------------------------------------
    if isinstance(pals, list):
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
    def plotcmaps(data, xpos, ypos, xstep, ystep):
        for pal in data:

            # Adding text
            ax.text(xpos + xstep * 0.02, ypos, pal["name"], name_args)

            # Getting colors, plotting color bar
            cmap(ax, pal["colors"], ncols, ypos - 0.8 * ystep / 2.,
                 ypos + 0.8 * ystep / 2., xpos + 0.35 * xstep, xpos + 0.99 * xstep) 

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
    fig, ax = plt.subplots()

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
        xpos, ypos = plotcmaps(data, xpos, ypos, xstep, ystep)
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
