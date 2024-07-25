

def divergingx_palettes(n = 5, **kwargs):
    """Diverging X HCL Palettes

    Returns pre-defined 'diverging xtra' color palettes based on the HCL
    (Hue-Chroma-Luminance) color model.

    Args:
        n (int): number of colors used when plotting, defaults to `5`.
        **kwargs: forwarded to :py:func:`hcl_palettes`. For a list and description
            of available arguments see the description of :py:func:`hcl_palettes`.

    Return:
        See :py:func:`hcl_palettes`.

    Examples:
        >>> from colorspace import divergingx_palettes
        >>>
        >>> # Get palettes
        >>> divergingx_palettes()
        >>>
        >>> #: Visualize palettes
        >>> divergingx_palettes(n = 15, ncol = 2, plot = True, figsize = (7, 5));
    """

    from .hcl_palettes import hcl_palettes
    return hcl_palettes(n = n, **kwargs, files_regex = ".*divergingx.*")


def hcl_palettes(n = 5, type_ = None, name = None, plot = False, custom = None, ncol = 4, **kwargs):
    """Pre-Defined HCL Palettes

    Function to retrieve and/or display pre-defined color palettes based on the
    HCL (Hue-Chroma-Luminance) color model, excludes 'diverging xtra'
    (see :py:func:`divergingx_palettes`).

    The inputs `type_` and `name` can be used to retrieve a custom subset,
    `custom` can be used to add custom palettes if if needed.

    If `plot = True`, `**kwargs` can be used to specify the figure size of the resulting
    image by specifying `figsize = (height, width)` where both, `height`
    and `width` must be int/float, specifying the height and width in inches.
    Note that `matplotlib` must be installed when `plot = True`.


    Args:
        n (int): The number of colors to be plotted, defaults to `7`.
            Only used if `plot = True`.
        type_ (None, str, list): Given a str or a list of str,
            only a subset of all available default color maps will
            returned/displayed. Can be used in combination with input argument
            `name`. Uses partial matching, not case sensitive.
        name (None, str, list): Similar to `type_`. If not specified
            all palettes will be returned. Can be set to a str or a list of
            str containing the names of the palettes which should be
            returned/plotted.
        plot (bool): If `False` (default) an object of type
            :py:class:`hclpalettes <colorspace.palettes.hclpalettes>` is returned, containing the
            (subset) of pre-defined HCL color palettes.
        custom (defaultpalette): One or multiple
            defaultpalettes can be provided in addition.
        ncol (int): Positive int, number of columns, defaults to `4`.
        **kwargs: Forwarded to the main
            :py:func:`swatchplot <colorspace.swatchplot.swatchplot>` 
            function if `plot = True`.

    Returns:
        Object of type `hclpalettes` or a `matplotlib.figure.Figure` object. If `plot = True`
        a plot will be created and the figure handler returned. If `plot = False` (default)
        an object of class :py:class:`hclpalettes <colorspace.palettes.hclpalettes>` is returned.

    Raises:
        TypeError: If `n`/`ncol` not of type int.
        TypeError: If `type_` is not None or str.
        TypeError: If not is bool `plot`.
        TypeError: In case `custom` is an invalid input.
        ValueError: If `n` or `ncol` are not positive.
        Exception: If no palettes can be found matching the `type_` argument.

    Examples:

        Basic usage:

        >>> from colorspace import hcl_palettes
        >>> # Get all pre-defined HCL palettes shipped with the package
        >>> hcl_palettes()
        >>> #: Get all diverging HCL palettes (basic and advanced)
        >>> hcl_palettes(type_ = "Diverging")
        >>> #: Get only basic diverging HCL palettes
        >>> hcl_palettes(type_ = "Basic: Diverging")
        >>> #: Get specific HCL palettes by name
        >>> hcl_palettes(name = ["Oranges", "Tropic"]) 
        >>>
        >>> #: Visualize all diverging HCL palettes
        >>> hcl_palettes(type_ = "Diverging", ncol = 2,
        >>>              plot = True, figsize = (6, 4));
        >>> #: Visualize specific palettes selected by name
        >>> hcl_palettes(name = ["Oranges", "Tropic"],
        >>>              plot = True, ncol = 1, figsize = (6, 2));
        >>>
        >>> #: Specify number of colors shown
        >>> hcl_palettes(n = 5,  type_ = "Basic: Diverging",
        >>>              plot = True, ncol = 1, figsize = (6, 3));
        >>> #:
        >>> hcl_palettes(n = 51, type_ = "Advanced: Diverging",
        >>>              plot = True, ncol = 1, figsize = (6, 8));
        >>>
        >>> #: Extract specific palettes after loading
        >>> palettes = hcl_palettes()
        >>> c1 = palettes.get_palette("Oranges")
        >>> c1
        >>> #:
        >>> c2 = palettes.get_palette("Greens")
        >>> c2
        >>>
        >>> #: Modify palettes by overwriting palette settings
        >>> c1.set(h1 = 99, l2 = 30, l1 = 30)
        >>> c1.rename("Custom Palette #1")
        >>> c2.set(h1 = -30, l1 = 40, l2 = 30, c1 = 30, c2 = 40)
        >>> c2.rename("Custom Palette #2")
        >>> 
        >>> # Visualize customized palettes
        >>> hcl_palettes(type_ = "Custom", custom = [c1, c2],
        >>>              plot = True, ncol = 1, figsize = (6, 1));

    """

    # Loading pre-defined palettes from within the package
    from . import hclpalettes
    # Loading palettes. Ignore all files labeled 'divergingx' in some way as long
    # as no files_regex is provided on **kwargs
    files_regex = "(?!.*divergingx.*)" if not "files_regex" in kwargs.keys() else kwargs["files_regex"]
    pals = hclpalettes(files_regex = files_regex)

    # Sanity type checks
    if not isinstance(n, int):     raise TypeError("argument `n` must be int")
    if not isinstance(ncol, int):  raise TypeError("argument `ncol` must be int")
    if not isinstance(type_, (type(None), str)):
        raise TypeError("Argument 'type_' must be None (default) or str.")
    if not isinstance(plot, bool): raise TypeError("argument `plot` must be bool")

    # Sanity value checks
    if not n > 0 or not ncol > 0: raise ValueError("arguments `n` and `ncol` must be positive int")

    # If custom palettes have been added: add them as well (if
    # the types are correct, of course).
    if not custom is None:
        from numpy import all
        from .palettes import defaultpalette
        def customerror():
            import inspect
            str = "List with custom palettes provided to {:s}".format(inspect.stack()[0][3])
            str += " but not all elements are of type defaultpalette"
            raise TypeError(str)

        if isinstance(custom, defaultpalette):
            pals._palettes_["Custom"] = [custom]
        # Check if all inputs are of correct type
        elif isinstance(custom, list):
            if not all([isinstance(x, defaultpalette) for x in custom]): customerror()
            pals._palettes_["Custom"] = custom
        # Else append pals._palettes_["Custom"] = custom
        else:
            raise TypeError("argument `custom` not one of the allowed types")


    if not type_ is None:
        if isinstance(type_, str): type_ = [type_]

        # Drop palettes from hclpalettes object not requested
        # by the user.
        for t in pals.get_palette_types():
            if not any([x.upper() in t.upper() for x in type_]):
                del pals._palettes_[t]
    else:
        type_ = pals.get_palette_types()

    # Now dropping all color maps not matching a name, if the
    # user has set a name.
    if not name is None:
        if isinstance(name, str): name = [name]
        # Looping over palette types
        for t in pals.get_palette_types():
            palettenames = [p.name() for p in pals.get_palettes(t)]
            drop = []
            for i in range(0, len(palettenames)):
                if not palettenames[i] in name: drop.append(i)
            # Drop all?
            if len(drop) == len(palettenames):
                del pals._palettes_[t]
            else:
                drop.sort(reverse = True)
                for i in drop: del pals._palettes_[t][i]

    # No palettes survived the selection above?
    if len(pals.get_palettes()) == 0:
        raise Exception(f"no palettes found matching one of: {', '.join(type_)}")

    # Return if plot is not required
    if not plot:
        return pals
    else:
        from .swatchplot import swatchplot
        from numpy import ceil
        nrow = int(ceil((pals.length() + len(pals.get_palette_types())) / ncol))
        return swatchplot(pals, nrow = nrow, n = n, **kwargs)



