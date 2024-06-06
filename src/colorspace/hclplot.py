



def hclplot(x, _type = None, h = None, c = None):
    """
    Requires `matplotlib` to be installed.

    Args:
        _type (None, str):
        h (None, int, float): if int, float: Must be within `[-360, 360]`
        c (None, int, float): must be positive
    """

    from .colorlib import hexcols
    import numpy as np

    # Sanity checks
    if not isinstance(_type, (type(None), str)):
        raise TypeError("argument `_type` must be None or str")
    if not isinstance(c, (int, float, type(None))):
        raise TypeError("argument `c` must be None, int, or float")
    elif c is not None and c <= 0:
        raise ValueError("argument `c` must be positive if set")
    if not isinstance(h, (int, float, type(None))):
        raise TypeError("argument `h` must be None, int, or float")
    elif h is not None and (h < -360. or h > 360):
        raise ValueError("argument `h` must be in range [-360, 360]")

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


    # Helper function mimiking Rs split() function.
    # Takes two numpy arrays (x, y) of same length.
    # Splits x in segments according to the values of y (whenever
    # the value in y changes). E.g.,
    #
    # >>> tmp = np.asarray([1, 2, 3, 4, 5])
    # >>> split(tmp, tmp == 3)
    # >>> [[1, 2], [3], [4, 5]]
    #
    # >>> tmp = np.asarray([1, 2, 3, 4, 5])
    # >>> split(tmp, np.asarray([1, 1, 2, 2, 1]))
    # >>> [[1, 2], [3, 4], [5]]
    def split(x, y):
        #print(f"{x=} ({len(x)}) {y=} ({len(y)})")
        assert isinstance(x, np.ndarray), TypeError("argument `x` must be numpy array")
        assert isinstance(y, np.ndarray), TypeError("argument `y` must be numpy array")
        assert len(x) > 0, ValueError("array x must be length >= 1")
        assert len(x) == len(y), ValueError("arrays x/y must be of same length")
        if len(x) == 1: return [x]
        # Start with list-of-lists containing first element
        res = [[x[0]]]
        for i in range(1, len(x)):
            if y[i] == y[i - 1]:  res[len(res) - 1].append(x[i]) # Append
            else:                 res.append([x[i]]) # Add new list
        return res

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
        maxchroma = np.maximum(100., np.minimum(180, np.ceil(np.max(cols.get("H")) / 20) * 20))

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

        # Start preparing plot
        from .colorlib import polarLUV

        # Delete colors where C > 0 and L < 1
        kill = np.where(np.logical_and(nd[1] >= 0, nd[2] < 1))[0]

        hexcols = polarLUV(H = nd[0], C = nd[1], L = nd[2])
        hexcols.to("hex", fixup = False)
        # Find 'nan' colors (due to fixup)
        kill = np.where([x == 'nan' for x in hexcols.colors()])
        nd = np.delete(nd, kill, axis = 1)
        print("replace [L < 1 and C > 0] values with np.nan?")
        print("HERE PLOT NOW")

        cols = hexcols.colors()
        cols = np.delete(cols, kill)

        from matplotlib import pyplot as plt
        print(nd.shape)
        print(len(hexcols.colors()))
        plt.scatter(nd[1], nd[2], color = cols)
        plt.show()



    elif _type == "diverging":
        print(f"RETO: HERE plotting for {_type}")

    elif _type == "qualitative":
        print(f"RETO: HERE plotting for {_type}")


    print(cols)






