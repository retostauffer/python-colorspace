
import os
import sys

import logging as log
log.basicConfig(format="[%(levelname)s] %(message)s", level=log.DEBUG)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class default_palette(object):

    def __init__(self, type, method, parameter, name, settings):

        self._type_      = type
        self._name_      = name
        self._method_    = method
        self._parameter_ = parameter
        self._settings_  = settings

    def type(self):
        return self._type_

    def get(self, what):

        if what in self._settings_.keys():
            return self._settings_[what]
        else:
            return None

    def name(self):
        return self._name_

    def rename(self, name):
        self.name = name

    def set(self, key, val):
        self._settings_[key] = val

    def settings(self):
        return self._settings_

    def parameters(self):
        return self._parameter_

    def colors(self, n = 10):

        # Dynamically load color function
        mod  = __import__("colorspace")
        cfun = getattr(mod, self._method_)

        # Calling color method with arguments of this object. 
        args = {}
        for key in self._parameter_: args[key] = self.get(key)
        return cfun(n, settings = args).colors(n)

    def show(self):

        print("Palette: {:s}".format(self.name()))
        print("         Type {:s}".format(self.type()))
        for key,val in self._settings_.items():
            if   isinstance(val,bool):   val = "   True" if val else "   False"
            elif isinstance(val,int):    val = "   {:d}".format(val)
            elif isinstance(val,float):  val = "   {:5.1f}".format(val)
            print("         {:s} {:s}".format(key,val))


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class palettes(object):

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
        for file in files:
            [palette_type, pals] = self._load_palette_config_(file)
            if not pals: continue

            # Append
            self._palettes_[palette_type] = pals
            #DEMO# for p in pals: p.show()

    def get_palette_types(self):

        return self._palettes_.keys()

    def get_palettes(self, type_ = None):

        if not type_:
            all = []
            for key,pals in self._palettes_.items():
                all += pals
            return all

        # Else reutnr palette if available
        if not type_ in self._palettes_.keys():
            log.error("No palettes for type \"{:s}\".".format(type_)); sys.exit(9)

        # Else return list with palettes
        return self._palettes_[type_]

    def get_palette(self, name):

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

            pals.append(default_palette(palette_type, palette_method,
                        palette_parameter, name, settings))


        # Return dictionary with palettes
        if len(pals) == 0:
            return [None, None]
        else:
            return [palette_type, pals]






# -------------------------------------------------------------------
# -------------------------------------------------------------------
class hclpalette(object):

    n     = None
    h1    = None
    h2    = None
    l1    = None
    l2    = None
    p1    = None
    p2    = None
    fixup = True

    def hello():
        print("Hello!")

    def get(self, key):
        if not key in self.settings.keys():
            return None
        return self.settings[key]


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class qualitative_hcl(hclpalette):

    def __init__(self, n, h = None, c = 50, l = 70,
        fixup = True, alpha = 1, palette = None, rev = False, **kwargs):

        # Input checks
        for key in ["n", "c", "l"]:
            if not isinstance(eval(key), int):
                log.error("Input \"{:s}\" has to be of type integer.".format(key)); sys.exit(9)
        for key in ["fixup", "rev"]:
            if not isinstance(eval(key), bool):
                log.error("Input \"{:s}\" has to be of type bool.".format(key)); sys.exit(9)
        if n < 1:
            log.error("Input \"n\" has a positive integer."); sys.exit(9)

        # For handy use of the function
        if isinstance(h,str):
            palette = h; h = None

        # Correcting "h" if set
        if not h is None and not isinstance(h, str):
            if not isinstance(h, list): h = [h]
            if len(h) == 1:  h = [h[0]] * 2
            if len(h) > 2:   h = h[0:2]
        elif h is None:
            h = [0, 360 / (n + 1) * n]

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            default_palettes = palettes().get_palettes("Qualitative")
            default_names    = [x.name() for x in default_palettes]
            if not palette in default_names:
                log.error("Palette \"{:s}\" is not a valid qualitative palette.".format(palette))
                log.error("Choose one of: {:s}".format(", ".join(default_names)))
                sys.exit(9)

            # Else pick the palette
            pal = default_palettes[default_names.index(palette)]

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
            settings = pal.settings()
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
            settings["n"]     = n

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
        if type_ == "HCL": return transpose(vstack([H,C,L]))

        # Convet polarLUV -> LUV -> XYZ -> RGB -> hex
        colorlib = colorlib()

        L, U, V = colorlib.polarLUV_to_LUV(L, C, H)
        if type_ == "LUV": return transpose(vstack([L,U,V]))

        X, Y, Z = colorlib.LUV_to_XYZ(L, U, V)
        if type_ == "XYZ": return transpose(vstack([X,Y,Z]))

        R, G, B = colorlib.XYZ_to_RGB(X, Y, Z)
        if type_ == "RGB": return transpose(vstack([R,G,B]))
        if type_ == "rgb": return transpose(vstack([R / 255.,G / 255. ,B / 255.]))

        hex = colorlib.RGB_to_hex(R, G, B, self.get("fixup"))
        if self.get("rev"): hex.reverse()

        return hex 


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class diverge_hcl(hclpalette):

    def __init__(self, n, h = [260, 0], c = 80, l = [30, 90],
        power = 1.5, fixup = True, alpha = 1, palette = None, rev = False, **kwargs):

        # Input checks
        for key in ["n", "c"]:
            if not isinstance(eval(key), int):
                log.error("Input \"{:s}\" has to be of type integer.".format(key)); sys.exit(9)
        for key in ["l"]:
            if not isinstance(eval(key), list):
                log.error("Input \"{:s}\" has to be a list with two values.".format(key)); sys.exit(9)
        for key in ["fixup", "rev"]:
            if not isinstance(eval(key), bool):
                log.error("Input \"{:s}\" has to be of type bool.".format(key)); sys.exit(9)
        if n < 1:
            log.error("Input \"n\" has a positive integer."); sys.exit(9)

        # For handy use of the function
        if isinstance(h,str):
            palette = h; h = None

        # Correcting "h" if set
        if not h is None and not isinstance(h, str):
            if not len(h) == 2:
                log.error("Input \"h\" has to be of length 2 for diverging color maps.")
                sys.exit(9)
        if not len(l) == 2:
            log.error("Input \"l\" has to be of length 2 for diverging color maps.")
            sys.exit(9)

        # If user selected a named palette: load palette settings
        if isinstance(palette, str):
            default_palettes = palettes().get_palettes("Diverging")
            default_names    = [x.name() for x in default_palettes]
            if not palette in default_names:
                log.error("Palette \"{:s}\" is not a valid qualitative palette.".format(palette))
                log.error("Choose one of: {:s}".format(", ".join(default_names)))
                sys.exit(9)

            # Else pick the palette
            pal = default_palettes[default_names.index(palette)]

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
            settings = pal.settings()
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
            settings["n"]     = n

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
        if type_ == "HCL": return transpose(vstack([H,C,L]))

        # Convet polarLUV -> LUV -> XYZ -> RGB -> hex
        colorlib = colorlib()

        L, U, V = colorlib.polarLUV_to_LUV(L, C, H)
        if type_ == "LUV": return transpose(vstack([L,U,V]))

        X, Y, Z = colorlib.LUV_to_XYZ(L, U, V)
        if type_ == "XYZ": return transpose(vstack([X,Y,Z]))

        R, G, B = colorlib.XYZ_to_RGB(X, Y, Z)
        if type_ == "RGB": return transpose(vstack([R,G,B]))
        if type_ == "rgb": return transpose(vstack([R / 255.,G / 255. ,B / 255.]))

        hex = colorlib.RGB_to_hex(R, G, B, self.get("fixup"))

        return hex




























