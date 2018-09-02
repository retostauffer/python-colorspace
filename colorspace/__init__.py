
import logging
log   = logging.getLogger("colorspace")
log.setLevel(logging.INFO)
handler  = logging.FileHandler('colorspace.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

log.info("Loading package")

from .colorlib import colorlib
from .palettes import hclpalettes
from .palettes import qualitative_hcl
from .palettes import diverge_hcl
from .palettes import sequential_hcl
from .palettes import rainbow_hcl
from .specplot import specplot
from .gui import gui


