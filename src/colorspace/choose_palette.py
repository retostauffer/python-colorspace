
import sys
from tkinter import *

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
class Slider(object):
    """Slider Constructor

    Initializes a new Slider object for the graphical user interface
    :py:class:`gui`. A Slider is a combination of a `Tk.Frame`
    including a `Tk.Label`, `Tk.Slider`, and a `Tk.Entry` element with
    all necessary interactions.

    Args:
        x (int): X-position on the Tk interface.
        y (int): Y-position on the Tk interface.
        width (int): Width of the Slider object (`Tk.Frame` taking up `Tk.Scale`,
            `Tk.Label`, and `Tk.Entry`).
        height (int): height of the Slider object (`Tk.Frame` taking up `Tk.Scale`,
            `Tk.Label`, and `Tk.Entry`).
        type_ (str): Name of the Slider.
        from_ (float): Lower value of the Slider (see :py:func:`isValidInt`,
            :py:func:`isValidFloat`).
        to (numeric): Upper value of the Slider (see :py:func:`isValidInt`,
            :py:func:`isValidFloat`).
        resolution (float): Resolution of the slider, the increments when moving the Slider.
        **kwargs: Unused.
    """

    _Frame     = None # Used to store the Tk.Frame object
    _Scale     = None # Used to store the Tk.Scale object
    _Label     = None # Used to store the Tk.Label object
    _Entry     = None # Used to store the Tk.Entry object
    _Value     = None # Used to store/trac the current value of the Slider
    _name      = None # Name of the slider
    _is_active = True # Bool, used to store the Slider state

    FGACTIVE     = "#b0b0b0"
    BGACTIVE     = "#b0b0b0"
    FGDISABLED   = "#dadada"
    BGDISABLED   = "#efefef"
    DISABLED     = "#b0b0b0"
    BGDEFAULT    = "#d9d9d9"


    def __init__(self, master, name, x, y, width, height, active,
                 type_, from_, to, resolution, **kwargs):

        if type_ == "int":
            self._Value = IntVar(master)
            vcmd = getattr(self, "isValidInt")
        elif type_ == "float":
            self._Value = DoubleVar(master)
            vcmd = getattr(self, "isValidFloat")
        else:
            raise Exception(f"unexpected input on argument `type_` when initializing {self.__class__.__name__}")

        self._name = name

        # Frame around the slider objects
        self._Frame = Frame(master)
        self._Frame.place(x = x, y = y, width = width, height = height)

        # Object handling slider actions/callbacks
        self._Scale = Scale(self._Frame, variable = self._Value, orient = HORIZONTAL,
                showvalue = 0, length = width - 100, width = 15, 
                from_ = from_, to = to, resolution = resolution)
        self._Scale.place(x = 50)

        # Placing the label
        self._Label = Label(self._Frame, text = name.upper())
        self._Label.config(anchor = CENTER)
        self._Label.place(x = 0)

        # Adding text element
        self._Entry = Entry(self._Frame, bd = 0, width = 4)
        self._Entry.insert(INSERT, 0)

        # Register a function which checks if the user input is valid or not.
        vcmd = self._Entry.register(vcmd)
        self._Entry.config(justify = RIGHT, validate = "key",
                           validatecommand = (vcmd, "%P", from_, to))
        self._Entry.place(x = width - 40)

        # Changing the Tk.Value triggers the GUI update
        def fun(event, parent):
            val = event.widget.get()
            # Empty? Use existing value
            if len(val) == 0:
                event.widget.insert(0, self._Value.get())
            # Else change value
            else:
                # Just to double-check: must be a number
                try:
                    val = float(val)
                    self._Value.set(event.widget.get())
                # This exception should never happen!
                except:
                    pass
        self._Entry.bind("<Return>",   lambda event: fun(event, self))
        self._Entry.bind("<FocusOut>", lambda event: fun(event, self))

        # Tracing the _Value
        self._Value.trace(mode = "w", callback = self.OnTrace)

        # Disable if necessary
        if not active: self.disable()

    def isValidInt(self, x, from_ = -999, to = 999):
        """Check for Valid Integer

        Helper function to check whether `x` is a valid int
        in the range `[from_, to]`.

        Args:
            x (int): Value to be validated.
            from_ (int): Lower limit of the valid range, defaults to `-999`.
            to (int): Upper limit of the valid range, defaults to `999`.

        Returns:
            bool: Returns `True` if `x` is a valid float within
            `[from_, to]` and `False` otherwise.
        """
        # If empty
        if len(x) == 0: return True
        import re
        # If not matching signed int: return False
        if not re.match("^-?(0|[1-9]|[1-9][0-9]{1,2})?$", x): return False
        # Only a "-": that's OK
        if re.match("^-$", x): return True
        # Outside range? Return False
        if float(x) < float(from_) or float(x) > float(to):
            return False
        # Else True
        return True

    def isValidFloat(self, x, from_ = -999., to = 999.):
        """Check for Valid Float

        Helper function to check whether `x` is a valid float
        in the range `[from_,to]`.

        Args:
            x (float): Value to be validated.
            from_ (float): Lower limit of the valid range, defaults to `-999.`.
            to (float): Upper limit of the valid range, defaults to `999.`.

        Returns:
            bool: Returns `True` if `x` is a valid float within
            `[from_, to]` and `False` otherwise.
        """
        # If empty
        if len(x) == 0: return True
        # If no valid float: return False
        try:
            x     = float(x)
            from_ = float(from_)
            to    = float(to)
        except Exception as e:
            return False
        # If more than one digits:
        import re
        if from_ >= 0:
            if not re.match("[0-9]+(\\.|\\.[0-9])?$", str(x)): return False
        else:
            if not re.match("-?[0-9]+(\\.|\\.[0-9])?$", str(x)): return False
        return True

    def OnTrace(self, *args, **kwargs):
        """On Trace Action

        Triggered when :py:func:`Slider.trace` is triggered. The method
        is loading the current value and sets the `Tk.Scale` and
        `Tk.Entry` element to the new value.
        """
        val = self._Value.get()
        self.set(self._Value.get())

    def name(self):
        """Slider Name

        Returns the name of the current slider (the object).

        Returns:
            str: Returns the name of the :py:class:`Slider`.
        """
        return self._name

    def set(self, val):
        # Ensure it is integer if slider only accepts integer
        if isinstance(self._Value, IntVar): val = int(val)
        # Setting slider
        self._Scale.set(val)
        # Setting Text
        self._Entry.delete(0, END)
        self._Entry.insert(0, val)

    def get(self):
        """Get Value

        Allows to get the current value of the slider (the object).

        Returns:
            int, float: Returns the current value of the slider.  The return
            value depends on the slider configuration (`int` or `float`).
        """
        return self._Value.get()


    def trace(self, mode, *args, **kwargs):
        """Trace Method

        Trace method of the :py:class:`Slider` object.

        Args:
            mode (str): Default is `w` (call observer when variable is written).
            args: Passed to `Tkinter.<vartype>.trace()`, at least
                one argument (a callback function) should be provided.
            **kwargs: Passed to `Tkinter.<vartype>.trace()`, unused.
        """
        self._Value.trace(mode, *args, **kwargs)

    def disable(self):
        """Disable Slider

        Disables the current slider (the object).
        """

        self._Scale.configure(state = "disabled",
                relief = FLAT,
                bg = self.FGDISABLED,
                activebackground = self.FGDISABLED,
                troughcolor = self.BGDISABLED)
        self._Label.configure(fg = self.DISABLED)
        self._Entry.configure(state = "disabled",
                relief = FLAT,
                fg = self.DISABLED,
                bg = self.BGDISABLED)
        self._is_active = False
        self._Entry.delete(0, END)
        self._Entry.insert(0, 0)

    def enable(self):
        """Enable Slider

        Enables the current slider (the object).
        """

        self._Scale.configure(state = "active",
                bg = self.FGACTIVE,
                activebackground = self.FGACTIVE,
                troughcolor = self.BGACTIVE)
        self._Label.configure(fg = "black")
        self._Entry.configure(state = "normal",
                relief = FLAT,
                fg = "#000000", bg = "white")
        self._is_active = True

    def is_active(self):
        """Check if Active

        To check if the slider is currently active or not.

        Returns:
            bool: Returns `True` if the :py:class:`Slider` is active
            and `False` otherwise.
        """
        return self._is_active



# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
class defaultpalettecanvas(object):
    """Draw Default Palette Canvas

    Sets up a `Tk.Canvas` element containing the colors of the default
    HCL color palettes which will be placed in the top part of the GUI.

    Args:
        palframe (Tk.Frame): The bounding `Tk.Frame` which takes up the palettes.
        sliders (list): List of :py:class:`Slider` objects. When a user selects a new
            default palette the sliders will be set to the specification
            given the selected palette (and enabled/disabled corresponding
            to the palette specification).
        pal (defaultpalette): The default color palette.
        n (int): Number of colors to be drawn.
        xpos (float): X-position within `Tk.Canvas` (palframe input).
        figwidth (float): Width of the `Tk.Canvas` element (palframe input).
        figheight (float): Width of the `Tk.Canvas` element (palframe input).
    """

    def __init__(self, palframe, sliders, pal, n, xpos, figwidth, figheight):  

        self._palframe = palframe
        self._sliders  = sliders
        self._pal      = pal

        colors = pal.colors(n)
        self._draw_canvas(colors, xpos, figwidth, figheight)

    def _draw_canvas(self, colors, xpos, figwidth, figheight):

        # Compute width and height of the color map
        offset = 0 # White frame around the palettes
        n = len(colors)
        h = (figheight - 2. * offset) / len(colors)
        w = figwidth  - 2. * offset

        canvas = Canvas(self._palframe, width = figwidth,
                        height = figheight, bg = "#ffffff")
        canvas.place(x = xpos, y = 0)
        # Binding for interaction
        canvas.bind("<Button-1>", lambda event: \
                self._activate(event, self._pal, self._sliders))

        for i in range(0, n):
            canvas.create_rectangle(offset, i*h, w, (i+1)*h,
                                    width = 0, fill = colors[i])

    def _activate(self, event, pal, sliders):

        # Loading settings of the current palette
        settings = pal.get_settings()

        # For some palettes, elements can be lambda functions (mainly h1, h2).
        # Run over all settings and execute the function. For that, we need n
        for k,v in settings.items():
            if callable(v):
                if v.__code__.co_argcount == 1:
                    settings[k] = v(7)
                else:
                    settings[k] = v(7, settings["h1"])

        # Setting sliders
        for elem in sliders:
            # Setting value, enables the slider
            if elem.name() == "n":
                continue
            elif elem.name() in settings.keys():
                elem.set(settings[elem.name()])
                elem.enable()
            # Disable slider
            else:
                elem.disable()


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
class currentpalettecanvas:
    """Draw Current Palette Canvas

    Draws the current palette (the palette as specified on the
    GUI), will be displayed in the lower part of the GUI.

    Args:
        parent (`Tk`): The `Tk` object (interface).
        x (float): X-position on the interface.
        y (float): Y-position on the interface.
        width (float): Width of the palette on the interface.
        height (float): Height of the palette on the interface.
    """

    def __init__(self, parent, x, y, width, height):

        self.parent = parent
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height

        self.canvas = Canvas(self.parent, width = self.width, height = self.height)
        self.canvas.config(borderwidth = 1, bg = "#000000")
        self.canvas.place(x = self.x, y = self.y + 20)

    def _draw_canvas(self, colors):

        from numpy import floor

        n = len(colors)
        w = floor(float(self.width) / float(len(colors)))
        h = self.height
        # Overwrite everything with a white box
        self.canvas.create_rectangle(0, 0, self.width, self.height + 1, width = 0, fill = "white")
        for i in range(0, n):
            if colors[i] is None: continue
            # Dropping Nan's
            if len(str(colors[i])) < 7: continue
            # Last box to self.width
            x1 = (i+1) * w if i < (n-1) else self.width
            self.canvas.create_rectangle(i*w, 0, x1, h+1,
                    width = 0, fill = colors[i])



# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
def choose_palette(**kwargs):
    """Graphical user interface to choose HCL based color palettes

    Opens a Tcl/Tk based graphical user interface (GUI) which allows
    to tweak existing Hue-Chroma-Luminance (HCL) based color palettes
    and define custom palettes.

    Args:
        **kwargs: Optional, can be used to change the defaults when starting the
            GUI. Currently a parameter called `palette` is allowed to
            specify the initial color palette. If not set, `palette = "Blue-Red"`
            is used.

    Returns:
        hclpalette: An HCL palette object which allows to extract the colors in
        different ways. The default is to retrieve hex colors.
        More details on:
        :py:class:`diverging_hcl <colorspace.palettes.diverging_hcl>`,
        :py:class:`qualitative_hcl <colorspace.palettes.qualitative_hcl>`, or
        :py:class:`sequential_hcl <colorspace.palettes.sequential_hcl>`.
    """

    obj = gui(**kwargs)
    obj.mainloop()

    from . import palettes
    method = getattr(palettes, obj.method())

    # Overwrite __init__ method, add new defaults
    import sys
    if sys.version_info.major < 3:
        varnames = list(method.__init__.im_func.func_code.co_varnames)
        defaults = list(method.__init__.im_func.func_defaults)
    else:
        varnames = list(method.__init__.__code__.co_varnames)
        defaults = list(method.__init__.__defaults__)


    # Getting current parameters from slider object
    settings = {}
    for s in obj.sliders():
        # Only read active sliders
        if not s.is_active(): continue
        # If active, store current value
        settings[s.name()] = s.get()

    # Prepare new default arguments
    for key in ["h","c","l","p"]:
        k1  = f"{key}1"
        k2  = f"{key}2"
        key = "power" if key == "p" else key
        if k1 in settings.keys() and k2 in settings.keys():
            settings[key] = [settings[k1], settings[k2]]
            del settings[k1]
            del settings[k2]
        elif k1 in settings.keys():
            settings[key] = settings[k1]
            del settings[k1]
        elif k2 in settings.keys():
            settings[key] = settings[k2]
            del settings[k2]

    for idx,key in enumerate(varnames[1:(len(defaults)+1)]):
        if key in settings.keys():
            defaults[idx] = settings[key]

    import types
    method.__init__ = types.FunctionType(method.__init__.__code__,
                                         method.__init__.__globals__,
                                         method.__init__.__name__,
                                         tuple(defaults),
                                         method.__init__.__closure__)

    return method()


# -------------------------------------------------------------------
# This is the GUI itself (called by choose_palette which is handling
# the return).
# -------------------------------------------------------------------
class gui(Tk):
    """Graphical user interface to choose custom HCL-based color palettes

    Args:
        **kwargs: Optional, can be used to change the defaults when starting the
            GUI. Currently a parameter called `palette` is allowed to
            specify the initial color palette. If not set, `palette = "Blue-Red"`
            is used.

    Example:

        >>> colorspace.choose_palette()
    """

    WIDTH = 400
    HEIGHT = 700
    FRAMEHEIGHT = 100
    FRAMEWIDTH  = WIDTH - 20

    # Slider settings
    _slider_settings = {
        "h1"   : {"type": "int",   "from": -360, "to": 360, "resolution": 1},
        "h2"   : {"type": "int",   "from": -360, "to": 360, "resolution": 1},
        "c1"   : {"type": "int",   "from": 0,    "to": 100, "resolution": 1},
        "cmax" : {"type": "int",   "from": 0,    "to": 180, "resolution": 1},
        "c2"   : {"type": "int",   "from": 0,    "to": 100, "resolution": 1},
        "l1"   : {"type": "int",   "from": 0,    "to": 100, "resolution": 1},
        "l2"   : {"type": "int",   "from": 0,    "to": 100, "resolution": 1},
        "p1"   : {"type": "float", "from": 0,    "to": 3,   "resolution": .1},
        "p2"   : {"type": "float", "from": 0,    "to": 3,   "resolution": .1},
        "n"    : {"type": "int",   "from": 2,    "to": 30,  "resolution": 1}
    }
    _sliders = []

    # Canvas for the current palette
    _currentpalette = None

    # Drop down menu (Dropdown)
    _Dropdown       = None

    # Frame taking up the default palettes
    _palframe       = None

    # Tkiter object for the demo
    _demoTk         = None

    # Used to store the control buttons (desaturate, reversed, ...)
    _control        = None

    # Used with the .after method to 'lock' updating/calling certain tkinter functions
    _locked         = False

    # Initialize defaults
    _setting_names = ["h1", "h2", "c1", "cmax", "c2", "l1", "l2", "p1", "p2", "n"]
    _settings       = {}
    for key in _setting_names:
        _settings[key] = 7 if key == "n" else None

    def __init__(self, **kwargs):
        super().__init__()

        # Initialization arguments, if any
        init_args = {}
        # Default if no inputs are set
        if not "palette" in kwargs.keys():  palette = "Blue-Red"
        else:                               palette = kwargs["palette"]

        # Find initial values
        from . import hclpalettes
        self._palettes = hclpalettes()
        pal            = self._palettes.get_palette(palette)

        # Store palette name and palette type to select
        # the correct drop down entries
        init_args["name"] = pal.name()
        init_args["type"] = pal.type()
        for key,val in pal.get_settings().items():
            init_args[key] = val

        # Save palette settings
        self.settings(**pal.get_settings())

        # Initialize gui
        self._master         = self._init_master()

        # The different palette types
        self._Dropdown       = self._add_paltype_dropdown(pal.type())

        # Adding current palette has to be before the sliders
        # as they need the current palette canvas for the
        # to be able to be reactive.
        self._sliders        = self._add_sliders()

        # Adding drop down menu and select color map
        # Add the frame with the default palettes
        # on top of the GUI
        self._palframe       = self._add_palframe(pal.type())

        ## Add the horizontal color map for current colors.
        self._currentpalette = self._add_currentpalettecanvas()
        self._draw_currentpalette()

        self._DEMO           = self._add_demo_options()
        self._add_return_button()

        # Adding control checkboxes and radio buttons
        self._control = self._add_control()

    def _add_paltype_dropdown(self, type_):
        """Add Palette Type Option

        Adds a drop down menu to the GUI which allows to
        switch between the different types of the default
        palettes (see also :py:class:`palettes.hclpalettes`).

        Args:
            type_ (str): The default selected palette type on GUI initialization.
        """

        # Removing DivergingX class of HCL palettes; not included in choose_palette
        from re import match
        opts = []
        for o in self.palettes().get_palette_types():
            if not match(r".*DivergingX", o): opts.append(o)

        paltypevar = StringVar(self)
        paltypevar.set(type_) # default value

        # Option menu
        menu = OptionMenu(self, paltypevar, *opts, command = self.OnPaltypeChange)
        menu.config(width = 40, pady = 5, padx = 5)
        menu.grid(column = 1, row = len(opts))
        menu.place(x = 10, y = 30)

        return paltypevar

    def OnPaltypeChange(self, *args, **kwargs):
        """On Palette Type Changed Action

        The callback function of the drop down element. Triggered
        every time the drop down element changes.
        """

        import time

        self._locked = True

        # Updating the palette-frame.
        self._palframe = self._add_palframe(args[0])

        # Take first palette
        p = self.palettes().get_palettes(args[0], exact = True)[0]

        # Enable/disable/set sliders
        settings = p.get_settings()
        
        n = 7
        for elem in self.sliders():
            if elem.name() == "n":
                n = elem.get()
                break

        # For some palettes, elements can be lambda functions (mainly h1, h2).
        # Run over all settings and execute the function.
        for k,v in settings.items():
            if callable(v):
                if v.__code__.co_argcount == 1:
                    settings[k] = v(n)
                else:
                    settings[k] = v(n, settings["h1"])

        # Setting up slider
        for elem in self.sliders():
            # Setting value, enables slider
            if elem.name() == "n":
                continue
            elif elem.name() in settings.keys():
                elem.set(settings[elem.name()])
                elem.enable()
            # Disable slider
            else:
                elem.disable()

        # All sliders set; unlock and call _draw_currentpalette()
        self._locked = False
        time.sleep(0.1)
        self._draw_currentpalette()

    def _add_control(self):
        """Add Control Options

        Adds the check buttons (`Tk.Checkbutton`) and radio button
        (`Tk.Radiobutton`) elements. Color fixup, revert colors,
        and CVD options.
        """
        control = {}

        frame = Frame(self, height = 30, width = self.WIDTH - 20)
        frame.grid()
        frame.place(x = 10, y = self.HEIGHT - 140)
        col = 0; row = 0

        # Fixup colors
        fixupvar      = BooleanVar()
        fixupbutton   = Checkbutton(frame, text="Fixup colors",
                                    variable = fixupvar, command = self.OnChange)
        fixupbutton.grid(column = col, row = row, sticky = "w"); row += 1
        fixupbutton.select()
        control["fixup"] = fixupvar

        # Reverse colors
        revvar      = BooleanVar()
        revbutton   = Checkbutton(frame, text="Reverse colors",
                                  variable = revvar, command = self.OnChange)
        revbutton.grid(column = col, row = row, sticky = "w"); row += 1
        control["reverse"] = revvar

        # Buttons for Desaturation/CVD
        ypos = self.HEIGHT - 40

        desatvar    = BooleanVar()
        desatbutton = Checkbutton(frame, text="Desaturation",
                                  command = self.OnChange, variable = desatvar)
        desatbutton.grid(column = col, row = row, sticky = "w"); row += 1
        control["desaturate"] = desatvar

        cvdvar      = BooleanVar()
        cvdbutton   = Checkbutton(frame, text="Color blindness",
                                  command = self.OnChange, variable = cvdvar)
        cvdbutton.grid(column = col, row = row, sticky = "w"); col += 1
        control["cvd"] = cvdvar

        # Radio buttons for CVD
        ypos = self.HEIGHT - 20
        cvdtypevar  = StringVar()
        radio_deutan = Radiobutton(frame, text = "deutan", command = self.OnChange,
                                   variable = cvdtypevar, value = "deutan")
        radio_protan = Radiobutton(frame, text = "protan", command = self.OnChange,
                                   variable = cvdtypevar, value = "protan")
        radio_tritan = Radiobutton(frame, text = "tritan", command = self.OnChange,
                                   variable = cvdtypevar, value = "tritan")
        radio_deutan.grid(column = col, row = row, sticky = "w"); col += 1
        radio_protan.grid(column = col, row = row, sticky = "w"); col += 1
        radio_tritan.grid(column = col, row = row, sticky = "w"); col += 1
        cvdtypevar.set("deutan")
        control["cvdtype"] = cvdtypevar

        return control

    def control(self):
        """Get control options

        Returns:
            dict: Returns a dictionary with the current control options (see
            :py:func:`_add_control`).
        """


        if not self._control:
            return {"reverse" : False, "desaturate" : False, "cvd" : False,
                    "cvdtype" : "deutan", "fixup": True}
        else:
            res = {}
            res["reverse"]    = self._control["reverse"].get()
            res["desaturate"] = self._control["desaturate"].get()
            res["cvd"]        = self._control["cvd"].get()
            res["cvdtype"]    = self._control["cvdtype"].get()
            res["fixup"]      = self._control["fixup"].get()
            return res


    def settings(self, *args, **kwargs):
        """Load or Store Current Palette Settings

        Used to load/store current palette settings (gui settings).

        Args:
            args: Strings to load one/several parameters.
            kwargs: Named arguments, used to store values.

        Returns:
            dict: Returns a dictionary with the current slider settings.
        """
        # Return current settings
        if len(args) == 0 and len(kwargs) == 0:
            return self._settings
        # Return some settings
        elif len(args):
            res = {}
            for key in args:
                if not isinstance(key, str): continue
                # Loading setting
                if key in self._setting_names:
                    res[key] = self._settings[key]
            if len(res) == 1:   return res[list(res.keys())[0]]
            else:               return reskk
        # Store values, if possible.
        else:
            for key,val in kwargs.items():
                if key in self._setting_names:
                    self._settings[key] = val

    def _init_master(self):
        """Initializes the `Tk` GUI window."""

        # initialize mater TK interface
        self.wm_title("Colorspace - Choose Color Palette")
        self.configure()
        self.resizable(width=False, height=False)
        self.geometry("{:d}x{:d}".format(self.WIDTH, self.HEIGHT))
        self.bind("<Destroy>", self._return_to_python)
        self.bind("<Return>", self._return_to_python)
        self.bind("<Escape>", self._return_to_python)

    def _destroy(self, x, *args, **kwargs):
        try:
            x.destroy()
        except:
            pass

    def palettes(self):
        """Get Palettes Available

        Returns:
            :py:class:`palettes.hclpalettes`: Returns the default palettes available.
        """
        return self._palettes

    def sliders(self):
        """Get Sliders

        Returns all slider elements.

        Returns:
            list: List of :py:class:`Slider` objects.
        """
        return self._sliders

    def palframe(self):
        """Get Palette Frame

        Returns:
            `Tk.Frame`: Returns the palette frame (`Tk.Frame` object, see
            :py:func:`_add_palframe`).
        """

        return self._palframe

    def _add_palframe(self, type_):
        """Add Palette Frame

        Adds a `Tk.Frame` to the `Tk` element (see :py:func:`_init_master`).
        This frame is used to take up the default palettes.
        """

        frame = Frame(self, bg = "#ffffff",
                      height = self.FRAMEHEIGHT, width = self.FRAMEWIDTH)
        frame.place(x = 10, y = 80)

        # Loading palettes of currently selected palette type
        from numpy import min, sum
        pals = self.palettes().get_palettes(type_, exact = True)
        for child in frame.winfo_children(): child.destroy()

        # Number of palettes to be drawn (where gui = 1 in palette config)
        npals    = sum([x.get("gui") for x in pals])

        # Adding new canvas
        figwidth = min([30, self.FRAMEWIDTH / npals])
        xpos = 0
        for pal in pals:
            if pal.get("gui") <= 0: continue
            defaultpalettecanvas(frame, self.sliders(), pal, 5, xpos, figwidth, self.FRAMEHEIGHT)
            xpos += figwidth

        return frame

    def _add_currentpalettecanvas(self):
        """
        Adds a `Tk.Canvas` object to the GUI to display the
        current color palette as specified by the GUI settings.

        Returns:
            `Tk.Canvas`: Returns the canvas.
        """
        canvas = currentpalettecanvas(self,
               x = 20, y = 500, width = self.WIDTH - 40, height = 30) 

        return canvas

    def _draw_currentpalette(self):
        """Draw Current Palette

        Shows the colors in the current palette frame."""

        # Re-draw the canvas.
        if not self._locked:
            self._currentpalette._draw_canvas(self.get_colors())

    def get_colors(self):
        """Get Colors

        Returns:
            list: Returns a list of hex colors and `nan` given the current
            settings on the GUI. `numpy.nan` will be returned if `fixup` is
            set to False but some colors lie outside the RGB color space.
        """

        # Getting current arguments
        params = {}
        for elem in self.sliders():
            if elem.is_active():
                params[elem.name()] = float(elem.get())

        # Small helper function to check if e.g., "c1", "c2", "cmax"
        # are parameters in the params dict. Scopes 'dim' (loop variable)
        # and 'params' (the parameters for this palette).
        def phas(x):
            return f"{dim}{str(x)}" in params.keys()

        # Similar to the 'phas' method but will return the 
        # actual value. Will throw an error if it does not exist (that means
        # you have not properly checked if has(x)!
        def pget(x):
            x = f"{dim}{str(x)}"
            assert x in params.keys(), Exception(f"get(\"{str(x)}\"): None or not existing")
            return params[x]

        # Similar to the two functions above.
        # Will delete an element from 'params', again scoping.
        def pdel(x):
            del params[f"{dim}{str(x)}"]

        # Manipulate params
        from re import match
        for dim in ["h", "c", "l", "p"]:

            # Generate "h1", "h2", "hmax" (if dim = h)
            # to check if these are available parameters.
            dim1 = f"{dim}1"
            dim2 = f"{dim}2"
            dim3 = f"{dim}max"
            dim  = "power" if dim == "p" else dim

            # All three available? That must be c1, c2, cmax.
            # Get it in the order [c1, cmax, c2] as the hcl palette function requires it.
            if phas(1) and phas(2) and phas("max"):
                params[dim] = [pget(x) for x in ["1", "max", "2"]]

            # If has 1 and 2: [c1, c2]
            elif phas(1) and phas("max"):
                # Diverging chemes: only [c1, cmax] allowed, for
                # others [c1, cmax] (sequential)
                if match(".*[Dd]iverging.*", self._Dropdown.get()) and dim == "c":
                    params[dim] = [pget(x) for x in ["1", "max"]]
                else:
                    params[dim] = [pget(1), pget("max")]
            # If has 1 and 2: [c1, c2]
            elif phas(1) and phas(2):
                params[dim] = [pget(x) for x in ["1", "2"]]

            # If has 1: [c1]
            elif phas(1):
                params[dim] = pget(1)

            # Remove the individual parameters from 'params'
            for x in ["1", "2", "max"]:
                if phas(x): pdel(x)

        # Loading 'n' from slider
        for elem in self.sliders():
            if elem.name() == "n":
                n = elem.get()
                break

        # Check if we have to return the colors reversed.
        # and whether or not fixup is set to True/False
        control = self.control()
        if not "h" in params.keys(): sys.exit("whoops, lost h")
        if "n" in params: del params["n"]
        params["fixup"] = control["fixup"]

        # Draw colors from current color map
        from . import palettes
        type_    = self._Dropdown.get()
        colorfun = self.palettes().get_palettes(type_, exact = True)[0].method()
        fun      = getattr(palettes, colorfun)

        # Return colors
        colors = fun(**params)(n, rev = control["reverse"])

        # Do we have to desaturate the colors?
        if control["desaturate"]:
            from .CVD import desaturate
            colors = desaturate(colors)

        # Do we have to apply CVD simulation?
        if control["cvd"]:
            from . import CVD
            fun = getattr(CVD, control["cvdtype"])
            colors = fun(colors)

        return colors

    def method(self):
        """Get Palette Class/Method

        Returns:
            str: Returns the name of the object which has to be called to get
            the colors. The name of the object is defined in the palconfig.
            config files. For "Diverging" palettes this will be
            :py:class:`palettes.diverging_hcl`, for "Qualitative"
            :py:class:`palettes.qualitative_hcl`, and for "Sequential" palettes
            :py:class:`palettes.sequential_hcl`.
        """
        type_    = self._Dropdown.get()
        colorfun = self.palettes().get_palettes(type_, exact = True)[0].method()
        return colorfun


    def _add_sliders(self):
        """Add Sliders

        Adds a set of sliders to the GUI.

        Returns:
            list: A list of :py:class:`Slider` objects.
        """

        sliders = []

        # For each key in self._setting_names add a Slider object
        # (a Slider is a combined Tkinter.Scale, Tkinter.Entry, and
        # Tkinter.Label element with bindings).
        for idx,key in enumerate(self._setting_names):
            # Initialize with default 0 if nothing yet specified.
            s = Slider(self,
                       key,                                            # name
                       10, 100 + idx * 30 + self.FRAMEHEIGHT,          # x, y
                       self.WIDTH - 20, 30,                            # width, height
                       False if self.settings()[key] is None else True,    # active
                       type_      = self._slider_settings[key]["type"],
                       from_      = self._slider_settings[key]["from"],
                       to         = self._slider_settings[key]["to"],
                       resolution = self._slider_settings[key]["resolution"])
            if not self.settings(key): s.set("0")
            else:                      s.set(str(self.settings(key)))

            # Append slider to list
            sliders.append(s)

        # Add the trace element to make them interactive
        # (an observer, call OnChange whenever the Scale changes).
        for x in sliders: x.trace("w", self.OnChange)

        return sliders

    # Callback when an item is getting changed
    def OnChange(self, *args, **kwargs):
        """On Slider Changed Action

        Triggered any time the slider values or control arguments change.
        Draws new current palette (see :py:func:`_draw_currentpalette`).
        """
        self._draw_currentpalette()

        # Is the demo running?
        if self._demoTk: self._show_demo()


    def _add_demo_options(self):
        """Add Demo Plot Options

        Adds a `Tk.Button` to open the demo plot window.
        """
        but = Button(self, text = "Demo",
                command = self._show_demo,
                pady = 5, padx = 5)
        but.place(x = self.WIDTH - 70, y = self.HEIGHT - 40)

        # Variable to store current selection
        opts = ["Bar", "Heatmap", "Pie", "Spine", "Matrix", "Lines", "Spectrum"]
        demovar = StringVar(self)
        demovar.set(opts[0]) # default value

        # Demo plot option menu. No callback
        menu = OptionMenu(self, demovar, *opts, command = self.OnChange)
        menu.config(width = 10, pady = 5, padx = 5)
        menu.grid(column = 1, row = len(opts))
        menu.place(x = 180, y = self.HEIGHT - 40)

        return demovar

    def _add_return_button(self):
        """Add Return Button

        Adds the button to return to Python, a `Tk.Button` element.
        When clicked :py:func:`_return_to_python` is triggered (callback
        function for this button).
        """

        but = Button(self, text = "Return to Python",
                command = self._return_to_python, pady = 5, padx = 5)
        but.place(x = 10, y = self.HEIGHT - 40)


    def _return_to_python(self, *args):
        """Return To Python

        Used when closing the GUI, returning the current palette.

        Returns to :py:func:`choose_palette`. Destroys the `Tk` interface
        but not the object such that :py:func:`choose_palette` can read the
        settings of the sliders and control elements. Used to create the
        palette which will then be returned to the console/user console.
        """
        # Close demo window if not already closed
        try:
            self._demoTk.quit() # or .destroy()
        except:
            pass
        self.quit()


    def _show_demo(self):
        """Show Demo Plot

        Requires matplotlib to be installed.
        """
        try:
            import matplotlib
            matplotlib.use("TkAgg")
            hasmatplotlib = True
        except:
            hasmatplotlib = False

        # If has matplotlib: plot
        if hasmatplotlib:

            def draw_figure(canvas, figure, loc=(0, 0)):
                """Draw a matplotlib figure onto a Tk canvas

                loc (list of int): location of top-left corner of figure on canvas in pixels.

                Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
                """
                figure_canvas_agg = FigureCanvasAgg(figure)
                figure_canvas_agg.draw()
                figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
                figure_w, figure_h = int(figure_w), int(figure_h)
                photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)

                # Position: convert from top-left anchor to center anchor
                canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

                # Unfortunately, there's no accessor for the pointer to the native renderer
                tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

                # Return a handle which contains a reference to the photo object
                # which must be kept live or else the picture disappears
                return photo


            # Getting demo plotting function
            from . import demos
            fun = getattr(demos, self._DEMO.get())

            # Initialize (or update) the app
            if not self._demoTk:
                root = Tk()
                self._demoTk = DemoApp(root, fun, self.get_colors())
                self._demoTk.bind("<Destroy>", self._close_demo)
            else:
                self._demoTk.plot(fun, self.get_colors())

        else:

            info = [""]
            info.append("To be able to run the demo plots")
            info.append("the Python matplotlib package has to be")
            info.append("installed.")
            info.append("")
            info.append("Install matplotlib and try again!")

            txt = Text(self._demoTk, height=10, width=45)
            txt.pack()
            txt.insert(END, "\n".join(info))

    def _close_demo(self, *args, **kwargs):
        if not self._demoTk is None: self._demoTk.destroy()
        self._demoTk = None


# Tcl/Tk helper class for demo plots
class DemoApp(Frame):
    def __init__(self, master, fun, colors):
        from tkinter import Frame
        from matplotlib import pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        Frame.__init__(self, master)
        self.fig    = plt.figure(figsize = (8, 8), clear = True)
        self.master = master

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.master)

        self.plot(fun, colors)
        self.canvas.get_tk_widget().grid(row = 0, column = 1)

    def plot(self, fun, colors):
        if not callable(fun):
            raise TypeError("argument `fun` must be a callable function")

        # Clearing figure, adding axis and call plotting function
        self.fig.clear(True)
        ax     = self.fig.add_axes([0.025, 0.025, 0.95, 0.95])
        fun(colors, ax = ax, fig = self.fig)
        self.canvas.draw()

