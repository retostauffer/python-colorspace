
import os
import sys



class palette:
    """A class for custom color palettes with a fixed number of colors.
    Creates a custom color map based on a list of hex colors (fixed number of
    colors) and a name. Used for e.g., :py:func:`hcl_palettes.swatchplot`.

    Args:
        colors (str, list, colorspace.colorlib.colorobject): One or multiple
            colors which will make up the custom palette.
        name (str): Name of this custom palette. Defaults to `"user_palette"`.
        n (int): positive integer, number of colors drawn from an `hclpalette` object.
            Only taken into account if the object provided on `colors` inherits
            from :py:class:`colorspace.palettes.hclpalette`.

    Returns:
        An object of class :py:class:`colorspace.palettes.palette`.

    Example:

        >>> from colorspace.palettes import palette
        >>> colors = ["#070707", "#690056", "#C30E62", "#ED8353", "#FDF5EB"]
        >>> custom_pal = palette(colors, "test palette")
        >>> print(custom_pal)
        >>>
        >>> ## Testing different input types (str, list, colorobject)
        >>> from colorspace.colorlib import hexcols
        >>> from colorspace import palette
        >>> hexcols = hexcols(colors)
        >>> 
        >>> pal1 = palette("#ff0033")
        >>> pal2 = palette("#ff0033", name = "custom name")
        >>> pal3 = palette(colors,  name = "custom 1.1")
        >>> pal4 = palette(hexcols, name = "custom 1.2")
        >>> print(pal1)
        >>> print(pal2)
        >>> print(pal3)
        >>> print(pal4)
        >>>
        >>> from colorspace import swatchplot
        >>> swatchplot([pal3, pal4])

    """

    def __init__(self, colors, name = None, n = 7):

        # Sanity check for input
        from colorspace.colorlib import colorobject
        from colorspace.palettes import hclpalette
        from colorspace import check_hex_colors, palette

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

        # Now check if all our colors are valid hex colors
        self._colors = check_hex_colors(colors)

        if not isinstance(name, (type(None), str)):
            raise TypeError("Argument 'name' must be `None` or a string.")

        self._name = name

    def __len__(self):
        """Returns number of colors of this palette

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
        """Rename custom palette

        Args:
            name (None, str): new name for the palette.

        Raises:
            ValueError: If input 'name' is not of type string.
        """
        if not isinstance(name, (type(None), str)):
            raise ValueError("Argument 'name' must be `None` or a string.")
        self._name = name

    def name(self):
        """Get name of palette

        Returns:
            None, str: Name of the palette (if set).
        """
        return self._name

    def colors(self, *args, **kwargs):
        """Get colors of palette.

        Returns:
            list: List of all colors of the palette.
        """
        return self._colors
        ###TODO(R) Remove? Return [str(x) for x in self._colors]

    def swatchplot(self, **kwargs):
        """Interfacing the :py:func:`swatchplot.swatchplot` function.
        Plotting the spectrum of the current color palette.

        Args:
            **kwargs: forwarded to :py:func:`swatchplot`. Note that
                ``show_names`` will always be set to ``False``.

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
        swatchplot(pals = self.colors(), show_names = False, **kwargs)

    def cmap(self, n = None, rev = False):
        """Return matplotlib compatible color map

        Converts the current palette into a `matplotlib.colors.LinearSegmentedColormap` color map.
        If input argument `n = None` the color map will provide the same number
        of colors as defined for this palette. Can also be set higher to
        allow matplotlib to interpolate between the colors.

        Args:
            n (None or int): `None` or a positive integer which is greater or equal
                to the number of colors of the palette (check `len()` of the object).
            rev (bool): If set to ``True`` the color map will be reversed,
                defaults to False.

        Return:
            Returns a :py:class:`matplotlib.colors.LinearSegmentedColormap` (cmap) to be used
            with the matplotlib library.

        TODO:
            Is `n = None` a good default?

        Example:

            >>> from colorspace import diverging_hcl
            >>> pal = diverging_hcl()
            >>>
            >>> cmap = pal.cmap()
            >>> print(type(cmap))
            >>> print(cmap.N)
            >>>
            >>> cmap2 = pal.cmap(n = 256)
            >>> print(cmap2.N)
        """

        import matplotlib
        from matplotlib.colors import LinearSegmentedColormap
        from numpy import linspace, round, fmin, fmax

        from .colorlib import hexcols
        cobj = hexcols(self.colors())
        cobj.to("sRGB")

        if n is None:
            n = len(self.colors())
        elif not isinstance(n, int) or n < len(self.colors()):
            raise ValueError("Argument 'n' must be `None` or a valid positive integer greater " + \
                             "than the number of colors in the palette.")

        # Get coordinates
        pos = round(linspace(0, 1, len(self.colors())), 6)
        # Fixup RGB colors if not within [0,1]
        r   = fmax(0, fmin(1, round(cobj.get("R"),   6)))
        g   = fmax(0, fmin(1, round(cobj.get("G"),   6)))
        b   = fmax(0, fmin(1, round(cobj.get("B"),   6)))

        # Create dict for cmap
        cdict = {'red':[], 'green':[], 'blue':[]}
        for i in range(0, len(self.colors())):
            j = i if not rev else n - i - 1
            cdict['red'].append(   (pos[i], r[j], r[j]) ) 
            cdict['green'].append( (pos[i], g[j], g[j]) )
            cdict['blue'].append(  (pos[i], b[j], b[j]) )

        cmap = LinearSegmentedColormap(self.name(), cdict, n)
        return cmap



# -------------------------------------------------------------------
# -------------------------------------------------------------------
class defaultpalette:
    """Default color palette object. This object is not intended to be used by the
    user itself but is used to store the pre-defined color palettes contained
    in the package.

    Args:
        type (str): Type of palette.
        method (str): Name of the method which has to be called to retrieve colors
            (e.g., :py:class:`colorspace.palettes.diverging_hcl`).
        name (str): Name of the color palette.
        settings (dict): A python dictionary containing the parameter settings.

    Returns:
        Object of class :py:class:`colorspace.palettes.defaultpalette`.
    """

    def __init__(self, type, method, name, settings):

        self._type_      = type
        self._name_      = name
        self._method_    = method
        self._settings_  = settings

    # Default representation of defaultpalette objects.
    def __repr__(self):
        """Prints the current settings on stdout.
        Development method."""

        res = []
        res.append("Palette Name: {:s}".format(self.name()))
        res.append("        Type: {:s}".format(self.type()))
        res.append("        Inspired by: {:s}".format(self.get("desc")))
        #for key,val in self._settings_.items():
        keys = list(self.get_settings().keys())
        keys.sort()
        print(keys)
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
        """Wrapper function for :py:func:`colors`.

        Args:
            n (int): Number of colors, defaults to 7.

        Returns:
            list: List of hex colors.
        """
        return self.colors(n)

    def method(self):
        """Returns method used to create this palette.

        Returns:
            Returns the method (`str`, name of the function to be called
            to create the palette) of the palette.
        """
        return self._method_

    def type(self):
        """Get type of the color palette.

        Returns:
            Returns the type (`str`) of the palette.
        """
        return self._type_

    def name(self):
        """Get name of color palette.

        Returns:
            Returns the name (`str`) of the palette.
        """
        return self._name_

    def rename(self, name):
        """Allows to rename the palette.

        Args:
            name (str): New palette name.
        """
        self._name_ = name

    def get(self, what):
        """Allows to load the settings of the palette for the
        different parameters (e.g., ``h1``, ``h2``, ...). Returns
        `None` if the parameter does not exist.
        Another method (:py:func:`set`) allows to set the
        parameters.

        Args:
            what (str): Name of the parameter which should be extracted and
                returned from the settings of this color palette.

        Returns:
            Returns `None` if the parameter ``what`` cannot be found,
            else the value of the parameter ``what`` is returned.
        """
        if what in self._settings_.keys():
            return self._settings_[what]
        else:
            return None


    def set(self, **kwargs):
        """Allows to set/overwrite color palette parameters (e.g., ``h1``,
        ``h2``, ...).  Another method (:py:func:`get`) allows to retrieve the
        parameters.

        Args:
            **kwargs: A set of named arguments (``key = value`` pairs) where the key
            defines the parameter which should be overruled, value the
            corresponding value. Allowed value types are bool, int, and float.
        """
        for key,val in kwargs.items():
            #if not key in self._settings_.keys():
            #    raise ValueError("{:s} named {:s}".format(self.__class__.__name__, self.name()) + \
            #            " has no parameter called {:s}".format(key))
            # Else check current type specification and append
            # if possible (and convert to the new type).
            if not isinstance(val, (int, float, bool)):
                raise ValueError("input {:s} to {:s}".format(key, self.__class__.__name__) + \
                        " is of type {:s}. Only bool, int, and float allowed.".format(type(val)))
            if isinstance(val, bool):
                val = 1 if val else 0

            # Not yet a parameter in our dictionary? Add None first
            if not key in self._settings_.keys():
                self._settings_[key] = val
            # If already existing we convert the new value into the existing type.
            elif isinstance(self._settings_[key], int):
                self._settings_[key] = int(val)
            elif isinstance(self._settings_[key], float):
                self._settings_[key] = int(val)
            else:
                raise Exception("whoops, some code needed here in {:s}.set".format(
                    self.__class__.__name__))

        self._settings_[key] = val

    def get_settings(self):
        """Allows to get the current settings of the palette object.
        To retrieve single parameters use :py:func:`get`.

        Returns:
            Returns a `dict` object with all parameter specification of this
            palette.
        """
        return self._settings_

    def colors(self, n = 11):
        """Load a set of ``n`` colors from this palette.  This method evaluates
        the `method` argument to generate a set of hex colors which will be
        returned.  Please note that it is possible that none-values will be
        returned if the fixup-setting is set to `False` (see
        :py:class:`colorlib.hexcols`).

        Args:
            n (int): Number of colors to be returned, defaults to 11.

        Returns:
            Returns a `list` object with all parameter names.
        """

        # Dynamically load color function
        mod  = __import__("colorspace")
        cfun = getattr(mod, self._method_)

        # Calling color method with arguments of this object. 
        from copy import copy
        args = copy(self.get_settings())

        #TODO(R): No one needs this, right?
        ## If Remove h1/h2 and store them in h
        #for dim in ["h", "c", "l", "p"]:
        #    dim1 = "{:s}1".format(dim)
        #    dim2 = "{:s}2".format(dim)
        #    dim3 = "{:s}max".format(dim)
        #    dim = "power" if dim == "p" else dim
        #    if dim1 in args.keys() and dim2 in args.keys() and dim3 in args.keys():
        #        args[dim] = [args[dim1], args[dim2], args[dim3]]
        #        del args[dim1]; del args[dim2]; del args[dim3]
        #    # For Chroma we can have [c1, c2, cmax] for sequential palettes.
        #    # For diverging it can be [c1] or [c1, cmax].
        #    elif dim1 in args.keys() and dim3 in args.keys():
        #        if not self._method_ == "diverging_hcl":
        #            args[dim] = [args[dim1], args[dim1], args[dim3]] 
        #        else:
        #            args[dim] = [args[dim1], args[dim3]] 
        #        del args[dim1]; del args[dim3]
        #    # For Hue, Luminance, and Power there are only two (for now)
        #    elif dim1 in args.keys() and dim2 in args.keys():
        #        args[dim] = [args[dim1], args[dim2]]
        #        del args[dim1]; del args[dim2]
        #    elif dim1 in args.keys():
        #        args[dim] = args[dim1]
        #        del args[dim1]
        #    elif dim2 in args.keys():
        #        args[dim] = args[dim2]
        #        del args[dim2]

        pal = cfun(**args)
        return [str(x) for x in pal.colors(n, fixup = True)]



# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalettes:
    """Prepares the pre-specified hclpalettes.  Reads the config files and creates
    a set of :py:class:`defaultpalette` objects.

    Args:
        files (None, str list): If `None` (default) the default color palette
            configuration from within the package will be loaded. A path to a custom
            config file (str) or a list of paths can be provided to read custom
            palettes.

    Return:
        :py:class:`colorspace.palettes.hclpalettes`: Collection of predefined
        hcl color palettes.

    See Also:
        :py:func:`divergingx_palettes`.

    Examples:

        >>> from colorspace import hclpalettes
        >>> hclpals = hclpalettes()
        >>> print(hclpals)
        >>>
        >>> hclpals.plot()
        >>> hclpals.plot(n = 11)
    """
    def __init__(self, files = None, files_regex = None):


        assert isinstance(files, (type(None), str, list)), TypeError("argument 'files' must either be None, str, or list of str")
        if isinstance(files, str): files = [files]
        if isinstance(files, list):
            for file in files: assert isinstance(file, str), TypeError("not all elements in 'files' are of type str")

        if files is None:
            import glob
            resource_package = os.path.dirname(__file__)
            files = glob.glob(os.path.join(resource_package, "palconfig", "*.conf"))

        # Input 'files' specified:
        assert len(files) > 0, ValueError(f"no palette config files provided ({self.__class__.__name__})")
        for file in files:
            assert os.path.isfile(file), FileNotFoundError(f"file {file} does not exist")


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
        """Standard representation of the object."""
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
        """Get all palette types.

        Returns:
            list: Returns a `list` of strings (`str`) with the names of all palette types
            or groups.
        """

        return list(self._palettes_.keys())

    def get_palettes(self, type_ = None):
        """Get all palettes of a specific type.

        Args:
            type_ (None, str): (Partial) Name of the palettes which should be returned.
                String matching is used; partial matches are allowed.
                If set to `None` (default) all palettes will be returned. Names
                have to match but are not case sensitive, defaults to None.

        Returns:
            Returns a `list` containing :py:class:`defaultpalette` objects.
        """
        if not isinstance(type_, str) and not type_ is None:
            raise ValueError("input type_ to {:s} has to be None or a single string.".format(
                self.__class__.__name__))

        if not type_:
            res = []
            for key,pals in self._palettes_.items(): res += pals

        # Else return palette if available
        else:
            found = None
            res = []
            for t in self._palettes_.keys():
                if type_.upper() in t.upper():
                    found = t
                    res += self._palettes_[t]
            if not found:
                raise ValueError("No palettes for type \"{:s}\".".format(type_))
            else:
                type_ = found

        # Else return list with palettes
        return res

    def get_palette(self, name):
        """Get a palette with a specific name.

        Args:
            name (str): Name of the color palette which should be returned. Not
                case sensitive; blanks are ignored (removed).

        Returns:
            Returns an object of class :py:class:`defaultpalette` if a palette with
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
            raise ValueError("Palette {:s} not found.".format(name))

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
            raise Exception("misspecification in palconfig file {:s}: {:s}".format(file,str(e)))

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
            # "fixup": interpreted as boolean
            # rest:    interpreted as integer
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
                        print(val)
                        try:
                            val = eval(val)
                            if not callable(val): raise Exception
                        except:
                            raise ValueError("Element '{:s}' for palette '{:s}' neither an integer nor a proper lambda function!".format(
                                             key, sec))
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
        """Get length of palette.

        Returns:
            int: Integer, number of palettes in the object.
        """

        npals = 0
        for type_ in self.get_palette_types():
            for pal in self.get_palettes(type_): npals += 1

        return npals


    def plot(self, n = 5):
        """Create swatchplot.

        Args:
            n (int): Positive integer, number of colors.

        Raises:
            TypeError: If 'n' is not an integer.
            ValueError: If 'n' is not positive.
        """
        if not isinstance(n, int): raise TypeError("Argument 'n' must be integer.")
        if not n > 0:              raise ValueError("Argument 'n' must be positive.")

        from .swatchplot import swatchplot
        swatchplot(self, n = n)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalette:
    """Hy, I am the base class.  Is extended by the different HCL based color
    palettes such as the classes diverging_hcl, qualitative_hcl, rainbow_hcl,
    sequential_hcl, and maybe more in the future."""

    # Default call: return n hex colors
    def __call__(self, *args, **kwargs):
        """__call__(*args, **kwargs)

        Call interface, calls objects ``colors(...)`` method.

        Args:
            *args: Unnamd arguments forwarded to the color method.
            **kwargs:: Named arguments forwarded to the color method.

        Returns:
            See colors method.
        """
        return self.colors(*args, **kwargs)

    def specplot(self, n = 180, *args, **kwargs):
        """Interfacing the :py:func:`specplot.specplot` function.
        Plotting the spectrum of the current color palette.

        Args:
            n (int): Number of colors, defaults to 180.
            *args: Forwarded to :py:func:`specplot.specplot`.
            **kwargs: Forwarded to :py:func:`specplot.specplot`.

        Example:

            >>> from colorspace import diverging_hcl
            >>> pal = diverging_hcl()
            >>> pal.specplot()
            >>> pal.specplot(rgb = False)
        """

        from .specplot import specplot
        specplot(self.colors(n), *args, **kwargs)

        return

    def swatchplot(self, n = 7, *args, **kwargs):
        """Interfacing the :py:func:`swatchplot.swatchplot` function.
        Plotting the spectrum of the current color palette.

        Args:
            n (int): Number of colors, defaults to 7.

        Example:

            >>> from colorspace import diverging_hcl
            >>> pal = diverging_hcl()
            >>> pal.swatchplot()
            >>> pal.swatchplot(n = 21)
        """

        from .swatchplot import swatchplot
        swatchplot(self.colors(n))


    def name(self):
        """Get name of color palette.

        Returns:
            Returns the name of the palette, string.
        """
        return self._name

    def get(self, key):
        """Returns one specific item of the palette settings,
        e.g., the current value for ``h1`` or ``l2``.
        If not existing a `None` will be returned.

        Args:
            key (str): Name of the setting to be returned.

        Returns:
            None if ``key`` does ont exist, else the current value will be
            returned.

        Example:

            >>> from colorspace.palettes import rainbow_hcl
            >>> a = rainbow_hcl()
            >>> a.get("h1")
            >>> a.get("c1")
            >>> a.get("l1")
            >>> a.get("not_defined")
        """
        if not key in self.settings.keys():
            return None
        return self.settings[key]

    def show_settings(self):
        """Shows the current settings (table like print to stdout). Should more be
        seen as a development method than a very useful thing.

        Example:

            >>> from colorspace.palettes import rainbow_hcl
            >>> a = rainbow_hcl(10)
            >>> a.show_settings()
        """

        def get(key):
            val = self.get(key)
            if val is None:
                return "    ---"
            elif isinstance(val, int):
                return "{:7d}".format(val)
            elif isinstance(val, bool):
                return "{:7s}".format("True" if val else "False")
            else:
                return "{:7.1f}".format(val)

        from .palettes import divergingx_hcl

        # Not very pretty ...
        if not isinstance(self, divergingx_hcl):
            print("Class:  {:s}".format(self.__class__.__name__))
            print("h1    {:s}    ".format(get("h1"))),
            print("h2    {:s}    ".format(get("h2")))
            print("c1    {:s}    ".format(get("c1"))),
            print("c2    {:s}    ".format(get("c2")))
            print("cmax  {:s}    ".format(get("cmax"))),
            print("l1    {:s}    ".format(get("l1"))),
            print("l2    {:s}    ".format(get("l2")))
            print("p1    {:s}    ".format(get("p1"))),
            print("p2    {:s}    ".format(get("p2")))
            print("fixup {:s}    ".format(get("fixup")))
        else:
            print("Class:  {:s}".format(self.__class__.__name__))
            print("h1    {:s}    ".format(get("h1"))),
            print("h2    {:s}    ".format(get("h2")))
            print("h3    {:s}    ".format(get("h3"))),
            print("c1    {:s}    ".format(get("c1"))),
            print("c2    {:s}    ".format(get("c2")))
            print("c3    {:s}    ".format(get("c3")))
            print("cmax1 {:s}    ".format(get("cmax1"))),
            print("cmax2 {:s}    ".format(get("cmax2"))),
            print("l1    {:s}    ".format(get("l1"))),
            print("l2    {:s}    ".format(get("l2")))
            print("l3    {:s}    ".format(get("l3")))
            print("p1    {:s}    ".format(get("p1"))),
            print("p2    {:s}    ".format(get("p2")))
            print("p3    {:s}    ".format(get("p3"))),
            print("p4    {:s}    ".format(get("p4")))
            print("fixup {:s}    ".format(get("fixup")))


    # Better input handling
    def _checkinput_(self, dtype, length_min = None, length_max = None,
            recycle = False, nansallowed = False, **kwargs):
        """Used to check/convert/extend input arguments to the palette functions.

        Args:
            dtype (object): E.g. int or float, the type in which the inputs
                should be converted.
            length_min (None, int): Optional. Minimum length of the input data.
                If not fulfilled and ``recycle`` is set to True it expands the
                input to ``length_min``. Defaults to None, see also ``length_max``.
            lenth_max (None, int): Optional. Maximum length of the input data.
                If longer, the script will stop. If not set (default is ``None``)
                only the ``length_min`` will be checked.
            recycle (bool): if set to ``True`` the user inputs will be recycled
                to match the expected number of inputs, defaults to False.
            nansallowed (bool): if False an error will be raised if the final
                arguments contain ``numpy.nan`` values. Else ``numpy.nan``s are
                passed trough and will be returned, defaults to False.
            **kwargs: List of named arguments, the ones to be checked. If only
                one is given the function returns the values of this specific
                input. If multiple arguments are handed over a dict will be
                returned with the names corresponding to the user input.

        Returns:
            If ``kwargs`` is of length one the values of this specific variable
            will be returned. If multiple ``kwargs`` arguments are set a dict is
            returned.  Note that ``None`` will simply stay ``None``.  The function
            raises errors if the user inputs do not match the required
            specifications.
        """

        # Support function
        def fun(key, value, dtype, length_min, length_max, recycle, nansallowed):

            from numpy import vstack, asarray, isnan, nan, any, atleast_1d

            # If None
            if value == None: return value

            # Converting the data
            try:
                value = asarray([value], dtype = dtype).flatten()
            except Exception as e:
                msg = "wrong input for \"{:s}\" to {:s}: {:s}".format(key,
                        self.__class__.__name__, str(e))
                raise ValueError(msg)

            # Not enough input values, check if we are allowed to
            # recycle.
            if length_min and len(value) < length_min:
                # Input was too short: check if we are allowed to
                # recycle the value or not.
                if not recycle:
                    msg = "wrong length of input \"{:s}\", ".format(key) + \
                          "expected min {:d} elements, got {:d} ".format(length_min, len(value)) + \
                          "when calling {:s}".format(self.__class__.__name__)
                    raise ValueError(msg)
                else:
                    value = vstack([value] * length_min).flatten()[0:length_min]
            elif length_min and not length_max and len(value) > length_min:
                value = value[0:length_min]

            # Check if the input exceeds length_max if set
            if length_max and len(value) > length_max:
                msg = "wrong length of input \"{:s}\", ".format(key) + \
                      "expected max {:d} elements, got {:d} ".format(length_max, len(value)) + \
                      "when calling {:s}".format(self.__class__.__name__)
                raise ValueError(msg)
            # Cropping data if too much elements are given.
            elif length_max and len(value) > length_max:
                value = value[0:length_max]

            # Checking nan's
            if not nansallowed and any(isnan(value)):
                msg = "arguments for \"{:s}\" ".format(key) + \
                      "to function calling {:s} ".format(self.__class__.__name__) + \
                      "contain nan values: not allowed"
                raise ValueError(msg)

            # Return single value if length is set to 1.
            if len(value) == 1: value = value[0]

            return atleast_1d(value) # Return 1d array

        # Looping over all kwargs
        for key,value in kwargs.items():
            kwargs[key] = fun(key, value, dtype, length_min, length_max, recycle, nansallowed)

        # If only one kwarg was given: return values, else return dict.
        if len(kwargs) == 1:
            return kwargs[list(kwargs.keys())[0]]
        else:
            return kwargs



    def _check_inputs_(self, n, h, c, l, p, palette):

        from numpy import all

        # Convert input x into a list with elements of type
        # "totype".
        def tolist(x, totype, n, cls):
            # Converting inputs to list
            if not x:
                return None
            elif isinstance(x, float) or isinstance(x, int):
                x = [totype(x)]
            elif isinstance(x, list):
                x = [totype(e) for e in x]
            else:
                raise ValueError("don't know how to convert {:s} to list".format(type(x)))
            if not all([isinstance(e, totype) for e in x]):
                raise ValueError("problems with inputs for {:s}: {:s}".format(self.__class__.__name__, e))
            # Checking length
            if len(x) < n:   x = x * n
            elif len(x) > n: x = x[0:2]
            return x

        # Converts inputs to single values of "totype".
        def tovalue(x, totype, cls):
            if not x:
                return None
            elif isinstance(x, float) or isinstance(x, int):
                return totype(x)
            else:
                raise ValueError("problems with inputs for {:s}: {:s}".format(self.__class__.__name__, e))

        # If "h" is a string this is ment to be the palette
        # argument, switch "palette" and "h"
        if isinstance(h, str):
            palette = h; h = None 

        if isinstance(n, int) or isinstance(n, float):
            n = int(n)
        else:
            raise ValueError("input \"n\" to {:s} has to be a single integer".format(self.__class__.__name__))

        # For sequential hcl palettes
        if isinstance(self, sequential_hcl):
            n = tovalue(n, int, cls)
            h = tolist(h,  int, 2, cls)
            c = tolist(c,  int, 2, cls)
            l = tolist(l,  int, 2, cls)
            p = tolist(p,  float, 2, cls)
        # For sequential hcl palettes
        elif isinstance(self, diverging_hcl):
            n = tovalue(n, int, cls)
            h = tolist(h,  int, 2, cls)
            c = tovalue(c, int, cls)
            l = tolist(l,  int, 2, cls)
            p = tovalue(p, float, cls)

        # If "n" is set to small: exit
        if n <= 0:
            raise ValueError("input \"n\" to {:s} has to be a positive integer".format(self.__class__.__name__))

        return [n, h, c, l, p, palette]


    def cmap(self, n = 101, name = "custom_hcl_cmap"):
        """Allows to retrieve a matplotlib LinearSegmentedColormap color map.
        Clasically LinearSegmentedColormaps allow to retrieve a set of ``N``
        colors from a set of ``n`` colors where ``N >> n``. The matplotlib
        simply linearely interpolates between all ``n`` colors to extend
        the number of colors to ``N``.

        In case of :py:func:`colorspace.palettes.hclpalette` objects this is not necessary as
        :py:func:`colorspace.palettes.hclpalette` objects allow to retrieve ``N`` colors directly
        along well-specified Hue-Chroma-Luminance paths. Thus, this method
        returns a matplotlib color map with ``n==N`` colors. The linear 
        interpolation between the colors (as typically done by
        LinearSegmentedColormap) is not necessary. However, for convenience
        cmaps have been implemented such that you can easily use hcl based
        palettes in your existing workflow.

        Args:
            n (int): Number of colors the cmap should be based on; default is ``n = 101``.
            name (str): Name of the custom color map. Default is ``custom_hcl_cmap``

        Returns:
            Returns a ``LinearSegmentedColormap`` (cmap) to be used
            with the matplotlib library.
        """
        import matplotlib
        from matplotlib.colors import LinearSegmentedColormap
        from numpy import linspace, round, fmin, fmax

        cobj = self.colors(n, colorobject = True)
        cobj.to("sRGB")

        # Get coordinates
        pos = round(linspace(0,1,n), 6)
        # Fixup RGB colors if not within [0,1]
        r   = fmax(0, fmin(1, round(cobj.get("R"),   6)))
        g   = fmax(0, fmin(1, round(cobj.get("G"),   6)))
        b   = fmax(0, fmin(1, round(cobj.get("B"),   6)))

        # Create dict for cmap
        cdict = {'red':[], 'green':[], 'blue':[]}
        for i in range(0,n):
            j = i if not self._rev else n - i - 1
            cdict['red'].append(   (pos[i], r[j], r[j]) ) 
            cdict['green'].append( (pos[i], g[j], g[j]) )
            cdict['blue'].append(  (pos[i], b[j], b[j]) )

        cmap = LinearSegmentedColormap(name, cdict, n)
        return cmap



    def _chroma_trajectory(self, i, p1, c1, c2, cmax):
        """Helper function: Calculate linear or triangle trajectory for chroma dimension.

        Args:
            i (numpy array; float): Position across the palette, a sequence
                of values between 1 and 0. For diverging palettes this function
                is called twice, once for 1 to 0.5, and once for <0.5 t0 0.
            p1 (float): Power parameter p1.
            c1 (float): Chroma value of the left end of the color palette.
            c2 (float): Chroma value of the right end of the color palette.
            cmax (float or None): Max choma value.

        Returns:
            numpy array: Linear trajectory for the chroma color dimension.
        """

        def _linear_trajectory(i, c1, c2):
            return c2 - (c2 - c1) * i

        def _triangle_trajectory(i, j, c1, c2, cmax):
            from numpy import where, abs, linspace
            return where(i <= j,
                         c2 - (c2 - cmax) * i / j,
                         cmax - (cmax - c1) * abs((i - j) / (1 - j)))

        if cmax is None:
            C = _linear_trajectory(i**p1, c1, c2)
        else:
            # Calculate the position of the triangle point
            j = 1. / (1. + abs(cmax - c1) / abs(cmax - c2))
            if not j is None and (j < 0 or j > 1): j = None

            if j is None:  C = _linear_trajectory(i**p1, c1, c2)
            else:          C = _triangle_trajectory(i**p1, j, c1, c2, cmax)

        return C



# -------------------------------------------------------------------
# -------------------------------------------------------------------
class qualitative_hcl(hclpalette):
    """Qualitative HCL color palette.

    Args:
        h (float, int, or list): Hue values defining the 'color'. Qualitative color
            palettes require two hues. If more than two values are provided the first
            two will be used while the rest is ignored.  If input `h` is a string this
            argument acts like the `palette` argument (see `palette` input parameter).
            Can also be lambda functions or a list of lambda functions which take up
            one single argument `n` (number of colors; see default value).
        c (numeric): Chroma value (colorfullness), a single numeric value. If
            multiple values are provided only the first one will be used.
        l (numeric): luminance value (lightness), a single numeric value. If
            multiple values are provided only the first one will be used.
        fixup (bool): Only used when converting the HCL colors to hex.  Should RGB
            values outside the defined RGB color space be corrected?
        palette (None, string): Can be used to load a default diverging color
            qpalette specification. If the palette does not exist an exception will be
            qraised.  Else the settings of the palette as defined will be used to create
            qthe color palette.
        rev (bool): Should the color map be reversed? Default ``False``.
        **kwargs: Additional arguments to overwrite the h/c/l settings.  @TODO has
            to be documented.

    See Also:
        :py:class:`sequential_hcl`,
        :py:class:`diverging_hcl`,
        :py:class:`divergingx_hcl`,
        :py:class:`rainbow_hcl`,
        :py:class:`heat_hcl`,
        :py:class:`terrain_hcl`,
        :py:class:`diverging_hsv`,
        and :py:class:`rainbow`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object. Raises a set of errors if the parameters are
        misspecified. Note that the object is callable, the default object call can
        be used to return hex colors (identical to the ``.colors()`` method), see
        examples.

    Example:

        >>> from colorspace import diverging_hcl
        >>> a = qualitative_hcl()
        >>> a.colors(10)
        >>> b = qualitative_hcl("Dynamic")
        >>> b.colors(10)
        >>> # The standard call of the object also returns hex colors. Thus,
        >>> # you can make your code slimmer by calling:
        >>> qualitative_hcl("Dynamic")(10)


    TODO:
        Class does not allow for lambda function for h. Thus, the colors
        on both ends of a qualitative color map with ``h = [0, 360]`` are
        identical. See also palette definition (text files). I would need
        to allow for lambda functions which will require quite some adaptions
        of the current code (reading config files; _checkinput function; evaluation
        of the function whenever needed).

        Just adding lambda. Write tests for this.


    Raises:
        TypeError: If `h` is not a single int or float, or a list (see next).
        TypeError: If `h` is a list but not all elements are of type int, float, or 
            callable (lambda functions).
    """

    _name = "Qualitative"

    def __init__(self, h = [0, lambda n: 360. * (n - 1.) / n], c = 80, l = 60,
        fixup = True, palette = None, rev = False, **kwargs):

        # Store reverse flag
        self._rev = rev

        # If a string is given on "h": exchange with "palette".
        if isinstance(h, str):
            palette = h
            h       = [0, lambda n: 360. * (n - 1.) / n]

        # Custom check for 'h' as we also allow for lambda functions
        if not isinstance(h, (list, float, int)) and not callable(h):
            raise TypeError("Wrong type of input on argument 'h'.")
        else:
            if not isinstance(h, list): h = [h]
            for rec in h:
                if   callable(rec):                 pass
                elif isinstance(rec, (float, int)): pass
                else:
                    raise TypeError("Wrong type of input on argument 'h'.")

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            #h     = self._checkinput_(int,   2, False, False, h = h)
            c     = self._checkinput_(int,   1, False, False, c = c)
            l     = self._checkinput_(int,   1, False, False, l = l)
        except Exception as e:
            raise ValueError(str(e))


        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            from numpy import where
            pals = hclpalettes().get_palettes("Qualitative")
            idx  = where([x.name().upper().replace(" ", "") == palette.upper().replace(" ", "") for x in pals])[0]
            if len(idx) == 0:
                raise ValueError("palette {:s} is not a valid qualitative palette. ".format(palette) + \
                        "Choose one of: {:s}".format(", ".join([x.name() for x in pals])))
            pal = pals[idx[0]]

            # Allow to overrule few things
            for key,value in kwargs.items():
                if key in ["h1", "c1", "l1"]: pal.set({key: value})

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
            settings["c1"]    = c
            settings["l1"]    = l
            settings["fixup"] = fixup
            settings["rev"]   = rev

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in ["h1", "h2", "c1", "l1"]: settings[key] = value

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if not kwargs is None:
            if "settings" in kwargs.keys():
                for key,val in kwargs["settings"].items():
                    if key in settings.keys() and not val is None:
                        settings[key] = val

        # Save settings
        self.settings = settings


    def colors(self, n = 11, fixup = None, **kwargs):
        """Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned, defaults to 11.
            fixup (None, bool): should sRGB colors be corrected if they lie outside
                the defined color space?  If ``None`` the ``fixup`` parameter from the
                object will be used. Can be set to ``True`` or ``False`` to explicitly
                control the fixup here.
        """

        from numpy import repeat, linspace, asarray
        from numpy import vstack, transpose
        from . import colorlib

        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        # If either h1 or h2 is a lambda function: evaluate now.
        h1 = self.get("h1")(n) if callable(self.get("h1")) else self.get("h1")
        h2 = self.get("h2")(n) if callable(self.get("h2")) else self.get("h2")

        # Calculate the coordinates for our HCL color(s)
        L = repeat(self.get("l1"), n)
        C = repeat(self.get("c1"), n)
        H = linspace(h1, h2, n)

        # Create new HCL color object
        from .colorlib import HCL
        HCL = HCL(H, C, L)

        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HCL

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return [str(x) for x in HCL.colors(fixup = fixup, rev = rev)]


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class rainbow_hcl(qualitative_hcl):
    """HCL rainbow, a qualitative cyclic rainbow color palette with uniform
    luminance and chroma.

    Args:
        c (int): Chroma (colorfullness) of the color map ``[0-100+]``.
        l (int): Luminance (lightness) of the color map ``[0-100]``.
        start (int): Hue at which the rainbow should start.
        end (int): Hue at which the rainbow should end.
        gamma (float): Gamma value used for transfiromation from/to sRGB.
            @TODO implemented? Check!
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        rev (bool): Should the color map be reversed? Default ``False``.
        *args: Currently unused.
        **kwargs: Processed internally; can be used to overwrite ``h1``,
            ``h2``, ``c1``, ``l1``, ``l2`` and ``p1``.

    See Also:
        :py:class:`qualitative_hcl`,
        :py:class:`sequential_hcl`,
        :py:class:`diverging_hcl`,
        :py:class:`divergingx_hcl`,
        :py:class:`heat_hcl`,
        :py:class:`terrain_hcl`,
        :py:class:`diverging_hsv`,
        and :py:class:`rainbow`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the ``.colors()`` method),
        see examples.

    Example:

        >>> from colorspace import rainbow_hcl
        >>> pal = rainbow_hcl()
        >>> pal.colors(3); pal.colors(20)
        >>> # The standard call of the object also returns hex colors. Thus,
        >>> # you can make your code slimmer by calling:
        >>> rainbow_hcl("Dynamic")(10)
    """

    _allowed_parameters = ["h1", "h2", "c1", "l1", "l2", "p1"]
    _name = "Rainbow HCL"

    def __init__(self, c = 50, l = 70, start = 0, end = 360,
                 gamma = None, fixup = True, rev = False, *args, **kwargs):

        # Store reverse
        self._rev = rev

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            c     = self._checkinput_(int,   1, False, False, c = c)
            l     = self._checkinput_(int,   1, False, False, l = l)
            start = self._checkinput_(int,   1, False, False, start = start)
            end   = self._checkinput_(int,   1, False, False, end = end)
        except Exception as e:
            raise ValueError(str(e))

        # Save settins
        try:
            self.settings = {"h1": int(start), "h2": int(end),
                             "c1": int(c), "l1": int(l),
                             "fixup": bool(fixup)}
        except ValueError as e:
            raise ValueError("wrong inputs to {:s}: {:s}".format(
                self.__class__.__name__, str(e)))
        except Exception as e:
            raise Exception("in {:s}: {:s}".format(self.__class__.__name__, str(e)))

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if key in self._allowed_parameters:
                    settings[key] = val

# -------------------------------------------------------------------
# -------------------------------------------------------------------
class diverging_hcl(hclpalette):
    """Diverging HCL color palette.

    Args:
        h (list of numerics): Hue values (color), diverging color palettes should
            have different hues for both ends of the palette. If only one value is
            present it will be recycled ending up in a diverging color palette with the
            same colors on both ends.  If more than two values are provided the first
            two will be used while the rest is ignored.  If input ``h`` is a string
            this argument acts like the ``palette`` argument (see ``palette`` input
            parameter).
        c (numeric): Chroma value (colorfullness), a single numeric value. If two
            values are provided the first will be taken as `c1`, the second as `cmax`.
        l (list of numerics): luminance values (lightness). The first value is for
            the two ends of the color palette, the second one for the neutral center
            point. If only one value is given this value will be recycled.
        power (float): Power parameter for non-linear behaviour of the color
            palette.
        fixup (bool): Only used when converting the HCL colors to hex.  Should RGB
            values outside the defined RGB color space be corrected?
        palette (string): Can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be raised.
            Else the settings of the palette as defined will be used to create the
            color palette.
        rev (bool): Should the color map be reversed.
        *args: Currently unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.  @TODO has
            to be documented.

    See Also:
        :py:class:`qualitative_hcl`,
        :py:class:`sequential_hcl`,
        :py:class:`divergingx_hcl`,
        :py:class:`rainbow_hcl`,
        :py:class:`heat_hcl`,
        :py:class:`terrain_hcl`,
        :py:class:`diverging_hsv`,
        and :py:class:`rainbow`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the ``.colors()`` method),
        see examples.

    Example:

        >>> from colorspace import diverging_hcl
        >>> a = diverging_hcl()
        >>> a.colors(10)
        >>> b = diverging_hcl("Blue-Yellow 3")
        >>> b.colors(10)
        >>> # The standard call of the object also returns hex colors. Thus,
        >>> # you can make your code slimmer by calling:
        >>> diverging_hcl("Dynamic")(10)
    """

    _allowed_parameters = ["h1", "h2", "c1", "l1", "l2", "p1"]
    _name = "Diverging HCL"

    def __init__(self, h = [260, 0], c = 80, l = [30, 90],
        power = 1.5, fixup = True, palette = None, rev = False,
        *args, **kwargs):

        # Store reverse
        self._rev = rev

        if isinstance(h, str):
            palette = h; h = None
        if isinstance(power, int) or isinstance(power, float):
            power = [power]

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
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
            idx  = where([x.name().upper().replace(" ", "") == palette.upper().replace(" ", "") for x in pals])[0]
            if len(idx) == 0:
                raise ValueError("palette {:s} is not a valid diverging palette. ".format(palette) + \
                        "Choose one of: {:s}".format(", ".join([x.name() for x in pals])))
            pal = pals[idx[0]]

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in ["h1", "c1", "l1"]: pal.set(**{key: value})

            # Extending h2 if h1 = h2 (h2 None)
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
            if isinstance(c, ndarray):
                settings["c1"]    = c    if len(c) == 1 else c[0]
                if len(c) == 2: settings["cmax"] = c[1]
            else:
                settings["c1"]    = c
            settings["l1"]    = l[0]
            settings["l2"]    = l[1]
            if isinstance(power, ndarray):
                settings["p1"]    = power if len(power) == 1 else power[0]
                if len(power) == 2: settings["p2"] = power[1]
            else:
                settings["p1"]    = power
            settings["fixup"] = fixup
            settings["rev"]   = rev

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if key in self._allowed_parameters:
                    settings[key] = val

        # Save settings
        self.settings = settings


    # Return hex colors
    def colors(self, n = 11, fixup = True, alpha = None, **kwargs):
        """Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned.
            fixup (None, bool): Should sRGB colors be corrected if they lie
                outside the defined color space?  If ``None`` the ``fixup``
                parameter from the object will be used. Can be set to ``True`` or
                ``False`` to explicitly control the fixup here.
            alpha (None, float): Float (single value) or vector of floats in the
                range of ``[0.,1.]`` for alpha transparency channel (``0.`` means full
                transparency, ``1.`` opaque).  If a single value is provided it will be
                applied to all colors, if a vector is given the length has to be ``n``.
        """

        # Sanity checks
        if not isinstance(n, int):
            raise TypeError("Argument `n` must be integer.")
        elif not n > 1:
            raise TypeError("Argument `n` must be integer larger than 1.")

        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        from numpy import abs, ceil, linspace, power, repeat, arange, fmax, delete
        from numpy import asarray, ndarray, ndenumerate, concatenate, flip
        from numpy import vstack, transpose
        from . import colorlib

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

        # Calculate H/C/L
        rval = linspace(1., -1., n)

        L = l2 - (l2 - l1) * power(abs(rval), p2)
        H = ndarray(n, dtype = "float")
        for i,val in ndenumerate(rval): H[i] = h1 if val > 0 else h2

        # Calculate the trajectory for the chroma dimension
        i = fmax(0, arange(1., -1e-10, -2. / (n - 1.)))
        C = self._chroma_trajectory(i, p1, c1, c2, cmax)
        C = fmax(0., concatenate((C, flip(C))))

        # Non-even number of colors? We need to remove one.
        if n % 2 == 1: C = delete(C, int(ceil(n / 2.)))

        # Alpha handling
        if isinstance(alpha, float):
            alpha = repeat(alpha, n)
        elif isinstance(alpha, list):
            try:
                asarray(alpha, dtype = float)
            except Exception as e:
                raise ValueError("alpha values provided to {:s}".format(self.__class__.__name__) + \
                        "not of float-type: {:s}".format(str(e)))

        # Create new HCL color object
        from .colorlib import HCL
        HCL = HCL(H, C, L, alpha)

        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HCL

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return [str(x) for x in HCL.colors(fixup = fixup, rev = rev)]




# -------------------------------------------------------------------
# -------------------------------------------------------------------
class divergingx_hcl(hclpalette):
    """Diverging HCL color palette.

    Args:
        h (list of float or int): Hue values (color), divergingx color palettes should
            have different hues for both ends and the center of the palette.
            For this class three values must be provided. If input ``h`` is a string
            this argument acts like the ``palette`` argument (see ``palette`` input
            parameter).
        c (list of float or int): Chroma value (colorfullness), list of floats. In case two
            values are provided the firt is taken as `c1` and `c3` while the second
            one is used for `c2` (center value). When three or more are provided
            the first three are used for `c1`, `c2`, and `c3`. `cmax1` and `cmax2`
            have to provided as extra arguments.
        l (list of float or int): luminance values (lightness). In case two
            values are provided the firt is taken as `c1` and `c3` while the second
            one is used for `c2` (center value). When three or more are provided
            the first three are used for `c1`, `c2`, and `c3`. `cmax1` and `cmax2`
            have to provided as extra arguments.
        power (list of float): Power parameters for non-linear behaviour of the color
            palette. Up to four values can be provided for `p1`, `p2`, `p3`, `p4`.
            If two values are provided `power[0]` will be used for `p1` and `p4`
            while `power[1]` is used for `p2` and `p3` (symmetric).
        cmax (list of float or int): Maximum chroma. If one value is provided this
            will be used for both, `cmax1` and `cmax2`. Else the first two elements
            will be used for `cmax1` and `cmax2` respectively.
        fixup (bool): Only used when converting the HCL colors to hex.  Should RGB
            values outside the defined RGB color space be corrected?
        palette (string): Can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be raised.
            Else the settings of the palette as defined will be used to create the
            color palette.
        rev (bool): Should the color map be reversed.
        *args: Currently unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.  @TODO has
            to be documented.

    See Also:
        :py:class:`qualitative_hcl`,
        :py:class:`sequential_hcl`,
        :py:class:`diverging_hcl`,
        :py:class:`rainbow_hcl`,
        :py:class:`heat_hcl`,
        :py:class:`terrain_hcl`,
        :py:class:`diverging_hsv`,
        and :py:class:`rainbow`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the ``.colors()`` method),
        see examples.

    Example:

        >>> from colorspace import diverging_hcl
        >>> a = diverging_hcl()
        >>> a.colors(10)
        >>> b = diverging_hcl("Blue-Yellow 3")
        >>> b.colors(10)
        >>> # The standard call of the object also returns hex colors. Thus,
        >>> # you can make your code slimmer by calling:
        >>> diverging_hcl("Dynamic")(10)
    """

    _allowed_parameters = ["h1", "h2", "h3", "c1", "c2", "c3",
                           "l1", "l2", "l3", "p1", "p2", "p3", "p4",
                           "cmax1", "cmax2"]
    _name = "DivergingX HCL"

    def __init__(self, h = [192, 77, 21], c = [40, 35, 100], l = [50, 95, 50], \
                 power = [1.0, 1.0, 1.2, 1.0], cmax = 20, \
                 fixup = True, palette = None, rev = False, *args, **kwargs):


        # Store reverse
        self._rev = rev

        if isinstance(h, str):
            palette = h; h = None
        if isinstance(power, int) or isinstance(power, float):
            power = [power]

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   3, 3, False, False, h = h)
            c     = self._checkinput_(int,   2, 3, False, False, c = c)
            l     = self._checkinput_(int,   2, 3, False, False, l = l)
            power = self._checkinput_(float, 2, 4, False, False, power = power)
            cmax  = self._checkinput_(float, 1, 2, False, False, cmax = cmax)
        except Exception as e:
            raise ValueError(str(e))

        if len(c) == 2: c = [c[0], c[1], c[0]]
        if len(l) == 2: l = [l[0], l[1], l[0]]
        if len(power) < 4: power = [power[0], power[1], power[1], power[0]]
        if len(cmax) < 2:  cmax  = [cmax[0], cmax[0]]

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            from .hcl_palettes import divergingx_palettes
            from numpy import where
            pals = divergingx_palettes().get_palettes("Divergingx")
            idx  = where([x.name().upper().replace(" ", "") == palette.upper().replace(" ", "") for x in pals])[0]
            if len(idx) == 0:
                raise ValueError("palette {:s} is not a valid divergingx palette. ".format(palette) + \
                        "Choose one of: {:s}".format(", ".join([x.name() for x in pals])))
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
                raise Exception("Third hue coordinate (h3) must be specified.")
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
                if key in self._allowed_parameters:
                    settings[key] = val

        # Save settings
        self.settings = settings


    # Return hex colors
    def colors(self, n = 11, fixup = True, alpha = None, **kwargs):
        """Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned.
            fixup (None, bool): Should sRGB colors be corrected if they lie
                outside the defined color space?  If ``None`` the ``fixup``
                parameter from the object will be used. Can be set to ``True`` or
                ``False`` to explicitly control the fixup here.
            alpha (None, float): Float (single value) or vector of floats in the
                range of ``[0.,1.]`` for alpha transparency channel (``0.`` means full
                transparency, ``1.`` opaque).  If a single value is provided it will be
                applied to all colors, if a vector is given the length has to be ``n``.

        Todo:
            Move the function `get_one_side` to the `hclpalette` class. Rename it
            to `seqhcl` or something and also make use of this in sequential_hcl
            as it is basically the same.
        """

        # Sanity checks
        if not isinstance(n, int):
            raise TypeError("Argument `n` must be integer.")
        elif not n > 1:
            raise TypeError("Argument `n` must be integer larger than 1.")

        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        from numpy import abs, ceil, linspace, power, repeat, arange, fmax, delete
        from numpy import asarray, ndarray, ndenumerate, concatenate, flip
        from numpy import vstack, transpose
        from . import colorlib

        # Calculate H/C/L by basically calculating the sequential palette twice;
        # once for each side.

        # Helper function to get the two sides (multi-hue sequential)
        def get_one_side(n, ha, hb, ca, cb, la, lb, pa, pb, cmax):
            # Calculate H/C/L
            rval = linspace(1., 0., n)

            # Hue and Luminance
            H = hb - (hb - ha) * rval
            L = lb - (lb - la) * power(rval, pb)

            # Calculate the trajectory for the chroma dimension
            i = linspace(1., 0., n2)
            C = self._chroma_trajectory(i, pa, ca, cb, cmax)

            return [H, C, L]

        # n2 is half the number of colors, thus the number of colors on each of the two sides.
        n2 = int(ceil(n / 2))

        # Calculate H/C/L coordinates for both sides (called 'a' and 'b' not to get
        # confused with the numbering of the parameters).
        Ha, Ca, La = get_one_side(n2, ha = self.get("h1"), hb = self.get("h2"), 
                                      ca = self.get("c1"), cb = self.get("c2"),
                                      la = self.get("l1"), lb = self.get("l2"),
                                      pa = self.get("p1"), pb = self.get("p2"),
                                      cmax = self.get("cmax1"))
        Hb, Cb, Lb = get_one_side(n2, ha = self.get("h3"), hb = self.get("h2"), 
                                      ca = self.get("c3"), cb = self.get("c2"),
                                      la = self.get("l3"), lb = self.get("l2"),
                                      pa = self.get("p3"), pb = self.get("p4"),
                                      cmax = self.get("cmax2"))

        # In case the user requested an odd number of colors we need to
        # cut away one of one of the two sides (remove it from 'b').
        if not n == (2 * n2):
            Hb = Hb[:-1]
            Cb = Cb[:-1]
            Lb = Lb[:-1]

        # Concatenate the two sides
        H = concatenate((Ha, Hb[::-1]))
        C = concatenate((Ca, Cb[::-1]))
        L = concatenate((La, Lb[::-1]))

        # Create new HCL color object
        from .colorlib import HCL
        HCL = HCL(H, C, L, alpha)

        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HCL

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return [str(x) for x in HCL.colors(fixup = fixup, rev = rev)]




# -------------------------------------------------------------------
# -------------------------------------------------------------------
class sequential_hcl(hclpalette):
    """Sequential HCL color palette.

    Args:
        h (numeric): Hue values (color). If only one value is given the value
            is recycled which yields a single-hue sequential color palette.  If
            input `h` is a string this argument acts like the `palette` argument
            (see `palette` input parameter).
        c (numeric list): Chroma values (colorfullness), numeric of length one
            (constant chroma), two (linear), or three (advanced; [c1, c2, cmax]).
        l (numeric list): Luminance values (luminance), numeric of length two.
            If multiple values are provided only the first one will be used.
        power (numeric, numeric list): Power parameter for non-linear behaviour
            of the color palette. One or two values can be provided.
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        palette (string): Can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be
            raised.  Else the settings of the palette as defined will be used to
            create the color palette.
        rev (bool): Should the color map be reversed.
        *args: Currently unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.

    See Also:
        :py:class:`qualitative_hcl`,
        :py:class:`diverging_hcl`,
        :py:class:`divergingx_hcl`,
        :py:class:`rainbow_hcl`,
        :py:class:`heat_hcl`,
        :py:class:`terrain_hcl`,
        :py:class:`diverging_hsv`,
        and :py:class:`rainbow`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the ``.colors()`` method),
        see examples.

    Example:

        >>> from colorspace import sequential_hcl
        >>> a = sequential_hcl()
        >>> a.colors(10)
        >>> b = sequential_hcl("Reds")
        >>> b.colors(10)
        >>> # The standard call of the object also returns hex colors. Thus,
        >>> # you can make your code slimmer by calling:
        >>> sequential_hcl("Dynamic")(10)
    """

    # Allowed to overwrite via **kwargs
    _allowed_parameters = ["h1", "h2", "c1", "c2", "cmax", "l1", "l2", "p1", "p2"]
    _name = "Sequential HCL"

    def __init__(self, h = 260, c = [80, 0], l = [30, 90],
        power = 1.5, fixup = True, palette = None, rev = False,
        *args, **kwargs):

        # Save reverse flag
        self._rev = rev

        # If input "h" is a string: exchange with "palette"
        if isinstance(h, str):
            palette = h; h = None

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

        # For handy use of the function
        if isinstance(h,str):
            palette = h; h = None

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            from numpy import where
            pals = hclpalettes().get_palettes("Sequential")
            idx  = where([x.name().upper().replace(" ", "") == palette.upper().replace(" ", "") for x in pals])[0]
            if len(idx) == 0:
                raise ValueError("palette {:s} is not a valid sequential palette. ".format(palette) + \
                        "Choose one of: {:s}".format(", ".join([x.name() for x in pals])))
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
            #settings["h2"]        = h[0] if len(h) == 1 else h[1]
            if len(c) == 3:
                settings["c1"]    = c[0]
                settings["c2"]    = c[1]
                settings["cmax"]  = c[2]
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
                if key in self._allowed_parameters:
                    settings[key] = val

        if isinstance(settings["h2"], type(None)): settings["h2"] = settings["h1"]

        # Save settings
        self.settings = settings


    # Return hex colors
    def colors(self, n = 11, fixup = True, **kwargs):
        """Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned.
            fixup (None, bool): Should sRGB colors be corrected if they lie
                outside the defined color space?  If ``None`` the ``fixup``
                parameter from the object will be used. Can be set to ``True`` or
                ``False`` to explicitly control the fixup here.
        """

        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        from numpy import abs, linspace, power, asarray, ndarray, ndenumerate
        from numpy import vstack, transpose, where
        from . import colorlib

        # Calculate H/C/L
        rval = linspace(1., 0., n)
        p1   = self.get("p1")
        p2   = p1 if self.get("p2") is None else self.get("p2")
        c1   = self.get("c1")
        c2   = 0 if self.get("c2") is None else self.get("c2")
        cmax = None if not self.get("cmax") else self.get("cmax")
        l1   = self.get("l1")
        l2   = l1 if self.get("l2") is None else self.get("l2")
        h1   = self.get("h1")
        h2   = h1 if self.get("h2") is None else self.get("h2")

        # Hue and Luminance
        H = h2 - (h2 - h1) * rval
        L = l2 - (l2 - l1) * power(rval, p2)

        # Calculate the trajectory for the chroma dimension
        i = linspace(1., 0., n)
        C = self._chroma_trajectory(i, p1, c1, c2, cmax)

        # Create new HCL color object
        from .colorlib import HCL
        HCL = HCL(H, C, L)

        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HCL

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return [str(x) for x in HCL.colors(fixup = fixup, rev = rev)]


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class heat_hcl(sequential_hcl):
    """HEAT hcl, a sequential color palette.

    Args:
        h (list of int): Hue parameters (h1/h2).
        c (list of int): Chroma parameters (c1/c2).
        l (int): Luminance parameters (l1/l2).
        power (list of float): Power parameters (p1/p2).
        gamma (float): Gamma value used for transfiromation from/to sRGB.
            @TODO implemented? Check!
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        rev (bool): Should the color map be reversed.
        *args: Currently unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.

    See Also:
        :py:class:`qualitative_hcl`,
        :py:class:`sequential_hcl`,
        :py:class:`diverging_hcl`,
        :py:class:`divergingx_hcl`,
        :py:class:`rainbow_hcl`,
        :py:class:`terrain_hcl`,
        :py:class:`diverging_hsv`,
        and :py:class:`rainbow`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the ``.colors()`` method),
        see examples.

    Example:

        >>> from colorspace.palettes import heat_hcl
        >>> pal = heat_hcl()
        >>> pal.colors(3); pal.colors(20)
    """


    _allowed_parameters = ["h1", "h2", "c1", "c2", "l1", "l2", "p1", "p2"]
    _name = "Heat HCL"

    def __init__(self, h = [0, 90], c = [100, 30], l = [50, 90], power = [1./5., 1.],
                 fixup = True, rev = False, *args, **kwargs):

        # Save reverse flag
        self._rev = rev

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   2, False, False, h = h)
            c     = self._checkinput_(int,   2, False, False, c = c)
            l     = self._checkinput_(int,   2, False, False, l = l)
            power = self._checkinput_(float, 2, False, False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # Save settins
        try:
            self.settings = {"h1": int(h[0]), "h2": int(h[1]),
                             "c1": int(c[0]), "c2": int(c[1]),
                             "l1": int(l[0]), "l2": int(l[1]),
                             "p1": power[0],  "p2": power[1],
                             "fixup": bool(fixup)}
        except ValueError as e:
            raise ValueError("wrong inputs to {:s}: {:s}".format(
                self.__class__.__name__, str(e)))
        except Exception as e:
            raise Exception("in {:s}: {:s}".format(self.__class__.__name__, str(e)))

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if key in self._allowed_parameters:
                    settings[key] = val


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class terrain_hcl(sequential_hcl):
    """HCL terrain colors, a sequential palette.

    Args:
        h (list of int): Hue parameters (h1/h2).
        c (list of int): Chroma parameters (c1/c2).
        l (int): Luminance parameters (l1/l2).
        power (list of float): Power parameters (p1/p2).
        gamma (float): Gamma value used for transfiromation from/to sRGB.
            @TODO implemented? Check!
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        rev (bool): Should the color map be reversed.
        *args: unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.

    See Also:
        :py:class:`qualitative_hcl`,
        :py:class:`sequential_hcl`,
        :py:class:`diverging_hcl`,
        :py:class:`divergingx_hcl`,
        :py:class:`rainbow_hcl`,
        :py:class:`heat_hcl`,
        :py:class:`diverging_hsv`,
        and :py:class:`rainbow`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the ``.colors()`` method),
        see examples.

    Example:

        >>> from colorspace import terrain_hcl
        >>> pal = terrain_hcl()
        >>> pal.colors(3); pal.colors(20)
    """

    _allowed_parameters = ["h1", "h2", "c1", "c2", "l1", "l2", "p1", "p2"]
    _name = "Terrain HCL"

    def __init__(self, h = [130, 0], c = [80, 0], l = [60, 95], power = [1./10., 1.],
                 fixup = True, rev = False, *args, **kwargs):

        # Save reverse flag
        self._rev = rev

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   2, False, False, h = h)
            c     = self._checkinput_(int,   2, False, False, c = c)
            l     = self._checkinput_(int,   2, False, False, l = l)
            power = self._checkinput_(float, 2, False, False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # Save settins
        try:
            self.settings = {"h1": int(h[0]), "h2": int(h[1]),
                             "c1": int(c[0]), "c2": int(c[1]),
                             "l1": int(l[0]), "l2": int(l[1]),
                             "p1": power[0],  "p2": power[1],
                             "fixup": bool(fixup)}
        except ValueError as e:
            raise ValueError("wrong inputs to {:s}: {:s}".format(
                self.__class__.__name__, str(e)))
        except Exception as e:
            raise Exception("in {:s}: {:s}".format(self.__class__.__name__, str(e)))

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if key in self._allowed_parameters:
                    settings[key] = val


class diverging_hsv(hclpalette):
    """Diverging HSV color palette.

    Args:
        h (list of numerics): Hue values, diverging color palettes should have
            different hues for both ends of the palette. If only one value is present
            it will be recycled ending up in a diverging color palette with the same
            colors on both ends.  If more than two values are provided the first two
            will be used while the rest is ignored.  If input ``h`` is a string this
            argument acts like the ``palette`` argument (see ``palette`` input
            parameter).
        s (float): Saturation value for the two ends of the palette.
        v (float): Value (the HSV value) of the two ends of the palette.
        power (numeric): Power parameter for non-linear behaviour of the color
            palette.
        fixup (bool): Only used when converting the HCL colors to hex.  Should
            RGB values outside the defined RGB color space be corrected?
        rev (bool): Should the color map be reversed.
        *args: Unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.

    See Also:
        :py:class:`qualitative_hcl`,
        :py:class:`sequential_hcl`,
        :py:class:`diverging_hcl`,
        :py:class:`divergingx_hcl`,
        :py:class:`rainbow_hcl`,
        :py:class:`heat_hcl`,
        :py:class:`terrain_hcl`,
        and :py:class:`rainbow`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the ``.colors()`` method),
        see examples.

    Example:

        >>> from colorspace import diverging_hsv
        >>> a = diverging_hsv()
        >>> a.colors(10)
    """

    _allowed_parameters = ["h1", "h2", "s", "v"]
    _name = "Diverging HSV"

    def __init__(self, h = [240, 0], s = 1., v = 1., power = 1.,
        fixup = True, rev = False, *args, **kwargs):

        # Save reverse flag
        self._rev = rev

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   2, True,  False, h = h)
            s     = self._checkinput_(float, 1, False, False, s = s)
            v     = self._checkinput_(float, 1, False, False, v = v)
            power = self._checkinput_(float, 1, True,  False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # Save settins
        try:
            self.settings = {"h1": int(h[0]), "h2": int(h[1]),
                             "s":  s,  "v": v,  "power": power,
                             "fixup": bool(fixup)}
        except ValueError as e:
            raise ValueError("wrong inputs to {:s}: {:s}".format(
                self.__class__.__name__, str(e)))
        except Exception as e:
            raise Exception("in {:s}: {:s}".format(self.__class__.__name__, str(e)))

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if key in self._allowed_parameters:
                    settings[key] = val



    # Return hex colors
    def colors(self, n = 11, fixup = True, **kwargs):
        """Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned.
            fixup (None, bool): Should sRGB colors be corrected if they lie
                outside the defined color space?  If ``None`` the ``fixup``
                parameter from the object will be used. Can be set to ``True`` or
                ``False`` to explicitly control the fixup here.
        """

        from numpy import linspace, power, abs, repeat
        from numpy import ndarray, ndenumerate

        # Calculate palette
        rval = linspace(-self.get("s"), self.get("s"), n)
        H = ndarray(n, dtype = "float")
        for i,val in ndenumerate(rval):
            H[i] = self.get("h1") if val > 0 else self.get("h2")
        S = power(abs(rval), self.get("power"))
        V = repeat(self.get("v"), n)

        from .colorlib import HSV
        HSV = HSV(H, S, V)

        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HSV

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return [str(x) for x in HSV.colors(fixup = fixup, rev = rev)]



# -------------------------------------------------------------------
# -------------------------------------------------------------------
class rainbow(hclpalette):
    """Infamous rainbow palette.

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

    See Also:
        :py:class:`qualitative_hcl`,
        :py:class:`sequential_hcl`,
        :py:class:`diverging_hcl`,
        :py:class:`divergingx_hcl`,
        :py:class:`rainbow_hcl`,
        :py:class:`heat_hcl`,
        :py:class:`terrain_hcl`,
        and :py:class:`diverging_hsv`.
        All inherit from :py:class:`hclpalette`.

    Returns:
        Initialize new object, no return. Raises a set of errors if the parameters
        are misspecified. Note that the object is callable, the default object call
        can be used to return hex colors (identical to the ``.colors()`` method),
        see examples.

    Example:


    Raises:
        ValueError: If `s` or `v` are not single floating point values (or integers)
            in the range of `[0., 1.]`.
        ValueError: If `start` and `end` are not float/int in `[0., 1.]` or functions.
        ValueError: If `rev` is not boolean `True` or `False`.
    """

    _allowed_parameters = ["s", "v", "start", "end"]
    _name = "Diverging HCL"

    def __init__(self, s = 1, v = 1, start = 0, end = lambda n: max(1., n - 1.) / n,
        rev = False, *args, **kwargs):

        # Store reverse
        self._rev = rev

        # Doing all the sanity checks.
        if not isinstance(s, (float, int)): raise ValueError("Input 's' must be float.")
        if not isinstance(v, (float, int)): raise ValueError("Input 'v' must be float.")
        if s < 0. or s > 1.:                raise ValueError("Input 's' must be in [0, 1].")
        if v < 0. or v > 1.:                raise ValueError("Input 'v' must be in [0, 1].")
        # Check start and end. Either functions (lambda functions)
        # or a single floating point number in [0-1].
        if callable(start):                     pass
        elif isinstance(start, (float, int)):   start = float(start)
        if callable(end):                       pass
        elif isinstance(end, (float, int)):     end   = float(end)
        if not isinstance(rev, bool):       raise ValueError("Input 'rev' must be boolean.")

        # Store these settings
        self.settings = {"s": float(s), "v": float(v), "start": start, "end": end}


    # Return hex colors
    def colors(self, n = 11, alpha = None, **kwargs):
        """Returns the colors of the current color palette.

        Args:
            n (int): Number of colors which should be returned. Defaults to `11`.
            alpha (None, float): Float (single value) or vector of floats in the
                range of ``[0.,1.]`` for alpha transparency channel (``0.`` means full
                transparency, ``1.`` opaque).  If a single value is provided it will be
                applied to all colors, if a vector is given the length has to be ``n``.

        Raises:
            ValueError: If input `n` is not float/integer or smaller than 1.
        """

        from numpy import linspace, mod, repeat
        from .colorlib import HSV

        if not isinstance(n, (float, int)):
            raise ValueError("Input 'n' must be numeric (float/int).")
        n = int(n)
        if n < 1: raise ValueError("Input 'n' must be larger than 0.")

        # Evaluate start and end given 'n'
        start = self.settings["start"]
        start = start(n) if callable(start) else start
        end   = self.settings["end"]
        end   = end(n) if callable(end) else end

        h = mod(linspace(start, end, n), 1.)
        s = repeat(self.settings["s"], n)
        v = repeat(self.settings["v"], n)

        # Generate HSV colorobject
        HSV = HSV(h * 360., s, v)
        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HSV

        # Reversing colors if needed
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return [str(x) for x in HSV.colors(fixup = False, rev = rev)]


