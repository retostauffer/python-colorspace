

from Tkinter import *


class sliderObject(object):

    def __init__(self, name):

        self.name = name

    def callback(self, event):

        print("Callback received for {:s}!".format(self.name))

        self.value.delete("1.0", END)
        self.value.insert(INSERT,event)
        self.value.tag_add("right", "1.0", "end")

    def setvalue(self):
        # Reading text value and adjust slider
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

    # List to store the sliders
    nsliders = 0

    def __init__(self):

        # Initialize gui
        self._init_master_()
        self._add_sliders_()

        mainloop()

    def _init_master_(self):

        # initialize mater TK interface
        self.master = Tk()
        self.master.configure()
        self.master.resizable(width=False, height=False)
        self.master.geometry("{:d}x{:d}".format(self.width, self.height))

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
        ypos = self.nsliders*40 + 100

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
        but.place(x = 190, y = ypos)

        # Value (shows current slider value)
        val = Text(self.master, bd = 0, height = 1, width = 3)
        val.insert(INSERT, 0)
        val.tag_configure("right", justify="right")
        val.place(x = 160, y = ypos) 
        val.tag_add("right", "1.0", "end")

        obj.bind(h, lab, val, but)

        self.nsliders += 1
        #self._sliders_[name] = {"slider":h, "label":lab, "value":val}


