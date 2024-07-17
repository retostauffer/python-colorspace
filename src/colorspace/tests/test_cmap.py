

import pytest
from pytest import raises
from colorspace import diverging_hcl
from colorspace.colorlib import sRGB, hexcols
from colorspace.cmap import cmap_to_sRGB

# ---------------------------------
# Wrong use
# ---------------------------------
def test_cmap_to_sRGB_wrong_usage():

    raises(TypeError, cmap_to_sRGB, 1)
    raises(TypeError, cmap_to_sRGB, ["#ff0033"])
    raises(TypeError, cmap_to_sRGB, hexcols(["red", "blue"]))

    # Testing argument 'n'
    cmap = diverging_hcl().cmap()
    raises(TypeError, cmap_to_sRGB, x = cmap, n = 1.4) # Not int
    raises(TypeError, cmap_to_sRGB, x = cmap, n = "foo") # Not int
    raises(ValueError, cmap_to_sRGB, x = cmap, n = 1) # not >= 2

# ---------------------------------
# Testing different plots
# ---------------------------------
def test_cmap_to_sRGB_return():

    cmap = diverging_hcl().cmap()
    cols = cmap_to_sRGB(cmap)
    assert isinstance(cols, sRGB)
    assert isinstance(len(cols), int) and len(cols) == 256
    del cmap, cols

    cmap = diverging_hcl().cmap(n = 5)
    cols = cmap_to_sRGB(cmap)
    assert isinstance(cols, sRGB)
    assert isinstance(len(cols), int) and len(cols) == 5
    del cmap, cols

    cmap = diverging_hcl().cmap(6)
    cols = cmap_to_sRGB(cmap)
    assert isinstance(cols, sRGB)
    assert isinstance(len(cols), int) and len(cols) == 6
    del cmap, cols

    cmap = diverging_hcl().cmap()
    cols = cmap_to_sRGB(cmap, n = 7)
    assert isinstance(cols, sRGB)
    assert isinstance(len(cols), int) and len(cols) == 7
    del cmap, cols
