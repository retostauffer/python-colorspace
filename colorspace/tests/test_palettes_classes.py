

import colorspace
import numpy as np

types = ["diverging", "sequential", "qualitative", "heat", "rainbow", "terrain"]

# Test that palettes inherit from hclpalette
def test_return_issubclass():
    res = [issubclass(type(eval("colorspace.{:s}_hcl()".format(x))), colorspace.palettes.hclpalette) for x in types]
    assert np.all(res)

