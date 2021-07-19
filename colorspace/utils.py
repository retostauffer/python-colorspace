
def max_chroma(H, L, floor = False):
    """Get maximum chroma for a specific combination of hue and luminance.

    Extracted from a lookup table. Input `H` and `L` can be single values (float, int),
    lists of values which can be converted to. 

    H and L can be single values or multiple values. If both have length `> 1` the length
    must match. If one is of length `1` it will be repeated to match the length of the
    second argument. In case the function is not able to create two arrays of the same
    length an error will be thrown.

    Args:
        H (int, float, list, numpy.ndarray): hue, one or multiple values (must be
            convertable to float).
        L (int, float, list, numpy.ndarray): luminance, one or multiple values (must be
            convertable to float).
        floor (bool): should return be rounded? Defaults to `False`.

    Returns:
        `numpy.array` of the same length as `max(len(H), len(L))` with
        maximum possible chroma for these hue-luminance combinations.

    Raises:
        ValueError: If unexpected in put on `H` or `L`.
        ValueError: If length of `H` and `L` are not the same (see above).
        TypeError: If input `floor` is not boolean.
    """

    import numpy as np
    import os
    import re

    if isinstance(H, (float, int)):
        H = np.asarray([H], dtype = "float")
    elif isinstance(H, (list, np.ndarray)):
        H = np.asarray(H, dtype = "float")
    else:
        raise ValueError("Unexpected input on argument `H`.")
    if isinstance(L, (float, int)):
        L = np.asarray([L], dtype = "float")
    elif isinstance(L, (list, np.ndarray)):
        L = np.asarray(L, dtype = "float")
    else:
        raise ValueError("Unexpected input on argument `L`.")
    if not isinstance(floor, bool):
        raise TypeError("Input `floor` must be boolean `True` or `False`.")

    # Check if we have to repeat one of the two inputs.
    # This is only used if one is of length > 1 while the other
    # one is of length 1.
    if len(H) == 1 and len(L) > 1:    H = np.repeat(H, len(L))
    elif len(H) > 0 and len(L) == 1:  L = np.repeat(L, len(H))

    # Now both arrays must have the same number of elements. If not,
    # stop execution and throw an error.
    if not len(H) == len(L):
        raise ValueError("Number of values and `H` and `L` do not match or cannot be matched.")

    # Make sure that all hue values lie in the range of 0-360 
    while np.any(H < 0):   H = np.where(H < 0,   H + 360., H)
    while np.any(H > 360): H = np.where(H > 360, H - 360., H)

    # Prepare the values used for the 'table search'.
    # Fix luminance to values between [0., 100.]
    L = np.fmin(100, np.fmax(0, L))
    # Minimum/maximum hue and luminance
    hmin = int(np.floor(np.min(H) + 1e-08))
    lmin = int(np.floor(np.min(L) + 1e-08))
    hmax = int(np.ceil(np.max(H) - 1e-08))
    lmax = int(np.ceil(np.max(L) - 1e-08))

    #resource_package = os.path.dirname(__file__)
    resource_package = "/home/retos/Software/python-colorspace/python-colorspace/colorspace"
    filename = os.path.join(resource_package, "data", "max_chroma_table.csv")

    # Open file and read line-byline to identify the line we are looking for.
    def get_max(h, l):
        x = re.findall("^(?s){:d}-{:d},([0-9]+)".format(h, l), content, re.MULTILINE)
        if not len(x) == 1:
            raise Exception("Whoops, error in max_chroma table search.")
        return(float(x[0]))


    with open(filename, "r") as fid: content = "".join(fid.readlines())

    # Calculate max chroma
    C = (hmax - H) * (lmax - L) * get_max(hmin, lmin) + \
        (hmax - H) * (L - lmin) * get_max(hmin, lmax) + \
        (H - hmin) * (lmax - L) * get_max(hmax, lmin) + \
        (H - hmin) * (L - lmin) * get_max(hmax, lmax)
    C = np.where(L < 0. or L > 100., 0, C)

    # Floor if requested and return
    if floor: C = np.floor(C)
    return C

def darken(col, amount = 0.1, method = "relative", space = "HCL", fixup = True):
    """Algorithmically lighten or darken colors.

    See `help(lighten)` for more details.
    """
    return lighten(col, amount = amount * -1., method = method, space = space, fixup = fixup)


def lighten(col, amount = 0.1, method = "relative", space = "HCL", fixup = True):
    """Algorithmically lighten or darken colors.

    Args:
        col: color (or colors) to be manipulated. Can be a
            :py:class:`colorobject <colorspace.colorlib.colorobject>`,,
            a :py:class:`palette <colorspace.palettes.palette>` object, or a
            single string/list of strings with valid hex colors.
        amount (float): value between `[0., 1.]` with the amount the colors
            should be lightened. Defaults to `0.1`.
        method (str): either `"relative"` (default) or `"absolute"`.
        space (str): one of `"HCL"` or `"HSV"`. Defaults to `"HCL"`.
        fixup (bool): should colors which fall outside the defined RGB space
            be fixed (corrected)? Defaults to `True`.

    Example:

        >>> original = "#ff3322"
        >>> lighter  = lighten(original, amount = 0.3, method = "relative", space = "HCL")
        >>> darker   = darken(original,  amount = 0.3, method = "relative", space = "HCL")
        >>> swatchplot([lighter, original, darker], show_names = False)

    Raises:
        ValueError: If `method` is not one of `"absolute"` or `"relative"`.
        ValueError: If `space` is not one of `"HCL"` or `"HSV"`.
        TypeError: If input 'col' is not among the one of the recognized objects.
        ValueError: If `fixup` is not boolean.
    """

    from colorspace.colorlib import colorobject, hexcols
    from colorspace.palettes import palette
    from numpy import fmin, fmax, where

    if not isinstance(method, str) or not method in ["absolute", "relative"]:
        raise ValueError("Wrong input for 'method'. Must be `\"absolute\"` or `\"relative\"`.")
    if not isinstance(space, str) or not space in ["HCL", "HLS", "combined"]:
        raise ValueError("Wrong input for 'space'. Must be `\"HCL\"`, `\"HLS\"`, or `\"combined\"`.")
    if not isinstance(fixup, bool):
        raise ValueError("Input `fixup` must be boolean `True` or `False`.")

    # If the input is a colorobject (hex, HSV, ...) we first
    # put everything into a (temporary) palette.
    if isinstance(col, colorobject):  x = palette(col.colors(), "_temp_palette_object_")
    # In case the input is a string or a list of strings
    # we convert the input (temporarily) into a palette.
    # This allows us to check if all colors are valid hex colors.
    elif isinstance(col, str):        x = palette([col], "_temp_palette_object_")
    elif isinstance(col, list):       x = palette(col,   "_temp_palette_object_")
    # If the input is a palette object; keep it as it is.
    elif isinstance(col, palette):    x = col
    else:
        raise TypeError("Input object 'col' must be a colorobject, palette, or a string " + \
                        "or list of strings with valid hex colors.")

    # Function to lighten colors in the HCL space.
    # Returns a colorobject with transformed coordinates.
    def _lighten_in_HCL(colors, amount, method):
        tmp = hexcols(x.colors())
        tmp.to("HCL")
        tmp.set(L = fmin(100, fmax(0, tmp.get("L")))) # Fix bounds
        if method == "relative":
            tmp.set(L = where(amount >= 0, \
                              100. - (100. - tmp.get("L")) * (1. - amount), \
                              tmp.get("L") * (1. + amount)))

        else:
            tmp.set(L = tmp.get("L") + amount * 100.)
        tmp.set(L = fmin(100, fmax(0, tmp.get("L")))) # Fix bounds again
        tmp.set(C = fmin(max_chroma(tmp.get("H"), tmp.get("L"), floor = True), \
                         fmax(0, tmp.get("C"))))

        return tmp

    # Function to lighten colors in the HLS space.
    # Returns a colorobject with transformed coordinates.
    def _lighten_in_HLS(colors, amount, method):
        tmp = hexcols(x.colors())
        tmp.to("HLS")
        if method == "relative":
            tmp.set(L = where(amount >= 0, \
                              1. - (1. - tmp.get("L")) * (1. - amount), \
                              tmp.get("L") * (1. + amount)))
        else:
            tmp.set(L = tmp.get("L") + amount)
        tmp.set(L = fmin(1., fmax(0, tmp.get("L"))))

        return tmp


    # Lighten colors depending on the users choice 'space'
    if space == "HCL":
        tmp = _lighten_in_HCL(x.colors(), amount, method)
    elif space == "HLS":
        tmp = _lighten_in_HLS(x.colors(), amount, method)
    else:
        # TODO(R): Differs from colorspace. Reason is that we here
        #          go to HSL and convert HLS to HCL, I guess.
        tmp    = _lighten_in_HCL(x.colors(), amount, method) # Via HCL color space
        tmpHLS = _lighten_in_HLS(x.colors(), amount, method) # Via HLS color space
        tmpHLS.to("sRGB"); tmpHLS.to("HCL")

        # fix-up L and copy C over from HLS-converted color
        tmp.set(C = tmpHLS.get("C"))

        # make sure chroma is in allowed range
        tmp.set(C = fmin(max_chroma(tmp.get("H"), tmp.get("L"), floor = True), \
                         fmax(0, tmp.get("C"))))

    # Job done, convert back to HEX
    tmp.to("hex")

    # If the original input was a single string: return str
    if isinstance(col, str):              res = tmp.colors()[0]
    # In case the original input has been a list, return list
    elif isinstance(col, list):           res = tmp.colors()
    # In case the input was a palette, return palette with original name.
    elif isinstance(col, palette):        res = palette(tmp.colors(), col.name())
    # Else the input has been a colorobject, return hex color object :)
    else:                                 res = tmp

    return res


