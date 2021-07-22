

import colorspace
from colorspace.palettes import hclpalette
import numpy as np

types = ["diverging", "sequential", "qualitative", "heat", "rainbow", "terrain"]

# Test that palettes inherit from hclpalette
def test_return_issubclass():
    res = [isinstance(eval("colorspace.{:s}_hcl()".format(x)), hclpalette) for x in types]
    assert np.all(res)

