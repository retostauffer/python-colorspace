



def hclplot(x, _type = None, h = None, c = None, l = None, **kwargs):
    """
    Requires `matplotlib` to be installed.

    Args:
        x (str, list, colorobject): An object which can be converted into
            a :py:class:`hexcols <colorspace.colorlib.hexcols>` object.
        _type (None, str): Specifying which type of palette should be
            visualized (`"qualitative"`, `"sequential"`, or `"diverging"`). For
            qualitative palettes a hue-chroma plane is used, otherwise a
            chroma-luminance plane. By default (`_type = None`) the type is
            inferred from the luminance trajectory corresponding to `x`.
        h (None, int, float): if int or float, it must be within `[-360, 360]`
        c (None, int, float): if int or float, it must be positive
        l (None, int, float): if int or float, it must be positive
        **kwargs: Allowed to overwrite some default settings such as
            `title` (str), `xlabel` (str), `ylabel` (str), `figsize`
            (forwarded to `pyplot.figure`), `s` (int, float) to change
            marker size, defaults to `150`.

    Examples:
    >>> # Sequential HCL palette, hclplot with all available options
    >>> x = sequential_hcl("Red-Blue")(10)
    >>> hclplot(x, xlabel = "foo", ylabel = "bar",
    >>>         title = "Test", figsize = (2, 2), s = 500)

    Raises:
        TypeError: If argument `_type` is not None or str.
        TypeError: If argument `_type` is str but not one of the allowed types.
        TypeError: If argument `c`, `h`, and/or `l` are not None, str, or int.
        ValueError: If `c`,`l` is not None and smaller or equal to `0` (must be positive).
        ValueError: If `h` is not None and not within the range `[-360, 360]`.
    """

    from .colorlib import hexcols
    from .statshelper import split
    import numpy as np

    # Sanity checks
    if not isinstance(_type, (type(None), str)):
        raise TypeError("argument `_type` must be None or str")

    if not isinstance(h, (int, float, type(None))):
        raise TypeError("argument `h` must be None, int, or float")
    elif h is not None and (h < -360. or h > 360):
        raise ValueError("argument `h` must be in range [-360, 360]")

    if not isinstance(c, (int, float, type(None))):
        raise TypeError("argument `c` must be None, int, or float")
    elif c is not None and c <= 0:
        raise ValueError("argument `c` must be positive if set")

    if not isinstance(l, (int, float, type(None))):
        raise TypeError("argument `l` must be None, int, or float")
    elif h is not None and l <= 0:
        raise ValueError("argument `l` must be positive if set")

    allowed_types = ["diverging", "sequential", "qualitative"]
    if isinstance(_type, str):
        if not _type.lower() in allowed_types:
            raise ValueError("argument `_type` invalid. Must be None or any of: {', '.join(allowed_types)}")
        _type = _type.lower()
    
    # Requires matpotlib, a suggested package. If not avialable
    # raise an import error.
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("problems importing matplotlib.pyplt (not installed?)")

    # Convert input to hexcols object; then convert to HCL
    # to extract the coordinates of the palette.
    if isinstance(x, (str, list)):
        cols = hexcols(x)
    else:
        cols = hexcols(x.colors())
    cols.to("HCL")


    # Determine type of palette based on luminance trajectory
    if _type is None:
        seqn  = 1 + np.arange(0, len(cols), 1)

        # Range of luminance values
        lran = np.max(cols.get("L")) - np.min(cols.get("L"))

        # Calculate linear and triangular correlation
        from .statshelper import cor
        llin = cor(cols.get("L"), seqn)**2
        ltri = cor(cols.get("L"), np.abs(seqn - (len(cols) + 1) / 2))**2

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

            s = 0
            while len(idxs) > 0:
                if s in idxs[0]:
                    if len(idxs) > 1:
                        e = idxs[1][0] - 1
                    else:
                        e = len(cols) - 1
                else:
                    if (len(cols) - 1) in idxs[0]:
                        e = len(cols) - 1
                    else:
                        e = np.round(np.mean([np.max(idxs[0]), np.min(idxs[0])]))
                seq  = np.arange(s, e + 1)
                seql = np.asarray([x in idxs[0] for x in seq])
                io   = split(seq, seql)

                if len(io) == 2 and np.sum(seql) > 0:
                    tmpH = cols.get("H")
                    res = natural_cubic_spline(x    = seq[seql == False],
                                               y    = tmpH[seql == False],
                                               xout = seq[seql == True])
                    tmpH[seql == True] = res["y"]
                    cols.set(H = tmpH)
                    del tmpH, res

                # Remove first entry from list idxs
                del idxs[0]
                s = e + 1 # Next segment start

    # Getting maximum chroma
    if c is not None:
        maxchroma = np.ceil(c)
    else:
        maxchroma = np.maximum(100., np.minimum(180, np.ceil(np.max(cols.get("C")) / 20) * 20))

    # Depending on _type:
    if _type == "sequential":
        print(f"RETO: HERE plotting for {_type}")
        # Spanning grid, creates N x 3 array with H (np.nan), C, L values
        C  = np.linspace(0., maxchroma, int(maxchroma + 1))
        L  = np.linspace(0., 100., 101)
        nd = np.asarray([(np.nan, a, b) for a in C for b in L])
        nd = np.transpose(nd) # Transpose to [[H], [C], [L]]

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
            from .statshelper import lm
            mod = lm(y = cols.get("H"), X = X, Xout = Xout)

            if mod["sigma"] > 7.5:
                import warnings
                warnings.warn("cannot approximate H well as a linear function of C and L")
            # Nevermind, store fitted H values
            nd[0] = mod["Yout"]


        # Conver to polarLUV -> hexcols without fixup
        from .colorlib import polarLUV
        hexcols = polarLUV(H = nd[0], C = nd[1], L = nd[2])
        hexcols.to("hex", fixup = False)

        # Find colors where C > 0 and L < 1
        kill_lum = np.where(np.logical_and(nd[1] > 0, nd[2] < 1))[0]

        # Find 'nan' colors (due to fixup)
        kill_nan = np.where([x == 'nan' for x in hexcols.colors()])[0]
        kill = np.unique(np.concatenate((kill_lum, kill_nan), 0))
        del kill_nan, kill_lum # No longer needed

        # Deleting coordinates and colors we do not need
        nd   = np.delete(nd, kill, axis = 1)
        nd_cols = hexcols.colors()
        nd_cols = np.delete(nd_cols, kill)

        from matplotlib import pyplot as plt

        # Plotting HCL space
        figsize = None if not "figsize" in kwargs.keys() else kwargs["figsize"]
        fig = plt.figure(figsize = figsize)
        plt.scatter(nd[1], nd[2], color = nd_cols, s = 150)
        plt.xlim(np.min(nd[1]), np.max(nd[1])) # Chroma
        plt.ylim(np.min(nd[2]), np.max(nd[2])) # Luminance

        # Adding actual palette
        plt.plot(cols.get("C"), cols.get("L"), "-", color = "black", linewidth = 1,
                zorder = 3)

        s = 150 if not "s" in kwargs.keys() else float(kwargs["s"])
        plt.scatter(cols.get("C"), cols.get("L"), edgecolor = "white", s = s,
                linewidth = 2, color = cols.colors(), zorder = 3)

        # Plot labels
        # TODO(R): In R, the colors where C > 0 and L < 1 is TRUE are set to NA,
        #          but not the `nd` object. Thus, the title contains the Hue range
        #          from all the colors including those which got killed by fixup = TRUE.
        #          Bug or feature?
        if "title" in kwargs.keys():
            title = kwargs["title"]
        elif len(np.unique(np.round(nd[0]))) == 1:
            title = f"Hue = {np.round(nd[0][0])}"
        else:
            title = f"Hue = [{np.round(np.min(nd[0]))}, {np.round(np.max(nd[0]))}]"
        plt.title(title, fontsize = 10, fontweight = "bold")
        plt.xlabel("Chroma" if not "xlabel" in kwargs.keys() else kwargs["xlabel"])
        plt.ylabel("Luminance" if not "ylabel" in kwargs.keys() else kwargs["ylabel"])

        # Show figure
        plt.show()

    elif _type == "diverging":
        print(f"RETO: HERE plotting for {_type}")

    elif _type == "qualitative":
        print(f"RETO: HERE plotting for {_type}")


    print(cols)






