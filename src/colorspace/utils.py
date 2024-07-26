
def mixcolor(alpha, color1, color2, where):
    """Compute the Convex Combination of Two Colors

    This function can be used to compute the result of color mixing, assuming
    additive mixing (e.g., as appropriate for RGB and XYZ).

    Args:
        alpha (float): The mixed color is obtained by combining an amount
            `1 - alpha` of `color1` with an amount `alpha` of `color2`.
        color1: an object that can be converted into a
            :py:class:`palette <colorspace.palettes.palette>`.
        color2: a second object that can be converted into a
            :py:class:`palette <colorspace.palettes.palette>`. Must have the same number
            of colors as the argument on `color1`.
        where (str): The color space where the mixing is to take place, either `"RGB"` or `"CIEXYZ"`.

    Return:
        colorspace.colorlib.*: Returns an object of the same class as either
        `color1` with the new mixed color(s). Call `.swatchplot()` to check the
        result or `.colors()` to get a list of mixed hex colors.

    Examples:
        >>> from colorspace.colorlib import RGB
        >>> from colorspace.colorlib import hexcols
        >>> from colorspace import *
        >>>
        >>> # Mixing two colors defined in the RGB space
        >>> # via colorspace.colorlib.RGB. Mixing half-half
        >>> # in the RGB color space (M1) and in the HCL space (M2).
        >>> RGB_1  = RGB(R = 1, G = 0, B = 0)
        >>> RGB_2  = RGB(R = 0, G = 1, B = 0)
        >>> RGB_M1 = mixcolor(0.5, RGB_1, RGB_2, "sRGB")
        >>> RGB_M1
        >>> #: Mixing via XYZ color space
        >>> RGB_M2 = mixcolor(0.5, RGB_1, RGB_2, "CIEXYZ")
        >>> RGB_M2
        >>>
        >>> #: Mixing two lists of hex-colors of length 5.
        >>> #  Mixing takes place once in the RGB color space (M1)
        >>> #  and once in the HCL color space (M2)
        >>> HEX_1  = diverging_hcl()(5)
        >>> HEX_2  = diverging_hcl(rev = True)(5)
        >>> HEX_M1 = mixcolor(0.2, HEX_1, HEX_2, "sRGB")
        >>> HEX_M1
        >>>
        >>> #: Mixing via XYZ color space
        >>> HEX_M2 = mixcolor(0.8, HEX_1, HEX_2, "CIEXYZ")
        >>> HEX_M2
        >>>
        >>> #:
        >>> swatchplot([HEX_1, HEX_2, HEX_M1, HEX_M2],
        >>>            show_names = False, figsize = (5.5, 1));
        >>>
        >>> #: Mixing objects of different length and type
        >>> #  Coordinates of the shorter object (RGB_1) will be recycled
        >>> #  to the same number of colors as in the longer object (HEX_2)
        >>> RES_1 = mixcolor(0.2, RGB_1, HEX_2, "sRGB")
        >>> RES_1.colors()
        >>>
        >>> #:
        >>> RES_2 = mixcolor(0.8, RGB_1, HEX_2, "sRGB")
        >>> RES_2.colors()
        >>>
        >>> #:
        >>> swatchplot([RGB_1, RES_2, HEX_2, RES_1, RES_2],
        >>>            show_names = False, figsize = (5.5, 2));

    Raises:
        TypeError: In case `alpha` is not float or `int`.
        ValueError: If `alpha` is not larger than `0.0` and smaller than `1.0`.
        TypeError: If `where` is not a str.
        ValueError: If `where` is not among the allowed color spaces used for adaptive mixing.
        Exception: If `color1` or `color2` cannot be converted into a palette object.
    """

    from numpy import resize
    from colorspace.colorlib import colorobject, hexcols
    from colorspace.palettes import palette

    if not isinstance(alpha, (float, int)):
        raise TypeError("argument `alpha` must be float or int")
    if isinstance(alpha, int): alpha = float(alpha)
    if alpha < 0. or alpha > 1.:
        raise ValueError("argument `alpha` must be in the range of [0., 1.]")
    if not isinstance(where, str):
        raise TypeError("argument `where` must be str")

    # Allowed color types:
    allowed_spaces = ["sRGB", "CIEXYZ"]
    if not where in allowed_spaces:
        raise ValueError(f"argument `{where}` none of the allowed types: {', '.join(allowed_spaces)}")

    # Converting colors
    try:
        color1 = hexcols(palette(color1).colors())
    except:
        raise Exception("cannot convert object provided on `color1` into a `colorspace.palettes.palette`")
    try:
        color2 = hexcols(palette(color2).colors())
    except:
        raise Exception("cannot convert object provided on `color2` into a `colorspace.palettes.palette`")

    # Convert and extract coordinates
    color1.to(where)
    color2.to(where)
    coord1 = color1.get()
    coord2 = color2.get()

    # If length is not equal; recycle shorter color object
    if len(color1) > len(color2):
        for k in coord2:
            if coord2[k] is None: continue
            coord2[k] = resize(coord2[k], len(color1))
    elif len(color1) < len(color2):
        for k in coord1:
            if coord1[k] is None: continue
            coord1[k] = resize(coord1[k], len(color2))

    # Mixing
    res = dict()
    for k in coord1:
        if coord1[k] is None or coord2[k] is None: continue
        res[k] = coord1[k] * (1. - alpha) + coord2[k] * alpha

    import importlib
    module = importlib.import_module("colorspace.colorlib")
    FUN    = getattr(module, where)
    res    = FUN(**res)
    return res



# --------------------------------------------------------------------
# Performs the check on hex color str to see if they are valid.
# --------------------------------------------------------------------
def check_hex_colors(colors):
    """Checking Hex Color Validity

    Valid hex colors are three digit hex colors (e.g., `#F00`), six digit
    hex colors (e.g., `#FF00FF`), or six digit colors with additional transparency
    (eight digit representation) or `None`. If the inputs do not match one of these hex
    representations `matplotlib.color.to_hex` will be called. This allows
    to also convert standard colors such as `"0"`, `"black"`, or `"magenta"` into
    their corresponding hex representation.

    Args:
        colors (str, list, numpy.ndarray): str or list of str with colors.
            See function description for details. In case it is a
            `numpy.ndarray` it will be flattened to 1-dimensional if needed.

    Returns:
        list: Returns a list (length 1 or more) in case all values provided are
            valid hex colors or None. Three digit colors will be expanded to six
            digit colors, all upper case. Else the function will raise a
            ValueError.

    Examples:

        >>> from colorspace import check_hex_colors
        >>> check_hex_colors("#ff003311")
        >>> #:
        >>> check_hex_colors("#ff0033")
        >>> #:
        >>> check_hex_colors("#f03")
        >>> #:
        >>> check_hex_colors(["#f0f", "#00F", "#00FFFF", "#ff003311"])
        >>> #:
        >>> check_hex_colors(["#FFF", "0", "black", "blue", "magenta"])
        >>> #:
        >>> check_hex_colors([None, "#ff0033", None])
        >>>
        >>> #:
        >>> from numpy import asarray
        >>> check_hex_colors(asarray(["#f0f", "#00F", "#00FFFF", "#ff003311"]))

    Raises:
        ValueError: In case `colors` is a list but does not only contain strnigs.
        TypeError: If `colors` is neither str or list of str.
        ValueError: If at least one of the colors is an invalid hex color.
    """
    from re import match, compile
    from numpy import all, repeat, ndarray, nan, isnan
    from .colorlib import colorobject

    # Saniy checks
    if isinstance(colors, str):
        colors = [colors]
    elif isinstance(colors, list):
        if not all([isinstance(x, (str, type(None))) for x in colors]):
            raise ValueError("list on argument `colors` must only contain str or None")
    elif isinstance(colors, ndarray):
        if not len(colors.shape) == 1:
            raise TypeError("if an `numpy.ndarray` is provided on argument `colors` it must be 1-dimensional")
        colors = colors.flatten().tolist()
    elif isinstance(colors, colorobject):
        colors = colors.colors()
    else:
        raise TypeError("argument `colors` none of the allowed types")

    # Regular expression for checking for valid hex colors
    pat   = compile("^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})([0-9A-Fa-f]{2})?$")

    # check individual entry. Also extends the color if needed.
    def check(x, pat):
        # If is none, leave it as None (from fixup = False)
        if x is None: return x

        # Check if str is of allowed type
        tmp = pat.match(x)

        # In case this is no hex definition (not matching the regular expression
        # above) we try if we can convert the color via matplotlib.colors.to_hex.
        # This allows to convert e.g., "0" or "black" into hex cols. If this works
        # We once again shoot it trough our regular expression.
        if not tmp:
            if x[0] == "#":
                raise ValueError(f"string \"{x}\" is not a valid 3/6/8 digit hex color")
            try:
                from matplotlib.colors import to_hex
                x = to_hex(x)
            except:
                raise ValueError(f"string \"{x}\" could not be converted to valid hex color")
            x = x.upper()

        tmp = pat.match(x)
        # Testing pattern matching (hex color validation)
        if len(tmp.group(1)) == 3 and not tmp.group(2) == None:
            raise ValueError(f"string \"{x}\" is no valid hex color")
        # Three digit: extend
        elif len(tmp.group(1)) == 3:
            x = "#" + "".join(repeat([x for x in tmp.group(1)], 2))

        return x.upper()

    colors = [check(x, pat) for x in colors]

    return colors


# --------------------------------------------------------------------
# Get transparency (or None if there is none defined)
# --------------------------------------------------------------------
def extract_transparency(x, mode = "float"):
    """Extract Alpha Channel

    Currently only for colorobjects. This function interfaces the
    ``.get()`` method of the object.

    Args:
        x: an object which inherits from `colorsspace.colorlib.colorobject` or
           an object of class `colorspace.palettes.palette`.
        mode (str): mode of the return. One of `"float"`, `"int"`, or `"str"`.

    Returns:
        None, numpy.ndarray: `None` if the colorobject has no alpha channel,
            else a numpy.ndarray. The `dtype` of the array depends
            on the `mode` specified.

    Raises:
        TypeError: If input object does not inherit from `colorobject`.
        TypeError: If 'mode' is not str.
        ValueError: If 'mode' is not one of the allowed types shown in the arguments description.

    Examples:
        >>> from colorspace import *
        >>> from colorspace.colorlib import hexcols
        >>> 
        >>> # Three colors without alpha
        >>> cols1 = ['#023FA5',   '#E2E2E2',   '#8E063B']
        >>> # Same colors with transparency 80%, 40%, 80%
        >>> cols2 = ['#023FA5CC', '#E2E2E266', '#8E063BCC']
        >>> 
        >>> # Convert hex color lists to colorobjects
        >>> x1 = hexcols(cols1)
        >>> x2 = hexcols(cols2)
        >>>
        >>> # Extract transparency
        >>> extract_transparency(x1)
        >>> #:
        >>> extract_transparency(x2)
        >>>
        >>> #: Return mode
        >>> extract_transparency(x2, mode = "float")
        >>> #:
        >>> extract_transparency(x2, mode = "int")
        >>> #:
        >>> extract_transparency(x2, mode = "str")
        >>>
        >>> #: Extracting transparency from palette objects
        >>> from colorspace import palette
        >>> p1 = palette(cols1, name = "custom palette 1")
        >>> p2 = palette(cols2, name = "custom palette 2")
        >>>
        >>> #: No return as colors in palette `p1` have no transparency
        >>> extract_transparency(p1, mode = "str")
        >>> #: Extracting transparency from colors in palette `p2`
        >>> extract_transparency(p2, mode = "str")
    """

    from colorspace.palettes import palette
    from colorspace.colorlib import colorobject
    from numpy import asarray, int16

    if not isinstance(x, (colorobject, palette)):
        raise TypeError("argument `x` must inherit from `colorspace.colorlib.colorobject` or `colorspace.palettes.palette`")
    if not isinstance(mode, str):
        raise TypeError("argument `mode` must be a str")
    if not mode in ["float", "int", "str"]:
        raise ValueError("argument `mode` must be one of \"float\", \"int\", or \"str\"")

    # Convert colorspace.palettes.palette to colorspace.colorlib.hexcols
    if isinstance(x, palette):
        from colorspace.colorlib import hexcols
        x = hexcols(x.colors())

    # Extract alpha dimension
    alpha = x.get("alpha")

    # If not none we have to convert it given input argument 'mode'.
    # If mode == "float" we do not have to do anything, but for the other
    # two options we do.
    if not alpha is None:
        if mode == "int":
            alpha = asarray(alpha * 255, int16)
        elif mode == "str":
            alpha = asarray(["{:02X}".format(int(x * 255)) for x in alpha], dtype = "S2")
            alpha = alpha.astype(str)

    return alpha


# --------------------------------------------------------------------
# Remove or adjust transparency
# --------------------------------------------------------------------
def adjust_transparency(x, alpha):
    """Adjust Alpha Channel

    Allows to set, adjust, or remove transparency (alpha channel).
    In case `alpha` is a single float, a constant
    transparency will be added to all colors. If `alpha` is a list or `numpy.ndarray`
    it must be the same length as the number of colors in the object `x` and all
    values must be convertable to float/int in the range of `[0., 1.]`. Allows to
    add individual transparency for each color in `x`.

    Args:
        x: sequence of colors; an object which inherits from colorsspace.colorlib.colorobject.
        alpha (None, float, int, list, numpy.ndarray): ``None`` will remove existing
            transparency (if existing). If `float`, `list`, or numpy.ndarray` 
            trnasparency will be added. See function description for more details.

    Returns:
        numpy.ndarray or None: None if the colorobject has no defined transparency,
            else a numpy.ndarray is returned.

    Examples:
        >>> from colorspace import *
        >>> from colorspace.colorlib import hexcols
        >>> import numpy as np
        >>>
        >>> # Three colors without transparency
        >>> cols1 = ['#023FA5',   '#E2E2E2',   '#8E063B']
        >>> # Same colors as in `cols1` with transparency of 80%, 40%, 80%
        >>> cols2 = ['#023FA5CC', '#E2E2E266', '#8E063BCC']
        >>> 
        >>> # Converting list of hex colors `cols1` into `hexcolor` objects
        >>> x1 = hexcols(cols1)
        >>> x1
        >>>
        >>> #: Extract transparency
        >>> extract_transparency(x1) # Returns 'None' (no transparency)
        >>>
        >>> #: `x1`: Setting constant transparency of 0.5 for all colors
        >>> adjust_transparency(x1, 0.5)
        >>>
        >>> #: Setting custom transparency (adjusting; overwrite existing 0.5)
        >>> adjust_transparency(x1, [0.7, 0.3, 0.7]) # Add transparency
        >>>
        >>> #: Converting list of hex colors `cols2` into `hexcolor` objects
        >>> # and extract transparency defined via 8 digit hex color str
        >>> x2 = hexcols(cols2)
        >>> extract_transparency(x2)
        >>>
        >>> #: Removing transparency, extracting new values (None)
        >>> x2 = adjust_transparency(x2, None)
        >>> extract_transparency(x2) # Returns 'None' (no transparency)
        >>>
        >>> #: Adding transparency again
        >>> x2 = adjust_transparency(x2, np.asarray([0.8, 0.4, 0.8]))
        >>> x2
        >>> #:
        >>> extract_transparency(x2)

    Raises:
        TypeError: If input object does not inherit from `colorspace.colorlib.colorobject`.
        TypeError: If `alpha` is not one of the expected types.
        ValueError: If `alpha` is list or `numpy.ndarray` and does not match length
                of colors in `x`.
        ValueError: If `alpha` cannot be converted to float.
        ValueError: If `alpha` is outside of range `[0., 1.]`.
    """

    import numpy as np
    from colorspace.colorlib import colorobject
    from copy import deepcopy

    if not isinstance(x, colorobject):
        raise TypeError("argument `x` must inherit from `colorspace.colorlib.colorobject`")
    x = deepcopy(x)
    # Checking the alpha object
    if not isinstance(alpha, (type(None), list, float, int, np.ndarray)):
        raise TypeError("unexpected input on argument `alpha`")

    # Remove transparency as alpha was set to None
    if isinstance(alpha, type(None)):
        if "alpha" in x._data_.keys(): del x._data_["alpha"]
    # Adding constant transparency to all colors
    elif isinstance(alpha, (float, int)):
        if alpha < 0 or alpha > 1:
            raise ValueError("transparency (`alpha`) must be in the range of `[0., 1.]`")
        x._data_["alpha"] = np.repeat(float(alpha), len(x))
    # Using same procedure for lists and np.ndarrays.
    elif isinstance(alpha, (list, np.ndarray)):
        if not len(alpha) == len(x):
            raise ValueError("lengt of `alpha` must match length of `x`")
        try:
            alpha = np.asarray(alpha, dtype = "float")
        except:
            raise ValueError("argument `alpha` cannot be converted to float")
        # Check values
        if np.any(alpha < 0) or np.any(alpha > 1):
            raise ValueError("transparency (`alpha`) must be in the range of `[0., 1.]`")
        x._data_["alpha"] = alpha

    return x


# --------------------------------------------------------------------
# Calculate relative luminance
# --------------------------------------------------------------------
def relative_luminance(colors):
    """Calculate Relative Luminance

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
        fontsize = "xx-large", fontweight = "heavy", ha = "center", va = "center",
        **kwargs):
    """W3C Contrast Ratio

    Compute (and visualize) the contrast ratio of pairs of colors, as defined
    by the World Wide Web Consortium (W3C). Requires `matplotlib` to be installed.

    The W3C Content Accessibility Guidelines (WCAG) recommend a contrast ratio
    of at least 4.5 for the color of regular text on the background color, and
    a ratio of at least 3 for large text. See
    <https://www.w3.org/TR/WCAG21/#contrast-minimum>.

    The contrast ratio is defined in <https://www.w3.org/TR/WCAG21/#dfn-contrast-ratio>
    as `(L1 + 0.05) / (L2 + 0.05)` where `L1` and `L2` are the relative luminances
    (see <https://www.w3.org/TR/WCAG21/#dfn-relative-luminance>) of the lighter and darker
    colors, respectively. The relative luminances are weighted sums of scaled sRGB coordinates:
    `0.2126 * R + 0.7152 * G + 0.0722 * B` where each of `R`, `G`, and `B`
    is defined as `RGB / 12.92 if RGB <= 0.03928 else (RGB + 0.055)/1.055)^2.4` based on
    the `RGB` coordinates between 0 and 1.

    Args:
        colors (str, list, colorobject, palette): Single hex color (str), a list of hex colors (list),
            a color object ,
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
        **kwargs: Allows to specify `figsize` forwarded to `maptlotlib.pyplot.figure`,
            only used if `ax` is None.

    Returns:
        A numeric vector with the contrast ratios is returned (invisibly, if `plot` is `True`).

    Examples:
        >>> # check contrast ratio of default palette on white background
        >>> from colorspace import rainbow, contrast_ratio
        >>> colors = rainbow().colors(7)
        >>> contrast_ratio(colors, "#FFFFFF") # Against white
        >>> contrast_ratio(colors, "#000000") # Against black
        >>>
        >>> #: Visualize contrast ratio against white
        >>> contrast_ratio(colors, "#FFFFFF", plot = True);
        >>> #: Visualize contrast ratio against black
        >>> contrast_ratio(colors, "#000000", plot = True);
        >>> #: Changing figure size
        >>> contrast_ratio(colors, "#000000", plot = True, figsize = (4, 3));

    Raises:
        TypeError: If cols or bg is not one of the recognized types.
        TypeError: If argument plot is not bool.
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

    if not isinstance(plot, bool):
        raise TypeError("argument `plot` must be bool")
    if len(colors) > len(bg):
        bg = palette(resize(bg.colors(),   len(colors)), "_tmp_palette_")
    elif len(bg) > len(colors):
        colors = palette(resize(colors.colors(), len(bg)),   "_tmp_palette_")

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
            raise TypeError("argument `ax` must be `None` or a `matplotlib.axes.Axes` object")

        # Open figure if input "fig" is None, else use
        # input "fig" handler.
        if ax is None:
            figsize = (5., 5.) # Default
            figsize = (5., 5.) if not "figsize" in kwargs else kwargs["figsize"]
            fig = plt.figure(figsize = figsize)
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
            plt.show()

    return ratio



def max_chroma(H, L, floor = False):
    """Compute Maximum Chroma for Given Hue and Luminance in HCL

    Compute approximately the maximum chroma possible for a given hue
    and luminance combination in the HCL color space.

    `H` and `L` can be single values or multiple values. If both have length `>
    1`, the length must match. If one is of length `1` it will be recycled to
    match the length of the other argument. In case the function is not able to
    create two arrays of the same length an error will be thrown.

    Args:
        H (int, float, list, numpy.ndarray): hue, one or multiple values (must be
            convertable to float).
        L (int, float, list, numpy.ndarray): luminance, one or multiple values (must be
            convertable to float).
        floor (bool): should return be rounded? Defaults to `False`.

    Returns:
        numpy.ndarray: Array of the same length as `max(len(H), len(L))` with
        maximum possible chroma for these hue-luminance combinations.

    Examples:

        >>> from colorspace import max_chroma
        >>> # Max Chroma for Hue = 0 (red) with Luminance = 50
        >>> max_chroma(0, 50)
        >>>
        >>> #: Max Chroma for Hue = 0 (red) for different Luminance levels
        >>> max_chroma(0, [25, 50, 75])
        >>>
        >>> #: Max Chroma for Hue in sequence [0, 360] by 60, Luminace = 50
        >>> import numpy as np
        >>> max_chroma(np.arange(0, 360, 60), 50)
        >>> 
        >>> #: Same as above but floored
        >>> max_chroma(np.arange(0, 360, 60), 50, floor = True)

    Raises:
        TypeError: If unexpected input on `H` or `L`.
        TypeError: If length of `H` and `L` do not match (see description).
        TypeError: If input `floor` is not bool.
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
        raise TypeError("unexpected input on argument `H`")
    if isinstance(L, (float, int)):
        L = np.atleast_1d(np.asarray(L, dtype = "float"))
    elif isinstance(L, (list, np.ndarray)):
        L = np.atleast_1d(np.asarray(L, dtype = "float"))
    else:
        raise TypeError("unexpected input on argument `L`")
    if not isinstance(floor, bool):
        raise TypeError("argument `floor` must be bool")

    # Check if we have to repeat one of the two inputs.
    # This is only used if one is of length > 1 while the other
    # one is of length 1.
    if len(H) == 1 and len(L) > 1:    H = np.repeat(H, len(L))
    elif len(H) > 0 and len(L) == 1:  L = np.repeat(L, len(H))

    # Now both arrays must have the same number of elements. If not,
    # stop execution and throw an error.
    if not len(H) == len(L):
        raise ValueError("number of values and `H` and `L` do not match or cannot be matched")

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
    # Reading/loading the json data set takes about half of the time, maybe
    # more efficient to directly code it rather than reading it from disc.
    # TODO(enhancement): Investigate this at some point; room for improvement.
    def get_max(a, b):
        res = []
        for i in range(len(a)):
            res.append(mctab[f"{a[i]:d}-{b[i]:d}"])
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

def darken(col, amount = 0.1, method = "relative", space = "HCL", fixup = True):
    """Algorithmically Darken Colors

    Takes one or multiple colors and adjust them sucht hat they apper
    darkened. See also: :py:func:`lighten`.

    Args:
        col: color (or colors) to be manipulated. Can be a
            color object,
            a :py:class:`palette <colorspace.palettes.palette>` object, or a
            str/list of str with valid hex colors.
        amount (float): value between `[0., 1.]` with the amount the colors
            should be lightened. Defaults to `0.1`.
        method (str): either `"relative"` (default) or `"absolute"`.
        space (str): one of `"HCL"` or `"HSV"`. Defaults to `"HCL"`.
        fixup (bool): should colors which fall outside the defined RGB space
            be fixed (corrected)? Defaults to `True`.

    Example:

        >>> from colorspace import darken, lighten, swatchplot
        >>> original = "#ff3322"
        >>> lighter  = lighten(original, amount = 0.3, method = "relative", space = "HCL")
        >>> darker   = darken(original,  amount = 0.3, method = "relative", space = "HCL")
        >>> swatchplot([lighter, original, darker],
        >>>            show_names = False, figsize = (6, 1));

    Raises:
        TypeError: If `method` is not str.
        ValueError: If `method` is not one of `"absolute"` or `"relative"`.
        TypeError: If `space` is not str.
        ValueError: If `space` is not one of `"HCL"` or `"HSV"`.
        TypeError: If 'col' is not among the one of the recognized objects.
        TypeError: If `fixup` is not bool.
    """
    return lighten(col, amount = amount * -1., method = method, space = space, fixup = fixup)


def lighten(col, amount = 0.1, method = "relative", space = "HCL", fixup = True):
    """Algorithmically Lighten Colors

    Takes one or multiple colors and adjust them sucht hat they apper
    lightened. See also: :py:func:`darken`.

    Args:
        col: color (or colors) to be manipulated. Can be a color object
            a :py:class:`palette <colorspace.palettes.palette>` object, or a
            str/list of str with valid hex colors.
        amount (float): value between `[0., 1.]` with the amount the colors
            should be lightened. Defaults to `0.1`.
        method (str): either `"relative"` (default) or `"absolute"`.
        space (str): one of `"HCL"` or `"HLS"`. Defaults to `"HCL"`.
        fixup (bool): should colors which fall outside the defined RGB space
            be fixed (corrected)? Defaults to `True`.

    Example:

        >>> from colorspace import darken, lighten, swatchplot
        >>> original = "#ff3322"
        >>> lighter  = lighten(original, amount = 0.3, method = "relative", space = "HCL")
        >>> darker   = darken(original,  amount = 0.3, method = "relative", space = "HCL")
        >>> swatchplot([lighter, original, darker],
        >>>            show_names = False, figsize = (6, 1));

    Raises:
        TypeError: If `method` is not str.
        ValueError: If `method` is not one of `"absolute"` or `"relative"`.
        TypeError: If `space` is not str.
        ValueError: If `space` is not one of `"HCL"`, `"HLS"`, or `"combined"`.
        TypeError: If input 'col' is not among the one of the recognized objects.
        TypeError: If `fixup` is not bool.
    """

    from colorspace.colorlib import colorobject, hexcols
    from colorspace.palettes import palette
    from numpy import fmin, fmax, where

    if not isinstance(method, str):
        raise TypeError("argument `method` must be str")
    elif not method in ["absolute", "relative"]:
        raise ValueError("Wrong input for 'method'. Must be `\"absolute\"` or `\"relative\"`.")

    if not isinstance(space, str):
        raise TypeError("argument `space` must be str")
    elif not space in ["HCL", "HLS", "combined"]:
        raise ValueError("unexpected value on argument `space`. Must be `\"HCL\"`, `\"HLS\"`, or `\"combined\"`.")

    if not isinstance(fixup, bool):
        raise TypeError("argument `fixup` must be bool")

    # If the input is a colorobject (hex, HSV, ...) we first
    # put everything into a (temporary) palette.
    if isinstance(col, colorobject):  x = palette(col.colors(), "_temp_palette_object_")
    # In case the input is a str or a list of str
    # we convert the input (temporarily) into a palette.
    # This allows us to check if all colors are valid hex colors.
    elif isinstance(col, str):        x = palette([col], "_temp_palette_object_")
    elif isinstance(col, list):       x = palette(col,   "_temp_palette_object_")
    # If the input is a palette object; keep it as it is.
    elif isinstance(col, palette):    x = col
    else:
        raise TypeError("argument `col` must be a colorobject, palette, a str, " + \
                        "or list of str with valid hex colors")

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
        tmp    = _lighten_in_HCL(x.colors(), amount, method) # Via HCL color space
        tmpHLS = _lighten_in_HLS(x.colors(), amount, method) # Via HLS color space
        tmpHLS.to("RGB"); tmpHLS.to("HCL")

        # fix-up L and copy C over from HLS-converted color
        tmp.set(C = tmpHLS.get("C"))

        # make sure chroma is in allowed range
        tmp.set(C = fmin(max_chroma(tmp.get("H"), tmp.get("L"), floor = True), \
                         fmax(0, tmp.get("C"))))

    # Job done, convert back to HEX
    tmp.to("hex")

    # If the original input was a single str: return str
    if isinstance(col, str):              res = tmp.colors()[0]
    # In case the original input has been a list, return list
    elif isinstance(col, list):           res = tmp.colors()
    # In case the input was a palette, return palette with original name.
    elif isinstance(col, palette):        res = palette(tmp.colors(), col.name())
    # Else the input has been a colorobject, return hex color object :)
    else:                                 res = tmp

    return res


