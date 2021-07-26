

# --------------------------------------------------------------------
# Performs the check on hex color strings to see if they are valid.
# --------------------------------------------------------------------
def check_hex_colors(colors, allow_nan = False):
    """Checking hex colors

    Valid hex colors are three digit hex colors (e.g., `#F00`), six digit
    hex colors (e.g., `#FF00FF`), or six digit colors with additional transparency
    (eight digit representation).

    Args:
        colors (str, list, numpy.ndarray): single string or list of strings with hex colors.
            In case it is a `numpy.ndarray` it well be flattened to 1D if needed.
        allow_nan (bool): allow for missing values (`np.nan`). Defaults to `False`.

    Returns:
        list: Returns a list (length 1 or more) in case all values provided
            are valid hex colors. Three digit colors will be expanded to
            six digit colors. Else the function will raise a ValueError.

    Examples:
        >>> check_hex_colors("#ff003311")
        >>> check_hex_colors("#ff0033")
        >>> check_hex_colors("#f03")
        >>> check_hex_colors(["#f0f", "#00F", "#00FFFF", "#ff003311"])
        >>> from numpy import asarray
        >>> check_hex_colors(asarray(["#f0f", "#00F", "#00FFFF", "#ff003311"]))

    Raises:
        TypeError: If `allow_nan` is not boolean `True` or `False`.
        ValueError: In case `colors` is a list but does not only contain strnigs.
        TypeError: If `colors` is neither string or list of strings.
        ValueError: If at least one of the colors is an invalid hex color.
    """
    from re import match, compile
    from numpy import all, repeat, ndarray
    from .colorlib import colorobject

    # Saniy checks
    if not isinstance(allow_nan, bool): raise TypeError("Input 'allow_nan' is not boolean.")
    if isinstance(colors, str):
        colors = [colors]
    elif isinstance(colors, list):
        if not all([isinstance(x, str) for x in colors]):
            raise ValueError("List on argument 'colors' must only contain strings.")
    elif isinstance(colors, ndarray):
        if not len(colors.shape) == 1:
            raise TypeError("If an `numpy.ndarray` is provided on 'colors' it must be 1D!")
        colors = colors.flatten().tolist()
    elif isinstance(colors, colorobject):
        colors = colors.colors()
    else:
        raise TypeError("Argument 'colors' none of the allowed types.")

    # Checking all colors
    if not allow_nan:
        pat   = compile("^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})([0-9A-Fa-f]{2})?$")
    else:
        # TODO(R): Implement this one.
        raise Exception("allow_nan not yet implemented.")

    # check individual entry. Also extends the color if needed.
    def check(x, pat):
        tmp = pat.match(x)
        # Just not a proper definition
        if not tmp:
            raise ValueError("String '{:s}' is no valid hex color.".format(x))
        elif len(tmp.group(1)) == 3 and not tmp.group(2) == None:
            raise ValueError("String '{:s}' is no valid hex color!".format(x))
        # Three digit: extend
        elif len(tmp.group(1)) == 3:
            x = "#" + "".join(repeat([x for x in tmp.group(1)], 2))
        return x

    colors = [check(x, pat) for x in colors]

    return colors



# --------------------------------------------------------------------
# Calculate relative luminance
# --------------------------------------------------------------------
def relative_luminance(colors):
    """Calculate relative luminance

    Given a series of colors this function calculates the relative luminance.

    Args:
        colors (str, list, palette, colorobject): colors will be extracted from
            the :py:class:`colorspace.colorlib.colorobject` or
            :py:class:`colorspace.palette` object if provided. Else the input
            is passed to :py:func:`colorspace.check_hex_colors`.

    Returns:
        numpy.array: Containing relative luminance.

    Examples:
        >>> colors = hexcols(["#ff0033", "#0033ff", "#00ffff", "#cecece"])
        >>> relative_luminance(colors)

    Raises:
        TypeError: If cols is invalid.
    """

    from colorspace.colorlib import colorobject, hexcols
    from colorspace import palette
    from numpy import asarray, where, matmul, transpose

    ## If the input is a colorobject we take it as it is
    #if isinstance(colors, colorobject):
    #    pass
    #elif isinstance(colors, palette):
    #    colors = hexcols(colors.colors())
    ## Else we pass the input trough the hex checker first.
    #else:
    #    try:
    #        colors = hexcols(check_hex_colors(colors))
    #    except:
    #        raise TypeError("Input 'colors' non of the recoginzed types or no valid hex colors.")

    #colors.to("sRGB")
    colors = hexcols(palette(colors).colors())
    colors.to("sRGB")

    rgb = transpose(asarray([colors.get("R"), colors.get("G"), colors.get("B")]))
    rgb = where(rgb <= 0.03928, rgb / 12.92, ((rgb + 0.055) / 1.055)**2.4)
    return matmul(rgb, asarray([0.2126, 0.7152, 0.0722]))



# --------------------------------------------------------------------
# Calculate W3C contrast ratio
# --------------------------------------------------------------------
def contrast_ratio(colors, bg = "#FFFFFF", plot = False, ax = None, \
        fontsize = "xx-large", fontweight = "heavy", ha = "center", va = "center"):
    """W3C Contrast Ratio

    Compute (and visualize) the contrast ratio of pairs of colors, as defined
    by the World Wide Web Consortium (W3C).

    The W3C Content Accessibility Guidelines (WCAG) recommend a contrast ratio
    of at least 4.5 for the color of regular text on the background color, and
    a ratio of at least 3 for large text. See
    `https://www.w3.org/TR/WCAG21/#contrast-minimum`_.

    The contrast ratio is defined in `https://www.w3.org/TR/WCAG21/#dfn-contrast-ratio`_
    as `(L1 + 0.05) / (L2 + 0.05)` where `L1` and `L2` are the relative luminances
    (see `https://www.w3.org/TR/WCAG21/#dfn-relative-luminance`_) of the lighter and darker
    colors, respectively. The relative luminances are weighted sums of scaled sRGB coordinates:
    `0.2126 * R + 0.7152 * G + 0.0722 * B` where each of `R`, `G`, and `B`
    is defined as `RGB / 12.92 if RGB <= 0.03928 else (RGB + 0.055)/1.055)^2.4` based on
    the `RGB` coordinates between 0 and 1.

    Args:
        colors (str, list, colorobject, palette): Single hex color (str), a list of hex colors (list),
            or an object of class :py:class:`colorobject <colorspace.colorlib.colorobject>`
            or :py:class:`palette <colorspace.palettes.palette>`.
        bg (str): background color against which the contrast will be calculated.
            Defaults to white (`"#FFFFFF"`).
        plot (bool): logical indicating whether the contrast ratios should also be
            visualized by simple color swatches.
        ax (None or matplotlib.axes.Axes): If None, a new matplotlib figure will
            be created. If `ax` inherits from `matplotlib.axes.Axes` this object
            will be used to create the demoplot. Handy to create multiple subplots.
            Forwarded to different plot types.
        fontsize (float, str): size of text, forwarded to `matplotlib.pyplot.text`.
            Defaults to `"xx-large"`.
        fontweight (str): weight of text, forwarded to `matplotlib.pyplot.text`.
            Defaults to `"heavy"`.
        ha (str): horizontal alignment, forwarded to `matplotlib.pyplot.text`.
            Defaults to `"center"`.
        va (str): vertical alignment, forwarded to `matplotlib.pyplot.text`.
            Defaults to `"center"`.

    Returns:
        A numeric vector with the contrast ratios is returned (invisibly, if `plot` is `True`).

    Examples:
        >>> # check contrast ratio of default palette on white background
        >>> from colorspace import rainbow, contrast_ratio
        >>> colors = rainbow().colors(7)
        >>> contrast_ratio(colors, "#FFFFFF") # Against white
        >>> contrast_ratio(colors, "#000000") # Against black
        >>>
        >>> contrast_ratio(colors, "#FFFFFF", plot = True) # Visualization
        >>> contrast_ratio(colors, "#000000", plot = True) # Visualization

    Raises:
        TypeError: If cols or bg is not one of the recognized types.
        TypeError: If argument plot is not boolean.
        TypeError: If `ax` is not `None` or a `matplotlib.axes.Axes` object. Only
            checked if `plot = True`.
    """

    from colorspace.palettes import palette
    from colorspace.colorlib import colorobject, hexcols
    from numpy import resize, where

    # Convert inputs to palettes. They will fail in case the input
    # is invalid.
    colors = palette(colors)
    bg     = palette(bg)

    if not isinstance(plot, bool): raise TypeError("Input 'plot' must be boolean.")
    if   len(colors) > len(bg): bg   = palette(resize(bg.colors(),   len(colors)), "_tmp_palette_")
    elif len(bg) > len(colors): colors = palette(resize(colors.colors(), len(bg)),   "_tmp_palette_")

    # Compute contrast ratio
    cols_hex = hexcols(colors.colors())
    bg_hex   = hexcols(bg.colors())
    ratio    = (relative_luminance(cols_hex) + 0.05) / (relative_luminance(bg_hex) + 0.05)
    ratio    = where(ratio < 1, 1 / ratio, ratio)

    if plot:
        import matplotlib.pyplot as plt
        from matplotlib.axes import Axes
        from matplotlib.pyplot import text
        from matplotlib.patches import Rectangle

        if not isinstance(ax, (type(None), Axes)):
            raise TypeError("Argument 'ax' must be `None` or a `matplotlib.axes.Axes` object.")

        # Open figure if input "fig" is None, else use
        # input "fig" handler.
        if ax is None:
            fig = plt.figure()
            ax  = plt.gca()
            showfig = True
        else:
            showfig = False

        ax.set_xlim([0, 2]); ax.set_ylim(0, len(cols_hex) - 0.05)
        n       = len(cols_hex)

        # Drawing the information
        for i in range(n):
            # Drawing background
            rect = Rectangle((0, i), 1, .95, linewidth = 1, facecolor = cols_hex.colors()[i])
            ax.add_patch(rect)
            rect = Rectangle((1, i), 1, .95, linewidth = 1, facecolor = bg_hex.colors()[i])
            ax.add_patch(rect)
            # Adding text
            text(0.5, i + 0.5, "{:4.2f}".format(ratio[i]), color = bg_hex.colors()[i],
                    fontsize = fontsize, fontweight = fontweight, ha = ha, va = va)
            text(1.5, i + 0.5, "{:4.2f}".format(ratio[i]), color = cols_hex.colors()[i],
                    fontsize = fontsize, fontweight = fontweight, ha = ha, va = va)

        # Remove axis and make the thing tight
        ax.axis("off")

        if not showfig:
            return ax
        else:
            fig.tight_layout()
            fig.show()

    return ratio



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
        TypeError: If unexpected input on `H` or `L`.
        TypeError: If length of `H` and `L` are not the same (see above).
        TypeError: If input `floor` is not boolean.
    """

    import numpy as np
    import json
    import os
    import re

    if isinstance(H, (float, int)):
        H = np.atleast_1d(np.asarray(H, dtype = "float"))
    elif isinstance(H, (list, np.ndarray)):
        #H = np.asarray([H] if len(H.shape) == 0 else H, dtype = "float")
        H = np.atleast_1d(np.asarray(H, dtype = "float"))
    else:
        raise TypeError("Unexpected input on argument `H`.")
    if isinstance(L, (float, int)):
        L = np.atleast_1d(np.asarray(L, dtype = "float"))
    elif isinstance(L, (list, np.ndarray)):
        L = np.atleast_1d(np.asarray(L, dtype = "float"))
    else:
        raise TypeError("Unexpected input on argument `L`.")
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
    while np.any(H < 0):    H = np.where(H < 0,    H + 360., H)
    while np.any(H >= 360): H = np.where(H >= 360, H - 360., H)

    # Prepare the values used for the 'table search'.
    # Fix luminance to values between [0., 100.]
    L = np.fmin(100, np.fmax(0, L))

    # Loading json data set
    resource_package = os.path.dirname(__file__)
    filename = os.path.join(resource_package, "data", "max_chroma_table.json")
    with open(filename, "r") as fid:
        mctab = json.loads(fid.readline())

    # Minimum/maximum hue and luminance
    hmin = np.fmax(0,   [int(np.floor(x + 1e-08)) for x in H])
    lmin = np.fmax(0,   [int(np.floor(x + 1e-08)) for x in L])
    hmax = np.fmin(360, [int(np.ceil(x  + 1e-08)) for x in H])
    lmax = np.fmin(100, [int(np.ceil(x  + 1e-08)) for x in L])

    # Not very efficient. However, the best I came up for now :|
    # Reading/loading the json data set takes about half of the time,
    # maybe more efficient to directly code it rather than reading it from
    # disc. TODO(R): investigate this at some point.
    def get_max(a, b):
        res = []
        for i in range(len(a)):
            res.append(mctab["{:d}-{:d}".format(a[i], b[i])])
        return np.asarray(res).flatten()

    # Calculate max chroma
    C = (hmax - H) * (lmax - L) * get_max(hmin, lmin) + \
        (hmax - H) * (L - lmin) * get_max(hmin, lmax) + \
        (H - hmin) * (lmax - L) * get_max(hmax, lmin) + \
        (H - hmin) * (L - lmin) * get_max(hmax, lmax)
    C = np.where(np.logical_or(L < 0., L > 100.), 999, C)

    # Floor if requested and return
    if floor: C = np.floor(C)
    return C

def darken(col, amount = 0.1, space = "HCL", fixup = True):
    """Algorithmically lighten or darken colors.

    See `help(lighten)` for more details.
    """
    return lighten(col, amount = amount * -1., method = "relative", space = space, fixup = fixup)


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
        TypeError: If `method` is not str.
        ValueError: If `method` is not one of `"absolute"` or `"relative"`.
        TypeError: If `space` is not str.
        ValueError: If `space` is not one of `"HCL"` or `"HSV"`.
        TypeError: If input 'col' is not among the one of the recognized objects.
        TypeError: If `fixup` is not boolean.
    """

    from colorspace.colorlib import colorobject, hexcols
    from colorspace.palettes import palette
    from numpy import fmin, fmax, where

    if not isinstance(method, str):
        raise TypeError("Input 'method' must be str.")
    elif not method in ["absolute", "relative"]:
        raise ValueError("Wrong input for 'method'. Must be `\"absolute\"` or `\"relative\"`.")

    if not isinstance(space, str):
        raise TypeError("Input 'space' must be str.")
    elif not space in ["HCL", "HLS", "combined"]:
        raise ValueError("Wrong input for 'space'. Must be `\"HCL\"`, `\"HLS\"`, or `\"combined\"`.")

    if not isinstance(fixup, bool):
        raise TypeError("Input `fixup` must be boolean `True` or `False`.")

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
        print(tmp)
        if method == "relative":
            tmp.set(L = where(amount >= 0, \
                              1. - (1. - tmp.get("L")) * (1. - amount), \
                              tmp.get("L") * (1. + amount)))
        else:
            tmp.set(L = tmp.get("L") + amount)
            print(tmp)
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


