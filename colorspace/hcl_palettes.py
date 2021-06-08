

def hcl_palettes(n = 5, type_ = None, name = None, plot = False, custom = None, **kwargs):
    """Gives access to the default color palettes of the colorspace package.

    The method can be used to display the default color palettes or subsets or
    to get a :py:class:`colorspace.palettes.hclpalettes` object. 
    The inputs ``type_`` and ``name`` can be used to retrieve a custom subset,
    ``custom`` can be used to add custom :py:class:`colorspace.palettes.defaultpalette`
    objects if needed.

    Details: ``**kwargs`` can be used to specify the figure size of the resulting
    image by specifying ``figsize = (height, width)`` where both, ``height``
    and ``width`` must be int/float, specifying the height and width in inches.


    Args:
        n (int): The number of colors to be plotted, default is 7. Only used if ``plot = True``.
        type_ (None, str, list of str): Given a string or a list of strings
            only a subset of all available default color maps will be displayed. If
            not set, all default palettes will be returned/plotted. Can be used in
            combination with input argument ``name``.
        name (None, str, list of str): Similar to ``type_``. If not specified
            all palettes will be returned.  Can be set to a string or a list of
            strings containing the names of the palettes which should be
            returned/plotted.
        plot (bool): If ``False`` (default) an object of type
            :py:func:`colorspace.palettes.hclpalette` will be returned containing the
            (subset) of default color palettes.  Note that matplotlib has to be
            installed if ``plot = True``.
        custom (:py:class:`colorspace.palettes.defaultpalette`): One or multiple
            defaultpalettes can be provided in addition.
        **kwargs: Forwarded to :py:func:`colorspace.swatchplot.swatchplot` if
            argument ``plot = True``.

    Returns:
        Object of class :py:class:`colorspace.hcl_palettes`.

    Examples:

        Basic usage:

        >>> from colorspace.hcl_palettes import hcl_palettes
        >>>
        >>> print hcl_palettes()
        >>> print hcl_palettes(type_ = "Diverging")
        >>> print hcl_palettes(name = ["Oranges", "Tropic"]) 
        >>>
        >>> print hcl_palettes(type_ = "Diverging", plot = True)
        >>> print hcl_palettes(name = ["Oranges", "Tropic"], plot = True) 
        >>>
        >>> # Loading all available palettes (just to make custom palettes)
        >>> from colorspace.palettes import hclpalettes
        >>> pal = hclpalettes()
        >>> c1 = pal.get_palette("Oranges")
        >>> c2 = pal.get_palette("Greens")
        >>>
        >>> # Modify the custom palettes
        >>> c1.set(h1 = 99, l2 = 30, l1 = 30)
        >>> c1.rename("Retos custom 1")
        >>> c2.set(h1 = -30, l1 = 40, l2 = 30, c1 = 30, c2 = 40)
        >>> c2.rename("Retos custom 1")
        >>> 
        >>> hcl_palettes(type_ = "Custom", custom = [c1, c2], plot = True)
    """

    # Loading pre-defined palettes from within the package
    from . import hclpalettes
    pals = hclpalettes()                    # Loading palettes

    # If custom palettes have been added: add them as well (if
    # the types are correct, of course).
    if not custom is None:
        from numpy import all
        from .palettes import defaultpalette
        def customerror():
            import inspect
            str = "list with custom palettes provided to {:s}".format(inspect.stack()[0][3])
            str += " but not all elements are of type defaultpalette"
            raise ValueError(str)

        if isinstance(custom, defaultpalette):
            pals._palettes_["Custom"] = [custom]
        # Check if all inputs are of correct type
        elif isinstance(custom, list):
            if not all([isinstance(x, defaultpalette) for x in custom]):
                    customerror()
            pals._palettes_["Custom"] = custom
        # Else append pals._palettes_["Custom"] = custom
        else:
            raise ValueError("input custom to {:s} misspecified".format(self.__class__.__name__))


    if not type_ is None:
        if isinstance(type_, str): type_ = [type_]

        # Drop palettes from hclpalettes object not requested
        # by the user.
        for t in pals.get_palette_types():
            if not t.upper() in [x.upper() for x in type_]:
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
        import inspect
        raise Exception("no palettes found in {:s} matching one of: {:s}".format(
                inspect.stack()[0][3], ", ".join(type_)))

    # Return if plot is not required
    if not plot:
        return pals
    else:
        from .swatchplot import swatchplot
        from numpy import ceil
        nrow = int(ceil((pals.length() + len(pals.get_palette_types())) / 4))
        swatchplot(pals, n = n, nrow = nrow, **kwargs)
        return False



