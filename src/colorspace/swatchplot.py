

def swatchplot(pals, show_names = True, nrow = 20, n = 5, cvd = None, **kwargs):
    """Palette Swatch Plot

    Visualization of color palettes in columns of color swatches.
    The first argument `pals` is very flexible and can be:

    * List of hex colors,
    * a single object which inherits from `colorspace.palettes.palette`,
        `colorspace.palettes.hclpalette`,
        `colorspace.colorlib.colorobject`,
    * a list of objects listed above (all of the same type or mixed),
    * a dictionary with lists of objects as above. If a dictionary is used
        the keys of the dictionary are used as 'subtitles' to group sets
        of palettes,
    * an object of class `colorspace.palettes.hclpalettes`,
    * or an object of class `matplotlib.colors.LinearSegmentedColormap` or
        `matplotlib.colors.ListedColormap`.

    Requires the `matplotlib` to be installed.

    Args:
        pals: The color palettes or color objects to be visualized.
            See description for details and examples to demonstrate different
            usages.
        show_names (bool): Should palette names be shown (if available), defaults to True.
        nrow (int): Maximum number of rows of swatches, defaults to `20`.
        n (int): Number of colors to be drawn from palette objects, defaults to `5`.
        cvd (None or list): Allows to display one or multiple palettes and how they look
            with emulated color vision deficiencies. If `None`, this is not applied.
            Can be set to a list of characters. Allowed:
            `"protan"`, `"tritan"`, `"deutan"`, `"desaturate"` corresponding to the functions
            :py:func:`protan <colorspace.CVD.protan>`,
            :py:func:`tritan <colorspace.CVD.tritan>`,
            :py:func:`deutan <colorspace.CVD.deutan>`,
            :py:func:`desaturate <colorspace.CVD.desaturate>`.
        **kwargs: forwarded to `matplotlib.pyplot.subplot`, can be used to control e.g.,
            `figsize`.

    Example:

        >>> from colorspace import swatchplot, palette
        >>> from colorspace import sequential_hcl, diverging_hcl, heat_hcl
        >>>
        >>> # List of hex colors
        >>> swatchplot(['#7FBFF5', '#2A4962', '#111111', '#633C39', '#F8A29E'],
        >>>            figsize = (7, 0.5));
        >>>
        >>> #: Create a custom 'palette' (named):
        >>> pal = palette(['#7FBFF5', '#2A4962', '#111111', '#633C39', '#F8A29E'],
        >>>               "Custom Named Palette")
        >>> swatchplot(pal, figsize = (7, 0.5));
        >>>
        >>> #: A HCL palette. 'n' defines the number of colors.
        >>> swatchplot(sequential_hcl("PuBu"), n = 10,
        >>>            figsize = (7, 0.5));
        >>>
        >>> #: Combine all three
        >>> swatchplot([['#7FBFF5', '#2A4962', '#111111', '#633C39', '#F8A29E'],
        >>>             pal, sequential_hcl("PuBu")], n = 7,
        >>>             figsize = (7, 1.5));
        >>>
        >>> #: A color object (e.g., RGB, HCL, CIELUV, ...)
        >>> from colorspace.colorlib import hexcols
        >>> cobject  = hexcols(heat_hcl()(5))
        >>> cobject.to("HCL")
        >>> print(cobject)
        >>> #:
        >>> swatchplot(cobject, figsize = (7, 0.5));
        >>>
        >>> #: Using dictionaries to add subtitles
        >>> # to 'group' different palettes.
        >>> swatchplot({"Diverging": [diverging_hcl(), diverging_hcl("Red-Green")],
        >>>             "Sequential": [sequential_hcl("ag_Sunset"), sequential_hcl("OrRd")],
        >>>             "Others": [['#7FBFF5', '#2A4962', '#111111', '#633C39', '#F8A29E'],
        >>>                        pal, sequential_hcl("PuBu")]}, n = 15);

    Raises:
        ImportError: If `matplotlib` is not installed.
        TypeError: If `nrow` or `n` no int.
        TypeError: If `show_names` not bool.
        ValueError: If `nrow` or `n` are not positive.
        ImportError: If `matplotlib.pyplot` cannot be imported, maybe `matplotlib` not installed?
    """

    # Requires matplotlib. If not available, throw ImportError
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("problems importing matplotlib.pyplt (not installed?)")

    from numpy import all

    # Sanity checks: nrow and n only
    if not isinstance(nrow, int):         raise TypeError("argument `nrow` must be int")
    if not isinstance(n, int):            raise TypeError("argument `n` must be int")
    if not isinstance(show_names, bool):  raise TypeError("argument `show_names` must be bool")
    if not nrow > 0:                      raise ValueError("argument `nrow` must be positive")
    if not n > 0:                         raise ValueError("argument `n` must be positive")

    # Checking optional cvd argument
    if not isinstance(cvd, (str, list, type(None))):
        raise TypeError("unexpected input on argument `cvd`")
    if isinstance(cvd, list):
        if not all([isinstance(x, str) for x in cvd]):
            raise ValueError("unexpected input on argument for `cvd`")
    elif isinstance(cvd, str):
        cvd = [cvd]

    # Checking values
    if isinstance(cvd, list):
        valid_cvd_types = ["protan", "tritan", "deutan", "desaturate"]
        if not all([x in valid_cvd_types for x in cvd]):
            raise ValueError(f"allowed values for argument `cvd` are: {', '.join(valid_cvd_types)}")


    # ---------------------------------------------------------------
    # Setting up matplotlib for plotting
    # ---------------------------------------------------------------

    # Allow the user to specify figure size if needed
    if "figsize" in kwargs:
        figsize = kwargs["figsize"]
        if not isinstance(figsize, tuple) or not len(figsize) == 2:
            raise ValueError("argument `figsize` must be a tuple of length 2")
        for i in range(2):
            if not isinstance(figsize[i], int) and not isinstance(figsize[i], float):
                raise ValueError(f"element [{i}] in `figsize` not int or float.")
    else:
        figsize = (5, 4) # default figure size


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
    from .utils import check_hex_colors
    allowed = (palette, defaultpalette, hclpalette)

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
            dict: Returns a single dict with `name` (name of the palette)
            and `color` (list of hex colors).

        Raises:
            Exception: If input `x` is of unknown type/format and cannot be converted.
            ValueError: If the palette does not provide any color at all.
        """


        # In case argument 'pals' is a list we first check if this is
        # a valid list of hex colors. If so: convert to dictionary.
        if isinstance(x, list):
            res = {"name": None, "colors": check_hex_colors(x)}
        # Single colorobject (e.g., RGB, HCL, CIELUV, ...)
        elif isinstance(x, colorobject):
            res = {"name": None, "colors": x.colors(n)}
        # Single color hclpalette object (e.g., diverging_hcl, sequential_hcl, ...)
        elif isinstance(x, hclpalette):
            res = {"name": x.name(), "colors": x.colors(n)}
        # Single palette object (custom palette)
        elif isinstance(x, (palette, defaultpalette)):
            res = {"name": x.name(), "colors": x.colors(n)}
        else:
            raise Exception(f"could not convert `pals`, improper input (type {type(x)}).")

        # Checking length of color list
        if not len(res["colors"]) > 0:
            raise ValueError(f"got at least one color object/palette with 0 colors")
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
            of named palettes (`n_named`), the number of palettes (`n_palettes`),
            and the highest number of colors among these palettes as it can differ.
            The second list contains dictionaries where each dictionary contains
            two elements: `name` (str) defining name of the palette, and 
            `colors` (list) which is a list of hex colors (str), the colors
            to be displayed.
        """

        from matplotlib.colors import LinearSegmentedColormap, ListedColormap

        # In case we get a list let's check if we have a valid hex list.
        # Can also be a list of list processed later on.
        if isinstance(pals, (str, list)):
            try:
                pals = [check_hex_colors(pals)]
            except:
                pass

        if isinstance(pals, colorobject) or \
           isinstance(pals, hclpalette) or isinstance(pals, palette):
            res = [_pal_to_dict(pals, n)]
        # What else? If we have a list we now iterate over the different items
        # and convert each entry into a dict using _pal_to_dict(). Will fail
        # if we have no rule for this.
        elif isinstance(pals, list):
            res = [_pal_to_dict(x, n) for x in pals]
        # Matplotlib colormap? Convert
        elif isinstance(pals, (LinearSegmentedColormap, ListedColormap)):
            from .cmap import cmap_to_sRGB
            tmp_cols = cmap_to_sRGB(pals, n).colors()
            res = [_pal_to_dict(palette(tmp_cols, name = pals.name), n)]
            del tmp_cols
        # If we got a dictionary we keep the keys as names and extract
        # the colors from the object(s) itself.
        elif isinstance(pals, dict):
            res = []
            for key,pal in pals.items():
                tmp = _pal_to_dict(pal, n)
                res.append({"name": key, "colors": tmp["colors"]})
        else:
            raise TypeError(f"cannot deal with object of type \"{type(pals)}\"")


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
    # User request for CVD emulated palettes?
    # ---------------------------------------------------------------
    if not cvd is None:
        new_data = dict()
        counter  = 0

        # Reduce dictionary to list
        if isinstance(data, dict):
            from warnings import warn
            warn("Dictionary inputs to swatchplot in combination with cvd not allowed, " + \
                 "dictionary will be reduced to a list.")
            tmp_data = []
            for rec in data.values(): tmp_data += rec
            data = tmp_data; del tmp_data

        # Convert list back into a dictionary; each entry is one of the
        # palettes provided by the user with a series of palettes according
        # to the types of color vision deficiencies specified
        if isinstance(data, list):
            from colorspace import CVD
            for rec in data:
                tmp = [{"name": "original", "colors": rec["colors"]}]
                counter += 1
                for fn in cvd:
                    tmp.append({"name": fn, "colors": getattr(CVD, fn)(rec["colors"])})
                    counter += 1
                new_data[rec["name"]] = tmp

        # Overwrite existing 'data' object and re-specify the
        # meta information. From here on the plotting is the same
        # as if the user would have had provided a dictionary with a
        # series of named palettes in combination with cvd = None.
        data = new_data
        meta["n_named"]    = counter
        meta["n_palettes"] = counter
        del new_data, counter


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
               raise TypeError("non-suitable input argument (wrong type)")
        if not xpos  >= 0. or not xpos  <= 1. or not ypos  >= 0. or not ypos  <= 1. or \
           not xstep >= 0. or not xstep <= 1. or not ystep >= 0. or not ystep <= 1:
            raise ValueError("at least one of xpos/ypos/xstep/ystep out of valid bounds")


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
                    facecolor = "#FFFFFF" if cols[i] is None else cols[i],
                    edgecolor = edgecolor)
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
    #fig, ax = plt.subplots(figsize = figsize)
    if "files_regex" in kwargs.keys(): del kwargs["files_regex"]
    fig, ax = plt.subplots(**kwargs)

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

    # One or multiple palettes but no titles/grouping
    if isinstance(data, list):
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

    # Show figure
    plt.show()

    return fig


