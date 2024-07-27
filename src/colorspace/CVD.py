# All matrices in this file are adapted from https://github.com/njsmith/colorspacious/blob/master/colorspacious/cvd.py

# Color Vision Deficiency (CVD) Conversion Functions.
# 
# Conversion tables for simulating different types of color vision deficiency (CVD):
# Protanomaly, deutanomaly, tritanomaly.
# 
# Machado et al. (2009) have established a novel model, that allows to handle normal color
# vision, anomalous trichromacy, and dichromacy in a unified way. They also provide conversion
# formulas along with tables of certain constants that allow to simulate various types of
# CVD. See \code{\link{simulate_cvd}} for the corresponding simulation functions.

def deutan(cols, severity = 1., linear = True):
    """Simulate Color Vision Deficiency

    Transformation of colors by simulating color vision deficiencies, based on
    a CVD transform matrix. This function is an interface to the CVD object and
    returns simulated colors for deuteranope vision (green-yellow-red
    weakness).

    See also :py:func:`protan`, :py:func:`tritan`, :py:func:`desaturate`, and
    :py:func:`cvd_image <colorspace.cvd_image.cvd_image>`.

    Args:
        cols (list, colorobject, matplotlib.colors.LinearSegmentedColormap):
            Single hex color, list of hex colors (str), a matoplotlib cmap, or
            a color color object (such as RGB, hexcols, CIELUV).
        severity (float): Severity in `[0., 1.]`. Zero means no deficiency, one
            maximum deficiency, defaults to `1.`.
        linear (bool): Should the color vision deficiency transformation be applied to the
            linearised RGB coordinates (default)? If `False`, the transformation is applied to the
            gamma-corrected sRGB coordinates (as in the Machado et al. 2009 supplementary materials).

    Returns:
        colorobject: Returns an object of the same type as the input object `cols` with
        modified colors as people with deuteranomaly see these colors (simulated).

    Example:

        >>> from colorspace import rainbow_hcl, deutan, palette
        >>> from colorspace import specplot, swatchplot
        >>>
        >>> # Drawing 100 colors along the HCL rainbow color palette
        >>> cols = rainbow_hcl()(100)
        >>> specplot(cols);
        >>> #:
        >>> specplot(deutan(cols));
        >>> #:
        >>> specplot(deutan(cols, 0.5));
        >>>
        >>> #: List of (hex) colors
        >>> cols = ["magenta", "red", "orange", "#F2F204", "#6BF204", "#4DA00D"]
        >>> deutan(cols);
        >>>
        >>> #: Visualize original and simulated color swatches
        >>> swatchplot([cols, deutan(cols)],
        >>>            show_names = False, figsize = (5, 1.5));
        >>>
        >>> #: From palette object
        >>> pal = palette(cols, name = "custom palette")
        >>> deutan(pal)
        >>>
        >>> #: From cmap (returns cmap)
        >>> deutan(pal.cmap())
    """

    from .CVD import CVD
    from numpy import ndarray

    CVD = CVD(cols, "deutan", severity, linear)

    # Create return
    res = CVD.colors()
    return res.tolist() if isinstance(res, ndarray) else res


def protan(cols, severity = 1., linear = True):
    """Simulate Color Vision Deficiency

    Transformation of colors by simulating color vision deficiencies, based on
    a CVD transform matrix. This function is an interface to the CVD object and
    returns simulated colors for protanope vision.

    See also :py:func:`deutan`, :py:func:`tritan`, :py:func:`desaturate`, and
    :py:func:`cvd_image <colorspace.cvd_image.cvd_image>`.

    Args:
        cols (list, colorobject, matplotlib.colors.LinearSegmentedColormap): A list of valid hex colors (str)
            or a colorobject (such as RGB, HCL, CIEXYZ).
        severity (float): Severity in `[0., 1.]`. Zero means no deficiency, one
            maximum deficiency, defaults to `1.`.
        linear (bool): Should the color vision deficiency transformation be applied to the
            linearised RGB coordinates (default)? If `False`, the transformation is applied to the
            gamma-corrected sRGB coordinates (as in the Machado et al. 2009 supplementary materials).

    Returns:
        colorobject: Returns an object of the same type as the input object
        `cols` with modified colors as people with protanope color vision
        might see the colors (simulated).

    Example:

        >>> from colorspace import rainbow_hcl, protan, palette
        >>> from colorspace import specplot, swatchplot
        >>>
        >>> # Drawing 100 colors along the HCL rainbow color palette
        >>> cols = rainbow_hcl()(100)
        >>> specplot(cols);
        >>> #:
        >>> specplot(protan(cols));
        >>> #:
        >>> specplot(protan(cols, 0.5));
        >>>
        >>> #: List of (hex) colors
        >>> cols = ["magenta", "red", "orange", "#F2F204", "#6BF204", "#4DA00D"]
        >>> protan(cols);
        >>>
        >>> #: Visualize original and simulated color swatches
        >>> swatchplot([cols, protan(cols)],
        >>>            show_names = False, figsize = (5, 1.5));
        >>>
        >>> #: From palette object
        >>> pal = palette(cols, name = "custom palette")
        >>> protan(pal)
        >>>
        >>> #: From cmap (returns cmap)
        >>> protan(pal.cmap())
    """

    from .CVD import CVD
    from numpy import ndarray

    CVD = CVD(cols, "protan", severity, linear)

    # Create return
    res = CVD.colors()
    return res.tolist() if isinstance(res, ndarray) else res


def tritan(cols, severity = 1., linear = True):
    """Simulate Color Vision Deficiency

    Transformation of R colors by simulating color vision deficiencies, based
    on a CVD transform matrix. This function is an interface to the CVD object
    and returns simulated colors for tritanope vision.

    See also :py:func:`deutan`, :py:func:`protan`, :py:func:`desaturate`, and
    :py:func:`cvd_image <colorspace.cvd_image.cvd_image>`.

    Args:
        cols (list, colorobject, matplotlib.colors.LinearSegmentedColormap):
            Single hex color, list of hex colors (str), a matoplotlib cmap, or
            a color color object (such as RGB, hexcols, CIELUV).
        severity (float): Severity in `[0., 1.]`. Zero means no deficiency,
            one maximum deficiency, defaults to `1.`.
        linear (bool): Should the color vision deficiency transformation be applied to the
            linearised RGB coordinates (default)? If `False`, the transformation is applied to the
            gamma-corrected sRGB coordinates (as in the Machado et al. 2009 supplementary materials).

    Returns:
        colorobject: Returns an object of the same type as the input object `cols` with
        modified colors as people with tritanomaly see these colors (simulated).

    Example:

        >>> from colorspace import rainbow_hcl, tritan, palette
        >>> from colorspace import specplot, swatchplot
        >>>
        >>> # Drawing 100 colors along the HCL rainbow color palette
        >>> cols = rainbow_hcl()(100)
        >>> specplot(cols);
        >>> #:
        >>> specplot(tritan(cols));
        >>> #:
        >>> specplot(tritan(cols, 0.5));
        >>>
        >>> #: List of (hex) colors
        >>> cols = ["magenta", "red", "orange", "#F2F204", "#6BF204", "#4DA00D"]
        >>> tritan(cols);
        >>>
        >>> #: Visualize original and simulated color swatches
        >>> swatchplot([cols, tritan(cols)],
        >>>            show_names = False, figsize = (5, 1.5));
        >>>
        >>> #: From palette object
        >>> pal = palette(cols, name = "custom palette")
        >>> tritan(pal)
        >>>
        >>> #: From cmap (returns cmap)
        >>> tritan(pal.cmap())
    """

    from .CVD import CVD
    from numpy import ndarray

    CVD = CVD(cols, "tritan", severity, linear)

    # Create return
    res = CVD.colors()
    return res.tolist() if isinstance(res, ndarray) else res


class CVD(object):
    """Simulate Color Vision Defficiency

    Class simulating color vision deficiencies (CVD)
    for protanope, deteranope, and tritanope visual constraints.
    End-users are advised to use the convenience functions
    :py:func:`deutan`, :py:func:`protan`, and :py:func:`tritan`.

    No return values, initializes a new CVD object providing methods
    to manipulate the colors according to the color deficiency (`type_`).

    Args:
        cols (list, colorobject, matplotlib.colors.LinearSegmentedColormap):
            Single hex color, list of hex colors (str), a matoplotlib cmap, or
            a color color object (such as RGB, hexcols, CIELUV).
        type_ (str): Type of the deficiency which should be simulated; one
            of `"deutan"`, `"protan"`, and `"tritan"`
        severity (float): Severity in `[0., 1.]`. Zero means no deficiency,
            one maximum deficiency, defaults to 1.0.
        linear (bool): Should the color vision deficiency transformation be applied to the
            linearised RGB coordinates (default)? If `False`, the transformation is applied to the
            gamma-corrected sRGB coordinates (as in the Machado et al. 2009 supplementary materials).


    Example:

        >>> from colorspace import rainbow_hcl
        >>> cols = rainbow_hcl()(10)
        >>>
        >>> # Modify colors by emulating color vision deficiency
        >>> from colorspace.CVD import CVD
        >>> deut = CVD(cols, "deutan")
        >>> prot = CVD(cols, "protan")
        >>> trit = CVD(cols, "tritan")
        >>>
        >>> # Spectrum plots of modified colors
        >>> from colorspace import specplot
        >>> specplot(deut.colors(), figsize = (7, 0.5));
        >>> #:
        >>> specplot(prot.colors(), figsize = (7, 0.5));
        >>> #:
        >>> specplot(trit.colors(), figsize = (7, 0.5));

    Raises:
        TypeError: If argument `type_` not str.
        ValueError: If argument `type_` not among the allowed types. Not case sensitive.
        TypeError: If argument `severity` is no float or int.
        ValueError: If argument `severity` not in `[0., 1.]`.
        TypeError: If argument `linear` is no bool.
    """

    ALLOWED   = ["protan", "tritan", "deutan"]
    CMAP      = False
    CMAPINPUT = None

    def __init__(self, cols, type_, severity = 1., linear = True):

        from colorspace import palettes

        if not isinstance(severity, (int, float)):
            raise TypeError("argument `severity` must be float (`[0., 1.]`) or int (`[0, 1]`)")
        elif isinstance(severity, int): severity = float(severity)
        if severity < 0. or severity > 1.:
            raise ValueError("argument `severity` must be in `[0., 1.]`")
        if not isinstance(linear, bool):
            raise TypeError("argument `linear` must be bool")

        # Checking type
        if not isinstance(type_, str):
            raise TypeError("argument `type_` must be str.")
        if not type_.lower() in self.ALLOWED:
            raise ValueError(f"argument `type_` wrong, has to be one of {', '.join(self.ALLOWED)}")

        self._type     = type_.lower()
        self._severity = severity
        self._linear   = linear

        # Check if we have a matplotlib.cmap
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
        # Single hex string to list
        elif isinstance(cols, str):
            cols = [cols]

        # Default; overwritten if input was not hex (nor cmap)
        self._hexinput = True

        # Checking input `cols`:
        # If cmap (matplotlib LinearSegmentedColormap: Convert to sRGB
        if self.CMAP:
            # Create an sRGB object
            from .colorlib import sRGB
            cols = sRGB(R = [x[1] for x in cols._segmentdata["red"]],
                        G = [x[1] for x in cols._segmentdata["green"]],
                        B = [x[1] for x in cols._segmentdata["blue"]])
            cols.to("hex") # Faking 'hex input'

        elif isinstance(cols, (str, list)):
            from .utils import check_hex_colors
            from .colorlib import hexcols

            # Check/convert colors
            cols = check_hex_colors(cols)

            # Internally: create a hexcols object; will return hex colors
            # when calling .colors() method
            cols = hexcols(cols)
        else:
            self._hexinput = False
            from .colorlib import colorobject
            if not isinstance(cols, colorobject):
                raise TypeError("argument `cols` does not match any of the allowed types")

        # Convert
        from copy import deepcopy
        self._colors_ = deepcopy(cols)

    def _tomat(self, x):
        """Transformation/Rotation Matrix

        Helper function to convert input `x` to a proper (3 x 3)
        `numpy.ndarray` (matrix).

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape `3 x 3`.
            The color deficiency transformation or rotation matrix.
        """
        from numpy import reshape, asarray
        return asarray(x, dtype = float).reshape((3,3), order = "F")

    def protan_cvd_matrizes(self, s):
        """Protanope Transformation Matrix

        Returns the transformation matrix to simulate
        protanope color vision deficiency.

        Args:
            s (int): An int in `[0, 11]` to specify which matrix to be returned.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape `3 x 3`.
            The color deficiency transformation or rotation matrix.

        Raises:
            TypeError: If argument `s` is no int.
            ValueError: If argument `s` is not in `[0, 11]`.
        """
        if not isinstance(s, int): raise TypeError("argument `s` must be int")
        elif s < 0 or s > 11:      raise ValueError("argument `s` must be in [0, 11]")

        # Protanope CDV transformation matrix definition
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


    def deutan_cvd_matrizes(self, s):
        """Deuteranope Transformation Matrix

        Returns the transformation matrix to simulate
        deuteranope color vision deficiency.

        Args:
            s (int): An int in `[0, 11]` to specify which matrix to be returned.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape `3 x 3`.
            The color deficiency transformation or rotation matrix.

        Raises:
            TypeError: If argument `s` is no int.
            ValueError: If argument `s` is not in `[0, 11]`.
        """
        if not isinstance(s, int): raise TypeError("argument `s` must be int")
        elif s < 0 or s > 11:      raise ValueError("argument `s` must be in [0, 11]")

        # Deuteranope CDV transformation matrix definition
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
        """Tritanope Transformation Matrix

        Returns the transformation matrix to simulate
        tritanope color vision deficiency.

        Args:
            s (int): An int in `[0, 11]` to specify which matrix to be returned.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape `3 x 3`.
            The color deficiency transformation or rotation matrix.

        Raises:
            TypeError: If argument `s` is no int.
            ValueError: If argument `s` is not in `[0, 11]`.
        """
        if not isinstance(s, int): raise TypeError("argument `s` must be int")
        elif s < 0 or s > 11:      raise ValueError("argument `s` must be in [0, 11]")

        # Tritanope CDV transformation matrix definition
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
        """Interpolate Transformation Matrices

        The package provides 12 transformation matrices for deuteranope,
        protanope, and tritanope color vision deficiencies. To allow for
        more gradual changes, these matrices are linearly interpolated
        depending on the severity requested, performed by this method.

        Returns:
            numpy.ndarray: Returns a numpy float matrix of shape `3 x 3`.
            The interpolated color deficiency transformation or rotation matrix.
        """

        # Getting severity
        fun = getattr(self, f"{self._type.lower()}_cvd_matrizes")
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
                cvd = fun(lo) 
            else:
                cvd = (hi - severity * 10.) * fun(lo) + \
                      (severity * 10. - lo) * fun(hi)

        return cvd

    def _simulate(self):
        """Perform Color Transformation

        Performs the transformation of colors to simulate color
        vision deficiency.

        Returns:
            list: Returns a list of hex colors (str).
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
        """Get Color Object

        Allows to extract the modified colors (simulated color vision deficiency)
        to be used otherwise. The return is a color object of the same class
        as the original input to `CVD`.

        Returns:
            colorobject, matplotlib.colors.LinearSegmentedColormap: Returns
            the colors of the object with simulated colors for the color vision
            deficiency as specified when initializing the object.
        """

        # If input was no matplotlib cmap
        if not self.CMAP:
            return self._simulate()
        # Else simulate and re-create the colormap
        else:
            # We converted the cmap rgbs to hex, now revert this
            from .colorlib import hexcols
            cols = hexcols(self._simulate())
            cols.to("sRGB")

            r    = cols.get("R")
            g    = cols.get("G")
            b    = cols.get("B")

            # Get input cmap and manipulate colors
            from copy import deepcopy
            cmap = self.CMAPINPUT
            sd   = deepcopy(cmap._segmentdata)
            pos  = [x[0] for x in sd["red"]]

            for i in range(len(sd["red"])):
                sd["red"][i]   = (pos[i], r[i], r[i])
                sd["green"][i] = (pos[i], g[i], g[i])
                sd["blue"][i]  = (pos[i], b[i], b[i])
            
            from matplotlib.colors import LinearSegmentedColormap
            cmap = LinearSegmentedColormap(cmap.name, sd, cmap.N)

            return cmap


# -------------------------------------------------------------------
# The desaturation function
# -------------------------------------------------------------------
def desaturate(cols, amount = 1.):
    """Desaturate Colors by Chroma Removal in HCL Space

    Transform a vector of given colors to the corresponding colors
    with chroma reduced (by a tunable amount) in HCL space.

    The color object (`col`) is transformed to the HCL color
    space where the chroma is reduced, before converted back to the original
    color space.

    See also: :py:func:`deutan`, :py:func:`protan`, :py:func:`tritan`,
    :py:func:`desaturate`, and :py:func:`cvd_image <colorspace.cvd_image.cvd_image>`.

    Args:
        cols (str, list, matplotlib.colors.LinearSegmentedColormap, colorobject):
            Single hex color, list of hex colors (str), a matoplotlib cmap, or
            a color color object (such as RGB, hexcols, CIELUV).
        amount (float): A value in `[0.,1.]` defining the degree of desaturation.
            `amount = 1.` removes all color, `amount = 0.` none, defaults to `1.`.

    Returns:
        list: Returns a list of (modified) hex colors.

    Example:

        >>> from colorspace import palette, diverging_hcl, desaturate
        >>> from colorspace import specplot, swatchplot
        >>> from colorspace.colorlib import hexcols
        >>>
        >>> cols = hexcols(diverging_hcl()(10))
        >>> specplot(desaturate(cols));
        >>> #:
        >>> specplot(desaturate(cols, 0.5));
        >>>
        >>> #: Take a list of colors which can be interpreted/translated to hex
        >>> # colors and desaturate them via the HCL color space
        >>> cols = ["magenta", "red", "orange", "#F2F204", "#6BF204", "#4DA00D"]
        >>> desaturate(cols)
        >>> #:
        >>> swatchplot([cols, desaturate(cols)],
        >>>            show_names = False, figsize = (5, 1.5));
        >>>
        >>> #: Desaturate palette object (same colors as above)
        >>> pal = palette(cols, name = "custom palette")
        >>> desaturate(pal)
        >>>
        >>> #: Desaturate a matplotlib cmap object
        >>> desaturate(pal.cmap())
    """


    from .colorlib import colorobject
    from .palettes import palette
    from .colorlib import hexcols
    from copy import deepcopy

    # Sanity checks
    if not isinstance(amount, (float, int)):
        raise TypeError("argument `amount` must be float or int")
    elif isinstance(amount, int): amount = float(amount)
    if amount < 0. or amount > 1.:
        raise ValueError("argument `amount` must be in `[0., 1.]`")

    # If input is str, make list out of it
    if isinstance(cols, str): cols = [cols]

    # Keep class of input object for later
    input_cols = deepcopy(cols)

    # Convert palette object to list of hex colors
    if isinstance(cols, palette): cols = cols.colors()

    # Check if we have a matplotlib.cmap
    try:
        from matplotlib.colors import LinearSegmentedColormap, ListedColormap
        if isinstance(cols, (LinearSegmentedColormap, ListedColormap)):
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
    if CMAP:
        # Create an sRGB object
        from .cmap import cmap_to_sRGB
        cols = cmap_to_sRGB(cols)
    # If we have hex color input: convert to colorspace.colorlib.hexcols
    elif isinstance(cols, list) or isinstance(cols, str):
        cols = hexcols(cols)
    elif not isinstance(cols, colorobject):
        import inspect
        raise TypeError(f"argument `cols` to {inspect.stack()[0][3]} not among the allowed types.")

    # From here on "col" needs to be a colorspace.colorlib.colorobject
    if not isinstance(cols, colorobject):
        raise Exception("internal error; `cols` should be a colorobject by now but is not")

    # Checking amount
    if amount == 0.:
        if not CMAP:
            return input_cols if isinstance(input_cols, (str, list)) else input_cols.colors()
        else:
            return input_cols # CMAP

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

        from numpy import ndarray
        return cols.tolist() if isinstance(cols, ndarray) else cols

    # Else manipulate the original cmap object and return
    # a new cmap object with adjusted colors
    else:
        r    = cols.get("R")
        g    = cols.get("G")
        b    = cols.get("B")

        # Get input cmap and manipulate colors
        cmap = CMAPINPUT
        sd   = deepcopy(cmap._segmentdata)
        pos  = [x[0] for x in sd["red"]]

        for i in range(len(sd["red"])):
            sd["red"][i]   = (pos[i], r[i], r[i])
            sd["green"][i] = (pos[i], g[i], g[i])
            sd["blue"][i]  = (pos[i], b[i], b[i])
        
        from matplotlib.colors import LinearSegmentedColormap
        cmap = LinearSegmentedColormap(cmap.name, sd, cmap.N)

        return cmap





