

from .cslogger import cslogger

# The color library which contains all the
# color objects and required transformation
# methods.
from .colorlib import colorlib

# Color vision deficiency functions.
from .CVD import tritan
from .CVD import protan
from .CVD import deutan
from .CVD import desaturate

# Default HCL color palettes methods and
# functions.
from .palettes import hclpalettes
from .palettes import qualitative_hcl
from .palettes import diverge_hcl
from .palettes import sequential_hcl
from .palettes import rainbow_hcl

# Helper functions and methods
from .hcl_palettes import hcl_palettes
from .specplot import specplot
from .choose_palette import choose_palette


