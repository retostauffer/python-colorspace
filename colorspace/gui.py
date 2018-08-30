

from Tkinter import *


class ddObject(object):

    def __init__(self, master, sliders, name, palettes, init_args = None):

        self.master   = master
        self.name     = name
        self.palettes = palettes
        self.sliders  = sliders

        # Adding options menu
        opts = palettes.get_palette_types()

        # If init args contain type: use this type
        type_ = None # Default/not selected
        if not init_args == None:
            if "type" in init_args.keys():
                type_ = init_args["type"]
                if not type_ in opts:
                    log.error("Selected palette type \"{:s}\" does not exist. Stop.".format(type_))
                    sys.exit(9)
        type_ = opts[0] if type_ is None else type_

        # Adding dropdown menu with default arguments if init_args
        # was empty, or the settings provided by the user stored on
        # init_args (slider settings, selected dropdown item, ...)
        dropOpts = StringVar(master)
        dropOpts.set(type_) # default value
        self.selected(type_, init_args) # Initialize palettes

        #self.dd_type = apply(OptionMenu, (self.master, dropOpts) + tuple(opts))
        self.dd = OptionMenu(master, dropOpts, *opts,
                   command = self.selected)
        self.dd.config(width = 25, pady = 5, padx = 5)
        self.dd.grid(column = 1, row = len(opts))
        self.dd.place(x = 10, y = 30)
    
    def selected(self, val, args = None):

        print("New item selected ({:s})".format(val))
        pals = self.palettes.get_palettes(val)

        self._set_sliders_(pals[0], args)


    def _set_sliders_(self, pal, args = None):

        if args is None: args = {}

        for x in self.sliders:
            slider_id = x.getid()
            value     = pal.get(slider_id)
            # Take value from "args" if specified, else
            # the one from the palette.
            if slider_id in args.keys():  value = args[slider_id]
            if not value is None:         x.setvalue(value)


    def _add_dropdown_palettes_(self):

        opts = self.palettes.get_palette_types()

        dropOpts = StringVar(self.master)
        dropOpts.set(opts[0]) # default value

        obj = ddObject("type")

        #self.dd_type = apply(OptionMenu, (self.master, dropOpts) + tuple(opts))
        self.dd_type = OptionMenu(self.master, dropOpts, *opts,
                        command = obj.selected)
        self.dd_type.config(width = 25, pady = 5, padx = 5)
        self.dd_type.grid(column = 1, row = len(opts))
        self.dd_type.place(x = 10, y = 30)


class sliderObject(object):

    def __init__(self, name):

        self.name = name

        # Store the tag
        import re
        mtch = re.match("^slider_(.*)$", name)
        if not mtch:
            log.error("Whoops, slider name does not match \"^slider_(.*)$\".")
            sys.exit(9)
        self.id = mtch.group(1).lower()

    def callback(self, event):

        self.value.delete("1.0", END)
        self.value.insert(INSERT,event)
        self.value.tag_add("right", "1.0", "end")

    def getname(self):
        return self.name

    def getid(self):
        return self.id

    def setvalue(self, val = None):
        # Reading text value and adjust slider
        if not val:
            val = self.value.get("1.0",END)
        self.slider.set(val)

    def bind(self, slider, label, value, button):
        self.slider = slider
        self.label  = label
        self.value  = value
        self.button = button

class gui(object):

    width = 300
    height = 500

    _sliders_ = []

    def __init__(self, **kwargs):

        from . import palettes
        self.palettes = palettes()

        # Initialization arguments, if any
        init_args = {}
        # Default if no inputs are set
        if not "palette" in kwargs.keys():  palette = "Blue-Red"
        else:                               palette = kwargs["palette"]

        # Find initial values
        pal = self.palettes.get_palette(palette)
        # Store palette name and palette type to select
        # the correct dropdown entries
        init_args["name"] = pal.name()
        init_args["type"] = pal.type()
        for key,val in pal.settings().iteritems():
            init_args[key] = val

        # Custom user arguments on top
        for key,val in kwargs.iteritems(): init_args[key] = val

        # Initialize gui
        self._init_master_()
        self._add_sliders_()
        self._add_demo_options_()
        # Has to be called _after_ sliders have been added
        self._add_dropdown_type_(init_args = init_args)

        mainloop()

    def _init_master_(self):

        # initialize mater TK interface
        self.master = Tk()
        self.master.wm_title("Colorspace - Choose Color Palette")
        self.master.configure()
        self.master.resizable(width=False, height=False)
        self.master.geometry("{:d}x{:d}".format(self.width, self.height))


    def _add_dropdown_type_(self, init_args = None):

        self.dd_type = ddObject(self.master, self._sliders_, "type",
                                self.palettes, init_args = init_args)

    def _add_sliders_(self):

        self._add_slider_("slider_H1", -360, 360, "H1")
        self._add_slider_("slider_H2", -360, 360, "H2")
        self._add_slider_("slider_L1",    0, 100, "L1")
        self._add_slider_("slider_L2",    0, 100, "L2")

        self._add_slider_("slider_C1",    0, 100, "C1")
        self._add_slider_("slider_C2",    0, 100, "C2")
        self._add_slider_("slider_P1",    0,   3, "P1")
        self._add_slider_("slider_P1",    0,   3, "P2")

    def _add_slider_(self, name, from_, to, label, resolution = 1, orient = HORIZONTAL):

        # Position of the current slider
        ypos = len(self._sliders_) * 40 + 100

        # Object handling slider actions/callbacks
        obj = sliderObject(name)

        # Slider element
        h = Scale(self.master, var = name, from_ = from_, to = to,
                  command = obj.callback, showvalue = 0,
                  resolution = resolution, orient = orient)
        h.place(x = 50, y = ypos)

        # Label (static text)
        lab = Label(self.master, text = label)
        lab.config(anchor = CENTER)
        lab.place(x = 20, y = ypos) 

        # Button to change the value
        but = Button(self.master, text = "SET", command = obj.setvalue,
                pady = 0, padx = 0)
        but.place(x = 200, y = ypos)

        # Value (shows current slider value)
        val = Text(self.master, bd = 0, height = 1, width = 4)
        val.insert(INSERT, 0)
        val.tag_configure("right", justify="right")
        val.place(x = 160, y = ypos) 
        val.tag_add("right", "1.0", "end")

        obj.bind(h, lab, val, but)

        # Append slider object
        self._sliders_.append(obj)


    def _add_demo_options_(self):

        but = Button(self.master, text = "Demo", command = self._show_demo_,
                pady = 5, padx = 5)
        but.place(x = 30, y = 470)

    def _show_demo_(self):

        self.top = Toplevel()
        self.top.geometry("{:d}x{:d}".format(400, 400))

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        import numpy as np

        x = np.random.normal(0,2,100)
        y = np.random.normal(0,2,100)

        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        a.scatter(x,y,color='red')
        a.invert_yaxis()

        a.set_title ("Estimation Grid", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master = self.top)
        canvas.get_tk_widget().pack()
        canvas.draw()

        self.top.mainloop()
