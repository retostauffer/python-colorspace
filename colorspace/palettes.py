
import os
import sys


class palette(object):
    """palette(colors, name)

    Custom named color palette with a fixed number of colors.
    Used for :py:func:`hcl_palettes.swatchplot`.

    .. todo:
        Write docstrings.
    """

    def __init__(self, colors, name):
        self._colors = self._valid_hex(colors)
        if not isinstance(name, str):
            raise ValueError("argument name to {:s} ".format(self.__class__.__name__) + \
                    "has to be a string")
        self._name = name
    def __repr__(self):
        str = "Palette Name: {:s}\n".format(self.name()) + \
              "       Type: Custom palette\n" + \
              "       Number of colors: {:d}\n".format(len(self.colors()))
        return str
    def rename(self, name):
        if not isinstance(name, str):
            raise ValueError("argument name to {:s}.rename ".format(self.__class__.__name__) + \
                    "has to be a string")
        self._name = name
    def name(self):
        return self._name
    def colors(self, *args, **kwargs):
        return self._colors
    # Check if all values are valid hex colors
    def _valid_hex(self, colors):
        from re import match, compile
        from numpy import all
        pat   = compile("^#[0-9A-Fa-f]{6}([0-9]{2})?$")
        check = [match(pat, col) for col in colors]
        if not all(check):
            raise ValueError("not all colors are valid hex colors")
        return colors


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class defaultpalette(object):
    """defaultpalette(type, method, parameter, name, settings)

    Default color palette object. This object is not intended to be used by the
    user itself but is used to store the pre-defined color palettes contained
    in the package.

    Parameters
    ----------
    type : str
        palette type.
    method : str
        name of the method which has to be called to retrieve colors (e.g.,
        :py:class:`diverging_hcl`).
    name : str
        name of the color palette.  settings (`dict`): A dict object containing
        the parameter settings.
    """

    def __init__(self, type, method, name, settings):

        self._type_      = type
        self._name_      = name
        self._method_    = method
        self._settings_  = settings

    # Default representation of defaultpalette objects.
    def __repr__(self):
        """__repr__()
        
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
            if   isinstance(val,bool):   val = " True" if val else "False"
            elif isinstance(val,int):    val = "{:5d}".format(val)
            elif isinstance(val,float):  val = "{:5.1f}".format(val)
            res.append("         {:10s} {:s}".format(key,val))

        return "\n".join(res)

    def __call__(self, n = 11):
        """__call__(n = 11)

        Wrapper function for :py:func:`colors`.

        Returns
        -------
        list
            List of hex colors.
        """
        return self.colors(n)

    def method(self):
        """method()

        Return
        ------
        Returns the method (`str`, name of the function to be called
        to create the palette) of the palette.
        """
        return self._method_

    def type(self):
        """type()

        Return
        ------
        Returns the type (`str`) of the palette.
        """
        return self._type_

    def name(self):
        """name()
        Return
        ------
        Returns the name (`str`) of the palette.
        """
        return self._name_

    def rename(self, name):
        """rename(name)
        
        Allows to rename the palette.

        Parameters
        ----------
        name : str
            new palette name.
        """
        self._name_ = name

    def get(self, what):
        """get(what)

        Allows to load the settings of the palette for the
        different parameters (e.g., ``h1``, ``h2``, ...). Returns
        `None` if the parameter does not exist.
        Another method (:py:func:`set`) allows to set the
        parameters.

        Parameters
        ----------
        what : str
            Name of the parameter which should be extracted and returned from
            the settings of this color palette.

        Return
        ------
        Returns `None` if the parameter ``what`` cannot be found,
        else the value of the parameter ``what`` is returned.
        """
        if what in self._settings_.keys():
            return self._settings_[what]
        else:
            return None


    def set(self, **kwargs):
        """set(**kwargs)

        Allows to set/overwrite color palette parameters (e.g., ``h1``, ``h2``,
        ...).  Another method (:py:func:`get`) allows to retrieve the
        parameters.

        Parameters
        kwargs : ...
            a set of named arguments (``key = value`` pairs) where the key
            defines the parameter which should be overruled, value the
            corresponding value. Allowed value types are bool, int, and float.
        """
        for key,val in kwargs.items():
            if not key in self._settings_.keys():
                raise ValueError("{:s} named {:s}".format(self.__class__.__name__, self.name()) + \
                        "has no parameter called {:s}".format(key))
            # Else check current type specification and append
            # if possible (and convert to the new type).
            if not isinstance(val, int) and \
               not isinstance(val, float) and \
               not isinstance(val, bool):
                raise ValueError("input {:s} to {:s}".format(key, self.__class__.__name__) + \
                        " is of type {:s}. Only bool, int, and float allowed.".format(type(val)))
            if isinstance(val, bool):
                val = 1 if val else 0
            if isinstance(self._settings_[key],int):
                self._settings_[key] = int(val)
            elif isinstance(self._settings_[key],float):
                self._settings_[key] = int(val)
            else:
                raise Exception("whoops, some code needed here in {:s}.set".format(
                    self.__class__.__name__))

        self._settings_[key] = val

    def get_settings(self):
        """get_settings()

        Allows to get the current settings of the palette object.
        To retrieve single parameters use :py:func:`get`.

        Returns
        -------
        Returns a `dict` object with all parameter specification of this
        palette.
        """
        return self._settings_

    def colors(self, n = 11):
        """colors(n = 11)
        
        Load a set of ``n`` colors from this palette.  This method evaluates
        the `method` argument to generate a set of hex colors which will be
        returned.  Please note that it is possible that none-values will be
        returned if the fixup-setting is set to `False` (see
        :py:class:`colorlib.hexcols`).
        
        Parameters
        ----------
        n : int
            number of colors to be returned.

        Returns
        -------
        Returns a `list` object with all parameter names.
        """

        # Dynamically load color function
        mod  = __import__("colorspace")
        cfun = getattr(mod, self._method_)

        # Calling color method with arguments of this object. 
        from copy import copy
        args = copy(self.get_settings())

        # If Remove h1/h2 and store them in h
        for dim in ["h", "c", "l", "p"]:
            dim1 = "{:s}1".format(dim)
            dim2 = "{:s}2".format(dim)
            dim3 = "{:s}max".format(dim)
            dim = "power" if dim == "p" else dim
            # For Chroma we can have [c1, c2, cmax]
            if dim1 in args.keys() and dim2 in args.keys() and dim3 in args.keys():
                args[dim] = [args[dim1], args[dim2], args[dim3]]
                del args[dim1]; del args[dim2]; del args[dim3]
            elif dim1 in args.keys() and dim3 in args.keys():
                args[dim] = [args[dim1], args[dim1], args[dim3]] 
                del args[dim1]; del args[dim3]
            # For Hue, Luminance, and Power there are only two (for now)
            elif dim1 in args.keys() and dim2 in args.keys():
                args[dim] = [args[dim1], args[dim2]]
                del args[dim1]; del args[dim2]
            elif dim1 in args.keys():
                args[dim] = args[dim1]
                del args[dim1]
            elif dim2 in args.keys():
                args[dim] = args[dim2]
                del args[dim2]

        pal = cfun(**args)
        return pal.colors(n, fixup = True)



# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalettes(object):
    """hclpalettes(files = None)
    
    Prepares the pre-specified hclpalettes.  Reads the config files and creates
    a set of :py:class:`defaultpalette` objects.

    Parameters
    ----------
    files : None, str list
        If `None` (default) the default color palette configuration from within
        the package will be loaded. Technically, a list of file names (`str`)
        can be provided to load user-defined color palettes. Not yet tested!

    .. todo::
        Check if the files option is useful. If so, provide some
        more information about the config files and where/how to use.
    """
    def __init__(self, files = None):

        if files is None:
            resource_package = os.path.dirname(__file__)
            import glob
            files = glob.glob(os.path.join(resource_package, "palconfig", "*.conf"))


        for file in files:
            if not os.path.isfile(file):
                raise Exception("Cannot find file {:s}. Stop.".format(file))

        # Else trying to read the files. Returns a list with
        # palette configs.
        self._palettes_ = {}
        if len(files) == 0:
            raise ValueError("No palette config files found ({:s}.".format(self.__class__.__name__))

        # Else print debug message and read the config files
        for file in files:
            [palette_type, pals] = self._load_palette_config_(file)
            if not pals: continue

            # Append
            self._palettes_[palette_type] = pals

    def __repr__(self):
        """__repr__()

        Standard representation of the object.
        """
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
        """get_palette_types()

        Get all palette types.

        Returns
        -------
        list
            Returns a `list` of strings (`str`) with the names of all palette types
            or groups.
        """

        return list(self._palettes_.keys())

    def get_palettes(self, type_ = None):
        """get_palettes(type_ = None)

        Get all palettes of a specific type.

        Parmaeters
        ----------
        type_ : None, str
            Name of the palettes which should be returned. If set to `None`
            (default) all palettes will be returned. Names have to match but
            are not case sensitive.

        Returns
        -------
        Returns a `list` containing :py:class:`defaultpalette` objects.
        """
        if not isinstance(type_, str) and not type_ is None:
            raise ValueError("input type_ to {:s} has to be None or a single string.".format(
                self.__class__.__name__))

        if not type_:
            all = []
            for key,pals in self._palettes_.items():
                all += pals
            return all
        # Else reutnr palette if available
        else:
            found = None
            for t in self._palettes_.keys():
                if t.upper() == type_.upper():
                    found = t
                    break
            if not found:
                raise ValueError("No palettes for type \"{:s}\".".format(type_))
            else:
                type_ = found

        # Else return list with palettes
        return self._palettes_[type_]

    def get_palette(self, name):
        """get_palette(name)
        
        Get a palette with a specific name.

        Parameters
        ----------
        name : str
            name of the color palette which should be returned.

        Returns
        -------
        Returns an object of class :py:class:`defaultpalette` if a palette with
        the name as specified can be found.  Else an error will be dropped.
        """

        # Try to find the palette with the name 'name'
        take_pal = None
        for type_,pals in self._palettes_.items():
            # Looping over palettes
            for pal in pals:
                if pal.name() == name:
                    take_pal = pal
                    break;
            # If already found: break outer loop
            if take_pal: break;

        # Else return list with palettes
        return take_pal


    # Helper method to load the palette config files.
    def _load_palette_config_(self, file):

        import sys
        if sys.version_info.major < 3:
            from ConfigParser import ConfigParser
        else:
            from configparser import ConfigParser
        import re

        CNF = ConfigParser()
        CNF.read(file)

        # Reading type (or name)
        try:
            palette_type = CNF.get("main", "type")
            palette_method = CNF.get("main", "method")
        except Exception as e:
            raise Exception("misspecification in palconfig file {:s}: {:s}".format(file,str(e)))

        # The dictionary which will be returned.
        pals = []

        # Looping over all sections looking for palette specifications.
        for sec in CNF.sections():
            mtch = re.match("^palette\s+(.*)$", sec)
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
                elif key in ["p1","p2"]:
                    settings[key] = float(val)
                else:
                    settings[key] = int(val)

            pals.append(defaultpalette(palette_type, palette_method, name, settings))

        # Return dictionary with palettes
        if len(pals) == 0:
            return [None, None]
        else:
            return [palette_type, pals]





# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalette(object):
    """Hy, I am the base class.
    Is extended by the different HCL based color palettes such as
    the classes diverging_hcl, qualitative_hcl, rainbow_hcl, sequential_hcl,
    and maybe more in the future."""

    # Default call: return n hex colors
    def __call__(self, *args, **kwargs):
        """__call__(*args, **kwargs)

        Call interface, calls objects ``colors(...)`` method.
        """
        return self.colors(*args, **kwargs)

    def specplot(self, n = 180, *args, **kwargs):
        """specplot(n = 180, *args, **kwargs)

        Interfacing the :py:func:`specplot.specplot` function.
        Plotting the spectrum of the current color palette.

        Parameters
        ----------
        n : int
            number of colors.
        args : ...
            forwarded to :py:func:`specplot.specplot`.
        kwargs : ...
            forwarded to :py:func:`specplot.specplot`.

        Examples
        --------
        >>> from colorspace import diverging_hcl
        >>> pal = diverging_hcl()
        >>> pal.specplot()
        >>> pal.specplot(rgb = False)
        """

        from .specplot import specplot
        specplot(self.colors(n), *args, **kwargs)

        return

    def name(self):
        """name()

        Returns
        -------
        Returns the name of the palette, string.
        """
        return self._name

    def get(self, key):
        """get(key)
        
        Returns one specific item of the palette settings,
        e.g., the current value for ``h1`` or ``l2``.
        If not existing a `None` will be returned.

        Parameters
        ----------
        key : str
            name of the setting to be returned.

        Returns
        -------
        None if ``key`` does ont exist, else the current value will be
        returned.

        Examples
        --------
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
        """show_settings()
        
        Shows the current settings (table like print to stdout). Should more be
        seen as a development method than a very useful thing.

        Examples
        --------
        >>> from colorspace.palettes import rainbow_hcl
        >>> a = rainbow_hcl(10)
        >>> a.show_settings()
        """

        def get(key):
            val = self.get(key)
            if val is None:
                return " ------"
            elif isinstance(val, int):
                return "{:7d}".format(val)
            elif isinstance(val, bool):
                return "{:7s}".format("True" if val else "False")
            else:
                return "{:7.1f}".format(val)

        print("Class:  {:s}".format(self.__class__.__name__))
        print("h1    {:s}    ".format(get("h1"))),
        print("h2    {:s}    ".format(get("h2")))
        print("c1    {:s}    ".format(get("c1"))),
        print("c2    {:s}    ".format(get("c2")))
        print("l1    {:s}    ".format(get("l1"))),
        print("l2    {:s}    ".format(get("l2")))
        print("p1    {:s}    ".format(get("p1"))),
        print("p2    {:s}    ".format(get("p2")))
        print("fixup {:s}    ".format(get("fixup")))


    # Better input handling
    def _checkinput_(self, dtype, length_min = None, length_max = None,
            recycle = False, nansallowed = False, **kwargs):
        """_checkinput_(dtype, length = None, recycle = False,
            nansallowed = False, **kwargs)
            
        Used to check/convert/extend input arguments to the palette functions.

        Parameters
        ----------
        dtype : object
            e.g. int or float, the type in which the inputs should be
            converted.
        length_min : None, int
            optional. Minimum length of the input data. If not fulfilled and
            ``recycle`` is set to True it expands the input to ``length_min``.
            See also ``length_max``.
        lenth_max : None, int
            optional. Maximum length of the input data. If longer, the script
            will stop. If not set (default is ``Non``) only the ``length_min``
            will be checked.
        recycle : bool
            if set to ``True`` the user inputs will be recycled to match the
            expected number of inputs.
        nansallowed : bool
            if False an error will be raised if the final arguments contain
            ``numpy.nan`` values. Else ``numpy.nan``s are passed trough and will be returned.
        kwargs : ...
            list of named arguments, the ones to be checked. If only one is
            given the function returns the values of this specific input. If
            multiple arguments are handed over a dict will be returned with the
            names corresponding to the user input.

        Returns
        -------
        If ``kwargs`` is of length one the values of this specific variable
        will be returned. If multiple ``kwargs`` arguments are set a dict is
        returned.  Note that ``None`` will simply stay ``None``.  The function
        raises errors if the user inputs do not match the required
        specifications.
        """

        # Support function
        def fun(key, value, dtype, length_min, length_max, recycle, nansallowed):

            from numpy import vstack, asarray, isnan, nan, any

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

            return value

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


    def cmap(self, n = 51, name = "custom_hcl_cmap"):
        '''cmap(n = 51, name = "custom_hcl_cmap")

        Allows to retrieve a matplotlib LinearSegmentedColormap color map.
        Clasically LinearSegmentedColormaps allow to retrieve a set of ``N``
        colors from a set of ``n`` colors where ``N >> n``. The matplotlib
        simply linearely interpolates between all ``n`` colors to extend
        the number of colors to ``N``.

        In case of :py:func:`hclpalette` objects this is not necessary as
        :py:func:`hclpalette` objects allow to retrieve ``N`` colors directly
        along well-specified Hue-Chroma-Luminance paths. Thus, this method
        returns a matplotlib color map with ``n==N`` colors. The linear 
        interpolation between the colors (as typically done by
        LinearSegmentedColormap) is not necessary. However, for convenience
        cmaps have been implemented such that you can easily use hcl based
        palettes in your existing workflow.

        Parameters
        ----------
        n : int
            number of colors
        name : str
            name of the custom color map. Default is ``custom_hcl_cmap``

        Returns
        -------
        matplotlib.colors.LinearSegmentedColormap
            Returns a ``LinearSegmentedColormap`` (cmap) to be used
            with the matplotlib library.
        '''
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


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class qualitative_hcl(hclpalette):
    """qualitative_hcl(h = [0, 360.], c = 50, l = 70, \
            fixup = True, palette = None, rev = False, **kwargs)
    
    
    Qualitative HCL color palette.

    Parameters
    ----------
    h : numeric list
        hue values, qualitative color palettes require
        two hues.  If more than two values are provided the first two will
        be used while the rest is ignored.  If input `h` is a string this
        argument acts like the `palette` argument (see `palette` input
        parameter).
    c : numeric
        chroma value, a single numeric value. If multiple values are provided
        only the first one will be used.
    l : numeric
        luminance value, a single numeric value. If multiple values are
        provided only the first one will be used.
    fixup : bool 
        only used when converting the HCL colors to hex.  Should RGB values
        outside the defined RGB color space be corrected?
    palette : None, string
        can be used to load a default diverging color palette
        specification. If the palette does not exist an exception will be raised.
        Else the settings of the palette as defined will be used to create
        the color palette.
    rev : bool
        should the color map be reversed.
    args : ...
        unused.
    kwargs : ...
        Additional arguments to overwrite the h/c/l settings.
        @TODO has to be documented.

    Returns
    -------
    Initialize new object, no return. Raises a set of errors if the parameters
    are misspecified. Note that the object is callable, the default object call
    can be used to return hex colors (identical to the ``.colors()`` method),
    see examples.

    Examples
    --------
    >>> from colorspace import diverging_hcl
    >>> a = qualitative_hcl()
    >>> a.colors(10)
    >>> b = qualitative_hcl("Dynamic")
    >>> b.colors(10)
    >>> # The standard call of the object also returns hex colors. Thus,
    >>> # you can make your code slimmer by calling:
    >>> qualitative_hcl("Dynamic")(10)
    """

    _name = "Qualitative"

    def __init__(self, h = [0, 360.], c = 50, l = 70,
        fixup = True, palette = None, rev = False, **kwargs):

        # Store reverse flag
        self._rev = rev

        # If a string is given on "h": exchange with "palette".
        if isinstance(h, str):
            palette = h; h = None

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   2, False, False, h = h)
            c     = self._checkinput_(int,   1, False, False, c = c)
            l     = self._checkinput_(int,   1, False, False, l = l)
        except Exception as e:
            raise ValueError(str(e))


        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            defaultpalettes = hclpalettes().get_palettes("Qualitative")
            default_names    = [x.name() for x in defaultpalettes]
            if not palette in default_names:
                raise ValueError("palette {:s} is not a valid qualitative palette. ".format(palette) + \
                        "Choose one of: {:s}".format(", ".join(default_names)))

            # Else pick the palette
            pal = defaultpalettes[default_names.index(palette)]

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in ["h1", "c1", "l1"]: pal.set(key, value)

            # Extending h2 if h1 = h2 (h2 None)
            if pal.get("h2") == None or pal.get("h1") == pal.get("h2"):
                pal.set("h2", pal.get("h1") + 360)
                if pal.get("h2") > 360:
                    pal.set("h1", pal.get("h1") - 360)
                    pal.set("h2", pal.get("h2") - 360)

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
        """colors(n = 11, type_ = "hex", fixup = None)

        Returns the colors of the current color palette.

        Parameters
        ----------
        n : int
            number of colors which should be returned.
        fixup : None, bool
            should sRGB colors be corrected if they lie outside
            the defined color space?
            If ``None`` the ``fixup`` parameter from the object
            will be used. Can be set to ``True`` or ``False``
            to explicitly control the fixup here.
        """

        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        from numpy import repeat, linspace, asarray
        from numpy import vstack, transpose
        from . import colorlib

        L = repeat(self.get("l1"), n)
        C = repeat(self.get("c1"), n)
        H = linspace(self.get("h1"), self.get("h2"), n)

        # Create new HCL color object
        from .colorlib import HCL
        HCL = HCL(H, C, L)

        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HCL

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return HCL.colors(fixup = fixup, rev = rev)


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class rainbow_hcl(qualitative_hcl):
    """rainbow_hcl(c = 50, l = 70, start = 0, end = 360, \
            gamma = None, fixup = True, rev = False, *args, **kwargs)

    HCL rainbow, a qualitative cyclic rainbow color palette with uniform
    luminance and chroma.

    Parameters
    ----------
    c : int
        chroma of the color map ``[0-100+]``.
    l : int
        luminance of the color map ``[0-100]``.
    start : int
        hue at which the rainbow should start.
    end : int
        hue at which the rainbow should end.
    rev : bool
        should the color map be reversed.
    gamma : float
        gamma value used for transfiromation from/to sRGB.
        @TODO implemented? Check!
    fixup : bool 
        only used when converting the HCL colors to hex.  Should RGB values
        outside the defined RGB color space be corrected?

    Returns
    -------
    Initialize new object, no return. Raises a set of errors if the parameters
    are misspecified. Note that the object is callable, the default object call
    can be used to return hex colors (identical to the ``.colors()`` method),
    see examples.

    Example
    -------
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
    """diverging_hcl(h = [260, 0], c = 80, l = [30, 90], \
        power = 1.5, fixup = True, palette = None, rev = False, \
        *args, **kwargs)

    Diverging HCL color palette.

    Parameters
    ----------
    h : numeric list
        hue values, diverging color palettes should have different hues for
        both ends of the palette. If only one value is present it will be
        recycled ending up in a diverging color palette with the same colors on
        both ends.  If more than two values are provided the first two will be
        used while the rest is ignored.  If input ``h`` is a string this
        argument acts like the ``palette`` argument (see ``palette`` input
        parameter).
    c : numeric
        chroma value, a single numeric value. If multiple values are provided
        only the first one will be used.
    l : numeric list
        luminance values. The first value is for the two ends of the color
        palette, the second one for the neutral center point. If only one value
        is given this value will be recycled.
    power : numeric
        power parameter for non-linear behaviour of the color palette.
    fixup : bool
        only used when converting the HCL colors to hex.  Should RGB values
        outside the defined RGB color space be corrected?
    palette : string
        can be used to load a default diverging color palette
        specification. If the palette does not exist an exception will be raised.
        Else the settings of the palette as defined will be used to create
        the color palette.
    rev : bool
        should the color map be reversed.
    args : ...
        unused.
    kwargs : ...
        Additional arguments to overwrite the h/c/l settings.
        @TODO has to be documented.

    Returns
    -------
    Initialize new object, no return. Raises a set of errors if the parameters
    are misspecified. Note that the object is callable, the default object call
    can be used to return hex colors (identical to the ``.colors()`` method),
    see examples.

    Examples
    --------
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

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            h     = self._checkinput_(int,   2, 2, True,  False, h = h)
            c     = self._checkinput_(int,   1, 1, False, False, c = c)
            l     = self._checkinput_(int,   2, 2, True,  False, l = l)
            power = self._checkinput_(float, 1, 1, True,  False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            defaultpalettes = hclpalettes().get_palettes("Diverging")
            default_names    = [x.name() for x in defaultpalettes]
            if not palette in default_names:
                msg = "palette \"{:s}\" is not a valid qualitative palette.".format(palette) + \
                      "Choose one of: {:s}".format(", ".join(default_names))
                raise ValueError(msg)

            # Else pick the palette
            pal = defaultpalettes[default_names.index(palette)]

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in ["h1", "c1", "l1"]: pal.set(key, value)

            # Extending h2 if h1 = h2 (h2 None)
            if pal.get("h2") == None or pal.get("h1") == pal.get("h2"):
                pal.set("h2", pal.get("h1") + 360)
                if pal.get("h2") > 360:
                    pal.set("h1", pal.get("h1") - 360)
                    pal.set("h2", pal.get("h2") - 360)

            # Getting settings
            settings = pal.get_settings()
        else:
            settings = {}

            # User settings
            settings["h1"]    = h[0]
            settings["h2"]    = h[1]
            settings["c1"]    = c
            settings["l1"]    = l[0]
            settings["l2"]    = l[1]
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
        """colors(n = 11, type_ = "hex", fixup = None)

        Returns the colors of the current color palette.

        Parameters
        ----------
        n : int
            number of colors which should be returned.
        fixup : None, bool
            should sRGB colors be corrected if they lie outside
            the defined color space?
            If ``None`` the ``fixup`` parameter from the object
            will be used. Can be set to ``True`` or ``False``
            to explicitly control the fixup here.
        alpha : None, float
            float (single value) or vector of floats in the range
            of ``[0.,1.]`` for alpha transparency channel
            (``0.`` means full transparency, ``1.`` opaque).
            If a single value is provided it will be applied to
            all colors, if a vector is given the length has to be ``n``.
        """

        fixup = fixup if isinstance(fixup, bool) else self.settings["fixup"]

        from numpy import abs, linspace, power, repeat
        from numpy import asarray, ndarray, ndenumerate
        from numpy import vstack, transpose
        from . import colorlib

        # Calculate H/C/L
        p2   = self.get("p1") if self.get("p2") is None else self.get("p2")
        rval = linspace(1., -1., n)

        L = self.get("l2") - (self.get("l2") - self.get("l1")) * power(abs(rval), p2)
        C = self.get("c1") * power(abs(rval), self.get("p1"))
        from numpy import fmax
        C = fmax(.1,C)
        H = ndarray(n, dtype = "float")
        for i,val in ndenumerate(rval):
            H[i] = self.get("h1") if val > 0 else self.get("h2")

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
        return HCL.colors(fixup = fixup, rev = rev)




# -------------------------------------------------------------------
# -------------------------------------------------------------------
class sequential_hcl(hclpalette):
    """sequential_hcl(h = 260, c = [80, 30], l = [30, 90], \
        power = 1.5, fixup = True, palette = None, rev = False, \
        *args, **kwargs)

    Sequential HCL color palette.

    Parameters
    ----------
    h : numeric
        hue values. If only one value is given the value is recycled which
        yields a single-hue sequential color palette.  If input `h` is a string
        this argument acts like the `palette` argument (see `palette` input
        parameter).
    c : numeric list
        chroma values, numeric of length two. If multiple values are provided
        only the first one will be used.
    l : numeric list
        luminance values, numeric of length two. If multiple values are
        provided only the first one will be used.
    power : numeric, numeric list
        power parameter for non-linear behaviour of the
        color palette. One or two values can be provided.
    fixup : bool
        only used when converting the HCL colors to hex.  Should RGB values
        outside the defined RGB color space be corrected?
    palette : string
        can be used to load a default diverging color palette specification. If
        the palette does not exist an exception will be raised.  Else the
        settings of the palette as defined will be used to create the color
        palette.
    rev : bool 
        should the color map be reversed.
    args : ...
        unused.
    kwargs : ...
        Additional arguments to overwrite the h/c/l settings.
        @TODO has to be documented.

    Returns
    -------
    Initialize new object, no return. Raises a set of errors if the parameters
    are misspecified. Note that the object is callable, the default object call
    can be used to return hex colors (identical to the ``.colors()`` method),
    see examples.

    Examples
    --------
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
    _allowed_parameters = ["h1", "c1", "c2", "l1", "l2", "p1", "p2"]
    _name = "Sequential HCL"

    def __init__(self, h = 260, c = [80, 30], l = [30, 90],
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
            h     = self._checkinput_(int,   2, 2, True,  False, h = h)
            c     = self._checkinput_(int,   2, 3, True,  False, c = c)
            l     = self._checkinput_(int,   2, 2, True,  False, l = l)
            power = self._checkinput_(float, 2, 2, True,  False, power = power)
        except Exception as e:
            raise ValueError(str(e))

        # For handy use of the function
        if isinstance(h,str):
            palette = h; h = None

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            defaultpalettes = hclpalettes().get_palettes("Sequential")
            default_names    = [x.name() for x in defaultpalettes]
            if not palette in default_names:
                raise ValueError("palette {:s} is not a valid qualitative palette. ".format(palette) + \
                        "Choose one of: {:s}".format(", ".join(default_names)))

            # Else pick the palette
            pal = defaultpalettes[default_names.index(palette)]

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in self._allowed_parameters: pal.set(key, value)

            # Getting settings
            settings = pal.get_settings()
        else:
            # User settings
            settings = {}
            settings["h1"]    = h[0]
            settings["h2"]    = h[0] if len(h) == 1 else h[1]
            if len(c) == 3:
                settings["c1"]    = c[0]
                settings["c2"]    = c[1]
                settings["cmax"]  = c[2]
            else:
                settings["c1"]    = c[0]
                settings["c2"]    = c[1]
            settings["l1"]    = l[0]
            settings["l2"]    = l[1]
            settings["p1"]    = power[0]
            settings["p2"]    = power[1]
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
    def colors(self, n = 11, fixup = True, **kwargs):
        """colors(n = 11, type_ = "hex", fixup = None)

        Returns the colors of the current color palette.

        Parameters
        ----------
        n : int
            number of colors which should be returned.
        fixup : None, bool
            should sRGB colors be corrected if they lie outside
            the defined color space?
            If ``None`` the ``fixup`` parameter from the object
            will be used. Can be set to ``True`` or ``False``
            to explicitly control the fixup here.
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
        c2   = c1 if self.get("c2") is None else self.get("c2")
        cmax = None if not self.get("cmax") else self.get("cmax")
        l1   = self.get("l1")
        l2   = l1 if self.get("l2") is None else self.get("l2")
        h1   = self.get("h1")
        h2   = h1 if self.get("h2") is None else self.get("h2")

        # Special case if cmax is not None:
        if not cmax is None:
            cmaxat = 1. / (1. + abs(float(cmax) - float(c1)) / abs(float(cmax) - float(c2)))
        else:
            cmaxat = None

        # Hue and Luminance
        H = h2 - (h2 - h1) * rval
        L = l2 - (l2 - l1) * power(rval, p2)
        # Speical handling for Chroma due to cmax
        if not cmaxat:
            C = c2 - (c2 - c1) * power(rval, p1)
        else:
            C      = ndarray(len(rval), dtype = "float")
            idx    = where(power(rval, p1) < cmaxat)[0]
            C[idx] = c2 - (c2 - cmax) * power(rval[idx], p1) / cmaxat
            idx    = where(power(rval, p1) >= cmaxat)[0]
            C[idx] = cmax - (cmax - c1) * ((power(rval[idx], p1) - cmaxat) / (1. - cmaxat))

        # Create new HCL color object
        from .colorlib import HCL
        HCL = HCL(H, C, L)

        # If kwargs have a key "colorobject" return HCL colorobject
        if "colorobject" in kwargs.keys(): return HCL

        # Reversing colors
        rev = self._rev
        if "rev" in kwargs.keys(): rev = kwargs["rev"]

        # Return hex colors
        return HCL.colors(fixup = fixup, rev = rev)


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class heat_hcl(sequential_hcl):
    """heat_hcl(h = [0, 90], c = [100, 30], l = [50, 90], power = [1./5., 1.], \
               fixup = True, *args, **kwargs):

    HEAT hcl, a sequential palette.

    Parameters
    ----------
    h : list of int
        hue parameters (h1/h2).
    c : list of int
        chroma parameters (c1/c2).
    l : int
        luminance parameters (l1/l2).
    power : list of float
        power parameters (p1/p2).
    gamma : float
        gamma value used for transfiromation from/to sRGB.
        @TODO implemented? Check!
    fixup : bool 
        only used when converting the HCL colors to hex.  Should RGB values
        outside the defined RGB color space be corrected?
    args : ...
        unused.
    kwargs : ...
        Additional arguments to overwrite the h/c/l settings.
        @TODO has to be documented.

    Returns
    -------
    Initialize new object, no return. Raises a set of errors if the parameters
    are misspecified. Note that the object is callable, the default object call
    can be used to return hex colors (identical to the ``.colors()`` method),
    see examples.

    Example
    -------
    >>> from colorspace.palettes import heat_hcl
    >>> pal = heat_hcl()
    >>> pal.colors(3); pal.colors(20)
    """


    _allowed_parameters = ["h1", "h2", "c1", "c2", "l1", "l2", "p1", "p2"]
    _name = "Heat HCL"

    def __init__(self, h = [0, 90], c = [100, 30], l = [50, 90], power = [1./5., 1.],
                 fixup = True, *args, **kwargs):

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
    """terrain_hcl(h = [130, 0], c = [80, 0], l = [60, 95], power = [1./10., 1.], \
               fixup = True, *args, **kwargs):

    HCL terrain colors, a sequential palette.

    Parameters
    ----------
    h : list of int
        hue parameters (h1/h2).
    c : list of int
        chroma parameters (c1/c2).
    l : int
        luminance parameters (l1/l2).
    power : list of float
        power parameters (p1/p2).
    gamma : float
        gamma value used for transfiromation from/to sRGB.
        @TODO implemented? Check!
    fixup : bool 
        only used when converting the HCL colors to hex.  Should RGB values
        outside the defined RGB color space be corrected?
    args : ...
        unused.
    kwargs : ...
        Additional arguments to overwrite the h/c/l settings.
        @TODO has to be documented.

    Returns
    -------
    Initialize new object, no return. Raises a set of errors if the parameters
    are misspecified. Note that the object is callable, the default object call
    can be used to return hex colors (identical to the ``.colors()`` method),
    see examples.

    Example
    -------
    >>> from colorspace import terrain_hcl
    >>> pal = terrain_hcl()
    >>> pal.colors(3); pal.colors(20)
    """

    _allowed_parameters = ["h1", "h2", "c1", "c2", "l1", "l2", "p1", "p2"]
    _name = "Terrain HCL"

    def __init__(self, h = [130, 0], c = [80, 0], l = [60, 95], power = [1./10., 1.],
                 fixup = True, *args, **kwargs):

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
    """diverging_hsv(h = [260, 0], s = 1., v = 1., power = 1., \
        fixup = True)

    Diverging HSV color palette.

    Parameters
    ----------
    h : numeric list
        hue values, diverging color palettes should have different hues for
        both ends of the palette. If only one value is present it will be
        recycled ending up in a diverging color palette with the same colors on
        both ends.  If more than two values are provided the first two will be
        used while the rest is ignored.  If input ``h`` is a string this
        argument acts like the ``palette`` argument (see ``palette`` input
        parameter).
    s : float
        saturation value for the two ends of the palette.
    v : float
        value (the HSV value) of the two ends of the palette.
    power : numeric
        power parameter for non-linear behaviour of the color palette.
    fixup : bool
        only used when converting the HCL colors to hex.  Should RGB values
        outside the defined RGB color space be corrected?
    args : ...
        unused.
    kwargs : ...
        Additional arguments to overwrite the h/c/l settings.
        @TODO has to be documented.

    Returns
    -------
    Initialize new object, no return. Raises a set of errors if the parameters
    are misspecified. Note that the object is callable, the default object call
    can be used to return hex colors (identical to the ``.colors()`` method),
    see examples.

    Examples
    --------
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
        """colors(n = 11, type_ = "hex", fixup = None)

        Returns the colors of the current color palette.

        Parameters
        ----------
        n : int
            number of colors which should be returned.
        fixup : None, bool
            should sRGB colors be corrected if they lie outside
            the defined color space?
            If ``None`` the ``fixup`` parameter from the object
            will be used. Can be set to ``True`` or ``False``
            to explicitly control the fixup here.
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
        return HSV.colors(fixup = fixup, rev = rev)




