# All matrices in this file are adapted from https://github.com/njsmith/colorspacious/blob/master/colorspacious/cvd.py

#' Color Vision Deficiency (CVD) Conversion Functions.
#' 
#' Conversion tables for simulating different types of color vision deficiency (CVD):
#' Protanomaly, deutanomaly, tritanomaly.
#' 
#' Machado et al. (2009) have established a novel model, that allows to handle normal color
#' vision, anomalous trichromacy, and dichromacy in a unified way. They also provide conversion
#' formulas along with tables of certain constants that allow to simulate various types of
#' CVD. See \code{\link{simulate_cvd}} for the corresponding simulation functions.
#' 

def deutan(cols, severity = 1., linear = True):
    """Transformation of R colors by simulating color vision
    deficiencies, based on a CVD transform matrix.
    This function is a interface to the CVD object and
    returns simulated colors for deuteranope vision
    (green-yellow-red weakness).

    Args:
        cols (list of str or colorobject): A colorobject (such as RGB, HCL, CIEXYZ) or a list of hex colors
        severity (float): Severity in ``[0., 1.]``. Zero means no deficiency, one
            maximum deficiency, defaults to 1.0.
        linear (bool): Should the color vision deficiency transformation be applied to the
            linearized RGB coordinates (default)? If `False`, the transformation is applied to the
            gamma-corrected sRGB coordinates (as in the Machado et al. 2009 supplementary materials).

    Returns:
        colorobject: Returns an object of the same type as the input object ``cols`` with
        modified colors as people with deuteranomaly see these colors (simulated).

    See Also:
        :py:func:`protan`, :py:func:`tritan`,
        :py:func:`desaturate`, and `:py:func:`cvd_emulator`.

    Example:

        >>> from colorspace import rainbow_hcl, specplot
        >>> cols = rainbow_hcl()(100)
        >>> specplot(cols)
        >>> specplot(deutan(cols))
        >>> specplot(deutan(cols, 0.5))
        >>>
        >>> # List of (hex) colors
        >>> cols = ["magenta", "red", "orange", "#F2F204", "#6BF204", "#4DA00D"]
        >>> deutan(cols)
        >>> swatchplot([cols, deutan(cols)], show_names = False)
        >>>
        >>> # From palette object
        >>> pal = palette(cols, name = "custom palette")
        >>> deutan(pal)
        >>>
        >>> # From cmap (returns cmap)
        >>> deutan(pal.cmap())
    """

    from .CVD import CVD

    CVD = CVD(cols, "deutan", severity, linear)
    return CVD.colors()


def protan(cols, severity = 1., linear = True):
    """Transformation of R colors by simulating color vision
    deficiencies, based on a CVD transform matrix.
    This function is a interface to the CVD object and
    returns simulated colors for protanope vision.

    Args:
        cols (list of str or :py:class:`colorobject`): A colorobject (such as RGB,
            HCL, CIEXYZ) or a list of hex colors
        severity (float): Severity in ``[0., 1.]``. Zero means no deficiency, one
            maximum deficiency, defaults to 1.0.
        linear (bool): Should the color vision deficiency transformation be applied to the
            linearized RGB coordinates (default)? If `False`, the transformation is applied to the
            gamma-corrected sRGB coordinates (as in the Machado et al. 2009 supplementary materials).

    Returns:
        colorobject: Returns an object of the same type as the input object
        ``cols`` with modified colors as people with protanope color vision
        might see the colors (simulated).

    See Also:
        :py:func:`deutan`, :py:func:`tritan`,
        :py:func:`desaturate`, and `:py:func:`cvd_emulator`.

    Example:

        >>> from colorspace import rainbow_hcl, specplot
        >>> cols = rainbow_hcl()(100)
        >>> specplot(cols)
        >>> specplot(protan(cols))
        >>> specplot(protan(cols, 0.5))
        >>>
        >>> # List of (hex) colors
        >>> cols = ["magenta", "red", "orange", "#F2F204", "#6BF204", "#4DA00D"]
        >>> protan(cols)
        >>> swatchplot([cols, protan(cols)], show_names = False)
        >>>
        >>> # From palette object
        >>> pal = palette(cols, name = "custom palette")
        >>> protan(pal)
        >>>
        >>> # From cmap (returns cmap)
        >>> protan(pal.cmap())
    """

    from .CVD import CVD

    CVD = CVD(cols, "protan", severity, linear)
    return CVD.colors()


def tritan(cols, severity = 1., linear = True):
    """Transformation of R colors by simulating color vision
    deficiencies, based on a CVD transform matrix.
    This function is a interface to the CVD object and
    returns simulated colors for tritanope vision.

    Args:
        cols (list of str or :py:class:`colorobject`):
            A colorobject (such as RGB, HCL, CIEXYZ) or a list of hex colors
        severity (float): Severity in ``[0., 1.]``. Zero means no deficiency,
            one maximum deficiency, defaults to 1.0.
        linear (bool): Should the color vision deficiency transformation be applied to the
            linearized RGB coordinates (default)? If `False`, the transformation is applied to the
            gamma-corrected sRGB coordinates (as in the Machado et al. 2009 supplementary materials).

    See Also:
        :py:func:`deutan`, :py:func:`protan`,
        :py:func:`desaturate`, and `:py:func:`cvd_emulator`.

    Returns:
        colorobject: Returns an object of the same type as the input object ``cols`` with
        modified colors as people with tritanomaly see these colors (simulated).

    Example:

        >>> from colorspace import rainbow_hcl, specplot
        >>> cols = rainbow_hcl()(100)
        >>> specplot(cols)
        >>> specplot(tritan(cols))
        >>> specplot(tritan(cols, 0.5))
        >>>
        >>> # List of (hex) colors
        >>> cols = ["magenta", "red", "orange", "#F2F204", "#6BF204", "#4DA00D"]
        >>> tritan(cols)
        >>> swatchplot([cols, tritan(cols)], show_names = False)
        >>>
        >>> # From palette object
        >>> pal = palette(cols, name = "custom palette")
        >>> tritan(pal)
        >>>
        >>> # From cmap (returns cmap)
        >>> tritan(pal.cmap())
    """

    from .CVD import CVD

    CVD = CVD(cols, "tritan", severity, linear)
    return CVD.colors()


class CVD(object):
    """Object to simulate color vision deficiencies (CVD)
    for protanope, deteranope, and tritanope visual constraints.
    There are wrapper functions to provide simple access for
    the users, see :py:func:`deutan`, :py:func:`protan`, and
    :py:func:`tritan`.

    No return values, initializes a new CVD object which provides functions
    to manipulate the colors acording to the color deficiency (``type_``).

    Args:
        cols (list of str or :py:class:`colorobject`):
            A colorobject (such as RGB, HCL, CIEXYZ) or a list of hex colors
        type_ (str): Type of the deficiency which should be simulated. Currently
            allowed are ``deutan``, ``protan``, and ``tritan``
        severity (float): Severity in ``[0., 1.]``. Zero means no deficiency,
            one maximum deficiency, defaults to 1.0.
        linear (bool): Should the color vision deficiency transformation be applied to the
            linearized RGB coordinates (default)? If `False`, the transformation is applied to the
            gamma-corrected sRGB coordinates (as in the Machado et al. 2009 supplementary materials).

    See Also:
        :py:func:`deutan`, :py:func:`protan`, and :py:func:`tritan`, which are
        convenience interfaces for this class.

    Example:

        >>> from colorspace import rainbow_hcl
        >>> cols = rainbow_hcl()(10)
        >>> from colorspace.CVD import CVD
        >>> deut = CVD(cols, "deutan")
        >>> prot = CVD(cols, "protan")
        >>> trit = CVD(cols, "tritan")
        >>>
        >>> from colorspace import specplot
        >>> specplot(deut.colors())
        >>> specplot(prot.colors())
        >>> specplot(trit.colors())

    Raises:
        TypeError: If `type_` not str.
        ValueError: If `type_` not among the allowed types. Not case sensitive.
        TypeError: If `severity` is no float or integer.
        ValueError: If `severity` not in `[0., 1.]`.
        TypeError: If `linear` is no boolean.
    """

    ALLOWED   = ["protan", "tritan", "deutan"]
    CMAP      = False
    CMAPINPUT = None

    def __init__(self, cols, type_, severity = 1., linear = True):

        from colorspace import palettes

        if not isinstance(severity, (int, float)):
            raise TypeError("Argument 'severity' must be float or integer in `[0., 1.]`.")
        elif isinstance(severity, int): severity = float(severity)
        if severity < 0. or severity > 1.:
            raise ValueError("Severity must be in `[0., 1.]`.")
        if not isinstance(linear, bool):
            raise TypeError("Input `linear` must be boolean `True` or `False`.")

        # Checking type
        if not isinstance(type_, str):
            raise TypeError("Input 'type_' must be str.")
        if not type_.lower() in self.ALLOWED:
            raise ValueError("Input 'type_' wrong, has to be one of {:s}.".format(
                ", ".join(self.ALLOWED)))

        self._type     = type_.lower()
        self._severity = severity
        self._linear   = linear

        # Check if we have a matplotlib.cmap
        # TODO(R): Really needed? If so write tests and examples
        try:
            from matplotlib.colors import LinearSegmentedColormap
            if isinstance(cols, LinearSegmentedColormap):
                from copy import copy
                self.CMAP      = True
                self.CMAPINPUT = copy(cols)
        except:
            pass

        # If the input is a palettes.palette: extract colors and
        # store it in a list. Will then be handled further down as 'list' object.
        if isinstance(cols, palettes.palette):
            cols = cols.colors()

        # Checking input `cols`:
        # TODO(R): See comment above. Needed?
        if self.CMAP:
            # Create an sRGB object
            from .colorlib import sRGB
            cols = sRGB(R = [x[1] for x in cols._segmentdata["red"]],
                        G = [x[1] for x in cols._segmentdata["green"]],
                        B = [x[1] for x in cols._segmentdata["blue"]])
            self._hexinput = False

        elif isinstance(cols, (str, list, tuple)):
            from .utils import check_hex_colors
            from .colorlib import hexcols

            # Check/convert colors
            cols = check_hex_colors(list(cols))

            # Internally: create a hexcols object and store
            # self._hexinput = True. Will be used to also return
            # a hex color list at the end.
            cols = hexcols(cols)
            self._hexinput = True
        else:
            self._hexinput = False
            from .colorlib import colorobject
            if not isinstance(cols, colorobject):
                raise TypeError("Input 'cols' does not match any of the allowed types.")

        # Convert
        from copy import deepcopy
        self._colors_ = deepcopy(cols)

    def _tomat(self, x):
        """Helper function to convert input ``x`` to a proper ``(3x3)``
        `numpy.ndarray`` matrix.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape ``3 x 3``.
            The color deficiency transformation or rotation matrix.
        """
        from numpy import reshape, asarray
        return asarray(x, dtype = float).reshape((3,3), order = "F")

    def protan_cvd_matrizes(self, s):
        """Returns the transformation matrix to simpulate
        protanope color vision deficiency.

        Args:
            s (int): An integer in ``[0, 11]`` to specify which matrix sould be
                returned.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape ``3 x 3``.
            The color deficiency transformation or rotation matrix.
        """

        # Protan CVD
        x = []
        x.append(self._tomat(( 1.000000,  0.000000, -0.000000, 0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat(( 0.856167,  0.182038, -0.038205, 0.029342,  0.955115,  0.015544, -0.002880, -0.001563,  1.004443)))
        x.append(self._tomat(( 0.734766,  0.334872, -0.069637, 0.051840,  0.919198,  0.028963, -0.004928, -0.004209,  1.009137)))
        x.append(self._tomat(( 0.630323,  0.465641, -0.095964, 0.069181,  0.890046,  0.040773, -0.006308, -0.007724,  1.014032)))
        x.append(self._tomat(( 0.539009,  0.579343, -0.118352, 0.082546,  0.866121,  0.051332, -0.007136, -0.011959,  1.019095)))
        x.append(self._tomat(( 0.458064,  0.679578, -0.137642, 0.092785,  0.846313,  0.060902, -0.007494, -0.016807,  1.024301)))
        x.append(self._tomat(( 0.385450,  0.769005, -0.154455, 0.100526,  0.829802,  0.069673, -0.007442, -0.022190,  1.029632)))
        x.append(self._tomat(( 0.319627,  0.849633, -0.169261, 0.106241,  0.815969,  0.077790, -0.007025, -0.028051,  1.035076)))
        x.append(self._tomat(( 0.259411,  0.923008, -0.182420, 0.110296,  0.804340,  0.085364, -0.006276, -0.034346,  1.040622)))
        x.append(self._tomat(( 0.203876,  0.990338, -0.194214, 0.112975,  0.794542,  0.092483, -0.005222, -0.041043,  1.046265)))
        x.append(self._tomat(( 0.152286,  1.052583, -0.204868, 0.114503,  0.786281,  0.099216, -0.003882, -0.048116,  1.051998)))
        return x[s]


    # deutan CVD
    def deutan_cvd_matrizes(self, s):
        """Returns the transformation matrix to simpulate
        deuteranope color vision deficiency.

        Args:
            s (int): An integer in ``[0, 11]`` to specify which matrix sould be
                returned.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape ``3 x 3``.
            The color deficiency transformation or rotation matrix.
        """
        x = []
        x.append(self._tomat(( 1.000000,  0.000000, -0.000000, 0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat(( 0.866435,  0.177704, -0.044139, 0.049567,  0.939063,  0.011370, -0.003453,  0.007233,  0.996220)))
        x.append(self._tomat(( 0.760729,  0.319078, -0.079807, 0.090568,  0.889315,  0.020117, -0.006027,  0.013325,  0.992702)))
        x.append(self._tomat(( 0.675425,  0.433850, -0.109275, 0.125303,  0.847755,  0.026942, -0.007950,  0.018572,  0.989378)))
        x.append(self._tomat(( 0.605511,  0.528560, -0.134071, 0.155318,  0.812366,  0.032316, -0.009376,  0.023176,  0.986200)))
        x.append(self._tomat(( 0.547494,  0.607765, -0.155259, 0.181692,  0.781742,  0.036566, -0.010410,  0.027275,  0.983136)))
        x.append(self._tomat(( 0.498864,  0.674741, -0.173604, 0.205199,  0.754872,  0.039929, -0.011131,  0.030969,  0.980162)))
        x.append(self._tomat(( 0.457771,  0.731899, -0.189670, 0.226409,  0.731012,  0.042579, -0.011595,  0.034333,  0.977261)))
        x.append(self._tomat(( 0.422823,  0.781057, -0.203881, 0.245752,  0.709602,  0.044646, -0.011843,  0.037423,  0.974421)))
        x.append(self._tomat(( 0.392952,  0.823610, -0.216562, 0.263559,  0.690210,  0.046232, -0.011910,  0.040281,  0.971630)))
        x.append(self._tomat(( 0.367322,  0.860646, -0.227968, 0.280085,  0.672501,  0.047413, -0.011820,  0.042940,  0.968881)))
        return x[s]


    # tritanomaly CVD
    def tritan_cvd_matrizes(self, s):
        """Returns the transformation matrix to simpulate
        tritanope color vision deficiency.

        Args:
            s (int): An integer in ``[0, 11]`` to specify which matrix sould be
                returned.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape ``3 x 3``.
            The color deficiency transformation or rotation matrix.
        """

        x = []
        x.append(self._tomat(( 1.000000,  0.000000, -0.000000,  0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat(( 0.926670,  0.092514, -0.019184,  0.021191,  0.964503,  0.014306,  0.008437,  0.054813,  0.936750)))
        x.append(self._tomat(( 0.895720,  0.133330, -0.029050,  0.029997,  0.945400,  0.024603,  0.013027,  0.104707,  0.882266)))
        x.append(self._tomat(( 0.905871,  0.127791, -0.033662,  0.026856,  0.941251,  0.031893,  0.013410,  0.148296,  0.838294)))
        x.append(self._tomat(( 0.948035,  0.089490, -0.037526,  0.014364,  0.946792,  0.038844,  0.010853,  0.193991,  0.795156)))
        x.append(self._tomat(( 1.017277,  0.027029, -0.044306, -0.006113,  0.958479,  0.047634,  0.006379,  0.248708,  0.744913)))
        x.append(self._tomat(( 1.104996, -0.046633, -0.058363, -0.032137,  0.971635,  0.060503,  0.001336,  0.317922,  0.680742)))
        x.append(self._tomat(( 1.193214, -0.109812, -0.083402, -0.058496,  0.979410,  0.079086, -0.002346,  0.403492,  0.598854)))
        x.append(self._tomat(( 1.257728, -0.139648, -0.118081, -0.078003,  0.975409,  0.102594, -0.003316,  0.501214,  0.502102)))
        x.append(self._tomat(( 1.278864, -0.125333, -0.153531, -0.084748,  0.957674,  0.127074, -0.000989,  0.601151,  0.399838)))
        x.append(self._tomat(( 1.255528, -0.076749, -0.178779, -0.078411,  0.930809,  0.147602,  0.004733,  0.691367,  0.303900)))
        return x[s]

    def _interpolate_cvd_transform(self):
        """Method to interpolate the color vision deficiendy transformation
        or rotation matrices.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape ``3 x 3``.
            The interpolated color deficiency transformation or rotation matrix.
        """

        # Getting severity
        fun = getattr(self, "{:s}_cvd_matrizes".format(self._type.lower()))
        severity = self._severity
        if severity <= 0.:
            cvd = fun(0)
        elif severity >= 1.:
            cvd = fun(10)
        else:
            from numpy import floor, ceil
            lo = int(floor(severity * 10.))
            hi = int(ceil(severity * 10.))
            if lo == hi:
                cvd = fun(lo+1) 
            else:
                cvd = (hi - severity * 10.) * fun(lo) + \
                      (severity * 10. - lo) * fun(hi)

        return cvd

    def _simulate(self):
        """Performs the color transformation/simulation.

        Returns:
            list: Returns a list of hex colors.

        .. todo::
            Alpha handling in CVD._simulate.
        """


        from copy import deepcopy
        cols = deepcopy(self._colors_)

        from .colorlib import colorobject

        if not isinstance(cols, colorobject):
            raise ValueError("input cols to {:s}".format(self.__class__.__name__) + \
                    "has to be a colorobject (e.g., CIELAB, RGB, hexcols).")

        # Convert to linear RGB or gamma-corrected sRGB
        if self._linear:
            cols.to("RGB")
        else:
            cols.to("sRGB")

        # Transform color
        from numpy import dot, vstack
        RGB = vstack([cols.get("R"), cols.get("G"), cols.get("B")])
        CVD = self._interpolate_cvd_transform()

        # Apply coefficients/CVD transformation matrix
        [R, G, B] = [RGB[i] for i in [0,1,2]]
        RGB = RGB.transpose().dot(CVD).transpose()

        # Save simulated data
        cols.set(R = RGB[0], G = RGB[1], B = RGB[2])

        # User provided hex colors?
        from copy import copy
        if self._hexinput:
            return copy(cols.colors())
        else:
            return copy(cols)

    def colors(self):
        """Get color object.

        Returns:
            colorobject: Returns the colors of the object with simulated colors
            for the color vision deficiency as specified when initializing the
            object.
        """

        # If input was no matplotlib cmap
        if not self.CMAP:
            return self._simulate()
        # Else simulate and re-create the colormap
        else:
            sRGB = self._simulate()
            r    = sRGB.get("R")
            g    = sRGB.get("G")
            b    = sRGB.get("B")

            # Get input cmap and manipulate colors
            cmap = self.CMAPINPUT
            pos  = [x[0] for x in cmap._segmentdata["red"]]
            cmap._segmentdata = {"red": [], "green": [], "blue": []}
            for i in range(0, len(pos)):
                cmap._segmentdata["red"].append(   (pos[i], r[i], r[i]) )
                cmap._segmentdata["green"].append( (pos[i], g[i], g[i]) )
                cmap._segmentdata["blue"].append(  (pos[i], b[i], b[i]) )

            return cmap


# -------------------------------------------------------------------
# The desaturation function
# -------------------------------------------------------------------
def desaturate(cols, amount = 1.):
    """Transform a vector of given colors to the corresponding colors
    with chroma reduced (by a tunable amount) in HCL space.

    The colors of the color object ``col`` are transformed to the HCL color
    space. In HCL, In HCL, chroma is reduced and then the color is transformed
    back to a colorobject of the same class as the input.

    Args:
        cols (str, list, or colorobject): A colorspace color object such as
            RGB, hexcols, CIELUV, etc.
        amount (float): A value in ``[0.,1.]`` defining the degree of desaturation.
            ``amount = 1.`` removes all color, ``amount = 0.`` none, defaults to 1.0.

    Returns:
        list: Returns a list of modified hex colors.

    See Also:
        :py:func:`deutan`, :py:func:`protan`, :py:func:`tritan`,
        :py:func:`desaturate`, and `:py:func:`cvd_emulator`.

    Example:

        >>> from colorspace import diverging_hcl
        >>> from colorspace.colorlib import hexcols
        >>> cols = hexcols(diverging_hcl()(10))
        >>> from colorspace import specplot
        >>> specplot(desaturate(cols))
        >>> specplot(desaturate(cols, 0.5))
        >>>
        >>> # List of (hex) colors
        >>> cols = ["magenta", "red", "orange", "#F2F204", "#6BF204", "#4DA00D"]
        >>> desaturate(cols)
        >>> swatchplot([cols, desaturate(cols)], show_names = False)
        >>>
        >>> # From palette object
        >>> pal = palette(cols, name = "custom palette")
        >>> desaturate(pal)
        >>>
        >>> # From cmap (returns cmap)
        >>> desaturate(pal.cmap())
    """


    from .colorlib import colorobject
    from .palettes import palette
    from .colorlib import hexcols
    from copy import deepcopy

    # Sanity checks
    if not isinstance(amount, (float, int)):
        raise TypeError("Argument `amount` must be float or integer.")
    elif isinstance(amount, int): amount = float(amount)
    if amount < 0. or amount > 1.:
        raise ValueError("Argument `amount` must be in `[0., 1.]`.")

    # Keep class of input object for later
    input_cols = deepcopy(cols)

    # Convert palette object to list of hex colors
    if isinstance(cols, palette): cols = cols.colors()

    # Check if we have a matplotlib.cmap
    try:
        from matplotlib.colors import LinearSegmentedColormap
        if isinstance(cols, LinearSegmentedColormap):
            from copy import copy
            CMAP      = True
            CMAPINPUT = copy(cols)
        else:
            CMAP      = False
            CMAPINPUT = copy(cols)
    except:
        CMAP      = False
        CMAPINPUT = None

    # If input is a matploblib cmap: convert to sRGB
    # TODO(R): Really needed? If so write tests and examples
    if CMAP:
        # Create an sRGB object
        from .colorlib import sRGB
        cols = sRGB(R = [x[1] for x in cols._segmentdata["red"]],
                    G = [x[1] for x in cols._segmentdata["green"]],
                    B = [x[1] for x in cols._segmentdata["blue"]])
    # If we have hex color input: convert to colorspace.colorlib.hexcols
    elif isinstance(cols, list) or isinstance(cols, str):
        cols = hexcols(cols)

    # From here on "col" needs to be a colorspace.colorlib.colorobject
    if not isinstance(cols, colorobject):
        import inspect
        raise ValueError("input to function {:s} ".format(inspect.stack()[0][3]) + \
                         "has to be of class colorobject (e.g., HCL, CIELUV, ...)")

    # Checking amount
    if amount == 0.: return input_cols

    # Keep original class
    original_class = cols.__class__.__name__
    original_class = "hex" if original_class == "hexcols" else original_class

    from copy import deepcopy
    cols = deepcopy(cols)
    cols.to("HCL")

    # Desaturation
    x = (1. - amount) * cols.get("C")
    cols.set(C = (1. - amount) * cols.get("C"))

    from numpy import where, logical_or
    idx = where(logical_or(cols.get("L") <= 0, cols.get("L") >= 100))[0]
    if len(idx) > 0:
        C = cols.get("C"); C[idx] = 0
        H = cols.get("H"); H[idx] = 0
        cols.set(C = C, H = H)

    cols.to(original_class)

    # If input was no matplotlib cmap
    if not CMAP:
        if original_class == "hex": cols = cols.colors()
        return cols
    # Else manipulate the original cmap object and return
    # a new cmap object with adjusted colors
    else:
        r    = cols.get("R")
        g    = cols.get("G")
        b    = cols.get("B")

        # Get input cmap and manipulate colors
        cmap = CMAPINPUT
        pos  = [x[0] for x in cmap._segmentdata["red"]]
        cmap._segmentdata = {"red": [], "green": [], "blue": []}
        for i in range(0, len(pos)):
            cmap._segmentdata["red"].append(   (pos[i], r[i], r[i]) )
            cmap._segmentdata["green"].append( (pos[i], g[i], g[i]) )
            cmap._segmentdata["blue"].append(  (pos[i], b[i], b[i]) )

        return cmap








