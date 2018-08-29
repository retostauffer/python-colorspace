
import os
import sys

import logging as log
log.basicConfig(format="[%(levelname)s] %(message)s", level=log.DEBUG)


class hclPalette(object):

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

    def show(self):

        print("Palette: {:s}".format(self.name()))
        print("         Type {:s}".format(self.type()))
        for key,val in self._settings_.iteritems():
            if   isinstance(val,bool):   val = "   True" if val else "   False"
            elif isinstance(val,int):    val = "   {:d}".format(val)
            elif isinstance(val,float):  val = "   {:5.1f}".format(val)
            print("         {:s} {:s}".format(key,val))


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

            pals.append(hclPalette(palette_type, name, settings))


        # Return dictionary with palettes
        if len(pals) == 0:
            return [None, None]
        else:
            return [palette_type, pals]


