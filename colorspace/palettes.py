
import os
import sys

import logging as log
log.basicConfig(format="[%(levelname)s] %(message)s", level=log.DEBUG)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
class default_palette(object):

    def __init__(self, type, name, settings):

        self._type_ = type
        self._name_ = name
        self._settings_ = settings

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


    def show(self):

        print("Palette: {:s}".format(self.name()))
        print("         Type {:s}".format(self.type()))
        for key,val in self._settings_.iteritems():
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
            for key,pals in self._palettes_.iteritems():
                all += pals
            return all

        # Else reutnr palette if available
        if not type_ in self._palettes_.keys():
            log.error("No palettes for type \"{:s}\".".format(type_)); sys.exit(9)

        # Else return list with palettes
        return self._palettes_[type_]


    def _load_palette_config_(self, file):

        from ConfigParser import ConfigParser
        import re

        CNF = ConfigParser()
        CNF.read(file)

        # Reading type (or name)
        try:
            palette_type = CNF.get("main", "type")
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

            pals.append(default_palette(palette_type, name, settings))


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
            settings = pal.settings()

            # Allow to overule few things
            for key,value in kwargs.items():
                if key in ["h1", "c1", "l1"]:
                    settings[key] = value
        else:
            settings = {}

            # Overwrite palette settings with user args
            settings["h1"]    = h[0]
            settings["h2"]    = h[1]
            settings["c1"]    = c
            settings["l1"]    = l
            settings["fixup"] = fixup
            settings["alpha"] = alpha
            settings["rev"]   = rev
            settings["n"]     = n


        self.settings = settings
        print "---- calling polarLUV now with ..."
        print settings

    def get(self, key):
        if not key in self.settings.keys():
            return None
        return self.settings[key]

    def colors(self, n = None, type_ = "hex"):

        if n is None: n = self.get("n")
        if n < 1:     return None

        from numpy import repeat, linspace, asarray
        from numpy import vstack, transpose
        from .colorspace import *

        L = repeat(self.get("l1"), n)
        C = repeat(self.get("c1"), n)
        H = linspace(self.get("h1"), self.get("h2"), n)
        if type_ == "HCL": return transpose(vstack([H,C,L]))

        # Defaults
        Xn = asarray([ 95.047])
        Yn = asarray([100.000])
        Zn = asarray([108.883])

        # Convet polarLUV -> LUV -> XYZ -> RGB -> hex
        L, U, V = polarLUV_to_LUV(L, C, H)
        if type_ == "LUV": return transpose(vstack([L,U,V]))
        X, Y, Z = LUV_to_XYZ(L, U, V, Xn, Yn, Zn)
        if type_ == "XYZ": return transpose(vstack([X,Y,Z]))
        R, G, B = XYZ_to_RGB(X, Y, Z, Xn, Yn, Zn)
        if type_ == "RGB": return transpose(vstack([R,G,B]))
        if type_ == "rgb": return transpose(vstack([R / 255.,G / 255. ,B / 255.]))
        hex = RGB_to_hex(R, G, B, self.get("fixup"))

        return hex





























