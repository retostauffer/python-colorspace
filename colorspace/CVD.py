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

def deutan(cols, severity = 1.):
    """deutan(cols, severity = 1.)

    Transformation of R colors by simulating color vision
    deficiencies, based on a CVD transform matrix.
    This function is a interface to the CVD object and
    returns simulated colors for deuteranope vision
    (green-yellow-red weakness).

    Parameters
    ----------
    cols : list of str or :py:class:`colorobject`
        a colorobject (such as RGB, HCL, CIEXYZ) or a list of hex colors.
    severity : float
        severity in ``[0., 1.]``. Zero means no deficiency, one maximum
        deficiency.

    Returns
    -------
    Returns an object of the same type as the input object ``cols`` with
    modified colors as people with deuteranomaly see these colors (simulated).

    Examples
    --------
    >>> from colorspace import rainbow_hcl, specplot
    >>> cols = rainbow_hcl()(100)
    >>> specplot(cols)
    >>> specplot(deutan(cols))
    >>> specplot(deutan(cols, 0.5))
    """

    from .CVD import CVD

    CVD = CVD(cols, "deutan", severity)
    return CVD.colors()


def protan(cols, severity = 1.):
    """protan(cols, severity = 1.)

    Transformation of R colors by simulating color vision
    deficiencies, based on a CVD transform matrix.
    This function is a interface to the CVD object and
    returns simulated colors for protanope vision.

    Parameters
    ----------
    cols : list of str or :py:class:`colorobject`
        a colorobject (such as RGB, HCL, CIEXYZ) or a list of hex colors.
    severity : float
        severity in ``[0., 1.]``. Zero means no deficiency, one maximum
        deficiency.

    Returns
    -------
    Returns an object of the same type as the input object ``cols`` with
    modified colors as people with protanope color vision might see the
    colors (simulated).

    Examples
    --------
    >>> from colorspace import rainbow_hcl, specplot
    >>> cols = rainbow_hcl()(100)
    >>> specplot(cols)
    >>> specplot(protan(cols))
    >>> specplot(protan(cols, 0.5))
    """

    from .CVD import CVD

    CVD = CVD(cols, "protan", severity)
    return CVD.colors()


def tritan(cols, severity = 1.):
    """tritan(cols, severity = 1.)

    Transformation of R colors by simulating color vision
    deficiencies, based on a CVD transform matrix.
    This function is a interface to the CVD object and
    returns simulated colors for tritanope vision.

    Parameters
    ----------
    cols : list of str or :py:class:`colorobject`
        a colorobject (such as RGB, HCL, CIEXYZ) or a list of hex colors.
    severity : float
        severity in ``[0., 1.]``. Zero means no deficiency, one maximum
        deficiency.

    Returns
    -------
    Returns an object of the same type as the input object ``cols`` with
    modified colors as people with tritanomaly see these colors (simulated).

    Examples
    --------
    >>> from colorspace import rainbow_hcl, specplot
    >>> cols = rainbow_hcl()(100)
    >>> specplot(cols)
    >>> specplot(tritan(cols))
    >>> specplot(tritan(cols, 0.5))
    """

    from .CVD import CVD

    CVD = CVD(cols, "tritan", severity)
    return CVD.colors()


class CVD(object):
    """CVD(cols, type_, severity = 1.)

    Object to simulate color vision deficiencies (CVD)
    for protanope, deteranope, and tritanope visual constraints.
    There are wrapper functions to provide simple access for
    the users, see :py:func:`deutan`, :py:func:`protan`:, and
    :py:func:`tritan`.

    Parameters
    -----------
    cols : list of str or :py:class:`colorobject`
        a colorobject (such as RGB, HCL, CIEXYZ) or a list of hex colors.
    type_ : str
        type of the deficiency which should be simulated. Currently
        allowed are ``deutan``, ``protan``, and ``tritan``.
    severity : float
        severity in ``[0., 1.]``. Zero means no deficiency, one maximum
        deficiency.

    Returns
    -------
    No return values, initializes a new CVD object which provides functions
    to manipulate the colors acording to the color deficiency (``type_``).

    Examples
    --------
    >>> from colorspace import rainbow_hcl
    >>> cols = rainbow_hcl()(10)
    >>> from colorspace.CVD import CVD
    >>> deut = CVD(cols, "deutan")
    >>> prot = CVD(cols, "protan")
    >>> trit = CVD(cols, "tritan")

    >>> from colorspace import specplot
    >>> specplot(deut.colors())
    >>> specplot(prot.colors())
    >>> specplot(trit.colors())
    """

    ALLOWED = ["protan", "tritan", "deutan"]
    
    def __init__(self, cols, type_, severity = 1.):

        # Getting severity
        if severity < 0.:   severity = 0.
        elif severity > 1.: severity = 1.

        # Checking type
        if not type_.lower() in self.ALLOWED:
            raise ValueError("inpyt type_ to {:s} wrong. ".format(self.__class__.__name__) + \
                    "has to be one of: {:s}".format(", ".join(self.ALLOWED)))
        self._type_     = type_.lower()
        self._severity_ = severity

        # Checking input `cols`:
        if isinstance(cols, list) or isinstance(cols, tuple):
            cols = list(cols)
            from numpy import all
            from re import match, compile
            pat = compile("^(#\w{6}([0-9]{2})?)$")
            if not all([match(pat, x) for x in cols]):
                raise ValueError("got non-hex colors in {:s}. ".format(self.__class__.__name__) + \
                        "If you use hex colors (or a list of hex colors) as input all elements " + \
                        "have to be valid")

            # Internally: create a hexcols object and store
            # self._hexinput_ = True. Will be used to also return
            # a hex color list at the end.
            from .colorlib import hexcols
            cols = hexcols(cols)
            self._hexinput_ = True
        else:
            self._hexinput_ = False
            from .colorlib import colorobject
            if not isinstance(cols, colorobject):
                raise ValueError("input cols to {:s} has to be ".format(self.__class__.__name__) + \
                        "a colorobject (e.g., HCL, RGB, CIEXYZ)")

        # Convert
        from copy import deepcopy
        self._colors_ = deepcopy(cols)

    def _tomat_(self, x):
        """_tomat_(x)

        Helper function to convert input ``x`` to a proper ``(3x3)``
        `numpy.ndarray`` matrix.
        """
        from numpy import reshape, asarray
        return asarray(x, dtype = float).reshape((3,3), order = "F")

    def protan_cvd_matrizes(self, s):
        """protan_cvd_matrizes(s)

        Returns the transformation matrix to simpulate
        protanope color vision deficiency.

        Parameters
        ----------
        s : int
            an integer in ``[0, 11]`` to specify which matrix
            sould be returned.

        Returns
        -------
        Returns a ``(3x3)`` color deficiency transformation or rotation matrix.
        """

        # Protan CVD
        x = []
        x.append(self._tomat_(( 1.000000,  0.000000, -0.000000, 0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat_(( 0.856167,  0.182038, -0.038205, 0.029342,  0.955115,  0.015544, -0.002880, -0.001563,  1.004443)))
        x.append(self._tomat_(( 0.734766,  0.334872, -0.069637, 0.051840,  0.919198,  0.028963, -0.004928, -0.004209,  1.009137)))
        x.append(self._tomat_(( 0.630323,  0.465641, -0.095964, 0.069181,  0.890046,  0.040773, -0.006308, -0.007724,  1.014032)))
        x.append(self._tomat_(( 0.539009,  0.579343, -0.118352, 0.082546,  0.866121,  0.051332, -0.007136, -0.011959,  1.019095)))
        x.append(self._tomat_(( 0.458064,  0.679578, -0.137642, 0.092785,  0.846313,  0.060902, -0.007494, -0.016807,  1.024301)))
        x.append(self._tomat_(( 0.385450,  0.769005, -0.154455, 0.100526,  0.829802,  0.069673, -0.007442, -0.022190,  1.029632)))
        x.append(self._tomat_(( 0.319627,  0.849633, -0.169261, 0.106241,  0.815969,  0.077790, -0.007025, -0.028051,  1.035076)))
        x.append(self._tomat_(( 0.259411,  0.923008, -0.182420, 0.110296,  0.804340,  0.085364, -0.006276, -0.034346,  1.040622)))
        x.append(self._tomat_(( 0.203876,  0.990338, -0.194214, 0.112975,  0.794542,  0.092483, -0.005222, -0.041043,  1.046265)))
        x.append(self._tomat_(( 0.152286,  1.052583, -0.204868, 0.114503,  0.786281,  0.099216, -0.003882, -0.048116,  1.051998)))
        return x[s]


    # deutan CVD
    def deutan_cvd_matrizes(self, s):
        """deutan_cvd_matrizes(s)

        Returns the transformation matrix to simpulate
        deuteranope color vision deficiency.

        Parameters
        ----------
        s : int
            an integer in ``[0, 11]`` to specify which matrix
            sould be returned.

        Returns
        -------
        Returns a ``(3x3)`` color deficiency transformation or rotation matrix.
        """
        x = []
        x.append(self._tomat_(( 1.000000,  0.000000, -0.000000, 0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat_(( 0.866435,  0.177704, -0.044139, 0.049567,  0.939063,  0.011370, -0.003453,  0.007233,  0.996220)))
        x.append(self._tomat_(( 0.760729,  0.319078, -0.079807, 0.090568,  0.889315,  0.020117, -0.006027,  0.013325,  0.992702)))
        x.append(self._tomat_(( 0.675425,  0.433850, -0.109275, 0.125303,  0.847755,  0.026942, -0.007950,  0.018572,  0.989378)))
        x.append(self._tomat_(( 0.605511,  0.528560, -0.134071, 0.155318,  0.812366,  0.032316, -0.009376,  0.023176,  0.986200)))
        x.append(self._tomat_(( 0.547494,  0.607765, -0.155259, 0.181692,  0.781742,  0.036566, -0.010410,  0.027275,  0.983136)))
        x.append(self._tomat_(( 0.498864,  0.674741, -0.173604, 0.205199,  0.754872,  0.039929, -0.011131,  0.030969,  0.980162)))
        x.append(self._tomat_(( 0.457771,  0.731899, -0.189670, 0.226409,  0.731012,  0.042579, -0.011595,  0.034333,  0.977261)))
        x.append(self._tomat_(( 0.422823,  0.781057, -0.203881, 0.245752,  0.709602,  0.044646, -0.011843,  0.037423,  0.974421)))
        x.append(self._tomat_(( 0.392952,  0.823610, -0.216562, 0.263559,  0.690210,  0.046232, -0.011910,  0.040281,  0.971630)))
        x.append(self._tomat_(( 0.367322,  0.860646, -0.227968, 0.280085,  0.672501,  0.047413, -0.011820,  0.042940,  0.968881)))
        return x[s]


    # tritanomaly CVD
    def tritan_cvd_matrizes(self, s):
        """tritan_cvd_matrizes(s)

        Returns the transformation matrix to simpulate
        tritanope color vision deficiency.

        Parameters
        ----------
        s : int
            an integer in ``[0, 11]`` to specify which matrix
            sould be returned.

        Returns
        -------
        Returns a ``(3x3)`` color deficiency transformation or rotation matrix.
        """

        x = []
        x.append(self._tomat_(( 1.000000,  0.000000, -0.000000,  0.000000,  1.000000,  0.000000, -0.000000, -0.000000,  1.000000)))
        x.append(self._tomat_(( 0.926670,  0.092514, -0.019184,  0.021191,  0.964503,  0.014306,  0.008437,  0.054813,  0.936750)))
        x.append(self._tomat_(( 0.895720,  0.133330, -0.029050,  0.029997,  0.945400,  0.024603,  0.013027,  0.104707,  0.882266)))
        x.append(self._tomat_(( 0.905871,  0.127791, -0.033662,  0.026856,  0.941251,  0.031893,  0.013410,  0.148296,  0.838294)))
        x.append(self._tomat_(( 0.948035,  0.089490, -0.037526,  0.014364,  0.946792,  0.038844,  0.010853,  0.193991,  0.795156)))
        x.append(self._tomat_(( 1.017277,  0.027029, -0.044306, -0.006113,  0.958479,  0.047634,  0.006379,  0.248708,  0.744913)))
        x.append(self._tomat_(( 1.104996, -0.046633, -0.058363, -0.032137,  0.971635,  0.060503,  0.001336,  0.317922,  0.680742)))
        x.append(self._tomat_(( 1.193214, -0.109812, -0.083402, -0.058496,  0.979410,  0.079086, -0.002346,  0.403492,  0.598854)))
        x.append(self._tomat_(( 1.257728, -0.139648, -0.118081, -0.078003,  0.975409,  0.102594, -0.003316,  0.501214,  0.502102)))
        x.append(self._tomat_(( 1.278864, -0.125333, -0.153531, -0.084748,  0.957674,  0.127074, -0.000989,  0.601151,  0.399838)))
        x.append(self._tomat_(( 1.255528, -0.076749, -0.178779, -0.078411,  0.930809,  0.147602,  0.004733,  0.691367,  0.303900)))
        return x[s]

    def _interpolate_cvd_transform_(self):
        """_interpolate_cvd_transform_()

        Method to interpolate the color vision deficiendy transformation
        or rotation matrices.

        Returns
        -------
        Returns a ``(3x3)`` color deficiency transformation or rotation matrix.
        """

        # Getting severity
        fun = getattr(self, "{:s}_cvd_matrizes".format(self._type_.lower()))
        severity = self._severity_
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

    def _simulate_(self):
        """_simulate_()

        Performs the color transformation/simulation.

        Returns
        -------
        Returns a list of hex colors.

        .. todo::
            Alpha handling in CVD._simulate_.
        """


        from copy import deepcopy
        cols = deepcopy(self._colors_)

        from .colorlib import colorobject

        if not isinstance(cols, colorobject):
            raise ValueError("input cols to {:s}".format(self.__class__.__name__) + \
                    "has to be a colorobject (e.g., CIELAB, RGB, hexcols).")

        # Convert to sRGB
        cols.to("sRGB")

        # Transform color
        from numpy import dot, vstack
        RGB = vstack([cols.get("R"), cols.get("G"), cols.get("B")])
        CVD = self._interpolate_cvd_transform_()

        # Apply coefficients/CVD transformation matrix
        [R, G, B] = [RGB[i] for i in [0,1,2]]
        RGB = RGB.transpose().dot(CVD).transpose()

        # Save simulated data
        cols.set(R = RGB[0], G = RGB[1], B = RGB[2])

        # User provided hex colors?
        from copy import copy
        if self._hexinput_:
            return copy(cols.colors())
        else:
            return copy(cols)

    def colors(self):
        """colors()

        Returns
        -------
        Returns the colors of the object with simulated colors for the
        color vision deficiency as specified when initializing the
        object.
        """

        return self._simulate_()


# -------------------------------------------------------------------
# The desaturation function
# -------------------------------------------------------------------
def desaturate(col, amount = 1.):
    """desaturate(col, amount = 1.)
    
    Transform a vector of given colors to the corresponding colors
    with chroma reduced (by a tunable amount) in HCL space.

    The colors of the color object `col` are transformed to the HCL color
    space. In HCL, In HCL, chroma is reduced and then the color is transformed
    back to a colorobject of the same class as the input.

    Parameters:
    col : :py:class:`colorobject`
        a colorspace color object such as RGB, hexcols, CIELUV, ...
    amount : float
        a value in ``[0.,1.]`` defining the degree of desaturation.
            ``amount = 1.`` removes all color, ``amount = 0.`` none.

    Returns
    -------
    Returns a list of modified hex colors.

    >>> from colorspace import diverge_hcl
    >>> from colorspace.colorlib import hexcols
    >>> cols = hexcols(diverge_hcl()(10))
    >>> from colorspace import specplot
    >>> specplot(desaturate(cols))
    >>> specplot(desaturate(cols, 0.5))

    .. todo::
        Handling of alpha values. And, in addition, add support for hex colors.
        Currently a list of hex colors as input is not allowed (fix it).
    """


    from .colorlib import colorobject
    if not isinstance(col, colorobject):
        import inspect
        raise ValueError("input to function {:s} ".format(inspect.stack()[0][3]) + \
                         "has to be of class colorobject (e.g., HCL, CIELUV, ...)")

    # Checking amount
    try:
        amount = float(amount)
    except Exception as e:
        import inspect
        raise ValueError("input amount to function {:s} ".format(inspect.stack()[0][3]) + \
                         "has to be a single float: {:s}".format(e))
    if amount < 0. or amount > 1.:
        import inspect
        raise ValueError("input amount to function {:s} ".format(inspect.stack()[0][3]) + \
                         "has to be in [0., 1.]")
    elif amount == 0.: return col

    # Keep original class
    original_class = col.__class__.__name__
    original_class = "hex" if original_class == "hexcols" else original_class

    from copy import deepcopy
    col = deepcopy(col)
    col.to("HCL")
    
    # Desaturation
    col.set(C = (1. - amount) * col.get("C"))

    from numpy import where, logical_or
    idx = where(logical_or(col.get("L") <= 0, col.get("L") >= 100))[0]
    if len(idx) > 0:
        C = col.get("C"); C[idx] = 0
        H = col.get("H"); H[idx] = 0
        col.set(C = C, H = H)

    col.to(original_class)
    if original_class == "hex": col = col.colors()

    # Return color object
    return col


