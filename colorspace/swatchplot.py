

def swatchplot(pals, show_names = True, nrow = 20, n = 5, **kwargs):
    """Create color palette swatch plots.

    The first argument ``pals`` is very flexible. It can be

    * List of hex colors
    * Single object which inherits :py:class:`colorspace.palettes.palette`,
        :py:class:`colorspace.palettes.hclpalette`,
        :py:class:`colorspace.colorlib.colorobject`
    * List of objects listed above (all of the same type or mixed).
    * Dictionary with lists of objects as above. If a dictionary is used
        the keys of the dictionary are used as 'subtitles' to group sets
        of palettes.
    * An object of class :py:class:`colorspace.palettes.hclpalettes`.

    Note: ``**kwargs`` can be used to specify the figure size of the resulting
    image by specifying ``figsize = (height, width)`` where both, ``height``
    and ``width`` must be int/float, specifying the height and width in inches.

    Args:
        pals: The color palettes or color objects to be visualized.
            See description for details and examples to demonstrate different
            usages.
        show_names (bool): Should palette names be shown (if available), defaults to True.
        nrow (int): Positive; maximum number of rows of swatches, defaults to 20.
        n (int): (Positive) number of colors to be drawn from palette objects, defaults to 5.

    Raises:
        TypeError: If ``nrow`` or ``n`` no integers.
        TypeError: If ``show_names`` not boolean.
        ValueERror: If ``nrow`` or ``n`` are not positive.

    Example:

        Some examples using different types of palettes/objects from
        simple lists of hex colors over HCL palettes
        (e.g., :py:class:`colorspace.diverging_hcl`), custom palette objects (``pal``;
        :py:class:`colorspace.palettes.palette`) to custom
        color objects (``cobject``; :py:class:`colorspace.colorlib.colorobject`).

        >>> from colorspace import *
        >>> 
        >>> # List of hex colors
        >>> swatchplot(['#7FBFF5', '#2A4962', '#111111', '#633C39', '#F8A29E'])
        >>> 
        >>> # Create a custom 'palette' (named):
        >>> from colorspace import palette
        >>> pal = palette(['#7FBFF5', '#2A4962', '#111111', '#633C39', '#F8A29E'], "named palette")
        >>> swatchplot(pal)
        >>> 
        >>> # A HCL palette. 'n' defines the number of colors.
        >>> swatchplot(sequential_hcl("PuBu"), n = 10)
        >>> 
        >>> # Combine all three
        >>> swatchplot([['#7FBFF5', '#2A4962', '#111111', '#633C39', '#F8A29E'],
        >>>             pal, sequential_hcl("PuBu")], n = 7)
        >>> 
        >>> 
        >>> 
        >>> #from matplotlib import pyplot as plt
        >>> #fig, axs = plt.subplots(2)
        >>> #fig.suptitle('Vertically stacked subplots')
        >>> 
        >>> # A color object (e.g., RGB, HCL, CIELUV, ...)
        >>> from colorspace.colorlib import hexcols
        >>> cobject  = hexcols(heat_hcl()(5))
        >>> cobject.to("HCL")
        >>> print(cobject)
        >>> swatchplot(cobject)
        >>> 
        >>> # Using dictionaries to add subtitles
        >>> # to 'group' different palettes.
        >>> swatchplot({"Diverging": [diverging_hcl(), diverging_hcl("Red-Green")],
        >>>             "Sequential": [sequential_hcl("ag_Sunset"), sequential_hcl("OrRd")],
        >>>             "Others": [['#7FBFF5', '#2A4962', '#111111', '#633C39', '#F8A29E'],
        >>>                        pal, sequential_hcl("PuBu")]}, n = 15)


    .. note:
        Requires the ``matplotlib`` module to be installed.
    """

    # Sanity checks: nrow and n only
    if not isinstance(nrow, int) or not isinstance(n, int):
        raise TypeError("Argument 'n' and 'nrow' must be integers.")
    if not isinstance(show_names, bool):
        raise TypeError("Argument 'show_names' must be boolean True or False.")
    if not nrow > 0 or not n > 0:
        raise ValueError("Argument 'nrow' and 'n' must both be positive integers.")


    # ---------------------------------------------------------------
    # Setting up matplotlib for plotting
    # ---------------------------------------------------------------

    # Requires matpotlib, a suggested package. If not avialable
    # raise an import error.
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        import inspect
        msg = "{:s} requires matplotlib to be installed: {:s}".format(
                inspect.stack()[0][3], str(e))
        raise ImportError(msg)

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

    # TODO REMOVE # # Prepares a list item
    # TODO REMOVE # def prepare_listelement(rec, n = 5):
    # TODO REMOVE #     from numpy import ndarray
    # TODO REMOVE #     if isinstance(rec, list) or isinstance(rec, ndarray):
    # TODO REMOVE #         colors = rec
    # TODO REMOVE #     else:
    # TODO REMOVE #         raise Exception("problems preparing list item in swatchplot")

    # TODO REMOVE #     # Check if all hex colors are valid. If not, a
    # TODO REMOVE #     # ValueError will be raised.
    # TODO REMOVE #     valid(rec)

    # TODO REMOVE #     # Return
    # TODO REMOVE #     return ["custom", colors]



    # ---------------------------------------------------------------
    # Prepare the palettes for plotting the swatches.
    # The function allows for various types as iput which will
    # be converted to a list of dicts, or a dict of list of dicts.
    #
    # Note that <name> can also be empty if the palette is unnamed.
    #
    # One single palette results in:
    #    [{"name": <name>, "colors": <list of hex colors>}]
    # Multiple palettes result in:
    #    [{"name": <name palette 1>, "colors": <list of hex colors palette 1>},
    #     {"name": <name palette 2>, "colors": <list of hex colors palette 2>},
    #     ...]
    # Dict of palette collections:
    #    {"First Collection":  [{"name": <name palette 1>, "colors": <list of hex colors palette 1>},
    #                           {"name": <name palette 2>, "colors": <list of hex colors palette 2>},
    #                           ...],
    #     "Second Collection": [{"name": <name palette 1>, "colors": <list of hex colors palette 1>},
    #                          {"name": <name palette 2>, "colors": <list of hex colors palette 2>},
    #                          ...]}
    # 'hclpalettes' object will also be converted into
    # a dictionary as shown above.
    # ---------------------------------------------------------------

    from numpy import all, max, sum, where
    from .palettes import palette, defaultpalette, hclpalette, hclpalettes
    from .colorlib import colorobject
    allowed = (palette, defaultpalette, hclpalette)


    # Helper functiin; return boolean True if this is a list of character
    # strings and all entries are valid hex colors.
    def _check_is_hex_list(vals):
        """Helper function: Check if input is a list of valid hex colors.

        Checking in put argument ``vals``. In case this is a list of
        strings we will furthermore check if these strings are valid
        HEX strings.

        Args:
            vals: Any kind of object.

        Returns:
            bool: Returns ``True`` if the input is a list of strings of valid hex colors.
            Else ``False`` will be returned.
        """
        check = False
        if isinstance(vals, list) and all([isinstance(x, str) for x in vals]):
            from re import match
            check = all([match(u"^#[0-9A-Fa-f]{6}(o-9]{2})?$$", x) is not None for x in vals])
        return check


    # Helper function; Convert whatever we get (and can) into a simple
    # dictionary containing "name" (name of palette, defaults to None)
    # and "colors", a hex-list with colors.
    def _pal_to_dict(x, n):
        """Helper function: Converts one palette or color object

        Converts all possible tpes of color palettes or objects into
        a dictionary. Used to prepare the inputs to swatchplot for the
        plot itself.

        Args:
            x: Some kind of a color-representing object. See swatchplot
                description for more details.
            n (int): Number of colors to be drawn from non-fixed palettes.

        Return:
            dict: Returns a single dict with ``name`` (name of the palette)
            and ``color`` (list of hex colors).

        Raises:
            Exception: If input ``x`` is of unknown type/format and cannot be converted.
            ValueError: If the palette does not provide any color at all.
        """

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
        elif isinstance(x, (palette, defaultpalette)):
            res = {"name": x.name(), "colors": x.colors()}
        else:
            raise Exception("Could not convert 'pals', improper input (type {:s}).".format(str(type(x))))
        # Checking length of color list
        if not len(res["colors"]) > 0:
            raise ValueError("Got at least one color object/palette with 0 colors.")
        return res


    # If 'pals' is:
    # * a list with proper hex values
    # * a single colorobject (e.g., RGB, HCL, CIELUV, ...)
    # * a single hclpalette object (e.g., diverging_hcl, sequential_hcl, ...)
    # * a single palette object
    # ... convert and put it into a list of length 1.
    def _convert_pals_to_list(pals, n):
        """Helper function: convert list of palettes or color objects.

        Used as a generic function to convert a series of palettes or color
        objects given by the user into the format we will need later on for
        creating ths watchplot.

        Args:
            pals: forwarded from main swatchplot call.
            n (int): number of colors for palette objects, forwarded from main swatchplot call.

        Returns:
            list: A dictionary and a list consiting of dictionaries. 
            The first dictionary contains meta information about the number
            of named palettes (``n_named``), the number of palettes (``n_palettes``),
            and the highest number of colors among these palettes as it can differ.
            The second list contains dictionaries where each dictionary contains
            two elements: ``name`` (str) defining name of the palette, and 
            ``colors`` (list) which is a list of hex colors (str), the colors
            to be displayed.
        """
        if (isinstance(pals, list) and _check_is_hex_list(pals)) or \
           isinstance(pals, colorobject) or isinstance(pals, hclpalette) or \
           isinstance(pals, palette):
            res = [_pal_to_dict(pals, n)]
        # What else? If we have a list we now iterate over the different items
        # and convert each entry into a dict using _pal_to_dict(). Will fail
        # if we have no rule for this.
        elif isinstance(pals, list):
            res = [_pal_to_dict(x, n) for x in pals]
        # If we got a dictionary we keep the keys as names and extract
        # the colors from the object(s) itself.
        elif isinstance(pals, dict):
            res = []
            for key,pal in pals.items():
                tmp = _pal_to_dict(pal, n)
                res.append({"name": key, "colors": tmp["colors"]})
        else:
            raise TypeError("Cannot deal with object of type {:s}".format(str(type(pals))))


        # Extract number of palettes, number of named palettes,
        # and max number of colors.
        meta = {"n_named":    sum([0 if x is None else 1 for x in res]),
                "n_palettes": len(res),
                "max_colors": max([len(x["colors"]) for x in res])}

        # Return meta info and  data
        return meta, res


    # If input is an object of class hclpalettes we will first
    # convert it into a dictionary which is then further processed.
    if isinstance(pals, hclpalettes):
        tmp = {}
        for type_ in pals.get_palette_types(): tmp[type_] = pals.get_palettes(type_)
        # Overwrite input object
        pals = tmp


    # If 'pals' is not a dictionary we don't have "groups".
    # will be converted into one single list (the resulting
    # object "data").
    if not isinstance(pals, dict):
        meta, data = _convert_pals_to_list(pals, n)

    # Else (dictionary provided by the user) we will
    # process each item in the dictionary individually.
    # The result "data" is a dictionary itself (not a list as above).
    else:
        meta = None
        data = {}
        for key,pal in pals.items():
            tmp_meta, tmp_data = _convert_pals_to_list(pal, n)
            data[key] = tmp_data
            # Store meta information
            if meta is None:
                meta = tmp_meta
            else:
                meta["n_named"]    += tmp_meta["n_named"]
                meta["n_palettes"] += tmp_meta["n_palettes"]
                meta["max_colors"] = max([meta["max_colors"], tmp_meta["max_colors"]])

    # No named palettes? Well, then we can set 'show_names' to FALSE.
    if meta["n_named"] == 0: show_names = False


    # ---------------------------------------------------------------
    # Now let's start the fun with plotting!
    # ---------------------------------------------------------------
    # Helper function to plot the color palettes
    # Calls "cmap()" function (see below)
    def _plot_swatches(data, xpos, ypos, xstep, ystep, show_names, single_palette = False):
        """Helper function: plotting a swatch.

        Args:
            data (list): List of dicts as prepared in the upper part
                of the swatchplot function.
            xpos (float): Current X position on the plot.
            ypos (float): Current Y position on the plot.
            xstep (float): Step in X-direction for columns.
            ystep (float): Step in Y-direction for rows.
            single_palette (bool): Set to true if we have one single palette;
                changes the x-offset to make use of the full canvas.

        Raises:
            TypeError: Wrong unexpected type of input argument (xpos, ypos, xstep, ystep,
                single_palette, and show_names).
            ValueError: Arguments out of valid bounds (xpos, ypos, xstep, ystep).
        """

        if not isinstance(xpos, float)  or not isinstance(ypos, float) or \
           not isinstance(xstep, float) or not isinstance(ystep, float) or \
           not isinstance(show_names, bool) or not isinstance(single_palette, bool):
               raise TypeError("Non-suitable input argument (wrong type).")
        if not xpos  >= 0. or not xpos  <= 1. or not ypos  >= 0. or not ypos  <= 1. or \
           not xstep >= 0. or not xstep <= 1. or not ystep >= 0. or not ystep <= 1:
            raise ValueError("At least one of xpos/ypos/xstep/ystep out of valid bounds.")


        # Plotting one swatch after another.
        # Calculates new x/y position which will be returned
        # and re-used for the next set of palettes (if there are any).
        for pal in data:

            # Adding text (only if not single_palette)
            if show_names and not single_palette:
                ax.text(xpos + xstep * 0.02, ypos, pal["name"], name_args)

            # Getting colors, plotting color bar
            xoff = 0.35 if show_names and not single_palette else 0.
            _swatch(ax, pal["colors"], len(pal["colors"]), ypos - 0.8 * ystep / 2.,
                    ypos + 0.8 * ystep / 2., xpos + xoff * xstep, xpos + 0.99 * xstep) 

            ypos -= ystep
            # Start new column
            if ypos < 0:
                ypos = 1. - ystep / 2.; xpos = xpos + xstep

        return xpos, ypos


    # Helper function, draw the colormap
    def _swatch(ax, cols, ncols, ylo, yhi, xmin, xmax, boxedupto = 6, frameupto = 9):

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

    # Compute number of columns needed. Thus, we first of all have to check
    # if 'data' is a list (no group-titles) or a dictionary (each block/group
    # of palettes gets a title -> more space needed).
    if isinstance(data, dict):
        nblocks = meta["n_palettes"] + len(data)
    else:
        nblocks = meta["n_palettes"]
    if nblocks <= nrow:
        ncol = 1
        nrow = nblocks
    else:
        from numpy import ceil
        ncol = ceil(float(nblocks) / float(nrow))

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
    type_args["size"] = "large" if meta["n_palettes"] > 20 else "xx-large"
    name_args = {"va": "center", "ha": "left"}

    # Single swatch
    if meta["n_palettes"] == 1:
        xpos, ypos = _plot_swatches(data, xpos, ypos, xstep, ystep, show_names, True)
    # Multiple palettes but no titles/grouping
    elif isinstance(data, list):
        xpos, ypos = _plot_swatches(data, xpos, ypos, xstep, ystep, show_names)
    # Else dictionary: adding additional titles for grouping
    else:
        for key,pal in data.items():
            ax.text(xpos + xstep * 0.02, ypos, key, type_args)
            ypos -= ystep
            # Start new column
            if ypos < 0:
                ypos = 1. - ystep / 2.; xpos = xpos + xstep
            xpos, ypos = _plot_swatches(pal, xpos, ypos, xstep, ystep, show_names)

    plt.show()

    return
