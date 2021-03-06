

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
from .palettes import palette
from .palettes import qualitative_hcl
from .palettes import diverging_hcl
from .palettes import sequential_hcl
from .palettes import rainbow_hcl
from .palettes import heat_hcl
from .palettes import terrain_hcl
from .palettes import diverging_hsv

# Helper functions and methods
from .hcl_palettes import hcl_palettes
from .swatchplot import swatchplot
from .specplot import specplot
from .choose_palette import choose_palette
from .cvd_emulator import cvd_emulator


