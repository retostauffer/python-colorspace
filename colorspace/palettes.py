
import os
import sys
from .logger import logger
log = logger(__name__)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class defaultpalette(object):
    """
    Default color palette object. This object is not intended to be
    used by the user itself but is used to store the pre-defined
    color palettes contained in the package.

    Parameters:
        type (:class:`str`): Palette type.
        method (:class:`str`): Name of the method which has to be called
            to retrieve colors (e.g., :py:func:`diverge_hcl`).
        parameter (:class:`list`): A list of strings which define the
            allowed/valid parameters for this color palette.
        name (:class:`str`): Name of the color palette.
        settings (:class:`dict`): A dict object containing the
            parameter settings.
    """

    def __init__(self, type, method, parameter, name, settings):

        self._type_      = type
        self._name_      = name
        self._method_    = method
        self._parameter_ = parameter
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
        keys = self.get_settings().keys()
        keys.sort()
        for key in keys:
            if key in ["desc"]: continue
            val = self.get(key)
            if   isinstance(val,bool):   val = " True" if val else "False"
            elif isinstance(val,int):    val = "{:5d}".format(val)
            elif isinstance(val,float):  val = "{:5.1f}".format(val)
            res.append("         {:10s} {:s}".format(key,val))

        return "\n".join(res)

    def type(self):
        """
        Return:
            Returns the type (:class:`str`) of the palette.
        """
        return self._type_

    def name(self):
        """
        Return:
            Returns the name (:class:`str`) of the palette.
        """
        return self._name_

    def rename(self, name):
        """Allows to rename the palette.

        Parameters:
            name (:class:`str`): New palette name.
        """
        self._name_ = name

    def get(self, what):
        """Allows to load the settings of the palette for the
        different parameters (e.g., `h1`, `h2`, ...). Returns
        :class:`None` if the parameter does not exist.
        Another method (:py:func:`set`) allows to set the
        parameters.

        Parameters:
            what (:class:`str`): Name of the parameter which
                should be extracted and returned from the settings
                of this color palette.

        Return:
            Returns the type (:class:`str`) of the palette.
        """

        if what in self._settings_.keys():
            return self._settings_[what]
        else:
            return None


    def set(self, **kwargs):
        """Allows to set/overwrite color palette parameters (e.g., `h1`, `h2`,
        ...).  Another method (:py:func:`get`) allows to retrieve the
        parameters.

        Parameters:
            kwargs: a set of key=value pairs where the key defines the
                parameter which should be overruled, value the corresponding
                value. Allowed value types are bool, int, and float.
        """
        print self._parameter_
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
        """Returns a :class:`dict` with all parameters of this color palette.
        To retrieve single parameters use :py:func:`get`.

        Returns:
            Returns a :class:`dict` object with all parameter specification
            of this palette.
        """
        return self._settings_

    def parameters(self):
        """Returns a :class:`list` with the names of all parameters
        specified. The parameters themselves can be retrieved by calling
        the :py:func:`get_settings` method.

        Returns:
            Returns a :class:`list` object with all parameter names.
        """
        return self._parameter_

    def colors(self, n = 10):
        """Load `n` colors from this palette. 
        This method evaluates the `method` argument to generate
        a set of hex colors which will be returned.
        Please note that it is possible that none-values will
        be returned if the fixup-setting is set to `False`
        (see :py:class:`colorlib.hexcols`).
        
        Parameters:
            n (:class:`int`): Number of colors to be returned.
                The default is `10`.

        Returns:
            Returns a :class:`list` object with all parameter names.
        """

        # Dynamically load color function
        mod  = __import__("colorspace")
        cfun = getattr(mod, self._method_)

        # Calling color method with arguments of this object. 
        args = {}
        for key in self._parameter_:
            args[key] = self.get(key)

        # If Remove h1/h2 and store them in h
        for dim in ["h", "c", "l", "p"]:
            dim1 = "{:s}1".format(dim)
            dim2 = "{:s}2".format(dim)
            dim = "power" if dim == "p" else dim
            if dim1 in args.keys() and dim2 in args.keys():
                args[dim] = [args[dim1], args[dim2]]
                del args[dim1]; del args[dim2]
            elif dim1 in args.keys():
                args[dim] = args[dim1]
                del args[dim1]
            elif dim2 in args.keys():
                args[dim] = args[dim2]
                del args[dim2]

        pal = cfun(n, **args)
        return pal.colors(n, fixup = True)



# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalettes(object):
    """Prepares the pre-specified hclpalettes.
    Reads the config files and creates a set of :py:class:`defaultpalette`
    objects.

    Parameters:
        files (:class:`None` or :class:`list`): If `None` (default)
            the default color palette configuration from within the
            package will be loaded. Technically a list of file names
            (:class:`str`) can be provided to load user-defined color
            palettes. Not yet tested!

    .. todo::
        Check if the files option is useful. If so, provide some
        more information about the config files and where/how to use.
    """
    def __init__(self, files = None):

        if files is None:
            resource_package = os.path.dirname(__file__)
            log.debug("Package path is \"{0:s}\"".format(resource_package))
            import glob
            files = glob.glob(os.path.join(resource_package, "palconfig", "*.conf"))


        for file in files:
            if not os.path.isfile(file):
                log.error("Cannot find file {:s}. Stop.".format(file))
                sys.exit(9)

        # Else trying to read the files. Returns a list with
        # palette configs.
        self._palettes_ = {}
        if len(files) == 0:
            raise ValueError("No palette config files found ({:s}.".format(self.__class__.__name__))

        # Else print debug message and read the config files
        log.debug("Palette config files: {:s}".format(", ".join(files)))
        for file in files:
            [palette_type, pals] = self._load_palette_config_(file)
            if not pals: continue

            # Append
            self._palettes_[palette_type] = pals
            #DEMO# for p in pals: p.show()

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
        """Get palette types.

        Returns:
            Returns a :class:`list` of strings (:class:`str`)
                with the names of all palette types or groups.
        """

        return self._palettes_.keys()

    def get_palettes(self, type_ = None):
        """Get all palettes of a specific type.

        Parmaeters:
            type_ (:class:`None` or :class:`str`): Name of the palettes which should
                be returned. If set to `None` (default) all palettes
                will be returned. Names have to match but are not case sensitive.

        Returns:
            Returns a :class:`list` containing :py:class:`defaultpalette`
            objects.
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
        """Get a palette with a specific name.

        Parameters:
            name (:class:`str`): Name of the color palette which should
                be returned.

        Returns:
            Returns an object of class :py:class:`defaultpalette` if
            a palette with the name as specified can be found.
            Else an error will be dropped.
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

        # Else reutnr palette if available
        if not take_pal:
            log.error("No palettes named \"{:s}\".".format(name)); sys.exit(9)

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
            palette_parameter = [x.strip() for x in CNF.get("main", "parameter").split(",")]
        except Exception as e:
            log.error(e); sys.exit(9)

        # Reading all settings
        log.debug("[palette] loading {:s} from {:s}".format(palette_type, os.path.basename(file)))

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

            pals.append(defaultpalette(palette_type, palette_method,
                        palette_parameter, name, settings))


        # Return dictionary with palettes
        if len(pals) == 0:
            return [None, None]
        else:
            return [palette_type, pals]




# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalette(object):
    """Hy, I am the base class"""

    n     = None
    h1    = None
    h2    = None
    l1    = None
    l2    = None
    p1    = None
    p2    = None
    fixup = True

    def get(self, key):
        """Returns one specific item of the palette settings,
        e.g., the current value for "n" or "h1" or "l2".
        If not existing a `None` will be returned.

        Parameters:
            key (str): name of the setting to be returned.

        Returns:
            None if `key` does ont exist, else the current
                value will be returned.

        Examples:
            >>> from colorspace.palettes import rainbow_hcl
            >>> a = rainbow_hcl(10)
            >>> a.get("h1")
            >>> a.get("c1")
            >>> a.get("l1")
            >>> a.get("not_defined")
        """
        if not key in self.settings.keys():
            return None
        return self.settings[key]

    def show_settings(self):
        """Shows the current settings (table like print
        to stdout). Should more be seen as a development
        method than a very useful thing.

        Examples:
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
    def _checkinput_(self, dtype, length = None, recycle = False,
            nansallowed = False, **kwargs):
        """Used to check/convert/extend input arguments to the
        palette functions.

        Parameters:
            dtype (object): e.g. int or float, the type in which the
                inputs should be converted.
            length (int): optional. If set the script checks the length
                of the input argument and, if necessary and allowed,
                converts the data. If more values than required are
                provided by the user only the first few elements
                will be used (as specified by `length`). If the
                user gave less arguments than expected the user
                arguments are recycled if `recycle = True`, see
                parameter `recycle`. If `recycle = False` and the
                length of the input is shorter than expected an
                error will be raised.
            recycle (bool): if set to `True` the user inputs will
                be recycled to match the expected number of inputs.
            nansallowed (bool): if False an error will be raised
                if the final arguments contain `nan` values. Else
                `nan`s are passed trough and will be returned.
            **kwargs: list of named arguments, the ones to be
                checked. If only one is given the function returns
                the values of this specific input. If multiple
                arguments are handed over a dict will be returned
                with the names corresponding to the user input.

        Returns:
            If `**kwargs` is of length one the values of this
                specific variable will be returned. If multiple
                `**kwargs` arguments are set a dict is returned.
                Note that `None` will simply stay `None`.
                The function raises errors if the user inputs
                do not match the required specifications.
        """

        def fun(key, value, dtype, length, recycle, nansallowed):

            from numpy import vstack, asarray, isnan, nan, any

            # If None
            if value == None: return value

            # Converting the data
            try:
                value = asarray([value], dtype = dtype).flatten()
            except Exception as e:
                msg = "wrong input for \"{:s}\" to {:s}: {:s}".format(key, self.__class__.__name__, e)
                raise ValueError(msg)

            # Not enough input values, check if we are allowed to
            # recycle.
            if length and len(value) < length:
                # Input was too short: check if we are allowed to
                # recycle the value or not.
                if not recycle:
                    msg = "wrong length of input \"{:s}\", ".format(key) + \
                          "expected {:d} elements, got {:d} ".format(length, len(value)) + \
                          "when calling {:s}".format(self.__class__.__name__)
                    raise ValueError(msg)
                else:
                    value = vstack([value] * length).flatten()[0:length]
            # Cropping data if too much elements are given.
            elif length and len(value) > length:
                value = value[0:length]

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
            kwargs[key] = fun(key, value, dtype, length, recycle, nansallowed)

        # If only one kwarg was given: return values, else return dict.
        if len(kwargs) == 1:
            return kwargs[kwargs.keys()[0]]
        else:
            return kwargs



    def _check_inputs_(self, n, h, c, l, p, palette):

        # Class name for the error messages, if necessary.
        cls = self.__class__.__name__

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
                log.error("Error in \"tolist\", don't know what to do.")
                sys.exit(9)
            if not all([isinstance(e, totype) for e in x]):
                log.error("In \"tolist\"")
                log.error(x)
                log.error("Problems with inputs for {:s}".format(cls)); sys.exit(9)
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
                log.error("In \"tovalue\"")
                log.error(x)
                log.error("Problems with inputs for {:s}.".format(cls)); sys.exit(9)

        # If "h" is a string this is ment to be the palette
        # argument, switch "palette" and "h"
        if isinstance(h, str):
            palette = h; h = None 

        if isinstance(n, int) or isinstance(n, float):
            n = int(n)
        else:
            log.error("Input \"n\" to {:s} has to be a single integer.".format(cls))

        # For sequential hcl palettes
        if isinstance(self, sequential_hcl):
            n = tovalue(n, int, cls)
            h = tolist(h, int, 2, cls)
            c = tolist(c, int, 2, cls)
            l = tolist(l, int, 2, cls)
            p = tolist(p, float, 2, cls)
        # For sequential hcl palettes
        elif isinstance(self, diverge_hcl):
            n = tovalue(n, int, cls)
            h = tolist(h, int, 2, cls)
            c = tovalue(c, int, cls)
            l = tolist(l, int, 2, cls)
            p = tovalue(p, float, cls)

        # If "n" is set to small: exit
        if n <= 0:
            log.error("Input \"n\" has to be a positive integer."); sys.exit(9)

        return [n, h, c, l, p, palette]


    def data(self):
        return self._data_


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class qualitative_hcl(hclpalette):
    """Qualitative HCL color palette.

    Parameters:
        palette (str): optional. Can be set to load a specific default
            palette by name.
        n (inteter): number of values to be returned later.
        h (numeric): hue values, qualitative color palettes require
            two hues.  If more than two values are provided the first two will
            be used while the rest is ignored.  If input `h` is a string this
            argument acts like the `palette` argument (see `palette` input
            parameter).
            Default is [0-360] with respect to the number of colors "n".
        c (numeric): chroma value, a single numeric value. If multiple
            values are provided only the first one will be used.
        l (numeric): luminance value, a single numeric value. If multiple
            values are provided only the first one will be used.
        fixup (boolean): only used when converting the HCL colors to hex.
            Should RGB values outside the defined RGB color space be
            corrected?
        alpha (numeric): Not yet implemented.
        palette (string): can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be raised.
            Else the settings of the palette as defined will be used to create
            the color palette.
        rev (boolean): should the color map be reversed.

        *args: unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.
            @TODO has to be documented.

    Returns:
        No return. Raises a ValueError if a palette specified by input argument
            `palette` does not exist.

    Examples:
        >>> from colorspace.palettes import diverge_hcl
        >>> a = diverge_hcl(10)
        >>> a.colors(10)
        >>> b = diverge_hcl(10, "Blue-Yellow 3")
        >>> b.colors(10)

    .. todo::
        Try to make the code nicer (the part loading/overwriting settings).
        Looks messy and is extremely hard to debug. Rev implemented?
    """

    def __init__(self, n, h = lambda n: [0, 360. / (n + 1.) * n], c = 50, l = 70,
        fixup = True, alpha = 1, palette = None, rev = False, **kwargs):

        # If a string is given on "h": exchange with "palette".
        if isinstance(h, str):
            palette = h; h = None

        # Checking input "n"
        try:
            n     = self._checkinput_(int,   1, False, False, n = n)
        except Exception as e:
            raise ValueError(e)

        # Evaluate "end" if it is a function
        h = h(n) if callable(h) else h

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            n     = self._checkinput_(int,   1, False, False, n = n)
            h     = self._checkinput_(int,   2, False, False, h = h)
            c     = self._checkinput_(int,   1, False, False, c = c)
            l     = self._checkinput_(int,   1, False, False, l = l)
        except Exception as e:
            raise ValueError(e)


        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            defaultpalettes = hclpalettes().get_palettes("Qualitative")
            default_names    = [x.name() for x in defaultpalettes]
            if not palette in default_names:
                log.error("Palette \"{:s}\" is not a valid qualitative palette.".format(palette))
                log.error("Choose one of: {:s}".format(", ".join(default_names)))
                sys.exit(9)

            # Else pick the palette
            pal = defaultpalettes[default_names.index(palette)]

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in ["h1", "c1", "l1"]: pal.set(key, value)

            # Extending h2 if h1 = h2 (h2 None)
            if pal.get("h2") == None or pal.get("h1") == pal.get("h2"):
                print(" ++++++++++++++++++++ ")
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
            settings["l1"]    = l
            settings["fixup"] = fixup
            settings["alpha"] = alpha
            settings["rev"]   = rev

        settings["n"] = n

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if not kwargs is None:
            if "settings" in kwargs.keys():
                for key,val in kwargs["settings"].items():
                    if key in settings.keys() and not val is None:
                        settings[key] = val



        # Save settings
        self.settings = settings


    def colors(self, n = None, type_ = "hex", fixup = None):

        if n is None: n = self.get("n")
        if n < 1:     return None

        if isinstance(fixup, bool): self.settings["fixup"] = fixup

        from numpy import repeat, linspace, asarray
        from numpy import vstack, transpose
        from . import colorlib

        L = repeat(self.get("l1"), n)
        C = repeat(self.get("c1"), n)
        H = linspace(self.get("h1"), self.get("h2"), n)

        # Create new HCL color object
        from colorlib import HCL
        HCL = HCL(H, C, L)

        # Return hex colors
        return HCL.colors(fixup = fixup)


# -------------------------------------------------------------------
# The rainbow class extends the qualitative_hcl class.
# -------------------------------------------------------------------
class rainbow_hcl(qualitative_hcl):
    """HCL rainbow, a qualitative cyclic rainbow color palette
    with uniform luminance and chroma.

    Parameters:
        n (:class:`int`): number of colors you want to have.
        c (:class:`int`): chroma of the color map [0-100+].
        l (:class:`int`): luminance of the color map [0-100].
        start (:class:`int`): hue at which the rainbow should start,
            default is `start = 0` which corresponds to red.
        end (:class:`int`): hue at which the rainbow should stop. By default
            this is a function `360 * (n - 1) / n` such that the `n` colors
            are uniformly distributed across [0, 360].
        gamma (:class:`float`): default is `None`.
        fixup (:class:`bool`): should the colors be corrected to valid RGB
            when returned as hex colors? Default is `True`, if set to
            `False` colors outside the defined RGB color space will be
            set to :class:`np.nan`.
        alpha (:class:`alpha`): currently not implemented.

    Examples:
        >>> from colorspace.palettes import rainbow_hcl
        >>> pal = rainbow_hcl(100)
        >>> pal.colors(3); pal.colors(20)

    .. todo::
        Implement functionality for alpha, either here or
        in the colors method (and maybe even remove `n` from the
        class definition, but then we would also have to
        pass `end` trough the object.

    """

    _allowed_parameters_ = ["h1", "h2", "c1", "l1", "l2", "p1"]

    def __init__(self, n, c = 50, l = 70, start = 0, end = lambda n: 360 * (n - 1)/n,
                 gamma = None, fixup = True, alpha = 1, *args, **kwargs):

        # Checking input "n"
        try:
            n     = self._checkinput_(int,   1, False, False, n = n)
        except Exception as e:
            raise ValueError(e)

        # Evaluate "end" if it is a function
        end = end(n) if callable(end) else end

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            c     = self._checkinput_(int,   1, False, False, c = c)
            l     = self._checkinput_(int,   1, False, False, l = l)
            start = self._checkinput_(int,   1, False, False, start = start)
            end   = self._checkinput_(int,   1, False, False, end = end)
        except Exception as e:
            raise ValueError(e)

        # Save settins
        try:
            self.settings = {"h1": int(start), "h2": int(end),
                             "c1": int(c), "l1": int(l), "n": int(n),
                             "fixup": bool(fixup), "alpha": float(alpha)}
        except ValueError as e:
            raise ValueError("wrong inputs to {:s}: {:s}".format(
                self.__class__.__name__, e))
        except Exception as e:
            raise Exception("in {:s}: {:s}".format(self.__class__.__name__, e))

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if key in self._allowed_parameters_:
                    settings[key] = val

# -------------------------------------------------------------------
# -------------------------------------------------------------------
class diverge_hcl(hclpalette):
    """Diverging HCL color palette.

    Parameters:
        n (inteter): number of values to be returned later.
        h (numeric): hue values, diverging color palettes should have
            different hues for both ends of the palette. If only one
            value is present it will be recycled ending up in a
            diverging color palette with the same colors on both ends.
            If more than two values are provided the first two will
            be used while the rest is ignored.
            If input `h` is a string this argument acts like the
            `palette` argument (see `palette` input parameter).
        c (numeric): chroma value, a single numeric value. If multiple
            values are provided only the first one will be used.
        l (numeric): luminance values. The first value is for the two
            ends of the color palette, the second one for the neutral
            center point. If only one value is given this value will
            be recycled.
        power (numeric): power parameter for non-linear behaviour of the
            color palette.
        fixup (boolean): only used when converting the HCL colors to hex.
            Should RGB values outside the defined RGB color space be
            corrected?
        alpha (numeric): Not yet implemented.
        palette (string): can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be raised.
            Else the settings of the palette as defined will be used to create
            the color palette.
        rev (boolean): should the color map be reversed.

        *args: unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.
            @TODO has to be documented.

    Returns:
        No return. Raises a ValueError if a palette specified by input argument
            `palette` does not exist.

    Examples:
        >>> from colorspace.palettes import diverge_hcl
        >>> a = diverge_hcl(10)
        >>> a.colors(10)
        >>> b = diverge_hcl(10, "Blue-Yellow 3")
        >>> b.colors(10)

    .. todo::
        Try to make the code nicer (the part loading/overwriting settings).
        Looks messy and is extremely hard to debug. Rev implemented?
    """

    _allowed_parameters_ = ["h1", "h2", "c1", "l1", "l2", "p1"]

    def __init__(self, n, h = [260, 0], c = 80, l = [30, 90],
        power = 1.5, fixup = True, alpha = 1, palette = None, rev = False,
        *args, **kwargs):

        if isinstance(h, str):
            palette = h; h = None

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            n     = self._checkinput_(int,   1, False, False, n = n)
            h     = self._checkinput_(int,   2, True,  False, h = h)
            c     = self._checkinput_(int,   1, False, False, c = c)
            l     = self._checkinput_(int,   2, True,  False, l = l)
            power = self._checkinput_(float, 1, True,  False, power = power)
        except Exception as e:
            raise ValueError(e)

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
            settings["alpha"] = alpha
            settings["rev"]   = rev

        settings["n"] = n

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if key in self._allowed_parameters_:
                    settings[key] = val

        # Save settings
        self.settings = settings


    def data(self):
        return self._data_

    # Return hex colors
    def colors(self, n = None, fixup = True):

        if n is None: n = self.get("n")
        if n < 1:     return None

        if isinstance(fixup, bool): self.settings["fixup"] = fixup

        from numpy import abs, linspace, power, asarray, ndarray, ndenumerate
        from numpy import vstack, transpose
        from . import colorlib

        # Calculate H/C/L
        p2   = self.get("p1") if not self.get("p2") else self.get("p2")
        rval = linspace(1., -1., n)

        L = self.get("l2") - (self.get("l2") - self.get("l1")) * power(abs(rval), p2)
        C = self.get("c1") * power(abs(rval), self.get("p1"))
        from numpy import fmax
        C = fmax(.1,C)
        H = ndarray(n, dtype = "float")
        for i,val in ndenumerate(rval):
            H[i] = self.get("h1") if val > 0 else self.get("h2")

        # Create new HCL color object
        from colorlib import HCL
        HCL = HCL(H, C, L)

        # Return hex colors
        return HCL.colors(fixup = fixup)




# -------------------------------------------------------------------
# -------------------------------------------------------------------
class sequential_hcl(hclpalette):
    """Sequential HCL color palette.

    Parameters:
        n (inteter): number of values to be returned later.
        h (numeric): hue values. If only one value is given the
            value is recycled which yields a single-hue sequential
            color palette.
            If input `h` is a string this argument acts like the
            `palette` argument (see `palette` input parameter).
        c (numeric): chroma values, numeric of length to. If multiple
            values are provided only the first one will be used.
        l (numeric): luminance values, numeric of length to. If multiple
            values are provided only the first one will be used.
        power (numeric): power parameter for non-linear behaviour of the
            color palette. One or two values can be provided.
        fixup (boolean): only used when converting the HCL colors to hex.
            Should RGB values outside the defined RGB color space be
            corrected?
        alpha (numeric): Not yet implemented.
        palette (string): can be used to load a default diverging color palette
            specification. If the palette does not exist an exception will be raised.
            Else the settings of the palette as defined will be used to create
            the color palette.
        rev (boolean): should the color map be reversed.

        *args: unused.
        **kwargs: Additional arguments to overwrite the h/c/l settings.
            @TODO has to be documented.

    Returns:
        No return. Raises a ValueError if a palette specified by input argument
            `palette` does not exist.

    Examples:
        >>> from colorspace.palettes import sequential_hcl
        >>> a = sequential_hcl(10)
        >>> a.colors(10)
        >>> b = sequential_hcl(10, "Reds")
        >>> b.colors(10)

    .. todo::
        Try to make the code nicer (the part loading/overwriting settings).
        Looks messy and is extremely hard to debug. Rev implemented?

    .. todo::
        And there is definitively something wrong with the default palettes.
    """

    # Allowed to overwrite via **kwargs
    _allowed_parameters_ = ["h1", "c1", "c2", "l1", "l2", "p1", "p2"]

    def __init__(self, n, h = 260, c = [80, 30], l = [30, 90],
        power = 1.5, fixup = True, alpha = 1, palette = None, rev = False,
        *args, **kwargs):

        # If input "h" is a string: exchange with "palette"
        if isinstance(h, str):
            palette = h; h = None

        # _checkinput_ parameters (in the correct order):
        # dtype, length = None, recycle = False, nansallowed = False, **kwargs
        try:
            n     = self._checkinput_(int,   1, False, False, n = n)
            h     = self._checkinput_(int,   2, True,  False, h = h)
            c     = self._checkinput_(int,   2, True,  False, c = c)
            l     = self._checkinput_(int,   2, True,  False, l = l)
            power = self._checkinput_(float, 2, True,  False, power = power)
        except Exception as e:
            raise ValueError(e)

        # For handy use of the function
        if isinstance(h,str):
            palette = h; h = None

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            defaultpalettes = hclpalettes().get_palettes("Sequential (single-hue)")
            default_names    = [x.name() for x in defaultpalettes]
            if not palette in default_names:
                log.error("Palette \"{:s}\" is not a valid qualitative palette.".format(palette))
                log.error("Choose one of: {:s}".format(", ".join(default_names)))
                sys.exit(9)

            # Else pick the palette
            pal = defaultpalettes[default_names.index(palette)]

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in pal.parameters(): pal.set(key, value)

            # Getting settings
            settings = pal.get_settings()
        else:
            settings = {}

            # User settings
            settings["h1"]    = h[0]
            settings["h2"]    = h[0] if len(h) == 1 else h[1]
            settings["c1"]    = c[0]
            settings["c2"]    = c[1]
            settings["l1"]    = l[0]
            settings["l2"]    = l[1]
            settings["p1"]    = power[0]
            settings["p2"]    = power[1]
            settings["fixup"] = fixup
            settings["alpha"] = alpha
            settings["rev"]   = rev

        # Number of colors
        settings["n"] = n

        # If keyword arguments are set:
        # overwrite the settings if possible.
        if kwargs:
            for key,val in kwargs.items():
                if key in self._allowed_parameters_:
                    settings[key] = val

        # Save settings
        self.settings = settings


    # Return hex colors
    def colors(self, n = None, fixup = True):

        if n is None: n = self.get("n")
        if n < 1:     return None

        if isinstance(fixup, bool): self.settings["fixup"] = fixup

        from numpy import abs, linspace, power, asarray, ndarray, ndenumerate
        from numpy import vstack, transpose
        from . import colorlib

        # Calculate H/C/L
        rval = linspace(1., 0., n)
        p1   = self.get("p1")
        p2   = p1 if not self.get("p2") else self.get("p2")
        c1   = self.get("c1")
        c2   = c1 if not self.get("c2") else self.get("c2")
        l1   = self.get("l1")
        l2   = l1 if not self.get("l2") else self.get("l2")
        h1   = self.get("h1")
        h2   = h1 if not self.get("h2") else self.get("h2")

        L = l2 - (l2 - l1) * power(rval, p2)
        C = c2 - (c2 - c1) * power(rval, p1)
        H = h2 - (h2 - h1) * rval

        # Create new HCL color object
        from colorlib import HCL
        HCL = HCL(H, C, L)

        # Return hex colors
        return HCL.colors(fixup = fixup)

































