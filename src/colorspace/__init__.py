

# The color library which contains all the
# color objects and required transformation
# methods.
from .colorlib import colorlib
from .colorlib import polarLUV
from .colorlib import HCL
from .colorlib import CIELUV
from .colorlib import CIEXYZ
from .colorlib import RGB
from .colorlib import sRGB
from .colorlib import CIELAB
from .colorlib import polarLAB
from .colorlib import HSV
from .colorlib import HLS
from .colorlib import hexcols
from .colorlib import compare_colors

# Color vision deficiency functions.
from .CVD import tritan
from .CVD import protan
from .CVD import deutan
from .CVD import desaturate

# Default HCL color palettes methods and
# functions.
from .palettes import palette
from .palettes import hclpalettes
from .palettes import qualitative_hcl
from .palettes import diverging_hcl
from .palettes import divergingx_hcl
from .palettes import sequential_hcl
from .palettes import rainbow_hcl
from .palettes import heat_hcl
from .palettes import terrain_hcl
from .palettes import diverging_hsv
from .palettes import rainbow

# Color manipulation utils
from .utils import mixcolor
from .utils import lighten
from .utils import darken
from .utils import max_chroma
from .utils import contrast_ratio
from .utils import check_hex_colors
from .utils import extract_transparency
from .utils import adjust_transparency
from .utils import mixcolor

# Helper functions and methods
from .hcl_palettes import hcl_palettes
from .hcl_palettes import divergingx_palettes
from .swatchplot import swatchplot
from .specplot import specplot
from .hclplot import hclplot
from .choose_palette import choose_palette
from .cvd_image import cvd_image
from .demos import demoplot
from .datasets import dataset

# Adding version
from colorspace import version
__version__ = version.short_version
del version
