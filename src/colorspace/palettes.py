

class palette:
    """Custom Color Palette

    Allows for the construction of custom (named) color palettes with a fixed
    set of colors based on hex color inputs (or named matplotlib colors).

    Args:
        colors (str, list, colorspace.colorlib.colorobject, LinearSegmentedColormap):
            One or multiple colors which will make up the custom palette, or a
            `matplotlib.colors.LinearSegmentedColormap`.
        name (str): Name of this custom palette. Defaults to `"user_palette"`.
            Used for object representation/visualization.
        n (int): int (`>1`), number of colors drawn from an `hclpalette` object.
            Only taken into account if the object provided on `colors` inherits
            from `colorspace.palettes.hclpalette`.

    Returns:
        An object of class :py:class:`colorspace.palettes.palette`.

    Example:

        >>> from colorspace.palettes import palette
        >>> colors = ["#070707", "#690056", "#C30E62", "#ED8353", "#FDF5EB"]
        >>> custom_pal = palette(colors, "test palette")
        >>> custom_pal
        >>>
        >>> #: Creating custom palettes based on different input
        >>> # types (str, list, colorobject)
        >>> from colorspace.colorlib import hexcols
        >>> from colorspace import palette
        >>> hexcols = hexcols(colors)
        >>> 
        >>> # Creating a series of custom palette objects
        >>> pal1 = palette("#ff0033") # unnamed
        >>> pal2 = palette("#ff0033", name = "Custom Palette")
        >>> pal3 = palette(colors,  name = "Custom Palette #3")
        >>> pal4 = palette(hexcols, name = "Custom Palette #4")
        >>> print(pal1)
        >>> #:
        >>> print(pal2)
        >>> #:
        >>> print(pal3)
        >>> #:
        >>> print(pal4)
        >>>
        >>> #: Palette Swatch Plot
        >>> from colorspace import swatchplot
        >>> swatchplot([pal3, pal4], figsize = (5.5, 2.0));

    Raises:
        TypeError: If `n` is not int.
        ValueError: If `n` is `< 2`.
        TypeError: If `name` is neither `str` nor `None`.
    """

    def __init__(self, colors, name = None, n = 7):

        # Sanity check for input
        from colorspace.colorlib import colorobject
        from colorspace.palettes import hclpalette
        from colorspace import check_hex_colors, palette

        if not isinstance(n, int):
            raise TypeError("argument `n` must be int")
        elif n <= 1:
            raise ValueError("argument `n` must be > 1")

        # Trying to load matplotlib to allow 'colors' to be a
        # LinearSegmentedColormap
        try:
            from matplotlib.colors import LinearSegmentedColormap
            matplotlib_loaded = True
        except:
            matplotlib_loaded = False

        # This is a palette object? Well ...
        if isinstance(colors, hclpalette):
            colors = colors.colors(n)
        # Already a palette object? Simply extract the colors from it.
        elif isinstance(colors, palette):
            colors = colors.colors()
        # If the input inherits from colorspace.colorlib.colorobject we
        # draw the colors as a hex list.
        elif isinstance(colors, colorobject):
            colors = colors.colors()
        # Matplotlib loaded and 'colors' is a LinearSegmentedColormap
        elif matplotlib_loaded and isinstance(colors, LinearSegmentedColormap):
            colors = self._LinearSegmentedColormap_to_colors(colors, n)

        # Now check if all our colors are valid hex colors
        self._colors = check_hex_colors(colors)

        if not isinstance(name, (type(None), str)):
            raise TypeError("argument `name` must be None or a str")

        self._name = name


    def _LinearSegmentedColormap_to_colors(self, x, n):
        from matplotlib.colors import LinearSegmentedColormap
        from numpy import linspace
        from colorspace.colorlib import sRGB

        assert isinstance(x, LinearSegmentedColormap)
        assert isinstance(n, int) and n > 1

        # Evaluate at
        at  = linspace(0.0, 1.0, n)
        # Get sRGB Coordinates
        rgb = x(at).transpose()

        # Create sRGB colorobject, return hex color list
        return sRGB(R = rgb[0], G = rgb[1], B = rgb[2]).colors()


    def __len__(self):
        """Number of Colors

        Returns:
            int: Number of colors.
        """
        return len(self._colors)

    def __repr__(self):
        name = self.name()
        str = "Palette Name: {:s}\n".format("None" if name is None else name) + \
              "       Type: Custom palette\n" + \
              "       Number of colors: {:d}\n".format(len(self.colors()))
        return str

    def rename(self, name):
        """Rename Custom Palette

        Allows to set, remplace, or remove the name of a palette.

        Args:
            name (None, str): new name for the palette.

        Raises:
            ValueError: If input 'name' is not of type str.

        Examples:

            >>> from colorspace import palette
            >>> #: Starting from an unnamed palette
            >>> pal = palette(["#11C638", "#E2E2E2", "#EF9708"])
            >>> pal.name() # Returns None
            >>>
            >>> #: Naming the palette
            >>> pal.rename("Custom palette")
            >>> pal.name()
            >>>
            >>> #: Rename
            >>> pal.rename("Modified palette name")
            >>> pal.name()
            >>>
            >>> #: Unname (replace current name with None)
            >>> pal.rename(None)
            >>> pal.name() # Returns None
 
        """
        if not isinstance(name, (type(None), str)):
            raise ValueError("argument `name` must be None or a str")
        self._name = name

    def name(self):
        """Get Palette Name

        Returns:
            Returns `None` if the palette is unnamed, else
            the name of the palette as `str`.

        Examples:
            >>> from colorspace import palette
            >>> # Unnamed palette
            >>> pal = palette(["#11C638", "#E2E2E2", "#EF9708"])
            >>> pal.name()
            >>> #:
            >>> type(pal.name())
            >>> #: Named palette
            >>> pal = palette(["#11C638", "#E2E2E2", "#EF9708"],
            >>>               name = "My Custom Palette")
            >>> pal.name()
        """
        return self._name

    def colors(self, *args, **kwargs):
        """Get Palette Colors

        Returns the colors of the current palette as a list
        of hex colors (`str`).

        Args:
            *args: Ignored.
            **kwargs: Ignored.

        Returns:
            list: List of all colors of the palette.

        Examples:
            >>> from colorspace import palette
            >>> pal = palette(["#11C638", "#E2E2E2", "#EF9708"],
            >>>               name = "My Custom Palette")
            >>> pal.colors()
        """
        return self._colors

    def swatchplot(self, **kwargs):
        """Palette Swatch Plot

        Interfacing the main :py:func:`swatchplot <colorspace.swatchplot.swatchplot>`
        function. Plotting the spectrum of the current color palette.

        Args:
            **kwargs: forwarded to :py:func:`swatchplot <colorspace.swatchplot.swatchplot>`.
                Note that `show_names` will always be set to `False`.

        Return:
            Returns what :py:func:`colorspace.swatchplot.swatchplot` returns.

        Example:

            >>> from colorspace import palette
            >>> pal = palette(["#FCFFC9", "#E8C167", "#D67500", "#913640", "#1D0B14"],
            >>>               name = "Custom Palette")
            >>> pal.swatchplot()
            >>> pal.swatchplot(figsize = (5, 1))
        """

        from .swatchplot import swatchplot
        if "show_names" in kwargs.keys():
            del kwargs["show_names"]
        return swatchplot(pals = self.colors(), show_names = False, **kwargs)

    def specplot(self, *args, **kwargs):
        """Color Spectrum Plot

        Interfacing the :py:func:`colorspace.specplot.specplot` function.
        Plotting the spectrum of the current color palette.

        Args:
            *args: Forwarded to :py:func:`colorspace.specplot.specplot`.
            **kwargs: Forwarded to :py:func:`colorspace.specplot.specplot`.

        Return:
            Returns what :py:func:`colorspace.specplot.specplot` returns.

        Example:

            >>> from colorspace import palette, diverging_hcl
            >>> # Default diverging HCL palette
            >>> pal = palette(diverging_hcl().colors(7))
            >>> pal.specplot()
            >>> pal.specplot(rgb = False)
        """

        from .specplot import specplot
        return specplot(self.colors(), *args, **kwargs)


    def hclplot(self, **kwargs):
        """Palette Plot in HCL Space

        Internally calls :py:func:`hclplot <colorspace.hclplot.hclplot>`,
        additional arguments to this main function can be forwarded via the
        `**kwargs` argument.

        Args:
            **kwargs: Additional named arguments forwarded to
                :py:func:`hclplot <colorspace.hclplot.hclplot>`.

        Return:
            Returns what :py:func:`colorspace.hclplot.hclplot` returns.

        Example:

            >>> from colorspace import palette, diverging_hcl
            >>> pal = palette(diverging_hcl().colors(7))
            >>> pal.hclplot()
        """

        from .hclplot import hclplot
        return hclplot(x = self.colors(), **kwargs)


    def cmap(self, continuous = True):
        """Create Matplotlib Compatible Color Map

        Converts the current palette into a
        `matplotlib.colors.LinearSegmentedColormap` color map based on the
        colors provided creating this palette object. If `continuous = True`
        a series of `256` unique colors will be created using linear
        interpolation in the standard RGB color space. If `continuous = False`
        the resulting color map is solely based on the number of colors of
        the palette which yields a non-continuous color map with step-functions
        in R, G, and B (see Example).

        Args:
            continuous (bool): If `True` (default) the resulting colormap
                will contain 256 colors, linearely interpolated in between
                the colors of the palette. If `False`, only the `N` colors
                of the palette are used (see Examples).

        Return:
            matplotlib.colors.LinearSegmentedColormap: Colormap to be used with
            matplotlib.

        Example:

            >>> from colorspace import diverging_hcl, palette, specplot
            >>> pal = diverging_hcl()
            >>> pal = palette(pal(5), name = "Diverging Palette with 5 Colors")
            >>>
            >>> # Continuous colormap
            >>> cmap1 = pal.cmap(continuous = True)
            >>> cmap1.N # Internal number of colors
            >>>
            >>> #: Non-continuous version of the colormap
            >>> cmap2 = pal.cmap(continuous = False)
            >>> cmap2.N # Internal number of colors
            >>>
            >>> #: Using helper function for demonstration
            >>> specplot(cmap1, rgb = True, figsize = (8, 6));
            >>> #:
            >>> specplot(cmap2, rgb = True, figsize = (8, 6));

        Raises:
            TypeError: If `continuous` is not bool
        """

        from matplotlib.colors import LinearSegmentedColormap

        if not isinstance(continuous, bool):
            raise TypeError("argument `continuous` must be bool")

        # Create colormap
        n = 256 if continuous else len(self.colors())
        cmap = LinearSegmentedColormap.from_list(self.name(), self.colors(), n)
        return cmap



# -------------------------------------------------------------------
# -------------------------------------------------------------------
class defaultpalette:
    """Pre-defined HCL Color Palettes

    Object for handling the pre-defined HCL-based color palettes, not intended
    to be used by the users.

    Args:
        type (str): Type of palette.
        method (str): Name of the method which has to be called to retrieve colors
            (e.g., :py:class:`colorspace.palettes.diverging_hcl`).
        name (str): Name of the color palette.
        settings (dict): Dictionary containing the parameter settings.

    Returns:
        Object of class `colorspace.palettes.defaultpalette`.
    """

    def __init__(self, type, method, name, settings):

        self._type_      = type
        self._name_      = name
        self._method_    = method
        self._settings_  = settings

    # Default representation of defaultpalette objects.
    def __repr__(self):
        """Standard Representation

        Prints the current settings on stdout.
        Development method."""

        res = []
        res.append("Palette Name: {:s}".format(self.name()))
        res.append("        Type: {:s}".format(self.type()))
        res.append("        Inspired by: {:s}".format(self.get("desc")))
        #for key,val in self._settings_.items():
        keys = list(self.get_settings().keys())
        keys.sort()
        for key in keys:
            if key in ["desc"]: continue
            val = self.get(key)
            if   isinstance(val, bool):   val = " True" if val else "False"
            elif isinstance(val, int):    val = "{:5d}".format(val)
            elif isinstance(val, float):  val = "{:5.1f}".format(val)
            elif callable(val):           val = "{:s}".format(str(val))
            res.append("         {:10s} {:s}".format(key,val))

        return "\n".join(res)

    def __call__(self, n = 11):
        """Get Colors

        Wrapper function for :py:func:`colors`.

        Args:
            n (int): Number of colors, defaults to 7.

        Returns:
            list: List of hex colors.
        """
        return self.colors(n)

    def method(self):
        """Get Construction Method

        Returns method used to create this palette.

        Returns:
            Returns the method (`str`, name of the function to be called
            to create the palette) of the palette.
        """
        return self._method_

    def type(self):
        """Get Palette Type

        Get type of the color palette.

        Returns:
            Returns the type (`str`) of the palette.
        """
        return self._type_

    def name(self):
        """Get Palette Name

        Get name of color palette.

        Returns:
            str: Returns the name of the palette.
        """
        return self._name_

    def rename(self, name):
        """Rename Palette

        Allows to rename the palette.

        Args:
            name (str): New palette name.
        """
        self._name_ = name

    def get(self, what):
        """Get Specific Palette Settings

        Allows to load the settings of the palette for the different parameters
        (e.g., `h1`, `h2`, ...). Returns `None` if the parameter does not
        exist. Another method (:py:func:`set`) allows to set the parameters.

        Args:
            what (str): Name of the parameter which should be extracted and
                returned from the settings of this color palette.

        Returns:
            Returns `None` if the parameter `what` cannot be found,
            else the value of the parameter `what` is returned.
        """
        if what in self._settings_.keys():
            return self._settings_[what]
        else:
            return None


    def set(self, lambda_allowed = False, **kwargs):
        """Set Specific Palette Settings

        Allows to set/overwrite color palette parameters (e.g., `h1`, `h2`,
        ...).  Another method (:py:func:`get`) allows to retrieve the
        parameters.

        Args:
            lambda_allowed (bool): Defaults to `False`, for qualitative palettes this
                is set `True` for `h2`.
            **kwargs: A set of named arguments (`key = value` pairs) where the key
                defines the parameter which should be overruled, value the
                corresponding value. Allowed value types are bool, int, and float.
        """
        if not isinstance(lambda_allowed, bool):
            ValueError("argument `lambda_allowed` must be bool")

        for key,val in kwargs.items():
            # Float or integer? Default case; passing forward
            if isinstance(val, (float, int)):
                pass
            # If key == h2 and val is callable, we do allow this (for qualitative palettes)
            # if lambda_allowed is set True; passing foward as well
            elif key == "h2" and lambda_allowed and callable(val):
                pass
            # Else check current type specification and append
            # if possible (and convert to the new type).
            elif not isinstance(val, (int, float, bool)):
                raise ValueError(f"argument `{key}` to {self.__class__.__name__}" + \
                                 f" is of type {type(val)}; only bool, int, and float allowed.")
            elif isinstance(val, bool):
                val = 1 if val else 0
            else:
                raise Exception(f"whoops, no rule yet to handle {key} = {val}")

            # Not yet a parameter in our dictionary? Add as float
            if not key in self._settings_.keys():
                self._settings_[key] = float(val)
            # If already existing we convert the new value into the existing type.
            elif isinstance(self._settings_[key], int):
                self._settings_[key] = int(val)
            # If setitng exists and is float, int, or a lambda function: replace
            # If val is itself a callable function, take it as is. Else convert to float.
            elif isinstance(self._settings_[key], (int, float)) or callable(self._settings_[key]):
                self._settings_[key] = val if callable(val) else float(val)
            else:
                raise Exception(f"whoops, some code needed here in {self.__class__.__name__}.set")


    def get_settings(self):
        """Get All Palette Settings

        Allows to get the current settings of the palette object.
        To retrieve single parameters use :py:func:`get`.

        Returns:
            Returns a `dict` object with all parameter specification of this
            palette.
        """
        return self._settings_

    def colors(self, n = 11):
        """Get Colors

        Load a set of `n` colors from this palette.  This method evaluates
        the `method` argument to generate a set of hex colors which will be
        returned.  Please note that it is possible that none-values will be
        returned if the fixup-setting is set to `False` (see
        :py:class:`colorlib.hexcols`).

        Args:
            n (int): Number of colors to be returned, defaults to 11.

        Returns:
            list: Returns a list of str with `n` colors from the palette.
        """

        # Dynamically load color function
        mod  = __import__("colorspace")
        cfun = getattr(mod, self._method_)

        # Calling color method with arguments of this object. 
        from copy import copy
        args = copy(self.get_settings())

        pal = cfun(**args)
        return pal.colors(n, fixup = True)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalettes:
    """Prepare Pre-defined HCL Palettes

    Prepares the pre-specified hclpalettes.  Reads the config files and creates
    a set of `defaultpalette` objects.

    See also: :py:func:`divergingx_palettes <colorspace.hcl_palettes.divergingx_palettes>`.

    Args:
        files (None, str list): If `None` (default) the default color palette
            configuration from within the package will be loaded. A path to a custom
            config file (str) or a list of paths can be provided to read custom
            palettes.
        files_regex (None, str): Additional regular expression to filter files.
            Only used if `files = None`.

    Return:
        hclpalettes: Collection of predefined hcl color palettes.

    Examples:

        >>> from colorspace import hclpalettes
        >>> hclpals = hclpalettes()
        >>> hclpals
        >>> #: Palette swatch plots with 5 colors each
        >>> hclpals.plot(n = 5);
        >>> #: Palette swatch plots with 11 colors each
        >>> hclpals.plot(n = 11);
    """
    def __init__(self, files = None, files_regex = None):

        from os.path import dirname, join, isfile

        if not isinstance(files, (type(None), str, list)):
            raise TypeError("argument `files` must either be None, str, or list of str")
        if isinstance(files, str): files = [files]
        if isinstance(files, list):
            for file in files:
                if not isinstance(file, str):
                    raise TypeError("not all elements in `files` are of type str")

        if files is None:
            import glob
            resource_package = dirname(__file__)
            tmp = glob.glob(join(resource_package, "palconfig", "*.conf"))
            # Ensure files_regex is of appropriate type
            if not isinstance(files_regex, (str, type(None))):
                raise TypeError("argument `filex_regex` must be None or str")
            if files_regex:
                from re import match
                files = []
                for f in tmp:
                    if match(files_regex, f): files.append(f)
            else:
                files = tmp

        # Input 'files' specified:
        if not len(files) > 0:
            raise ValueError(f"no palette config files provided ({self.__class__.__name__})")
        for file in files:
            if not isfile(file):
                raise FileNotFoundError(f"file \"{file}\" does not exist")


        # Else trying to load palettes and append thenm to _palettes_
        self._palettes_ = {}
        for file in files:
            [palette_type, pals] = self._load_palette_config_(file)
            if pals: self._palettes_[palette_type] = pals  # append

        # A poor attempt to order the palettes somehow
        x = list(self._palettes_.keys())
        x.sort(reverse = True)
        tmp = {}

        for rec in x: tmp[rec] = self._palettes_[rec]
        self._palettes_ = tmp


    def __repr__(self):
        """Standard Representation

        Standard representation of the object."""
        res = ["HCL palettes"]

        for type_ in self.get_palette_types():
            res.append("") # Blank line
            res.append("Type:  {:s}".format(type_))
            nchar = 0
            for pal in self.get_palettes(type_):
                # Initialize new line
                if nchar == 0:
                    tmp = "Names: {:s}".format(pal.name())
                    nchar = len(tmp)
                elif (len(pal.name()) + nchar) > 60:
                    res.append(tmp)
                    tmp = "       {:s}".format(pal.name())
                    nchar = len(tmp)
                # Append
                else:
                    tmp += ", {:s}".format(pal.name())
                    nchar += len(pal.name()) + 2
            res.append(tmp)

        return "\n".join(res)


    def get_palette_types(self):
        """Get Palette Types

        Get all palette types.

        Returns:
            list: Returns a `list` of str with the names of all palette types
            or groups.
        """

        return list(self._palettes_.keys())

    def get_palettes(self, type_ = None, exact = False):
        """Get Type-Specific Palettes

        Get all palettes of a specific type.

        Args:
            type_ (None, str): (Partial) Name of the palettes which should be returned.
                String matching is used; partial matches are allowed.
                If set to `None` (default) all palettes will be returned. Names
                have to match but are not case sensitive, defaults to None.
            exact (bool): If `False` (default) partial matching is used. If `True`,
                `type_` must be an exact match (case sensitive).

        Examples:
            >>> # Initialize hclpalettes object
            >>> from colorspace import hclpalettes
            >>> hclpals = hclpalettes()
            >>>
            >>> # Get all Diverging palettes
            >>> pals1 = hclpals.get_palettes("Diverging")
            >>> len(pals1)
            >>>
            >>> #: Get 'Advanced: Diverging' palettes, also includes
            >>> # 'Advanced: DivergingX' (partial match).
            >>> pals2 = hclpals.get_palettes("Advanced: Diverging")
            >>> len(pals2)
            >>>
            >>> #: Only get 'Advanced: Diverging' (exact match)
            >>> pals3 = hclpals.get_palettes("Advanced: Diverging", exact = True)
            >>> len(pals3)
            >>> #:
            >>> pals3

        Returns:
            Returns a `list` containing `defaultpalette` objects objects.

        Raises:
            TypeError: If `type_` is not str or None.
            TypeError: If `exact` is not bool.
            ValueError: If no matching palette is found.
        """
        if not isinstance(type_, (str, type(None))):
            raise TypeError("argument `type_` must be str or None")
        if not isinstance(exact, bool):
            raise TypeError("argument `exact` must be bool.")

        # Return all available palettes
        if not type_:
            res = []
            for key,pals in self._palettes_.items(): res += pals

        # Else find matching palettes (given type_). Either exact matches or
        # partial matches depending on `exact`.
        else:
            from re import compile, IGNORECASE, escape
            if not exact:
                pattern = compile(f".*?{escape(type_)}.*?", IGNORECASE)
            else:
                pattern = compile(f"^{escape(type_)}$")

            # Searching trough available palettes
            res = []
            for t in self._palettes_.keys():
                if pattern.match(t):
                    res += self._palettes_[t]

            # No palettes found? Raise ValueError
            if len(res) == 0:
                raise ValueError(f"no palettes for type \"{type_}\" ({'exact' if exact else 'partial'} match)")

        # Else return list with palettes
        return res

    def get_palette(self, name):
        """Get Palette by Name

        Get a palette with a specific name.

        Args:
            name (str): Name of the color palette which should be returned. Not
                case sensitive; blanks are ignored (removed).

        Returns:
            Returns an object of class `defaultpalette` if a palette with
            the name as specified can be found.  Else an error will be dropped.
        """

        # Try to find the palette with the name 'name'
        take_pal = None
        for type_,pals in self._palettes_.items():
            # Looping over palettes
            for pal in pals:
                if pal.name().upper().replace(" ", "") == name.upper().replace(" ", ""):
                    take_pal = pal
                    break;
            # If already found: break outer loop
            if take_pal: break;

        # If none: not found
        if take_pal is None:
            raise ValueError(f"palette \"{name}\" not found")

        # Else return list with palettes
        return take_pal


    # Helper method to load the palette config files.
    def _load_palette_config_(self, file):

        import re
        import sys
        from configparser import ConfigParser

        CNF = ConfigParser()
        CNF.read(file)

        # Reading type (or name)
        try:
            palette_type   = CNF.get("main", "type")
            palette_method = CNF.get("main", "method")
        except Exception as e:
            raise Exception(f"misspecification in palconfig file = \"{file}\": {str(e)}")

        # The dictionary which will be returned.
        pals = []

        # Looping over all sections looking for palette specifications.
        for sec in CNF.sections():
            mtch = re.match("^palette\\s+(.*)$", sec)
            if not mtch: continue

            # Extracting palette name from section name
            name = mtch.group(1).strip()

            # Loading all available setting elements.
            # "desc":  interpreted as character
            # "p1/p1": interpreted as float
            # "fixup": interpreted as bool
            # rest:    interpreted as int
            settings = {}
            for key,val in CNF.items(sec):
                key  = key.lower()
                if key in ["desc"]:
                    settings[key] = val
                elif key in ["fixup"]:
                    settings[key] = True if int(val) else False
                elif key in ["p1","p2", "p3", "p4"]:
                    settings[key] = float(val)
                elif key in ["h1", "h2"]:
                    if re.match("^-?[0-9\\.]+$", val):
                        settings[key] = int(val)
                    else:
                        # Try to evaluate this as a lambda function.
                        try:
                            val = eval(val)
                            if not callable(val): raise Exception
                        except:
                            raise ValueError(f"element '{key}' for palette '{sec}' neither an int nor proper lambda function")
                        # Append lambda function to the settings
                        settings[key] = val

                else:
                    settings[key] = int(val)

            pals.append(defaultpalette(palette_type, palette_method, name, settings))

        # Return dictionary with palettes
        if len(pals) == 0:
            return [None, None]
        else:
            return [palette_type, pals]


    def length(self):
        """Get Number of Palettes

        Get length of palette.

        Returns:
            int: Integer, number of palettes in the object.
        """

        npals = 0
        for type_ in self.get_palette_types():
            for pal in self.get_palettes(type_): npals += 1

        return npals


    def plot(self, n = 5):
        """Palette Swatch Plot

        Interfacing the main :py:func:`swatchplot <colorspace.swatchplot.swatchplot>`
        function. Plotting the spectrum of the current color palette.

        Args:
            n (int): Number of colors, defaults to 7.
        """
        if not isinstance(n, int): raise TypeError("argument `n` must be int")
        if not n > 0:              raise ValueError("argument `n` must be positive")

        from .swatchplot import swatchplot
        swatchplot(self, n = n)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalette:
    """HCL Palette Superclass

    Hy, I am the base class.  Is extended by the different HCL based color
    palettes such as the classes :py:class:`diverging_hcl`, :py:class:`qualitative_hcl`,
    :py:class:`rainbow_hcl`, :py:class:`sequential_hcl`, and maybe even more in the future.
    """

    # Default call: return n hex colors
    def __call__(self, *args, **kwargs):
        """__call__(*args, **kwargs)

        Call interface, calls objects `colors(...)` method.

        Args:
            *args: Unnamd arguments forwarded to the color method.
            **kwargs: Named arguments forwarded to the color method.

        Returns:
            See colors method.
        """
        return self.colors(*args, **kwargs)

    def specplot(self, n = 180, *args, **kwargs):
        """Color Spectrum Plot

        Interfacing the :py:func:`colorspace.specplot.specplot` function.
        Plotting the spectrum of the current color palette.

        Args:
            n (int): Number of colors, defaults to 180.
            *args: Forwarded to :py:func:`colorspace.specplot.specplot`.
            **kwargs: Forwarded to :py:func:`colorspace.specplot.specplot`.

        Return:
            Returns what :py:func:`colorspace.specplot.specplot` returns.

        Example:

            >>> # Default diverging HCL palette
            >>> from colorspace import diverging_hcl
            >>> pal = diverging_hcl()
            >>> pal.specplot()
            >>> #:
            >>> pal.specplot(rgb = True)
            >>>
            >>> #: Default sequential HCL palette
            >>> from colorspace import sequential_hcl
            >>> pal = sequential_hcl()
            >>> pal.specplot(figsize = (8, 4))
            >>>
            >>> #: Default qualitative HCL palette
            >>> from colorspace import qualitative_hcl
            >>> pal = qualitative_hcl()
            >>> pal.specplot(figsize = (8, 4), hcl = False, rgb = True)
        """

        from .specplot import specplot
        return specplot(self.colors(n), *args, **kwargs)

    def swatchplot(self, n = 7, **kwargs):
        """Palette Swatch Plot

        Interfacing the main :py:func:`swatchplot <colorspace.swatchplot.swatchplot>`
        function. Plotting the spectrum of the current color palette.

        Args:
            n (int): Number of colors, defaults to 7.
            **kwargs: forwarded to :py:func:`swatchplot <colorspace.swatchplot.swatchplot>`.

        Return:
            Returns what :py:func:`colorspace.swatchplot.swatchplot` returns.

        Example:

            >>> # Exemplarily for diverging_hcl, works for
            >>> # all other HCL palettes as well.
            >>> from colorspace import diverging_hcl
            >>> pal = diverging_hcl()
            >>> pal.swatchplot(figsize = (8, 2))
            >>> #: Handing over a series of additional arguments
            >>> # forwarded to swatchplot()
            >>> pal.swatchplot(n = 21, figsize = (8, 2),
            >>>                show_names = False, cvd = "deutan")
            >>> #:
            >>> pal.swatchplot(n = 21, figsize = (8, 2),
            >>>                show_names = False,
            >>>                cvd = ["protan", "deutan", "tritan", "desaturate"])
        """

        from .swatchplot import swatchplot
        return swatchplot(self.colors(n), **kwargs)


    def hclplot(self, n = 7, **kwargs):
        """Palette Plot in HCL Space

        Internally calls :py:func:`hclplot <colorspace.hclplot.hclplot>`,
        additional arguments to this main function can be forwarded via the
        `**kwargs` argument.

        Args:
            n (int): Number of colors, defaults to 7.
            **kwargs: Additional named arguments forwarded to
                :py:func:`hclplot <colorspace.hclplot.hclplot>`.

        Return:
            Returns what :py:func:`colorspace.hclplot.hclplot` returns.

        Example:

            >>> from colorspace import diverging_hcl
            >>> pal = diverging_hcl()
            >>> pal.hclplot()
            >>> pal.hclplot(n = 11)
        """

        from .hclplot import hclplot
        return hclplot(x = self.colors(n), **kwargs)

    def name(self):
        """Get Palette Name

        Get name (generic) of color palette.

        Returns:
            str: Returns the name of the palette.

        Examples:
            >>> from colorspace import *
            >>> pal1 = diverging_hcl()
            >>> pal1.name()
            >>> #:
            >>> pal2 = sequential_hcl("ag_Sunset")
            >>> pal2.name()
            >>> #:
            >>> pal3 = heat_hcl()
            >>> pal3.name()
            >>> #:
            >>> pal4 = sequential_hcl("Rocket")
            >>> pal4.name()
        """
        return self._name

    def get(self, key):
        """Get Specific Palette Setting

        Returns one specific item of the palette settings,
        e.g., the current value for `h1` or `l2`.
        If not existing a `None` will be returned.

        Args:
            key (str): Name of the setting to be returned.

        Returns:
            None if `key` does ont exist, else the current value will be
            returned.

        Example:

            >>> # Exemplarily for rainbow_hcl (works for the
            >>> # other HCL palettes as well)
            >>> from colorspace import rainbow_hcl
            >>> a = rainbow_hcl()
            >>> a.get("h1")
            >>> #:
            >>> a.get("c1")
            >>> #:
            >>> a.get("l1")
            >>> #:
            >>> a.get("not_defined")
        """
        if not key in self.settings.keys():
            return None
        return self.settings[key]

    def show_settings(self):
        """Show Palette Settings

        Shows the current settings (table like print to stdout). Should more be
        seen as a development method than a very useful thing.

        Example:

            >>> from colorspace.palettes import rainbow_hcl
            >>> a = rainbow_hcl(10)
            >>> a.show_settings()
        """

        def get(key):
            val = self.get(key)
            if val is None:
                return f"{key:7s}      ---"
            elif callable(val):
                return f"{key:7s} <lambda>"
            elif isinstance(val, bool):
                return f"{key:7s} {str(val):>8s}"
            elif isinstance(val, int):
                return f"{key:7s} {val:8d}"
            else:
                return f"{key:7s} {val:8.1f}"

        from .palettes import divergingx_hcl

        if not isinstance(self, divergingx_hcl):
            keys = ["h1", "h2", "c1", "cmax", "c2", "l1", "l2", "p1", "p2", "fixup"]
        else:
            keys = ["h1", "h2", "h3", "c1", "cmax1", "c2", "cmax2", "c3",
                    "l1", "l2", "l3", "p1", "p2", "p3", "p4", "fixup"]

        print(f"Class:  {self.__class__.__name__}")
        for k in keys: print(get(k))


    # Better input handling
    def _checkinput_(self, dtype, length_min = None, length_max = None,
            recycle = False, nansallowed = False, **kwargs):
        """Used to check/convert/extend input arguments to the palette functions.

        Args:
            dtype (object): E.g. int or float, the type in which the inputs
                should be converted.
            length_min (None, int): Optional. Minimum length of the input data.
                If not fulfilled and `recycle` is set to True it expands the
                input to `length_min`. Defaults to None, see also `length_max`.
            lenth_max (None, int): Optional. Maximum length of the input data.
                If longer, the script will stop. If not set (default is `None`)
                only the `length_min` will be checked.
            recycle (bool): if set to `True` the user inputs will be recycled
                to match the expected number of inputs, defaults to False.
            nansallowed (bool): if False an error will be raised if the final
                arguments contain `numpy.nan` values. Else `numpy.nan`s are
                passed trough and will be returned, defaults to False.
            **kwargs: List of named arguments, the ones to be checked. If only
                one is given the function returns the values of this specific
                input. If multiple arguments are handed over a dict will be
                returned with the names corresponding to the user input.

        Returns:
            If `kwargs` is of length one the values of this specific variable
            will be returned. If multiple `kwargs` arguments are set a dict is
            returned.  Note that `None` will simply stay `None`.  The function
            raises errors if the user inputs do not match the required
            specifications.
        """

        # Support function
        def fun(key, value, dtype, length_min, length_max, recycle, nansallowed):

            from numpy import vstack, ndarray, asarray, isnan, nan, any, atleast_1d

            if not nansallowed and any(isnan(value)):
                raise ValueError(f"nan's not allowed in `{key}`")
            elif isinstance(value, ndarray) and len(value) < length_min:
                raise ValueError(f"argument `{key}` too short (< {length_min})")

            # If None
            if value == None: return value

            # Converting the data
            try:
                value = asarray([value], dtype = dtype).flatten()
            except Exception as e:
                raise ValueError(f"incorrect input on argument `{key}`: {str(e)}")

            # Vector of length 0?
            if len(value) == 0:
                raise ValueError(f"argument `{key}` of length 0")

            # Not enough input values, check if we are allowed to
            # recycle.
            if length_min and len(value) < length_min:
                # Input was too short: check if we are allowed to
                # recycle the value or not.
                if not recycle:
                    raise ValueError(f"wrong length of input \"{key}\", expected min {length_min} elements, " + \
                                     f"got {len(value)} when calling {self.__class__.__name__}")
                else:
                    value = vstack([value] * length_min).flatten()[0:length_min]
            elif length_min and not length_max and len(value) > length_min:
                value = value[0:length_min]

            # Check if the input exceeds length_max if set
            if length_max and len(value) > length_max:
                raise ValueError(f"wrong length of input \"{key}\", expected max {length_max} elements, " + \
                                 f"got {len(value)} when calling {self.__class__.__name__}")
            # Cropping data if too much elements are given.
            elif length_max and len(value) > length_max:
                value = value[0:length_max]

            # Checking nan's
            if not nansallowed and any(isnan(value)):
                raise ValueError(f"arguments for \"{key}\" to function calling {self.__class__.__name__}" + \
                                 "contain nan values: not allowed")

            # Return single value if length is set to 1.
            if len(value) == 1: value = value[0]

            return atleast_1d(value) # Return 1d array

        # Looping over all kwargs
        for key,value in kwargs.items():
            if value is None: raise ValueError(f"argument `{key}` cannot be None")
            kwargs[key] = fun(key, value, dtype, length_min, length_max, recycle, nansallowed)

        # If only one kwarg was given: return values, else return dict.
        if len(kwargs) == 1:
            return kwargs[list(kwargs.keys())[0]]
        else:
            return kwargs


    # Return matplotlib.colors.LinearSegmentedColormap
    def cmap(self, n = 256, name = "custom_hcl_cmap"):
        """Create Matplotlib Compatible Color Map

        Allows to retrieve a matplotlib LinearSegmentedColormap color map.
        Clasically LinearSegmentedColormaps allow to retrieve a set of `N`
        colors from a set of `n` colors where `N >> n`. The matplotlib
        simply linearely interpolates between all `n` colors to extend
        the number of colors to `N`.

        In case of `hclpalette` objects this is not necessary as
        `hclpalette` objects allow to retrieve `N` colors directly
        along well-specified Hue-Chroma-Luminance paths. Thus, this method
        returns a matplotlib color map with `n = N` colors. The linear 
        interpolation between the colors (as typically done by
        LinearSegmentedColormap) is not necessary. However, for convenience
        cmaps have been implemented such that you can easily use hcl based
        palettes in your existing workflow.

        Args:
            n (int): Number of colors the cmap should be based on; default is `n = 256`
            name (str): Name of the custom color map. Default is `custom_hcl_cmap`

        Example:

            >>> # Create LinearSegmentedColormap from diverging_hcl() palette.
            >>> # By default, 256 distinct colors are used across the palette.
            >>> from colorspace import diverging_hcl, specplot
            >>> pal = diverging_hcl()
            >>> cmap1 = pal.cmap()
            >>> cmap1.N
            >>>
            >>> #: Same as above, but only using 5 distinct colors.
            >>> cmap2 = pal.cmap(n = 5)
            >>> cmap2.N
            >>>
            >>> #: Plotting HCL and sRGB spectrum for both cmaps
            >>> specplot(cmap1, rgb = True, figsize = (8, 6));
            >>> #:
            >>> specplot(cmap2, rgb = True, figsize = (8, 6));

        Returns:
            Returns a `LinearSegmentedColormap` (cmap) to be used
            with the matplotlib library.

        Raises:
            TypeError: If `n` is not int
            ValueError: If `n` is lower than 2
        """
        import matplotlib
        from matplotlib.colors import LinearSegmentedColormap
        from numpy import linspace, round, fmin, fmax

        if not isinstance(n, int):
            raise TypeError("argument `n` must be int")
        elif n < 2:
            raise ValueError("argument `n` must be >= 2")

        cols = self.colors(n)
        return LinearSegmentedColormap.from_list(name, cols, n)


    def _set_rev(self, rev):
        """Helper function: Store 'rev' argument

        Args:
            rev (bool): Should the palette be reversed?

        Raises:
            TypeError: If argument `rev` is not bool.
        """
        if not isinstance(rev, bool):
            raise TypeError("argument `rev` must e bool")
        self._rev = rev # Just store it

    def _get_alpha_array(self, alpha, n):
        """Get numpy.ndarray for alpha values

        The .color() method allowes to specify an additonal alpha
        channel, a value between 0. (fully opaque) to 1. (fully transparent)
        which can be provided in different ways.

        Args:
            alpha (None, float, list, or numpy.ndarray): Can be `None`
                (default), a single float, a list, or a numpy array. If a list or
                array is provided it must be of length 1 or of length `n` and be
                convertible to float, providing values between `0.0` (full opacity)
                and `1.0` (full transparency)
            n (int): Number of colors (must be > 0).
        Raises:
            TypeError: If `n` is not int.
            ValueError: If `n` is not > 0.
            TypeError: If `alpha` is not among the allowed types.
            ValueError: If `alpha` is a numpy.array of length > 1 but not of length n.

        Return:
        None, numpy.ndarray: Returns None (if input alpha is None) or a numpy
        numeric numpy array of length 'n'.
        """
        import numpy as np

        if not isinstance(n, int):
            raise TypeError("argument `n` must be int")
        elif n <= 0:
            raise ValueError("argument `n` (int) must larger than 0")

        # checking alpha
        if not isinstance(alpha, (type(None), float, list, np.ndarray)):
            raise TypeError("argument `alpha` not among the allowed types")
        elif isinstance(alpha, (list, np.ndarray)) and len(alpha) == 0:
            raise ValueError("argument `alpha` is of length 0 (not allowed)")

        # If alpha is None, we can return immediately
        if alpha is None: return None

        # If alpha is a numpy array of length > 0, but not equal to n, error.
        if isinstance(alpha, np.ndarray) and len(alpha) > 1 and not len(alpha) == n:
            raise ValueError("if `alpha` is a numpy array, it must be of the same length as `n`")
        elif isinstance(alpha, list) and not len(alpha) == n:
            raise ValueError("if `alpha` is a list, it must be of the same length as `n`")
        elif isinstance(alpha, float):
            alpha = np.repeat(alpha, n)
        elif len(alpha) == 1:
            try:
                alpha = np.repeat(alpha[0], n)
                alpha = alpha.dtype("float")
            except Exception as e:
                raise Exception(f"problems converting alpha: {e}")
        else:
            try:
                alpha = np.asarray(alpha, dtype = "float")
            except Exception as e:
                raise Exception(f"problems converting alpha: {e}")

        # Now we know we have a float array
        if np.any(alpha < 0) or np.any(alpha > 1):
            raise ValueError("values `alpha` must be in the range of [0.0, 1.0]")

        # Returning numpy.ndarray
        return alpha

    def _chroma_trajectory(self, i, p1, c1, c2, cmax):
        """Helper function: Calculate linear or triangle trajectory for chroma dimension.

        Args:
            i (numpy array; float): Position across the palette, a sequence
                of values between 1 and 0. For diverging palettes this function
                is called twice, once for 1 to 0.5, and once for <0.5 t0 0.
            p1 (float): Power parameter p1.
            c1 (float): Chroma value of the left end of the color palette.
            c2 (float): Chroma value of the right end of the color palette.
            cmax (float, None, np.nan): Max choma value.

        Returns:
            numpy array: Linear trajectory for the chroma color dimension.
        """
        from numpy import isnan

        def _linear_trajectory(i, c1, c2):
            return c2 - (c2 - c1) * i

        def _triangle_trajectory(i, j, c1, c2, cmax):
            from numpy import where, abs, linspace
            res = where(i <= j,
                        c2 - (c2 - cmax) * i / j,
                        cmax - (cmax - c1) * abs((i - j) / (1 - j)))
            #print(res)
            return res

        if cmax is None or isnan(cmax):
            C = _linear_trajectory(i**p1, c1, c2)
        else:
            # Calculate the position of the triangle point
            j = 1. / (1. + abs(cmax - c1) / abs(cmax - c2))
            if not j is None and (j <= 0. or j >= 1.): j = None

            if j is None:  C = _linear_trajectory(i**p1, c1, c2)
            else:          C = _triangle_trajectory(i**p1, j, c1, c2, cmax)

        return C


    def _get_seqhcl(self, i, ha, hb, ca, cb, la, lb, pa, pb, cmax):
        """Get Sequential Palette Colors

        Get 'one side' of a sequential palette. This is also used
        by `divergingx_hcl` which is, per construction, nothing else
        than a combination of two flexible sequential palettes meeting
        in the center.

        Args:
            i (numpy.ndarray): Sequence of floats in `[0, 1]` where to draw the
                values from. Typically `linspace(1, 0, n)`, but for some palettes
                (diverging palettes with an even number of colors) they do not meet at 0.
            ha (float): Hue on end "A".
            hb (float): Hue on end "B".
            ca (float): Chroma on end "A".
            cb (float): Chroma on end "B".
            la (float): Luminance on end "A".
            lb (float): Luminance on end "B".
            pa (loat): Power parameter 1.
            pb (loat): Power parameter 2.
            cmax (float, None, np.nan): Max chroma.

        Return:
            list: List of `H`, `C`, and `L` coordinates.
        """
        from numpy import power

        # Hue and Luminance
        H = hb - (hb - ha) * i
        L = lb - (lb - la) * power(i, pb)

        # Calculate the trajectory for the chroma dimension
        C = self._chroma_trajectory(i, pa, ca, cb, cmax)

        return [H, C, L]


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class qualitative_hcl(hclpalette):
    """Qualitative HCL Color Palettes

    The HCL (hue-chroma-luminance) color model is a perceptual color model
    obtained by using polar coordinates in CIELUV space
    (i.e., :py:class:`polarLUV <colorspace.colorlib.polarLUV>`),
    where steps of equal size correspond to approximately equal perceptual
    changes in color. By taking polar coordinates the resulting three
    dimensions capture the three perceptual axes very well: hue is the type of
    color, chroma the colorfulness compared to the corresponding gray, and
    luminance the brightness. This makes it relatively easy to create balanced
    palettes through trajectories in this HCL space. In contrast, in the more
    commonly-used ‘HSV’ (hue-saturation-value) model (a simple transformation
    of ‘RGB’), the three axes are confounded so that luminance changes along
    with the hue leading to very unbalanced palettes.

    `qualitative_hcl` distinguishes the underlying categories by a
    sequence of hues while keeping both chroma and luminance constant to give
    each color in the resulting palette the same perceptual weight. Thus, `h`
    should be a pair of hues (or equivalently `h1` and `h2` can be used) with
    the starting and ending hue of the palette. Then, an equidistant sequence
    between these hues is employed, by default spanning the full color wheel
    (i.e, the full 360 degrees). Chroma `c` (or equivalently `c1`) and
    luminance `l` (or equivalently `l1`) are constants. If `h` is str it will
    overwrite the `palette` argument. In this case, pre-specified palette
    settings will be loaded but are allowed to be overwritten by the user. At
    any time the user can overwrite any of the settings. If `h` is str it will
    overwrite the `palette` argument. In this case, pre-specified palette
    settings will be loaded but are allowed to be overwritten by the user. At
    any time the user can overwrite any of the settings.

    By default, `qualitative_hcl` returns an object of class `hclpalette` which
    allows to draw a number of colors (`n`) uniformly distributed around the
    circle (`[0, 360 * (n - 1) / n]`) controlled via the `h` (Hue) argument. As
    the number of colors is not yet defined, the upper hue limit (`h[1]`, `h2`)
    is defined via lambda function.

    See also: :py:class:`sequential_hcl`, :py:class:`diverging_hcl`,
    :py:class:`divergingx_hcl`, :py:class:`rainbow_hcl`, :py:class:`heat_hcl`,
    :py:class:`terrain_hcl`, :py:class:`diverging_hsv`, and
    :py:class:`rainbow`.

    Args:
        h (list, str): Hue values defining the 'color' or name of pre-defined
            palette (`str`) or a list of two numeric values (float/int) defining
            the hue on the two ends of the palette. If str, it acts as the
            input argument `palette`.
            Elements in list can also be lambda functions with one single input
            argument `n` (number of colors; see default value).
        c (int, float): Chroma value (colorfullness), a single numeric value.
        l (int, float): luminance value (lightness), a single numeric value.
        fixup (bool): Only used when converting the HCL colors to hex.  Should RGB
            values outside the defined RGB color space be corrected?
        palette (None, str): Can be used to load a default diverging color
            qpalette specification. If the palette does not exist an exception will be
            raised.  Else the settings of the palette as defined will be used to create
            qthe color palette.
        rev (bool): Should the color map be reversed? Default `False`.
        **kwargs: Additional named arguments to overwrite the palette settings.
            Allowed: `h1`, `h2`, `c1`, `l1`.

    Returns:
        qualitative_hcl: Initialize new object. Raises exceptions if the parameters are
        misspecified. Note that the object is callable, the default object call can
        be used to return hex colors (identical to the `.colors()` method), see
        examples.

    Example:

        >>> from colorspace import qualitative_hcl
        >>> a = qualitative_hcl()
        >>> a.colors(10)
        >>> #:
        >>> b = qualitative_hcl("Warm")
        >>> b.colors(10)
        >>> #:
        >>> b.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>> #: The standard call of the object also returns hex colors
        >>> qualitative_hcl("Warm")(10)
        >>>
        >>> #: Example where `h` is a list of two lambda functions
        >>> from colorspace import hexcols
        >>> pal = qualitative_hcl([lambda n: 100. * (n - 1) / n,  
        >>>                        lambda n, h1: 300. * (n - 1) / n + h1], c = 30)
        >>> cols = hexcols(pal.colors(5))
        >>> cols
        >>> #:
        >>> cols.to("HCL")
        >>> cols


    Raises:
        TypeError: If `h` is neither str nor list of length 2.
        TypeError: If `h` is list of length 2, the elements must be int, float, or
            lambda functions.
        ValueError: If `c` and/or `l` contain unexpected values.
        ValueError: If `h` is str or `palette` is set, but a pre-defined palette
            with this name does not exist.
    """

    _allowed_parameters = ["h1", "h2", "c1", "l1"]
    _name = "Qualitative"

    def __init__(self, h = [0, lambda n: 360. * (n - 1.) / n], c = 80, l = 60,
        fixup = True, palette = None, rev = False, **kwargs):

        self._set_rev(rev)
        if not isinstance(fixup, bool): raise TypeError("argument `fixup` must be bool")
        if not isinstance(palette, (str, type(None))):
            raise TypeError("argument `palette` must be None or str")

        # If a str is given on "h": exchange with "palette".
        if isinstance(h, str):
            palette = h
            h       = [0, lambda n: 360. * (n - 1.) / n] # Temporary override
        # Else it must be list of length 2
        elif not isinstance(h, list) or not len(h) == 2:
            raise ValueError("argument `h` must be str or list of length 2")
        # Check list elements for allowed types
        else:
            for rec in h:
                if   callable(rec):                 pass
                elif isinstance(rec, (float, int)): pass
                else:
                    raise TypeError("unexpected type in list on argument `h`")

        # _checkinput_ parameters (in the correct order):
        # - dtype, length_min, length_max, recycle, nansallowed, **kwargs
        try:
            c = self._checkinput_(int, 1, 1, False, c = c)
            l = self._checkinput_(int, 1, 1, False, l = l)
        except Exception as e:
            raise ValueError(str(e))

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            from numpy import where
            pals = hclpalettes().get_palettes("Qualitative")
            idx  = where([x.name().upper().replace(" ", "") == palette.upper().replace(" ", "") for x in pals])[0]
            if len(idx) == 0:
                raise ValueError(f"palette {palette} is not a valid qualitative palette. " + \
                                 f"Choose one of: {', '.join([x.name() for x in pals])}")
            pal = pals[idx[0]]

            # Allow to overrule few things
            for key,value in kwargs.items():
                if key in self._allowed_parameters: pal.set(**{key: value}, lambda_allowed = True)

            # Extending h2 if h1 = h2 (h2 None)
            if pal.get("h2") == None or pal.get("h1") == pal.get("h2"):
                pal.set(h2 = pal.get("h1") + 360)
                if pal.get("h2") > 360:
                    pal.set(h1 = pal.get("h1") - 360)
                    pal.set(h2 = pal.get("h2") - 360)

            # Getting settings
            settings = pal.get_settings()
        else:
            # User settings
            settings = {}
            settings["h1"]    = h[0]
            settings["h2"]    = h[1]
            settings["c1"]    = c[0] # qualitative palette, constant
            settings["l1"]    = l[0] # qualitative palette, constant
            settings["fixup"] = fixup
            settings["rev"]   = rev

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in ["h1", "h2", "c1", "l1"]: settings[key] = value

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if not key in self._allowed_parameters + ["desc", "gui"]:
                    raise ValueError(f"argument `{key}` not allowed for {type(self).__name__}")
                settings[key] = val

        # Save settings
        self.settings = settings


    def colors(self, n = 11, fixup = None, alpha = None, **kwargs):
        """Get Colors

        Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned, defaults to 11.
            fixup (None, bool): should sRGB colors be corrected if they lie outside
                the defined color space?  If `None` the `fixup` parameter from the
                object will be used. Can be set to `True` or `False` to explicitly
                control the fixup here.
            alpha (None, float, list, or numpy.ndarray): Allows to add an transparency
                (alpha channel) to the colors. Can be a single float, a list, or a
                numpy array. If a list or array is provided it must be of length 1 or
                of length `n` and be convertible to float, providing values
                between `0.0` (full opacity) and `1.0` (full transparency)
            **kwargs: Currently allows for `rev = True` to reverse the colors.

        Returns:
            list: Returns a list of str with `n` colors from the
            color palette.

        Examples:
            >>> from colorspace import qualitative_hcl, rainbow_hcl
            >>> qualitative_hcl("Dark 3").colors()
            >>> #: Five colors with constant alpha of 0.3
            >>> qualitative_hcl().colors(5, alpha = 0.3)
            >>> #: Three colors with variying alpha
            >>> qualitative_hcl().colors(3, alpha = [0.2, 0.8, 0.3])
            >>>
            >>> #: Same for rainbow_hcl which is a special
            >>> # version of the qualitative HCL color palette
            >>> rainbow_hcl().colors(4)

        """

        from numpy import repeat, linspace, asarray
        from numpy import vstack, transpose
        from .colorlib import HCL

        alpha = self._get_alpha_array(alpha, n)
        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        # If either h1 or h2 is a lambda function: evaluate now.
        h1 = self.get("h1")(n) if callable(self.get("h1")) else self.get("h1")
        if callable(self.get("h2")):
            fn = self.get("h2")
            # Distinguish between lambda functions with one argument (n) or two (n + h1)
            h1 = self.get("h1")(n) if callable(self.get("h1")) else self.get("h1")
            h2 = fn(n) if fn.__code__.co_argcount == 1 else fn(n, h1)
        else:
            h2 = self.get("h2")

        # Calculate the coordinates for our HCL color(s)
        L = repeat(self.get("l1"), n)
        C = repeat(self.get("c1"), n)
        H = linspace(h1, h2, n)

        # Create new HCL color object
        HCL = HCL(H, C, L, alpha)

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return HCL.colors(fixup = fixup, rev = rev)


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class rainbow_hcl(qualitative_hcl):
    """HCL Based Rainbow Palette

    `rainbow_hcl` computes a rainbow of colors via :py:class:`qualitative_hcl`
    defined by different hues given a single value of each chroma and
    luminance. It corresponds to `rainbow` which computes a rainbow in
    HSV space.

    See also: :py:class:`qualitative_hcl`, :py:class:`sequential_hcl`,
    :py:class:`diverging_hcl`, :py:class:`divergingx_hcl`,
    :py:class:`heat_hcl`, :py:class:`terrain_hcl`, :py:class:`diverging_hsv`,
    and :py:class:`rainbow`.

    Args:
        c (float, int): Chroma (colorfullness) of the color map `[0-100+]`.
        l (float, int): Luminance (lightness) of the color map `[0-100]`.
        start (float, int, lambda): Hue at which the rainbow should start or lambda function
            with one argument. Defaults to 0.
        end (float, int, lambda): Hue (int) at which the rainbow should end or lambda function
            with one argument. By default a lambda function evaluated when
            drawing colors (`360 * (n - 1) / n`).
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        rev (bool): Should the color map be reversed? Default `False`.
        *args: Currently unused.
        **kwargs: Additional named arguments to overwrite the palette settings.
            Allowed: `h1`, `h2`, `c1`, `l1`, `l2`, `p1`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the `.colors()` method),
        see examples.

    Example:

        >>> from colorspace import rainbow_hcl
        >>> pal = rainbow_hcl()
        >>> pal.colors(10)
        >>> #:
        >>> pal.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>> #: The standard call of the object also returns hex colors. Thus,
        >>> # you can make your code slimmer by calling
        >>> rainbow_hcl()(10)
        >>>
        >>> #: Testing lambda function for both, start and end
        >>> pal = rainbow_hcl(start = lambda n: (n - 1) / n,
        >>>                   end   = lambda n: 360 - (n - 1) / n)
        >>> pal.swatchplot(n = 5, show_names = False, figsize = (5.5, 0.5))
        >>> #:
        >>> pal.swatchplot(n = 10, show_names = False, figsize = (5.5, 0.5))
    """

    _allowed_parameters = ["h1", "h2", "c1", "l1"]
    _name = "Rainbow HCL"

    def __init__(self, c = 50, l = 70, start = 0, end = lambda n: 360 * (n - 1) / n,
                 fixup = True, rev = False, *args, **kwargs):

        self._set_rev(rev)
        if not isinstance(fixup, bool): raise TypeError("argument `fixup` must be bool")

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            c     = self._checkinput_(int,   1, 1, False, c = c)
            l     = self._checkinput_(int,   1, 1, False, l = l)
        except Exception as e:
            raise ValueError(str(e))

        # Checking start and end. If int, use _checkinput_, if callable make
        # sure it is a lambda function with one single input argument.
        if isinstance(start, (float, int)):
            start = self._checkinput_(int,   1, False, False, start = start)
        elif callable(start):
            if not start.__code__.co_argcount == 1:
                raise Exception("if `start` is a lambda function it must have only one argument")
        else:
            raise TypeError("argument `start` must be int or lambda function")

        if isinstance(end, int):
            end   = self._checkinput_(int,   1, False, False, end = end)
        elif callable(end):
            if not end.__code__.co_argcount == 1:
                raise Exception("if `end` is a lambda function it must have only one argument")
        else:
            raise TypeError("argument `end` must be int or lambda function")

        # Save settins
        self.settings = {"h1": start if callable(start) else int(start[0]),
                         "h2": end if callable(end) else int(end[0]),
                         "c1": int(c[0]),
                         "l1": int(l[0]),
                         "fixup": bool(fixup)}

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if not key in self._allowed_parameters + ["desc", "gui"]:
                    raise ValueError(f"argument `{key}` not allowed for {type(self).__name__}")
                self.settings[key] = val

        self.settings["rev"] = self._rev

# -------------------------------------------------------------------
# -------------------------------------------------------------------
class diverging_hcl(hclpalette):
    """Diverging HCL Color Palettes

    The HCL (hue-chroma-luminance) color model is a perceptual color model
    obtained by using polar coordinates in CIELUV space
    (i.e., :py:class:`polarLUV <colorspace.colorlib.polarLUV>`),
    where steps of equal size correspond to approximately equal perceptual
    changes in color. By taking polar coordinates the resulting three
    dimensions capture the three perceptual axes very well: hue is the type of
    color, chroma the colorfulness compared to the corresponding gray, and
    luminance the brightness. This makes it relatively easy to create balanced
    palettes through trajectories in this HCL space. In contrast, in the more
    commonly-used ‘HSV’ (hue-saturation-value) model (a simple transformation
    of ‘RGB’), the three axes are confounded so that luminance changes along
    with the hue leading to very unbalanced palettes.

    `diverging_hcl` codes the underlying numeric values by a
    triangular luminance sequence with different hues in the left and
    in the right arm of the palette. Thus, it can be seen as a
    combination of two sequential palettes with some restrictions: (a)
    a single hue is used for each arm of the palette, (b) chroma and
    luminance trajectory are balanced between the two arms, (c) the
    neutral central value has zero chroma. To specify such a palette a
    vector of two hues `h` (or equivalently `h1` and `h2`), either a
    single chroma value `c` (or `c1`) or a vector of two chroma values
    `c` (or `c1` and `cmax`), a vector of two luminances `l` (or `l1`
    and `l2`), and power parameter(s) `power` (or `p1` and `p2`) are
    used. For more flexible diverging palettes without the
    restrictrictions above (and consequently more parameters)
    `divergingx_hcl` is available. For backward compatibility,
    `diverge_hcl` is a copy of `diverging_hcl`.

    If `h` is str it will overwrite the `palette` argument. In this case,
    pre-specified palette settings will be loaded but are allowed to be
    overwritten by the user. At any time the user can overwrite any of the
    settings. By default, `diverging_hcl` returns an object of class
    `hclpalette` identical to the pre-defined `"Blue-Red"` palette.

    See also: :py:class:`qualitative_hcl`, :py:class:`sequential_hcl`,
    :py:class:`divergingx_hcl`, :py:class:`rainbow_hcl`, :py:class:`heat_hcl`,
    :py:class:`terrain_hcl`, :py:class:`diverging_hsv`, and
    :py:class:`rainbow`.

    Args:
        h (list, float, int): Hue values (color), diverging color palettes should
            have different hues for both ends of the palette. If only one value is
            present it will be recycled ending up in a diverging color palette with the
            same colors on both ends.  If more than two values are provided the first
            two will be used while the rest is ignored.  If input `h` is a str
            this argument acts like the `palette` argument (see `palette` input
            parameter).
        c (float, int, list): Chroma value (colorfullness), a single numeric value. If two
            values are provided the first will be taken as `c1`, the second as `cmax`.
        l (float, int, list): luminance values (lightness). The first value is for
            the two ends of the color palette, the second one for the neutral center
            point. If only one value is given this value will be recycled.
        power (float, int, list): Power parameter for non-linear behaviour of the color
            palette.
        fixup (bool): Only used when converting the HCL colors to hex.  Should RGB
            values outside the defined RGB color space be corrected?
        palette (str): Can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be raised.
            Else the settings of the palette as defined will be used to create the
            color palette.
        rev (bool): Should the color map be reversed.
        *args: Currently unused.
        **kwargs: Additional named arguments to overwrite the palette settings.
            Allowed: `h1`, `h2`, `c1`, `cmax`, `l1`, `l2`, `p1`, `p2`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the `.colors()` method),
        see examples.

    Example:

        >>> from colorspace import diverging_hcl
        >>> a = diverging_hcl()
        >>> a.colors(10)
        >>> #: Different color palette by name
        >>> b = diverging_hcl("Tropic")
        >>> b.colors(10)
        >>> #:
        >>> b.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>> #: The standard call of the object also returns hex colors
        >>> diverging_hcl("Tropic")(10)
    """

    _allowed_parameters = ["h1", "h2", "c1", "cmax", "l1", "l2", "p1", "p2"]
    _name = "Diverging HCL"

    def __init__(self, h = [260, 0], c = 80, l = [30, 90],
        power = 1.5, fixup = True, palette = None, rev = False,
        *args, **kwargs):

        self._set_rev(rev)
        if not isinstance(fixup, bool): raise TypeError("argument `fixup` must be bool")
        if not isinstance(palette, (str, type(None))):
            raise TypeError("argument `palette` must be None or str")

        if isinstance(h, str):
            palette = h
            h       = -999 # Temporarliy setting to dummy value
        if isinstance(power, int) or isinstance(power, float):
            power   = [power]

        # _checkinput_ parameters (in the correct order):
        # - dtype, length_min, length_max, recycle, nansallowed, **kwargs
        try:
            h     = self._checkinput_(int,   2, 2, True,  False, h = h)
            c     = self._checkinput_(int,   1, 2, False, False, c = c)
            l     = self._checkinput_(int,   2, 2, True,  False, l = l)
            power = self._checkinput_(float, 1, 2, True,  False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            from numpy import where
            pals = hclpalettes().get_palettes("Diverging")
            idx  = where([x.name().upper().replace(" ", "") == \
                    palette.upper().replace(" ", "") for x in pals])[0]
            if len(idx) == 0:
                raise ValueError(f"palette {palette} is not a valid diverging palette. " + \
                                 f"Choose one of: {', '.join([x.name() for x in pals])}")
            pal = pals[idx[0]]

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in self._allowed_parameters: pal.set(**{key: value})

            # Extending h2 if h1 == h2 or h2 is None
            if pal.get("h2") == None or pal.get("h1") == pal.get("h2"):
                pal.set(h2 = pal.get("h1") + 360)
                if pal.get("h2") > 360:
                    pal.set(h1 = pal.get("h1") - 360)
                    pal.set(h2 = pal.get("h2") - 360)

            # Getting settings
            settings = pal.get_settings()
        else:
            settings = {}

            from numpy import ndarray

            # User settings
            settings["h1"]    = h[0]
            settings["h2"]    = h[1]
            settings["c1"]    = float(c[0])
            if len(c) == 2:
                settings["cmax"] = float(c[1])
            settings["l1"]    = l[0]
            settings["l2"]    = l[1]
            settings["p1"]    = float(power[0])
            if len(power) == 2:
                settings["p2"] = float(power[1])
            settings["fixup"] = fixup
            settings["rev"]   = rev

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if not key in self._allowed_parameters + ["desc", "gui"]:
                    raise ValueError(f"argument `{key}` not allowed for {type(self).__name__}")
                settings[key] = val

        # Save settings
        self.settings = settings


    # Return hex colors
    def colors(self, n = 11, fixup = None, alpha = None, **kwargs):
        """Get Colors

        Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned.
            fixup (None, bool): Should sRGB colors be corrected if they lie
                outside the defined color space?  If `None` the `fixup`
                parameter from the object will be used. Can be set to `True` or
                `False` to explicitly control the fixup here.
            alpha (None, float, list, or numpy.ndarray): Allows to add an transparency
                (alpha channel) to the colors. Can be a single float, a list, or a
                numpy array. If a list or array is provided it must be of length 1 or
                of length `n` and be convertible to float, providing values
                between `0.0` (full opacity) and `1.0` (full transparency)
            **kwargs: Currently allows for `rev = True` to reverse the colors.

        Returns:
            list: Returns a list of str with `n` colors from the
            color palette.


        Examples:
            >>> from colorspace import diverging_hcl, hexcols
            >>> diverging_hcl().colors()
            >>> #: Different diverging palette
            >>> cols = diverging_hcl("Green-Orange").colors(5)
            >>> cols
            >>> #:
            >>> hexcols(cols)
            >>> #: Five colors with constant alpha of 0.3
            >>> diverging_hcl().colors(5, alpha = 0.3)
            >>> #: Three colors with variying alpha
            >>> diverging_hcl().colors(3, alpha = [0.2, 0.8, 0.3])

        """

        from numpy import abs, ceil, linspace, power, repeat, arange, fmax, delete
        from numpy import asarray, ndarray, ndenumerate, concatenate, flip
        from numpy import vstack, transpose, repeat
        from .colorlib import HCL

        alpha = self._get_alpha_array(alpha, n)
        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        # Calculate H/C/L
        p1   = self.get("p1")
        p2   = p1 if self.get("p2") is None else self.get("p2")
        c1   = self.get("c1")
        c2   = 0 if self.get("c2") is None else self.get("c2")
        cmax = None if not self.get("cmax") else self.get("cmax")
        l1   = self.get("l1")
        l2   = l1 if self.get("l2") is None else self.get("l2")
        h1   = self.get("h1")
        h2   = h1 if self.get("h2") is None else self.get("h2")

        # If n == 1 we do as we have 3 colors, but then only return the middle one
        tmp_n = n if n > 1 else 3

        # Calculate H/C/L
        rval = linspace(1., -1., tmp_n)

        L = l2 - (l2 - l1) * power(abs(rval), p2)
        H = ndarray(tmp_n, dtype = "float")
        for i,val in ndenumerate(rval): H[i] = h1 if val > 0 else h2

        # Calculate the trajectory for the chroma dimension
        i = fmax(0, arange(1., -1e-10, -2. / (tmp_n - 1.)))
        C = self._chroma_trajectory(i, p1, c1, c2, cmax)
        C = fmax(0., concatenate((C, flip(C))))

        # Non-even number of colors? We need to remove one.
        if tmp_n % 2 == 1: C = delete(C, int(ceil(tmp_n / 2.)))

        # Create new HCL color object
        HCL = HCL(H, C, L, alpha)

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        cols = HCL.colors(fixup = fixup, rev = rev)
        return [cols[1]] if n == 1 else cols




# -------------------------------------------------------------------
# -------------------------------------------------------------------
class divergingx_hcl(hclpalette):
    """Diverging X HCL Color Palettes

    More flexible version of the `diverging_hcl` class. A diverging X
    palette basically consists of two multi-hue sequential palettes.

    The `divergingx_hcl` function simply calls :py:class:`sequential_hcl` twice
    with a prespecified set of hue, chroma, and luminance parameters. This is
    similar to :py:class:`diverging_hcl` but allows for more flexibility:
    :py:class:`diverging_hcl` employs two _single-hue_ sequential palettes,
    always uses zero chroma for the neutral/central color, and restricts the
    chroma/luminance path to be the same in both "arms" of the palette. In
    contrast, `divergingx_hcl` relaxes this to two full _multi-hue_ palettes
    that can thus go through a non-gray neutral color (typically light yellow).
    Consequently, the chroma/luminance paths can be rather unbalanced between
    the two arms.

    With this additional flexibility various diverging palettes
    suggested by <https://ColorBrewer2.org/> and CARTO
    (<https://carto.com/carto-colors/>), can be emulated along with
    the Zissou 1 palette from 'wesanderson', Cividis from 'viridis',
    and Roma from 'scico'.

    * Available CARTO palettes: ArmyRose, Earth, Fall, Geyser, TealRose,
      Temps, and Tropic (available in :py:class:`diverging_hcl`).
    * Available ColorBrewer.org palettes: PuOr, RdBu, RdGy, PiYG, PRGn,
      BrBG, RdYlBu, RdYlGn, Spectral.

    If `h` is str it will overwrite the `palette` argument. In this case,
    pre-specified palette settings will be loaded but are allowed to be
    overwritten by the user. At any time the user can overwrite any of
    the settings.

    See also: :py:class:`qualitative_hcl`, :py:class:`sequential_hcl`,
    :py:class:`diverging_hcl`, :py:class:`rainbow_hcl`, :py:class:`heat_hcl`,
    :py:class:`terrain_hcl`, :py:class:`diverging_hsv`, and
    :py:class:`rainbow`.

    Args:
        h (list): Hue values (color), list of three numerics. Divergingx color
            palettes should have different hues for both ends and the center of the
            palette. For this class three values must be provided. If input `h` is
            a str this argument acts like the `palette` argument (see `palette`
            input parameter).
        c (list): Chroma value (colorfullness), list of floats. In case two
            values are provided the firt is taken as `c1` and `c3` while the second
            one is used for `c2` (center value). When three values are provided
            they are used as `c1`, `c2`, and `c3` (see also `cmax`).
        l (list): Luminance values (lightness), list of float/int. In case two
            values are provided the firt is taken as `l1` and `l3` while the second
            one is used for `l2` (center value). When three are provided
            they are used as `l1`, `l2`, and `l3` respectively.
        power (list): Power parameters for non-linear behaviour of the color
            palette, list of floats.
            If two values are provided `power[0]` will be used for `p1` and `p4`
            while `power[1]` is used for `p2` and `p3` (symmetric). A list of length
            four allows to specify `p1`, `p2`, `p3`, and `p4` individually. List
            of length three acts like a list of length two, the last element is ignored.
        cmax (None, float, int, list, numpy.ndarray): Maximum chroma for
            triangular trajectory. Unused if set `Non`. If one value is provided it
            is used for `cmax1`, if two values are provided they are used as
            `cmax1` and `cmax2`, respectively.
        fixup (bool): Only used when converting the HCL colors to hex.  Should RGB
            values outside the defined RGB color space be corrected?
        palette (str): Can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be raised.
            Else the settings of the palette as defined will be used to create the
            color palette.
        rev (bool): Should the color map be reversed.
        *args: Currently unused.
        **kwargs: Additional named arguments to overwrite the palette settings.
            Allowed: `h1`, `h2`, `h3`, `c1`, `cmax1`, `c2`, `cmax2` `c3`,
            `l1`, `l2`, `l3`, `p1`, `p2`, `p3`, `p4`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the `.colors()` method),
        see examples.

    Example:

        >>> from colorspace import divergingx_hcl
        >>> pal1 = divergingx_hcl()
        >>> pal1.colors(5)
        >>> #:
        >>> pal1.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>>
        >>> #: Different color palette by name
        >>> pal2 = divergingx_hcl("ArmyRose")
        >>> pal2.colors(7)
        >>> #:
        >>> pal2.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>>
        >>> #: The standard call of the object also returns hex colors
        >>> divergingx_hcl("Fall")(3)
        >>>
        >>> #: Manual palette with user settings. The following diverginx
        >>> # palette goes from h = 180 (left) to h = 100 (center) and h = 20 (right).
        >>> # Croma is c = 30 (left), c = 5 (center), and c = 30 (right).
        >>> # In addition, both 'arms' have a maximum chroma of cmax = 70
        >>> # in the center of each of the two arms.
        >>> pal3 = divergingx_hcl(h = [180, 100, 20], 
        >>>                       c = [30, 5, 30],
        >>>                       cmax = [70, 70]) 
        >>> pal3.specplot();
        >>> #: Drawing 5 colors from the custom palette.
        >>> pal3(3)
        >>>
        >>> #: Available default palettes (divergingx_hcl palettes)
        >>> from colorspace import divergingx_hcl, swatchplot, palette
        >>>
        >>> carto  = ["ArmyRose", "Earth", "Fall",
        >>>           "Geyser", "TealRose", "Temps"]                 
        >>> brewer = ["PuOr", "RdBu", "RdGy", "PiYG", "PRGn",
        >>>           "BrBG", "RdYlBu", "RdYlGn", "Spectral"]
        >>> others = ["Zissou 1", "Cividis", "Roma"]
        >>>
        >>> # Create named palettes for swatchplot
        >>> col_carto  = [palette(divergingx_hcl(x)(11), name = x) for x in carto]
        >>> col_brewer = [palette(divergingx_hcl(x)(11), name = x) for x in carto]
        >>> col_others = [palette(divergingx_hcl(x)(11), name = x) for x in others]
        >>>
        >>> # Visualize available divergingx palettes
        >>> swatchplot({"Carto":  col_carto,
        >>>             "Brewer": col_brewer,
        >>>             "Others": col_others},
        >>>            figsize = (5.5, 6));
        >>>
        >>> #: Checking settings of a specific palette
        >>> pal4 = divergingx_hcl("PRGn")
        >>> pal4.show_settings()

    Raises:
        TypeError: If `fixup` is not bool.
        TypeError: If `palette` is not `None` or str.
        TypeError: If `cmax` not `Non`, float, int, list, numpy.ndarray.
        ValueError: If `cmax` is list of length `<1` or `>2`.
        ValueError: If `h`, `c`, `l`, `power`, `cmax` contain unexpected types or values.
        ValueError: If `palette` is string, but palette with this name cannot be found.
        Exception: If `h3` is not specified.
        ValueError: If `**kwargs` are provides which are not among the allowed ones.
    """

    _allowed_parameters = ["h1", "h2", "h3",
                           "c1", "cmax1", "c2", "cmax2", "c3",
                           "l1", "l2", "l3", "p1", "p2", "p3", "p4"]
    _name = "DivergingX HCL"

    def __init__(self, h = [192, 77, 21], c = [40, 35, 100], l = [50, 95, 50], \
                 power = [1.0, 1.0, 1.2, 1.0], cmax = 20, \
                 fixup = True, palette = None, rev = False, *args, **kwargs):

        import numpy as np

        self._set_rev(rev)
        if not isinstance(fixup, bool): raise TypeError("argument `fixup` must be bool")
        if not isinstance(palette, (str, type(None))):
            raise TypeError("argument `palette` must be None or str")

        if isinstance(h, str):
            palette = h
            h       = [-999.] * 3 # Temporarliy setting to dummy value
        if isinstance(power, int) or isinstance(power, float):
            power   = [power]

        # Handling cmax
        if not isinstance(cmax, (type(None), float, int, list, np.ndarray)):
            raise TypeError("argument `cmax` must be None, float, int, or list")
        elif isinstance(cmax, (list, np.ndarray)) and (len(cmax) < 1 or len(cmax) > 2):
            raise ValueError("if `cmax` is a list or numpy.ndarray it must be of lengt 1 or 2")
        # If cmax is a numpy array: Reduce to list
        if isinstance(cmax, np.ndarray): cmax = list(cmax)

        if isinstance(cmax, list) and len(cmax) == 1:
            cmax = cmax + [None]
        elif cmax is None:
            cmax = [None, None]  # Both set to None
        elif isinstance(cmax, (float, int)):
            cmax = [cmax, None]  # Use 'cmax' as 'cmax1'

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   3, 3, False, False, h = h)
            c     = self._checkinput_(int,   2, 3, False, False, c = c)
            l     = self._checkinput_(int,   2, 3, False, False, l = l)
            power = self._checkinput_(float, 2, 4, False, False, power = power)
            cmax  = self._checkinput_(float, 2, 2, False, True, cmax = cmax)
        except Exception as e:
            raise ValueError(str(e))

        if len(c) == 2:    c = [c[0], c[1], c[0]]
        if len(l) == 2:    l = [l[0], l[1], l[0]]
        if len(power) < 4: power = [power[0], power[1], power[1], power[0]]

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            from .hcl_palettes import divergingx_palettes
            from numpy import where
            pals = divergingx_palettes().get_palettes("Divergingx")
            idx  = where([x.name().upper().replace(" ", "") == palette.upper().replace(" ", "") for x in pals])[0]
            if len(idx) == 0:
                raise ValueError(f"palette {palette} is not a valid divergingx palette. " + \
                                 f"Choose one of: {', '.join([x.name() for x in pals])}")
            pal = pals[idx[0]]
            del pals, idx

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in self._allowed_parameters:
                    pal.set(**{key: value})

            # Extending h2 if h1 = h2 (h2 None)
            def isNone(x): return isinstance(x, type(None))
            if isNone(pal.get("p1")): pal.set(p1 = 1.0)
            # Second coordinate
            if isNone(pal.get("h2")): pal.set(h2 = pal.get("h1"))
            if isNone(pal.get("c2")): pal.set(c2 = 0.0)
            if isNone(pal.get("l2")): pal.set(l2  = pal.get("l1"))
            if isNone(pal.get("p2")): pal.set(p2  = pal.get("p1"))
            ## third coordinate
            if isNone(pal.get("h3")):
                raise Exception("third hue coordinate (h3) must be specified")
            if isNone(pal.get("c3")): pal.set(c3 = pal.get("c1"))
            if isNone(pal.get("l3")): pal.set(l3 = pal.get("l1"))
            if isNone(pal.get("p3")): pal.set(p3 = pal.get("p1"))
            if isNone(pal.get("p4")): pal.set(p4 = pal.get("p2"))

            # Getting settings
            settings = pal.get_settings()
        else:
            settings = {}

            from numpy import ndarray

            # User settings
            for i in range(3): settings["h{:d}".format(i + 1)] = h[i]
            for i in range(3): settings["c{:d}".format(i + 1)] = c[i]
            for i in range(3): settings["l{:d}".format(i + 1)] = l[i]
            for i in range(4): settings["p{:d}".format(i + 1)] = power[i]
            for i in range(2): settings["cmax{:d}".format(i + 1)] = cmax[i]
            settings["fixup"] = fixup
            settings["rev"]   = rev

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if not key in self._allowed_parameters + ["desc", "gui"]:
                    raise ValueError(f"argument `{key}` not allowed for {type(self).__name__}")
                settings[key] = val

        # Save settings
        self.settings = settings


    # Return hex colors
    def colors(self, n = 11, fixup = None, alpha = None, **kwargs):
        """Get Colors

        Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned.
            fixup (None, bool): Should sRGB colors be corrected if they lie
                outside the defined color space?  If `None` the `fixup`
                parameter from the object will be used. Can be set to `True` or
                `False` to explicitly control the fixup here.
            alpha (None, float, list, or numpy.ndarray): Allows to add an transparency
                (alpha channel) to the colors. Can be a single float, a list, or a
                numpy array. If a list or array is provided it must be of length 1 or
                of length `n` and be convertible to float, providing values
                between `0.0` (full opacity) and `1.0` (full transparency)
            **kwargs: Currently allows for `rev = True` to reverse the colors.


        Returns:
            list: Returns a list of str with `n` colors from the
            color palette.

        """

        import numpy as np
        from .colorlib import HCL

        alpha = self._get_alpha_array(alpha, n)
        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        # If n == 1 we do as we have 3 colors, but then only return the middle one
        tmp_n = n if n > 1 else 3

        # Calculate where to evaluate the trajectories
        # n2 is half the number of colors (n on either side of the palette)
        n2   = int(np.ceil(tmp_n / 2))
        rval = np.linspace(1., 0., n2) if n % 2 == 1 else np.linspace(1., 1. / (2 * n2 - 1), n2)

        # Calculate H/C/L coordinates for both sides (called 'a' and 'b' not to get
        # confused with the numbering of the parameters).
        Ha, Ca, La = self._get_seqhcl(rval, ha = self.get("h1"), hb = self.get("h2"), 
                                            ca = self.get("c1"), cb = self.get("c2"),
                                            la = self.get("l1"), lb = self.get("l2"),
                                            pa = self.get("p1"), pb = self.get("p2"),
                                            cmax = self.get("cmax1"))
        Hb, Cb, Lb = self._get_seqhcl(rval, ha = self.get("h3"), hb = self.get("h2"), 
                                            ca = self.get("c3"), cb = self.get("c2"),
                                            la = self.get("l3"), lb = self.get("l2"),
                                            pa = self.get("p3"), pb = self.get("p4"),
                                            cmax = self.get("cmax2"))

        # In case the user requested an odd number of colors we need to
        # cut away one of one of the two sides (remove it from 'b').
        if tmp_n % 2 == 1:
            Hb = Hb[:-1]
            Cb = Cb[:-1]
            Lb = Lb[:-1]

        # Concatenate the two sides
        H = np.concatenate((Ha, Hb[::-1]))
        C = np.concatenate((Ca, Cb[::-1]))
        L = np.concatenate((La, Lb[::-1]))

        # Create new HCL color object
        HCL = HCL(H, C, L, alpha)

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        cols = HCL.colors(fixup = fixup, rev = rev)
        return [cols[1]] if n == 1 else cols




# -------------------------------------------------------------------
# -------------------------------------------------------------------
class sequential_hcl(hclpalette):
    """Sequential HCL Color Palettes

    The HCL (hue-chroma-luminance) color model is a perceptual color model
    obtained by using polar coordinates in CIELUV space
    (i.e., :py:class:`polarLUV <colorspace.colorlib.polarLUV>`),
    where steps of equal size correspond to approximately equal perceptual
    changes in color. By taking polar coordinates the resulting three
    dimensions capture the three perceptual axes very well: hue is the type of
    color, chroma the colorfulness compared to the corresponding gray, and
    luminance the brightness. This makes it relatively easy to create balanced
    palettes through trajectories in this HCL space. In contrast, in the more
    commonly-used ‘HSV’ (hue-saturation-value) model (a simple transformation
    of ‘RGB’), the three axes are confounded so that luminance changes along
    with the hue leading to very unbalanced palettes.

    `qualitative_hcl` distinguishes the underlying categories by a sequence of
    hues while keeping both chroma and luminance constant to give each color in
    the resulting palette the same perceptual weight. Thus, `h` should be a
    pair of hues (or equivalently `h1` and `h2` can be used) with the starting
    and ending hue of the palette. Then, an equidistant sequence between these
    hues is employed, by default spanning the full color wheel (i.e, the full
    360 degrees). Chroma `c` (or equivalently `c1`) and luminance `l` (or
    equivalently `l1`) are constants. If `h` is str it will overwrite the
    `palette` argument. In this case, pre-specified palette settings will be
    loaded but are allowed to be overwritten by the user. At any time the user
    can overwrite any of the settings.

    By default, `sequential_hcl` returns an object of class `hclpalette`
    identical to the pre-defined `"Blues 2"` palette.

    `h1` and `h2` both allow for lambda functions to create uniformly distributed
    hues around the (full) circle (360 degrees).

    * `h1`: can be a lambda function with one single argument `n` (number of colors).
    * `h2`: can be a lambda function with one or two arguments. If only one, `n`
        (number of colors) will be handed over when evaluated. If two, the first
        one is expected to be `n` (number of colors), as second argument the
        value `h1` will be used.

    See also: :py:class:`qualitative_hcl`, :py:class:`diverging_hcl`,
    :py:class:`divergingx_hcl`, :py:class:`rainbow_hcl`, :py:class:`heat_hcl`,
    :py:class:`terrain_hcl`, :py:class:`diverging_hsv`, and
    :py:class:`rainbow`.

    Args:
        h (float, int, list, str): Hue values (color). If only one value is given the value
            is recycled which yields a single-hue sequential color palette.  If
            input `h` is a str this argument acts like the `palette` argument
            (see `palette` input parameter).
        c (float, int, list): Chroma values (colorfullness), int or float
            (linear to zero), list of two numerics (linear in interval), =
            or three numerics (advanced; `[c1, cmax, c2]`).
        l (float, int, list): Luminance values (luminance). If float or int,
            the element will be recycled, or a list of two numerics
            (defining `[l1, l2]`).
        power (float, int, list): Power parameter for non-linear behaviour
            of the color palette. Single float or int, or a list of numerics
            (defining `[p1, p2]`).
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        palette (str): Can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be
            raised.  Else the settings of the palette as defined will be used to
            create the color palette.
        rev (bool): Should the color map be reversed.
        *args: Currently unused.
        **kwargs: Additional named arguments to overwrite the palette settings.
            Allowed: `h1`, `h2`, `c1`, `c2`, `cmax`, `l1`, `l2`, `p1`, `p2`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the `.colors()` method),
        see examples.

    Example:

        >>> from colorspace import sequential_hcl
        >>> a = sequential_hcl()
        >>> a.colors(10)
        >>> #: Different color palette by name
        >>> b = sequential_hcl("Peach")
        >>> b.colors(10)
        >>> #:
        >>> b.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>> #: The standard call of the object also returns hex colors
        >>> sequential_hcl("Peach")(10)
    """

    # Allowed to overwrite via **kwargs
    _allowed_parameters = ["h1", "h2", "c1", "c2", "cmax", "l1", "l2", "p1", "p2"]
    _name = "Sequential HCL"

    def __init__(self, h = 260, c = 80, l = [30, 90],
        power = 1.5, fixup = True, palette = None, rev = False,
        *args, **kwargs):

        self._set_rev(rev)
        if not isinstance(fixup, bool): raise TypeError("argument `fixup` must be bool")
        if not isinstance(palette, (str, type(None))):
            raise TypeError("argument `palette` must be None or str")

        # If input "h" is a str: exchange with "palette"
        if isinstance(h, str):
            palette = h
            h       = -999 # Temporarliy setting to dummy value

        # _checkinput_ parameters (in the correct order):
        # dtype, length_min = None, length_max = None,
        # recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   1, 2, True,  False, h = h)
            c     = self._checkinput_(int,   1, 3, True,  False, c = c)
            l     = self._checkinput_(int,   2, 2, True,  False, l = l)
            power = self._checkinput_(float, 2, 2, True,  False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            from numpy import where
            pals = hclpalettes().get_palettes("Sequential")
            idx  = where([x.name().upper().replace(" ", "") == palette.upper().replace(" ", "") for x in pals])[0]
            if len(idx) == 0:
                raise ValueError(f"palette {palette} is not a valid sequential palette. " + \
                                 f"Choose one of: {', '.join([x.name() for x in pals])}")
            pal = pals[idx[0]]

            def isNone(x): return isinstance(x, type(None))

            if isNone(pal.get("h2")): pal.set(h2 = pal.get("h1"))

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in self._allowed_parameters: pal.set(**{key: value})

            # Getting settings
            settings = pal.get_settings()
        else:
            # User settings
            settings = {}
            settings["h1"]        = h[0]
            settings["h2"]        = None if len(h) == 1 else h[1]
            if len(c) == 3:
                settings["c1"]    = c[0]
                settings["cmax"]  = c[1]
                settings["c2"]    = c[2]
            elif len(c) == 2:
                settings["c1"]    = c[0]
                settings["c2"]    = c[1]
            else:
                settings["c1"]    = c[0]
                settings["c2"]    = 0
            settings["l1"]        = l[0]
            settings["l2"]        = l[1]
            settings["p1"]        = power[0]
            settings["p2"]        = power[1]
            settings["fixup"]     = fixup
            settings["rev"]       = rev

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if not key in self._allowed_parameters + ["desc", "gui"]:
                    raise ValueError(f"argument `{key}` not allowed for {type(self).__name__}")
                settings[key] = val

        if isinstance(settings["h2"], type(None)): settings["h2"] = settings["h1"]

        # Save settings
        self.settings = settings


    # Return hex colors
    def colors(self, n = 11, fixup = None, alpha = None, **kwargs):
        """Get Colors

        Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned.
            fixup (None, bool): Should sRGB colors be corrected if they lie
                outside the defined color space?  If `None` the `fixup`
                parameter from the object will be used. Can be set to `True` or
                `False` to explicitly control the fixup here.
            alpha (None, float, list, or numpy.ndarray): Allows to add an transparency
                (alpha channel) to the colors. Can be a single float, a list, or a
                numpy array. If a list or array is provided it must be of length 1 or
                of length `n` and be convertible to float, providing values
                between `0.0` (full opacity) and `1.0` (full transparency)
            **kwargs: Currently allows for `rev = True` to reverse the colors.

        Returns:
            list: Returns a list of str with `n` colors from the
            color palette.

        Examples:
            >>> from colorspace import sequential_hcl, hexcols
            >>> sequential_hcl().colors()
            >>> #: Different sequential palette
            >>> cols = sequential_hcl("Rocket").colors(5)
            >>> cols
            >>> #:
            >>> hexcols(cols)
            >>> #: Five colors with constant alpha of 0.3
            >>> sequential_hcl().colors(5, alpha = 0.3)
            >>> #: Three colors with variying alpha
            >>> sequential_hcl().colors(3, alpha = [0.2, 0.8, 0.3])

        """

        from numpy import linspace
        from .colorlib import HCL

        alpha = self._get_alpha_array(alpha, n)
        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        # Calculate H/C/L
        p1   = self.get("p1")
        p2   = p1 if self.get("p2") is None else self.get("p2")
        c1   = self.get("c1")
        c2   = 0 if self.get("c2") is None else self.get("c2")
        cmax = None if not self.get("cmax") else self.get("cmax")
        l1   = self.get("l1")
        l2   = l1 if self.get("l2") is None else self.get("l2")
        h1   = self.get("h1")
        h2   = h1 if self.get("h2") is None else self.get("h2")

        # Get colors and create new HCL color object
        [H, C, L] = self._get_seqhcl(linspace(1., 0., n), h1, h2, c1, c2, l1, l2, p1, p2, cmax)
        HCL = HCL(H, C, L, alpha)

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return HCL.colors(fixup = fixup, rev = rev)


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class heat_hcl(sequential_hcl):
    """HCL Based Heat Color Palette

    `heat_hcl` is an implementation of the base _R_ 'heat.colors' palette but
    constructed in HCL space based on a call to :py:class:`sequential_hcl`. 

    See also: :py:class:`qualitative_hcl`, :py:class:`sequential_hcl`,
    :py:class:`diverging_hcl`, :py:class:`divergingx_hcl`,
    :py:class:`rainbow_hcl`, :py:class:`terrain_hcl`,
    :py:class:`diverging_hsv`, and :py:class:`rainbow`.

    Args:
        h (list of int): Hue parameters (h1/h2).
        c (list of int): Chroma parameters (c1/c2).
        l (int): Luminance parameters (l1/l2).
        power (list of float): Power parameters (p1/p2).
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        rev (bool): Should the color map be reversed.
        *args: Currently unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.
            Allowed: `h1`, `h2`, `c1`, `c2`, `l1`, `l2`, `p1`, `p2`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the `.colors()` method),
        see examples.

    Example:

        >>> from colorspace.palettes import heat_hcl
        >>> pal = heat_hcl()
        >>> pal.colors(3)
        >>> #:
        >>> pal.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>> #: The standard call of the object also returns hex colors
        >>> heat_hcl()(10)
    """


    _allowed_parameters = ["h1", "h2", "c1", "c2", "l1", "l2", "p1", "p2"]
    _name = "Heat HCL"

    def __init__(self, h = [0, 90], c = [100, 30], l = [50, 90], power = [1./5., 1.],
                 fixup = True, rev = False, *args, **kwargs):

        self._set_rev(rev)
        if not isinstance(fixup, bool): raise TypeError("argument `fixup` must be bool")

        # _checkinput_ parameters (in the correct order):
        # - dtype, length_min, length_max, recycle, nansallowed, **kwargs
        try:
            h     = self._checkinput_(int,   2, 2, False, h = h)
            c     = self._checkinput_(int,   2, 2, False, c = c)
            l     = self._checkinput_(int,   2, 2, False, l = l)
            power = self._checkinput_(float, 2, 2, False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # Save settins
        self.settings = {"h1": int(h[0]), "h2": int(h[1]),
                         "c1": int(c[0]), "c2": int(c[1]),
                         "l1": int(l[0]), "l2": int(l[1]),
                         "p1": power[0],  "p2": power[1],
                         "fixup": bool(fixup)}

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if not key in self._allowed_parameters + ["desc", "gui"]:
                    raise ValueError(f"argument `{key}` not allowed for {type(self).__name__}")
                self.settings[key] = val

        self.settings["rev"] = self._rev


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class terrain_hcl(sequential_hcl):
    """HCL Based Terrain Color Palette

    `terrain_hcl` is an implementation of the base _R_ 'terrain.colors' palette but
    constructed in HCL space based on a call to :py:class:`sequential_hcl`. 

    See also: :py:class:`qualitative_hcl`, :py:class:`sequential_hcl`,
    :py:class:`diverging_hcl`, :py:class:`divergingx_hcl`,
    :py:class:`rainbow_hcl`, :py:class:`heat_hcl`, :py:class:`diverging_hsv`,
    and :py:class:`rainbow`.

    Args:
        h (list of int): Hue parameters (h1/h2).
        c (list of int): Chroma parameters (c1/c2).
        l (int): Luminance parameters (l1/l2).
        power (list of float): Power parameters (p1/p2).
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        rev (bool): Should the color map be reversed.
        *args: unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.
            Allowed: `h1`, `h2`, `c1`, `c2`, `l1`, `l2`, `p1`, `p2`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the `.colors()` method),
        see examples.

    Example:

        >>> from colorspace import terrain_hcl
        >>> pal = terrain_hcl()
        >>> pal.colors(10)
        >>> #:
        >>> pal.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>> #: The standard call of the object also returns hex colors
        >>> terrain_hcl()(10)
    """

    _allowed_parameters = ["h1", "h2", "c1", "c2", "l1", "l2", "p1", "p2"]
    _name = "Terrain HCL"

    def __init__(self, h = [130, 0], c = [80, 0], l = [60, 95], power = [1./10., 1.],
                 fixup = True, rev = False, *args, **kwargs):

        self._set_rev(rev)
        if not isinstance(fixup, bool): raise TypeError("argument `fixup` must be bool")

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   2, 2, False, h = h)
            c     = self._checkinput_(int,   2, 2, False, c = c)
            l     = self._checkinput_(int,   2, 2, False, l = l)
            power = self._checkinput_(float, 2, 2, False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # Save settins
        self.settings = {"h1": int(h[0]), "h2": int(h[1]),
                         "c1": int(c[0]), "c2": int(c[1]),
                         "l1": int(l[0]), "l2": int(l[1]),
                         "p1": power[0],  "p2": power[1],
                         "fixup": bool(fixup)}

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if not key in self._allowed_parameters + ["desc", "gui"]:
                    raise ValueError(f"argument `{key}` not allowed for {type(self).__name__}")
                self.settings[key] = val

        self.settings["rev"] = self._rev


class diverging_hsv(hclpalette):
    """Diverging HSV Color Palettes

    `diverging_hsv` provides an HSV-based version of :py:class:`diverging_hcl`.
    Its purpose is mainly didactic to show that HSV-based diverging palettes
    are less appealing, more difficult to read and more flashy than HCL-based
    diverging palettes.

    See also: :py:class:`qualitative_hcl`, :py:class:`sequential_hcl`,
    :py:class:`diverging_hcl`, :py:class:`divergingx_hcl`,
    :py:class:`rainbow_hcl`, :py:class:`heat_hcl`, :py:class:`terrain_hcl`, and
    :py:class:`rainbow`.

    Args:
        h (list of numerics): Hue values, diverging color palettes should have
            different hues for both ends of the palette. If only one value is present
            it will be recycled ending up in a diverging color palette with the same
            colors on both ends.  If more than two values are provided the first two
            will be used while the rest is ignored.  If input `h` is a str this
            argument acts like the `palette` argument (see `palette` input
            parameter).
        s (float, int): Saturation value for the two ends of the palette.
        v (float, int): Value (the HSV value) of the colors.
        power (numeric): Power parameter for non-linear behaviour of the color
            palette.
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        rev (bool): Should the color map be reversed.
        *args: Unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.
            Allowed: `h1`, `h2`, `s`, `v`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the `.colors()` method),
        see examples.

    Example:

        >>> from colorspace import diverging_hsv
        >>> pal = diverging_hsv()
        >>> pal.colors(10)
        >>> #:
        >>> pal.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>> #: The standard call of the object also returns hex colors
        >>> diverging_hsv()(10)
        >>> #: Manually modified palette from 'cyan' to 'orange'
        >>> diverging_hsv(h = [180, 30]).swatchplot(
        >>>               n = 7, show_names = False, figsize = (5.5, 0.5))
        >>> #: Additionally, lower saturation on the two ends
        >>> diverging_hsv(h = [180, 30], s = 0.4).swatchplot(
        >>>               n = 7, show_names = False, figsize = (5.5, 0.5))
        >>> #: Lowering the value
        >>> diverging_hsv(h = [180, 30], s = 0.4, v = 0.75).swatchplot(
        >>>               n = 7, show_names = False, figsize = (5.5, 0.5))
    """

    _allowed_parameters = ["h1", "h2", "s", "v"]
    _name = "Diverging HSV"

    def __init__(self, h = [240, 0], s = 1., v = 1., power = 1.,
        fixup = True, rev = False, *args, **kwargs):

        self._set_rev(rev)
        if not isinstance(fixup, bool): raise TypeError("argument `fixup` must be bool")

        # Doing all the sanity checks.
        if not isinstance(s, (float, int)):
            raise TypeError("argument 's' must be float or int")
        s = float(s)
        if s < 0. or s > 1.: raise ValueError("argument 's' must be in [0., 1.]")

        if not isinstance(v, (float, int)):
            raise TypeError("argument 'v' must be float or int")
        v = float(v)
        if v < 0. or v > 1.: raise ValueError("argument 'v' must be in [0., 1.]")

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   2, 2, False, h = h)
            power = self._checkinput_(float, 1, 1, False, power = power)[0]
        except Exception as e:
            raise ValueError(str(e))

        # Save settins
        self.settings = {"h1": int(h[0]),  "h2": int(h[1]),
                         "s": s,           "v": v,
                         "power": power,   "fixup": fixup}

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if not key in self._allowed_parameters + ["desc", "gui"]:
                    raise ValueError(f"argument `{key}` not allowed for {type(self).__name__}")
                self.settings[key] = val

        self.settings["rev"] = self._rev



    # Return hex colors
    def colors(self, n = 11, fixup = None, alpha = None, **kwargs):
        """Get Colors

        Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned.
            fixup (None, bool): Should sRGB colors be corrected if they lie
                outside the defined color space?  If `None` the `fixup`
                parameter from the object will be used. Can be set to `True` or
                `False` to explicitly control the fixup here.
            alpha (None, float, list, or numpy.ndarray): Allows to add an transparency
                (alpha channel) to the colors. Can be a single float, a list, or a
                numpy array. If a list or array is provided it must be of length 1 or
                of length `n` and be convertible to float, providing values
                between `0.0` (full opacity) and `1.0` (full transparency)
            **kwargs: Currently allows for `rev = True` to reverse the colors.

        Returns:
            list: Returns a list of str with `n` colors from the
            color palette.

        """

        from numpy import linspace, power, abs, repeat, where
        from numpy import ndarray, ndenumerate
        from .colorlib import HSV

        alpha = self._get_alpha_array(alpha, n)
        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        # Calculate palette
        rval = linspace(-self.get("s"), self.get("s"), n)

        # Calculate H, S, V coordinates
        H = repeat(self.get("h1"), n)
        H[where(rval > 0)] = self.get("h2")
        S = power(abs(rval), self.get("power"))
        V = repeat(self.get("v"), n)

        # Generate color object
        HSV = HSV(H, S, V, alpha)
        HSV.to("RGB") # Force to go trough RGB (not sRGB directly)

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return HSV.colors(fixup = fixup, rev = rev)



# -------------------------------------------------------------------
# -------------------------------------------------------------------
class rainbow(hclpalette):
    """Infamous sRGB Rainbow Color Palette

    Implements the (in-)famous rainbow (or jet) color palette that was used
    very frequently in many software packages but has been widely criticized
    for its many perceptual problems. It is specified by a `start` and `end`
    hue $\in [0.-1.]$ with `red = 0`, `yellow = 1/6`, `green = 2/6`, `cyan =
    3/6`, blue = `4/6`, and `magenta = 5/6`. However, these are very flashy and
    unbalanced with respect to both chroma and luminance which can lead to
    various optical illusions. Also, the hues that are equispaced in RGB space
    tend to cluster at the red, green, and blue primaries. Therefore, it is
    recommended to use a suitable palette from `hcl.colors` instead of
    `rainbow`.

    `start` and/or `end` both allow for lambda functions with one single
    argument `n` (number of colors), see examples.

    See also: :py:class:`qualitative_hcl`, :py:class:`sequential_hcl`,
    :py:class:`diverging_hcl`, :py:class:`divergingx_hcl`,
    :py:class:`rainbow_hcl`, :py:class:`heat_hcl`, :py:class:`terrain_hcl`, and
    :py:class:`diverging_hsv`.

    Args:
        s (float, int): saturation value, a value in `[0., 1.]`. Defaults to `1.0`.
        v (float, int): value, a value in `[0., 1.]`. Defaults to `1.0`.
        start (float, int, function): the (corrected) hue in `[0., 1.]` at which
            the rainbow begins. Defaults to `0.`. Can be a function with one input
            `n` (number of colors). If outside `[0., 1.]` it will be wrapped.
        end (float, int, function): the (corrected) hue in `[0., 1.]` at which
            the rainbow ends. Defaults to `0.`. Can be a function with one input
            `n` (number of colors). If outside `[0., 1.]` it will be wrapped.
        rev (bool): Should the color map be reversed.
        *args: Unused.
        **kwargs: Unused.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the `.colors()` method),
        see examples.

    Example:

        >>> from colorspace import rainbow
        >>> pal = rainbow()
        >>> pal.colors(10)
        >>> #:
        >>> pal.swatchplot(show_names = False, figsize = (5.5, 0.5));
        >>> #: The standard call of the object also returns hex colors
        >>> rainbow()(10)
        >>>
        >>> #: Using lambda functions for start/end
        >>> p = rainbow(start = lambda n: 1 / n, end = lambda n: 1 - 1 / n)
        >>> p.swatchplot(n = 5, show_names = False, figsize = (5.5, 0.5));
        >>> #:
        >>> p.swatchplot(n = 10, show_names = False, figsize = (5.5, 0.5));
        >>> #:
        >>> p.specplot(rgb = True, figsize = (8, 6))

    Raises:
        TypeError: If `s` or `v` are not float or int.
        ValueError: If `s` or `v` are outside range, must be in `[0., 1.]`.
        TypeError: If `start` and `end` are not float/int in `[0., 1.]` or lambda functions.
        TypeError: If `rev` is not bool.
    """

    _allowed_parameters = ["s", "v", "start", "end"]
    _name = "Diverging HCL"

    def __init__(self, s = 1, v = 1, start = 0, end = lambda n: max(1., n - 1.) / n,
        rev = False, *args, **kwargs):

        self._set_rev(rev)

        # Doing all the sanity checks.
        if not isinstance(s, (float, int)):
            raise TypeError("argument 's' must be float or int")
        s = float(s)
        if s < 0. or s > 1.: raise ValueError("argument 's' must be in [0., 1.]")

        if not isinstance(v, (float, int)):
            raise TypeError("argument 'v' must be float or int")
        v = float(v)
        if v < 0. or v > 1.: raise ValueError("argument 'v' must be in [0., 1.]")

        if not isinstance(start, (float, int)) and not callable(start):
            raise TypeError("argument `start` must be float, int, or lambda function")
        if not isinstance(end, (float, int)) and not callable(end):
            raise TypeError("argument `end` must be float, int, or lambda function")

        # Check start and end. Either functions (lambda functions)
        # or a single floating point number in [0-1].
        if callable(start):                     pass
        elif isinstance(start, (float, int)):   start = float(start)
        if callable(end):                       pass
        elif isinstance(end, (float, int)):     end   = float(end)

        # Store these settings
        self.settings = {"s": float(s), "v": float(v), "start": start, "end": end, "rev": self._rev}


    # Return hex colors
    def colors(self, n = 11, alpha = None, **kwargs):
        """Get Colors

        Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned. Defaults to `11`.
            alpha (None, float, list, or numpy.ndarray): Allows to add an transparency
                (alpha channel) to the colors. Can be a single float, a list, or a
                numpy array. If a list or array is provided it must be of length 1 or
                of length `n` and be convertible to float, providing values
                between `0.0` (full opacity) and `1.0` (full transparency)
            **kwargs: Currently allows for `rev = True` to reverse the colors.

        Returns:
            list: Returns a list of str with `n` colors from the
            color palette.

        Examples:
            >>> from colorspace import rainbow
            >>> rainbow().colors(4)

        Raises:
            ValueError: If input `n` is not float/int or smaller than 1.
        """

        from numpy import linspace, mod, repeat
        from .colorlib import HSV

        if not isinstance(n, int):
            raise TypeError("argument `n` must be int")
        n = int(n)
        if n <= 0: raise ValueError("argument `n` must be positive (>= 1)")

        alpha = self._get_alpha_array(alpha, n)

        # Evaluate start and end given 'n'
        start = self.settings["start"]
        start = start(n) if callable(start) else start
        end   = self.settings["end"]
        end   = end(n) if callable(end) else end

        h = mod(linspace(start, end, n), 1.)
        s = repeat(self.settings["s"], n)
        v = repeat(self.settings["v"], n)

        # Generate HSV colorobject
        HSV = HSV(h * 360., s, v, alpha)
        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HSV

        # Reversing colors if needed
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return HSV.colors(fixup = False, rev = rev)


