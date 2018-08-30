

import sys
if sys.version_info.major < 3:
    from Tkinter import *
else:
    from tkinter import *


class ddObject(object):

    def __init__(self, parent, name, init_args = None):

        self.parent   = parent
        self.master   = parent.master
        self.palettes = parent.palettes
        self.sliders  = parent._sliders_
        self.name     = name

        # Adding options menu
        opts = parent.palettes.get_palette_types()

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
        dropOpts = StringVar(parent.master)
        dropOpts.set(type_) # default value
        self.selected(type_, init_args) # Initialize palettes

        #self.dd_type = apply(OptionMenu, (self.master, dropOpts) + tuple(opts))
        self.dd = OptionMenu(parent.master, dropOpts, *opts,
                   command = self.selected)
        self.dd.config(width = 25, pady = 5, padx = 5)
        self.dd.grid(column = 1, row = len(opts))
        self.dd.place(x = 10, y = 30)
    
    def selected(self, val, args = None):

        print("New item selected ({:s})".format(val))

        self._selected_ = val
        pals = self.palettes.get_palettes(val)

        self._set_sliders_(pals[0], args)
        if hasattr(self.parent, "dd_type"):
            self.parent._add_palette_frame_()

    def get(self):
        return self._selected_

    def _set_sliders_(self, pal, args = None):

        if args is None: args = {}

        # Allowed parameter
        parameter = pal.parameters()

        for x in self.sliders:
            slider_id = x.getid()
            value     = pal.get(slider_id)
            # Disable slider if not in paramter, enable
            # if it is.
            if not slider_id in parameter:
                x.disable()
            else:
                x.enable()
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


class paletteCanvas(object):

    def __init__(self, parent, pal, n = 5, figwidth = 0.2):  

        self._parent_ = parent
        self._pal_    = pal

        colors = pal.colors(n)
        self._draw_canvas_(colors, figwidth)

    def _activate_(self, event):

        # Loading settings of the current palette
        sliders  = self._parent_._sliders_
        settings = self._pal_.settings()
        for rec in sliders:
            sid = rec.getid()
            if sid in settings.keys(): rec.setvalue(settings[sid])

        # Change slider settings
        parent = self._parent_

    def _draw_canvas_(self, colors, figwidth):

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from matplotlib.figure import Figure
        from matplotlib.patches import Rectangle

        fig = Figure(figsize=(figwidth, 1), frameon = False)
        a   = fig.add_subplot(111)
        a.set_xlim([0,1]); a.set_ylim([0,1])

        n = len(colors)
        for i in range(0, n):
            r = Rectangle((0, i * 1. / n), 1, 1. / n, color = colors[i])
            a.add_patch(r)

        # Adjusting outer margins
        fig.subplots_adjust(left = .05, bottom = 0.01, right = .95,
                            top = .99, wspace = 0, hspace = 0)
        a.axis("off")

        canvas = FigureCanvasTkAgg(fig, master = self._parent_._palframe_)
        canvas.get_tk_widget().pack(side = LEFT)
        def callback(event): self._activate_(event)
        canvas.mpl_connect('button_press_event', callback) #self._activate_)
        canvas.draw()


class sliderObject(object):

    #FGDISABLED = "#b0b0b0"
    #BGDISABLED = "#b0b0b0"
    #FGACTIVE   = "#dadada"
    #BGACTIVE   = "#efefef"
    FGACTIVE = "#b0b0b0"
    BGACTIVE = "#b0b0b0"
    FGDISABLED   = "#dadada"
    BGDISABLED   = "#efefef"
    DISABLED  = "#b0b0b0"
    BGDEFAULT   = "#d9d9d9"

    def __init__(self, name, bgcolor = "#d9d9d9"):

        self.name    = name
        self.BGDEFAULT = bgcolor

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

    def disable(self):
        self.slider.configure(state = "disabled",
                relief = FLAT,
                bg = self.FGDISABLED,
                activebackground = self.FGDISABLED,
                troughcolor = self.BGDISABLED)
        self.label.configure(fg = self.DISABLED)
        self.value.configure(state = "disabled",
                relief = FLAT,
                fg = self.DISABLED,
                bg = self.BGDISABLED)
        self.button.configure(state = "disabled",
                relief = FLAT,
                fg = self.DISABLED,
                bg = self.BGDISABLED)

    def enable(self):
        self.slider.configure(state = "active",
                bg = self.FGACTIVE,
                activebackground = self.FGACTIVE,
                troughcolor = self.BGACTIVE)
        self.label.configure(fg = "black")
        self.value.configure(state = "normal",
                relief = FLAT,
                fg = "#000000", bg = "white")
        self.button.configure(state = "active",
                relief = RAISED, 
                fg = "#000000", bg = self.BGDEFAULT)


class gui(object):

    FRAMEHEIGHT = 100
    FRAMEWIDTH  = 280
    WIDTH = 300
    HEIGHT = 500

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
        for key,val in pal.settings().items():
            init_args[key] = val

        # Custom user arguments on top
        for key,val in kwargs.items(): init_args[key] = val

        # Initialize gui
        self._init_master_()
        self._add_sliders_()
        self._add_demo_options_()
        self._add_close_button_()
        self._add_return_button_()
        # Has to be called _after_ sliders have been added
        self._add_dropdown_type_(init_args = init_args)
        # Drawing default palettes
        self._add_palette_frame_()

        mainloop()


    def _init_master_(self):

        # initialize mater TK interface
        self.master = Tk()
        self.master.wm_title("Colorspace - Choose Color Palette")
        self.master.configure()
        self.master.resizable(width=False, height=False)
        self.master.geometry("{:d}x{:d}".format(self.WIDTH, self.HEIGHT))


    def _add_palette_frame_(self):

        if hasattr(self, "_palframe_"): self._palframe_.destroy()

        self._palframe_ = Frame(self.master, bg = "#ffffff", height = self.FRAMEHEIGHT,
                                width = self.FRAMEWIDTH)
        self._palframe_.place(x = 10, y = 80)

        # Loading palettes of currently selected palette type
        from numpy import min
        pals = self.palettes.get_palettes(self.dd_type.get())
        for pal in pals:
            paletteCanvas(self, pal, figwidth = min([0.3, 2.8 / len(pals)]))


    def _add_dropdown_type_(self, init_args = None):

        self.dd_type = ddObject(self, "type", init_args = init_args)

    def _add_sliders_(self):

        self._add_slider_("slider_H1", -360, 360, "H1")
        self._add_slider_("slider_H2", -360, 360, "H2")
        self._add_slider_("slider_L1",    0, 100, "L1")
        self._add_slider_("slider_L2",    0, 100, "L2")

        self._add_slider_("slider_C1",    0, 100, "C1")
        self._add_slider_("slider_C2",    0, 100, "C2")
        self._add_slider_("slider_P1",    0,   3, "P1")
        self._add_slider_("slider_P2",    0,   3, "P2")

    def _add_slider_(self, name, from_, to, label, resolution = 1, orient = HORIZONTAL):

        # Position of the current slider
        ypos = len(self._sliders_) * 30 + 100 + self.FRAMEHEIGHT

        # Object handling slider actions/callbacks
        obj = sliderObject(name, self.master.cget("bg"))

        # Slider element
        scale = Scale(self.master, var = name, from_ = from_, to = to,
                  command = obj.callback, showvalue = 0,
                  length = 150, width = 15,
                  resolution = resolution, orient = orient)
        scale.place(x = 50, y = ypos)

        # Label (static text)
        lab = Label(self.master, text = label)
        lab.config(anchor = CENTER)
        lab.place(x = 20, y = ypos) 

        # Button to change the value
        but = Button(self.master, text = "SET", command = obj.setvalue,
                pady = 0, padx = 0)
        but.place(x = 250, y = ypos)

        # Value (shows current slider value)
        val = Text(self.master, bd = 0, height = 1, width = 4)
        val.insert(INSERT, 0)
        val.tag_configure("right", justify="right")
        val.place(x = 210, y = ypos) 
        val.tag_add("right", "1.0", "end")

        obj.bind(scale, lab, val, but)

        # Append slider object
        self._sliders_.append(obj)


    def _add_demo_options_(self):

        but = Button(self.master, text = "Demo", command = self._show_demo_,
                pady = 5, padx = 5)
        but.place(x = 30, y = 460)

    def _add_close_button_(self):

        but = Button(self.master, text = "Cancel", command = sys.exit,
                pady = 5, padx = 5)
        but.place(x = 200, y = 460)

    def _add_return_button_(self):

        but = Button(self.master, text = "Ok", command = sys.exit,
                pady = 5, padx = 5)
        but.place(x = 150, y = 460)

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
