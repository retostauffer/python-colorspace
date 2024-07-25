



def hclplot(x, _type = None, h = None, c = None, l = None, axes = True,
            linewidth = 1, s = 150, **kwargs):
    """Palette Plot in HCL Space

    The function `hclplot` is an auxiliary function for illustrating
    the trajectories of color palettes in two-dimensional HCL space
    projections. It collapses over one of the three coordinates
    (either the hue H or the luminance L) and displays a heatmap of
    colors combining the remaining two dimensions. The coordinates for
    the given color palette are highlighted to bring out its
    trajectory.

    The function `hclplot` has been designed to work well with the
    :py:func:`hcl_palettes <colorspace.hcl_palettes.hcl_palettes>`
    in this package. While it is possible to apply it
    to other color palettes as well, the results might look weird or
    confusing if these palettes are constructed very differently.

    More specifically, the following palettes can be visualized well:

    * Qualitative with (approximately) constant luminance. In this
      case, `hclplot` shows a hue-chroma plane (in polar
      coordinates), keeping luminance at a fixed level (by default
      displayed in the main title of the plot). If the luminance
      is, in fact, not approximately constant, the luminance varies
      along with hue and chroma, using a simple linear function
      (fitted by least squares). `hclplot` shows a
      chroma-luminance plane, keeping hue at a fixed level (by
      default displayed in the main title of the plot). If the hue
      is, in fact, not approximately constant, the hue varies along
      with chroma and luminance, using a simple linear function
      (fitted by least squares.

    * Diverging with two (approximately) constant hues: This case
      is visualized with two back-to-back sequential displays.

    To infer the type of display to use, by default, the following
    heuristic is used: If luminance is not approximately constant
    (`range > 10`) and follows rougly a triangular pattern, a diverging
    display is used. If luminance is not constant and follows roughly
    a linear pattern, a sequential display is used. Otherwise a
    qualitative display is used.

    Note: Requires `matplotlib` to be installed.

    Args:
        x (str, list, colorobject): An object which can be converted into
            a :py:class:`hexcols <colorspace.colorlib.hexcols>` object.
        _type (None, str): Specifying which type of palette should be
            visualized (`"qualitative"`, `"sequential"`, or `"diverging"`). For
            qualitative palettes a hue-chroma plane is used, otherwise a
            chroma-luminance plane. By default (`_type = None`) the type is
            inferred from the luminance trajectory corresponding to `x`.
        h (None, int, float): If int or float, it must be within `[-360, 360]`
        c (None, int, float): If int or float, it must be positive
        l (None, int, float): If int or float, it must be positive
        axes (bool): Wheter or not axes should be drawn, defaults to `True`.
        linewidth (int, float, None): Line width, if set `0` or `None` the line connecting
            the colors of the palette will be suppressed.
        s (int, float, None): Marker size, defaults to `150`. If set `0` or `None` the
            position of the colors of the palette will be suppressed.
        **kwargs: Allowed to overwrite some default settings such as
            `title` (str), `xlabel` (str), `ylabel` (str), `figsize` (forwarded
            to `pyplot.figure`). `xlabel`/`ylabel` only used for qualitative
            and diverging plots. A matplotlib axis can be provided via `ax`
            (object of type `matplotlib.axes._axes.Axes`) which allows to draw
            multiple HCL spaces on one figure.

    Returns:
        No return, visualizes the palette and HCL space either on a new
        figure or on an existing axis (if `ax` is provided, see `**kwargs`).

    Examples:

        >>> # Sequential HCL palette, hclplot with all available options
        >>> from colorspace import sequential_hcl, hclplot
        >>>
        >>> x = sequential_hcl("PurpOr")(5)
        >>> hclplot(x,
        >>>         xlabel  = "Chroma dimension",
        >>>         ylabel  = "Luminance dimension",
        >>>         title   = "hclplot Example (Sequential)",
        >>>         figsize = (5, 5), s = 250);
        >>> #: Multiple subplots
        >>> import matplotlib.pyplot as plt 
        >>> from colorspace import sequential_hcl, hclplot
        >>> 
        >>> # Three different palettes  
        >>> pal1 = sequential_hcl(h = 260, c = 80,          l = [35, 95], power = 1)
        >>> pal2 = sequential_hcl(h = 245, c = [40, 75, 0], l = [30, 95], power = 1)
        >>> pal3 = sequential_hcl(h = 245, c = [40, 75, 0], l = [30, 95], power = [0.8, 1.4])
        >>> #:
        >>> pal1.show_settings()
        >>> #:
        >>> pal2.show_settings()
        >>> #:
        >>> pal3.show_settings()
        >>> 
        >>> #:
        >>> fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (12, 4))
        >>> hclplot(pal1(7), ax = ax1)            
        >>> hclplot(pal2(7), ax = ax2) 
        >>> hclplot(pal3(7), ax = ax3) 
        >>> plt.show();
        >>>
        >>> #: Another example with two sequential and one
        >>> # diverging palettes with custom settings
        >>> from colorspace import sequential_hcl, diverging_hcl, hclplot
        >>> import matplotlib.pyplot as plt
        >>>
        >>> pal1 = sequential_hcl(h = [260, 220], c = [50, 0, 75], l = [30, 95], power = 1)       
        >>> pal2 = sequential_hcl(h = [260, 60],  c = 60,          l = [40, 95], power = 1)  
        >>> pal3 = diverging_hcl( h = [260, 0],   c = 80,          l = [35, 95], power = 1)  
        >>> 
        >>> fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (12, 4))
        >>> hclplot(pal1(7), ax = ax1)
        >>> hclplot(pal2(7), ax = ax2)
        >>> hclplot(pal3(7), ax = ax3)
        >>> plt.show();
        >>>
        >>> #: Another example with two sequential and one
        >>> # diverging palettes with custom settings
        >>> from colorspace import sequential_hcl, diverging_hcl, qualitative_hcl, hclplot
        >>> import matplotlib.pyplot as plt
        >>>
        >>> fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (12, 4))
        >>> hclplot(sequential_hcl()(7), ax = ax1)
        >>> hclplot(diverging_hcl()(7), ax = ax2)
        >>> hclplot(qualitative_hcl()(7), ax = ax3)
        >>> plt.show();

    Raises:
        ImportError: If `matplotlib` is not installed.
        TypeError: If argument `_type` is not None or str.
        TypeError: If argument `_type` is str but not one of the allowed types.
        TypeError: If argument `c`, and/or `l` are not None, str, or int.
        TypeError: If argument `h` is neither None, int, float, or tuple, or tuple
            not containing int/float.
        ValueError: If `c`,`l` is not None and smaller or equal to `0` (must be positive).
        ValueError: If `h` is tuple length `0` or `>2` (must be one or two).
        ValueError: If `h` is not None and not within the range `[-360, 360]`.
        TypeError: If `s`, `linewidth` are not int, float, or None.
        ValueError: If `s`, `linewidth` are int/float but negative (`<0`).
    """

    # Requires matpotlib for plotting. If not available, throw ImportError
    try:
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap, ListedColormap
    except ImportError as e:
        raise ImportError("problems importing matplotlib.pyplt (not installed?)")

    from .colorlib import hexcols
    from .statshelper import split, nprange, lm
    import numpy as np
    import warnings

    # Sanity checks
    if not isinstance(_type, (type(None), str)):
        raise TypeError("argument `_type` must be None or str")

    if not isinstance(c, (int, float, type(None))) or isinstance(c, bool):
        raise TypeError("argument `c` must be None, int, or float")
    elif c is not None and c <= 0:
        raise ValueError("argument `c` must be positive if set")

    if not isinstance(l, (int, float, type(None))) or isinstance(l, bool):
        raise TypeError("argument `l` must be None, int, or float")
    elif l is not None and l <= 0:
        raise ValueError("argument `l` must be positive if set")

    # Checking line width and marker size (linewidth, s)
    if not isinstance(linewidth, (type(None), int, float)):
        raise TypeError("argument `linewidth` must be None or int")
    elif isinstance(linewidth, (int, float)) and linewidth < 0.:
        raise ValueError("argument `linewidth` must be >= 0.")
    elif isinstance(linewidth, (int, float)) and linewidth == 0.:
        linewidth = None # Setting line width to 0

    if not isinstance(s, (type(None), int, float)):
        raise TypeError("argument `s` must be None, int or float")
    elif isinstance(s, (int, float)) and s < 0.:
        raise ValueError("argument `s` must be >= 0.")
    elif isinstance(s, (int, float)) and s == 0.:
        s = None # Setting line width to 0

    allowed_types = ["diverging", "sequential", "qualitative"]
    if isinstance(_type, str):
        if not _type.lower() in allowed_types:
            raise ValueError("argument `_type` invalid. Must be None or any of: {', '.join(allowed_types)}")
        _type = _type.lower()

    # Testin 'h' which is a bit more complex
    if not isinstance(h, (int, float, type(None), tuple)) or isinstance(h, bool):
        raise TypeError("argument `h` must be None, int, or float, or tuple")
    # If int/float: Convert to tuple for easier handling later on.
    elif isinstance(h, (int, float)):
        h = (h, )
    # In case h is not None it is now a tuple. Check that length is 1 or 2,
    # and that all elements are int/float and withing range. Else raise
    # TypeError or ValueError.
    if isinstance(h, tuple):
        if len(h) < 1 or len(h) > 2:
            raise ValueError(f"h (if set) must be of length 1 or two, got {len(h)}")
        for tmp in h:
            if not isinstance(tmp, (int, float)) or isinstance(tmp, bool):
                raise TypeError("elements in `h` (tuple) must be int or float")
            elif tmp < -360. or tmp > 360:
                raise ValueError("argument(s) in `h` must be in range [-360, 360]")

    if not isinstance(axes, bool):
        raise TypeError("argument `axes` must be bool (True or False)")

    # Convert input to hexcols object; then convert to HCL
    # to extract the coordinates of the palette.
    if isinstance(x, (str, list)):
        cols = hexcols(x)
    elif isinstance(x, (LinearSegmentedColormap, ListedColormap)):
        from colorspace.cmap import cmap_to_sRGB
        cols = cmap_to_sRGB(x, 11) # Currently defaulting to 11 colors (hardcoded)
        cols.to("hex")
    else:
        cols = hexcols(x.colors())
    cols.to("HCL")

    # Determine type of palette based on luminance trajectory
    if _type is None:
        seqn  = 1 + np.arange(0, len(cols), 1)

        # Range of luminance values
        lran = np.max(cols.get("L")) - np.min(cols.get("L"))

        # Calculate linear and triangular correlation
        llin = (np.corrcoef(cols.get("L"), seqn)[0][1])**2
        ltri = (np.corrcoef(cols.get("L"), np.abs(seqn - (len(cols) + 1) / 2))[0][1])**2

        # Guess (inferr) which type of palette we have at hand
        if ltri > 0.75 and lran > 10:    _type = "diverging"
        elif llin > 0.75 and lran > 10:  _type = "sequential"
        else:                            _type = "qualitative"


    if len(cols) > 1:
        # Correcting negative Hues if we have a jump
        tmpH = cols.get("H")
        for i in range(1, len(cols)):
            d = tmpH[i] - tmpH[i - 1]
            if np.abs(d) > 320.:
                tmpH[i] = tmpH[i] - np.sign(d) * 360
            if tmpH[i] > 360:
                tmpH[list(range(i + 1))] = tmpH[list(range(i + 1))] - np.sign(tmpH[i])
        cols.set(H = tmpH)
        del tmpH

        # Smoothing the values in batches where chroma is very low
        idx = np.where(cols.get("C") < 8.)[0]
        # If all Chroma values are very low (<8); replace hue with mean hue
        if len(idx) == len(cols):
            cols.set(H = np.repeat(np.mean(cols.get("H")), len(cols)))
        # If not all but at least some colors have very low chroma
        elif len(idx) > 0:
            from .statshelper import natural_cubic_spline

            # Pre-smoothing hue
            if len(cols) >= 49:
                # Weighted rolling mean
                tmp = cols.get("H")[np.concatenate(([1, 1], np.arange(1, len(cols) - 1)))] + \
                      cols.get("H")[np.concatenate(([1],    np.arange(1, len(cols))))]     + \
                      cols.get("H")
                cols.set(H = 1./3. * tmp) # Calculate weighted mean, write back
                del tmp

            # Split index into 'continuous segments'.
            idxs = split(idx, np.cumsum(np.concatenate(([1], np.diff(idx))) > 1))

            seg = 0
            while len(idxs) > 0:
                if seg in idxs[0]:
                    if len(idxs) > 1:
                        e = idxs[1][0] - 1
                    else:
                        e = len(cols) - 1
                else:
                    if (len(cols) - 1) in idxs[0]:
                        e = len(cols) - 1
                    else:
                        e = np.round(np.mean([np.max(idxs[0]), np.min(idxs[0])]))
                seq  = np.arange(seg, e + 1)
                seql = np.asarray([x in idxs[0] for x in seq])
                io   = split(seq, seql)

                if len(io) == 2 and np.sum(seql) > 0:
                    tmpH = cols.get("H")
                    iii  = np.asarray(seq[seql == False], dtype = np.int16) # int
                    res  = natural_cubic_spline(x    = seq[seql == False],
                                                y    = tmpH[iii],
                                                xout = seq[seql == True])
                    jjj  = np.asarray(seq[seql == True], dtype = np.int16) # int
                    tmpH[jjj] = res["y"]
                    cols.set(H = tmpH)
                    del tmpH, res, iii, jjj

                # Remove first entry from list idxs
                del idxs[0]
                seg = e + 1 # Next segment start

    # Getting maximum chroma
    if c is not None:
        maxchroma = np.ceil(c)
    else:
        maxchroma = np.maximum(100., np.minimum(180, np.ceil(np.max(cols.get("C")) / 20) * 20))

    # ---------------------------------------------------------------
    # Preparing plot/axes
    # ---------------------------------------------------------------
    # If `ax` is specified, must be matplotlib.axes._axes.Axes
    if "ax" in kwargs.keys():
        from matplotlib import axes
        ax = kwargs["ax"] # Keep this for plotting
        if not isinstance(ax, axes._axes.Axes):
            raise TypeError("argument `ax` (if set) must be a matplotlib.axes._axes.Axes")
    else:
        figsize = None if not "figsize" in kwargs.keys() else kwargs["figsize"]
        fig,ax = plt.subplots(1, 1, figsize = figsize)


    # ---------------------------------------------------------------
    # Helper functon to convert coordinates to hex colors and remove
    # unwanted colors (those where the hex color is 'nan' due to 'fixup = False'
    # and low-luminance colors with chroma > 1.
    # ---------------------------------------------------------------
    def conv_colors(nd):
        from .colorlib import polarLUV
        hexcols = polarLUV(H = nd[0], C = np.abs(nd[1]), L = nd[2])
        hexcols.to("hex", fixup = False)

        # Find colors where |C| > 0 and L < 1
        kill_lum = np.where(np.logical_and(np.abs(nd[1]) > 0, nd[2] < 1))[0]

        # Find 'nan' colors (due to fixup)
        kill_nan = np.where([x is None for x in hexcols.colors()])[0]
        kill = np.unique(np.concatenate((kill_lum, kill_nan), 0))

        # Deleting coordinates and colors we do not need
        nd      = np.delete(nd, kill, axis = 1)
        nd_cols = hexcols.colors()
        nd_cols = np.delete(nd_cols, kill)

        return nd, nd_cols

    # ---------------------------------------------------------------
    # Sequential plot
    # ---------------------------------------------------------------
    if _type == "sequential":

        # Spanning grid, creates N x 3 array with H (np.nan), C, L values
        C  = np.linspace(0., maxchroma, int(maxchroma + 1))
        L  = np.linspace(0., 100., 101)
        nd = np.asarray([(np.nan, a, b) for a in C for b in L])

        #                0    1    2
        # Transpose to [[H], [C], [L]
        nd = np.transpose(nd)

        if h is not None:
            nd[0] = np.repeat(h, len(nd[0]))
        elif len(cols) < 3 or (np.max(cols.get("H")) - np.min(cols.get("H"))) < 12:
            nd[0] = np.repeat(np.median(cols.get("H")), len(nd[0]))
        else:
            # Model matrix for estimation and prediction
            X    = np.transpose(np.asarray([np.repeat(1., len(cols)),
                                           cols.get("C"), cols.get("L")]))
            Xout = np.transpose(np.asarray([np.repeat(1., nd.shape[1]),
                                            nd[1], nd[2]]))
            mod = lm(y = cols.get("H"), X = X, Xout = Xout)
            if mod["sigma"] > 7.5:
                warnings.warn("cannot approximate H well as a linear function of C and L")

            # Write prediction for H
            nd[0] = mod["Yout"]


        # Convert to polarLUV -> hexcols without fixup
        nd, nd_cols = conv_colors(nd)

        # Plotting HCL space
        ax.scatter(nd[1], nd[2], color = nd_cols, s = 150)
        ax.set_xlim(np.floor(np.min(nd[1]) / 2.5) * 2.5,
                    np.ceil(np.max(nd[1]) / 2.5) * 2.5) # Chroma
        ax.set_ylim(np.floor(np.min(nd[2]) / 2.5) * 2.5,
                    np.ceil(np.max(nd[2]) / 2.5) * 2.5) # Luminance

        # Adding actual palette
        if linewidth is not None:
            ax.plot(cols.get("C"), cols.get("L"), "-", color = "black",
                    linewidth = linewidth, zorder = 3)
        if s is not None:
            ax.scatter(cols.get("C"), cols.get("L"), edgecolor = "white", s = s,
                    linewidth = 2, color = cols.colors(), zorder = 3)

        # Plot labels
        if "title" in kwargs.keys():
            title = kwargs["title"]
        elif len(np.unique(np.round(nd[0]))) == 1:
            title = f"Hue = {nd[0][0]:.0f}"
        else:
            title = f"Hue = [{np.min(nd[0]):.0f}, {np.max(nd[0]):.0f}]"


    # ---------------------------------------------------------------
    # Diverging plot
    # ---------------------------------------------------------------
    elif _type == "diverging":

        # TODO(R): When using the following sequence of colors in R
        # x <- c('#11C638', '#60CD6B', '#CCFF00', '#B0DAB3', '#D2E0D3',
        #        '#E7DAD2', '#EDC9B0', '#CCFF00', '#F1A860', '#EF9708')
        # hclplot(x, "diverging")
        # ... is that actually correct? To me, the Python version looks more reasonable.
        #
        # Compare to Python
        # x = ['#11C638', '#60CD6B', '#CCFF00', '#B0DAB3', '#D2E0D3',
        #      '#E7DAD2', '#EDC9B0', '#CCFF00', '#F1A860', '#EF9708']
        # hclplot(x, "diverging")

        # Spanning grid, creates N x 5 array with H (np.nan), C, L, as well
        # as left (binary) and right (binary) based on C (negative C = left, else right)
        C  = np.linspace(-maxchroma, +maxchroma, int(1 + 2 * maxchroma))
        L  = np.linspace(0., 100., 101)
        nd = np.asarray([(np.nan, a, b, a < 0, a >= 0) for a in C for b in L])

        #                0    1    2      3       4
        # Transpose to [[H], [C], [L], [left], [right]]
        # If C <  0:  left = 0, right = 1
        # IF C >= 0:  left = 1, right = 0
        # ... dummy coding used later for linear regression.
        nd = np.transpose(nd)

        # Left and right hand side of the diverging palette; original colors
        left  = np.arange(0, np.floor(len(cols) / 2) + 1).astype(np.int8)
        left  = left[np.where(cols.get("C")[left] > 10.)[0]]
        right = np.arange(np.ceil(len(cols) / 2), len(cols)).astype(np.int8)
        right = right[np.where(cols.get("C")[right] > 10.)[0]]

        # If the user has set h's (after sanity checks we know it is 
        # now a tuple of one or two numerics)
        if h is not None:
            if len(h) == 2:
                nd[0, np.where(nd[3] == 1)] = float(h[0]) # left
                nd[0, np.where(nd[4] == 1)] = float(h[1]) # right
            else:
                nd[0]        = float(h[0])

        # Else we will infer it from the data (cols)
        elif len(cols) < 6 \
            or np.diff(nprange(cols.get("H")[left])  - np.min(cols.get("H")[left]))[0]  < 12 \
            or np.diff(nprange(cols.get("H")[right]) - np.min(cols.get("H")[right]))[0] < 12:

            # Update H
            nd[0, np.where(nd[3] == 1)] = np.median(cols.get("H")[left] - \
                                          np.min(cols.get("H")[left])) + \
                                          np.min(cols.get("H")[left])
            nd[0, np.where(nd[3] == 0)] = np.median(cols.get("H")[right] -\
                                          np.min(cols.get("H")[right])) + \
                                          np.min(cols.get("H")[right])

        # Else
        else:
            # Adding 'left' to nd dimension 0 as 4th element
            tmp = np.concatenate((np.repeat(True, len(left)), np.repeat(False, len(right))))

            # Setting up y (response) and X (model matrix) for linear model
            is_left  = np.asarray([x in left  for x in np.arange(len(cols))], dtype = np.int16)
            is_right = np.asarray([x in right for x in np.arange(len(cols))], dtype = np.int16)

            y = cols.get("H")
            X = np.transpose([np.repeat(1, len(y)),      # Intercept
                              is_left,                   # Dummy 'left'
                              cols.get("C"),             # Chroma
                              cols.get("L"),             # Luminance
                              cols.get("C") * is_left,   # + one-way interactions
                              cols.get("L") * is_left])

            # left/right must have C > 10 (this is done before
            # this if-elif-else condition), here we are checking for colors
            # which are neither left nor right. If found, remove from y and X
            # before modeling.
            kill = np.where(is_right + is_left == 0)[0]
            y    = np.delete(y, kill)
            X    = np.delete(X, kill, axis = 0)

            # Create xout based on nd
            Xout = np.transpose([np.repeat(1, nd.shape[1]), # Intercept
                                 nd[3],                     # Dummy 'left'
                                 np.abs(nd[1]),             # Chroma
                                 nd[2],                     # Luminance
                                 np.abs(nd[1]) * nd[3],     # + one-way interactions
                                 nd[2] * nd[3]])

            # Estimate model
            m = lm(y = y, X = X, Xout = Xout)
            if m["sigma"] > 7.5:
                warnings.warn("cannot approximate H well as a linear function of C and L")

            # Write prediction for H
            nd[0] = m["Yout"]


        # Convert to polarLUV -> hexcols without fixup
        nd, nd_cols = conv_colors(nd)

        # Plotting HCL space
        ax.scatter(nd[1], nd[2], color = nd_cols, s = 150)
        ax.set_xlim(np.floor(np.min(nd[1]) / 2.5) * 2.5,
                    np.ceil(np.max(nd[1]) / 2.5) * 2.5) # Chroma
        ax.set_ylim(np.floor(np.min(nd[2]) / 2.5) * 2.5,
                    np.ceil(np.max(nd[2]) / 2.5) * 2.5) # Luminance

        # Modify tick-labels on x-axis to always show positive value
        xtick = ax.get_xticks()
        ax.set_xticks(xtick)
        ax.set_xticklabels([int(t) for t in np.abs(xtick)])

        # Adding actual palette if needed
        C  = cols.get("C")
        il = np.arange(len(cols) / 2, dtype = np.int16)
        C[il] = -1 * C[il]
        if linewidth is not None:
            ax.plot(C, cols.get("L"), "-", color = "black",
                    linewidth = linewidth, zorder = 3)
        if s is not None:
            ax.scatter(C, cols.get("L"), edgecolor = "white", s = s,
                       linewidth = 2, color = cols.colors(), zorder = 3)

        # Specifying title
        if "title" in kwargs.keys():
            title = kwargs["title"]
        elif len(np.unique(np.round(nd[0]))) <= 2:
            hl    = nd[0, nd[3] == 1][0] # Picking left ...
            hr    = nd[0, nd[4] == 1][0] # ... and right hue.
            title = f"Hue = {hl:.0f} | {hr:.0f}"
        else:
            from .statshelper import nprange
            hl    = nprange(nd[0, nd[3] == 1]) # Range of Hue 'left'
            hr    = nprange(nd[0, nd[4] == 1]) # Range of Hue 'right'
            title  = f"Hue = [{np.min(hl[0]):.0f}, {np.max(hl[1]):.0f}]"
            title += f"/[{np.min(hr[0]):.0f}, {np.max(hr[1]):.0f}]"


    # ---------------------------------------------------------------
    # Qualitative plot
    # ---------------------------------------------------------------
    elif _type == "qualitative":

        # Spanning grid, creates N x 3 array with H, C, and L (np.nan)
        H  = np.linspace(0, 360, 180, endpoint = False) # 0-360 w/ interval width = 2
        C  = np.linspace(0, maxchroma, int(maxchroma + 1))
        nd = np.asarray([(a, b, np.nan) for a in H for b in C])

        #                0    1    2
        # Transpose to [[H], [C], [L]]
        # ... dummy coding used later for linear regression.
        nd = np.transpose(nd)

        # If the user has specified l: Use this value.
        if l is not None:
            nd[2] = np.repeat(float(l), nd.shape[1])
        elif len(cols) < 3 or np.diff(nprange(cols.get("L"))) < 10.:
            nd[2] = np.median(cols.get("L"))
        else:
            # Model matrix for estimation and prediction
            X    = np.transpose(np.asarray([np.repeat(1., len(cols)),
                                            cols.get("C"), cols.get("H")]))
            Xout = np.transpose(np.asarray([np.repeat(1., nd.shape[1]),
                                            nd[1], nd[0]]))
            mod = lm(y = cols.get("L"), X = X, Xout = Xout)
            if mod["sigma"] > 7.5:
                warnings.warn("cannot approximate L well as a linear function of C and H")

            # Write prediction for L [0., 100.]
            nd[2] = np.minimum(100., np.maximum(0., mod["Yout"]))

        # Convert to polarLUV -> hexcols without fixup
        nd, nd_cols = conv_colors(nd)

        def HC_to_xy(H, C):
            assert isinstance(H, np.ndarray)
            assert isinstance(C, np.ndarray)
            if len(H.shape) > 0:
                assert len(H) == len(C)
            return [np.cos(H * np.pi / 180.) * C, # x
                    np.sin(H * np.pi / 180.) * C] # y

        nd_x, nd_y = HC_to_xy(nd[0], nd[1])

        # Plotting HCL space
        ax.scatter(nd_x, nd_y, color = nd_cols, s = 150)
        ax.set_xlim(-maxchroma * 1.1, +maxchroma * 1.1)
        ax.set_ylim(-maxchroma * 1.1, +maxchroma * 1.1)
        ax.set_aspect("equal")

        # Adding actual palette if needed
        cols_x, cols_y = HC_to_xy(cols.get("H"), cols.get("C"))
        if linewidth is not None:
            ax.plot(cols_x, cols_y, "-", color = "black",
                    linewidth = linewidth, zorder = 3)
        if s is not None:
            ax.scatter(cols_x, cols_y, edgecolor = "white", s = s,
                    linewidth = 2, color = cols.colors(), zorder = 3)

        # Adding outer circle
        cx, cy = HC_to_xy(np.linspace(0, 360, 361), np.repeat(maxchroma, 361))
        ax.plot(cx, cy, zorder = 1, color = "black", linewidth = 0.5)

        # Adding axes if requested
        if axes:
            tx, ty = HC_to_xy(np.asarray(0), np.asarray(maxchroma + 20))
            ax.text(tx, ty, "Hue", horizontalalignment = "left", verticalalignment = "center")
            for hue in np.linspace(0, 360, 6, endpoint = False):
                tx, ty = HC_to_xy(np.asarray(hue), np.asarray(maxchroma + 10))
                ax.text(tx, ty, f"{hue:.0f}" if hue > 0 else "0\n360",
                        horizontalalignment = "center", verticalalignment = "center")
                lx, ly = HC_to_xy(np.repeat(hue, 2), np.asarray([0, 4]) + maxchroma)
                ax.plot(lx, ly, color = "black", linewidth = 0.5)
            del cx, cy, tx, ty, lx, ly

            # Radial 'axis'
            ax.plot(np.asarray([0, maxchroma]), np.repeat(0, 2),
                    color = "black", linewidth = 0.5)
            tmp = np.arange(0, maxchroma, 50 if maxchroma > 150 else 25)
            ax.text(np.mean(tmp), -17, "Chroma",
                    horizontalalignment = "center", verticalalignment = "top")
            for t in tmp:
                ax.text(t, -7.5, f"{t:.0f}",
                        horizontalalignment = "center", verticalalignment = "top")
                ax.plot(np.repeat(t, 2), np.asarray([0., -5.]),
                        color = "black", linewidth = 0.5)
            del tmp
        

        # Specifying title
        if "title" in kwargs.keys():
            title = kwargs["title"]
        elif len(np.unique(np.round(nd[2]))) <= 1:
            title = f"Luminance = {nd[2][0]:.0f}"
        else:
            title = f"Luminance = [{np.min(nd[2]):.0f}, {np.max(nd[2]):.0f}]"


    # Plot annotations, done
    ax.set_title(title, fontsize = 10, fontweight = "bold")
    if _type == "qualitative" or not axes:
        ax.set_axis_off()
    else:
        ax.set_xlabel("Chroma" if not "xlabel" in kwargs.keys() else kwargs["xlabel"])
        ax.set_ylabel("Luminance" if not "ylabel" in kwargs.keys() else kwargs["ylabel"])

    # If the user did not provide an axis, we started
    # a new figure and can now display it.
    if not "ax" in kwargs.keys():
        plt.show()
        return fig
    else:
        return ax







