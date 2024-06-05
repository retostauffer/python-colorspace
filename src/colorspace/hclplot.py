


def hclplot(x, _type = None):

    from .colorlib import hexcols
    import numpy as np

    # Sanity checks
    if not isinstance(_type, (type(None), str)):
        raise TypeError("argument `_type` must be None or str")

    allowed_types = ["diverging", "sequential", "qualitative"]
    if isinstance(_type, str):
        if not _type.lower() in allowed_types:
            raise ValueError("argument `_type` invalid. Must be None or any of: {', '.join(allowed_types)}")
        _type = _type.lower()


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
        llin = np.corrcoef(cols.get("L"), seqn)[0][1]
        ltri = np.corrcoef(cols.get("L"), np.abs(seqn + (len(cols) + 1) / 2))[0][1]

        # Guess (inferr) which type of palette we have at hand
        if ltri > 0.75 and lran > 10:    _type = "diverging"
        elif llin > 0.75 and lran > 10:  _type = "sequential"
        else:                            _type = "qualitative"

        # Smoothing the values in batches where chroma is very low
        idx = np.where(cols.get("C") < 8.)[0]
        # If all Chroma values are very low (<8); replace hue with mean hue
        if len(idx) == len(cols):
            cols.set(H = np.repeat(np.mean(cols.get("H")), len(cols)))
        # If not all but at least some colors have very low chroma
        elif len(idx) > 0:
            # Pre-smoothing hue
            if True or len(cols) >= 49:
                # Weighted rolling mean
                tmp = cols.get("H")[np.concatenate(([1, 1], np.arange(1, len(cols) - 1)))] + \
                      cols.get("H")[np.concatenate(([1],    np.arange(1, len(cols))))]     + \
                      cols.get("H")
                cols.set(H = 1./3. * tmp)

            # Split index into 'continuous segments'.
            print(f"{idx=}")
            idxs = split(idx, np.cumsum(np.concatenate(([1], np.diff(idx))) > 1))

            s = 0
            print(idxs)
            while len(idxs) > 0:
                if s in idxs[0]:
                    e = len(cols) - 1 if len(idxs) == 1 else idxs[1] - 1
                else:
                    if len(cols) in idxs[0]:
                        e = len(cols) - 1
                    else:
                        e = np.round(np.mean([np.max(idxs[0]), np.min(idxs[0])]))
                seq  = np.arange(s, e + 1)
                seql = np.asarray([x in idxs[0] for x in seq])
                io = split(seq, seql)

                if len(io) == 2 and np.sum(cols.get("H")[seq[seql == False]]) > 0:
                    print("RETO HERE")
                    print("woo")
                else:
                    print("RETO THERE")
                    print('baa')

                # Remove first entry from list idxs
                del idxs[0]
                s += 1



    print(f"llin {llin}, ltri {ltri}")
    print(cols)






