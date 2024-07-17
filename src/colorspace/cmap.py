


def cmap_to_sRGB(x, n = None):
    """Convert Matplotlib Colormap to sRGB Color Object

    This function is for internal use, e.g., when providing
    a `LinearSegmentedColormap` (cmap) to `specplot()`.
    Internally, the cmap will be converted to an sRGB colorobject
    used to extract the required information for plotting.

    Args:
        x (LinearSegmentedColormap, ListedColormap): matplotlib cmap.
        n (None, int): None or integer >= 2.

    Raises:
    TypeError: If argument `x` is not LinearSegmentedColormap or ListedColormap.
    TypeError: If `n` is not None or int.
    ValueError: If `n` is smaller or equal to 1.

    Return:
    sRGB: A colorobject of class `sRGB`.
    """

    from colorspace.palettes import palette
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap
    from numpy import linspace
    from colorspace.colorlib import sRGB

    if not isinstance(x, (LinearSegmentedColormap, ListedColormap)):
        raise TypeError("argument `x` must be LinearSegmentedColormap or ListedColormap")

    if not isinstance(n, (type(None), int)):
        raise TypeError("argument `n` must be None or int")
    if isinstance(n, int) and n <= 1:
        raise ValueError("argument `n` must be > 1")

    # Taking 'N' from colormap
    if n is None: n = x.N
    
    at   = linspace(0., 1., n)
    tmp  = x(at).transpose()
    sRGB = sRGB(R = tmp[0], G = tmp[1], B = tmp[2])

    return sRGB


