
from colorspace import hcl_palettes
from colorspace.palettes import hclpalettes
import numpy as np

from pytest import raises

types = ["diverging", "sequential", "qualitative", "heat", "rainbow", "terrain"]

# Test that the return values for ...()(3) and ...().colors(3) is always
# of type list and of length 3 (hex colors).

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():
    # 'n'/'ncol' must be positive integers
    raises(TypeError, hcl_palettes, n = "3")
    raises(TypeError, hcl_palettes, n = 1.5)
    raises(ValueError, hcl_palettes, n = 0)
    raises(TypeError, hcl_palettes, ncol = "3")
    raises(TypeError, hcl_palettes, ncol = 1.5)
    raises(ValueError, hcl_palettes, ncol = 0)

    # plot must be bool
    raises(TypeError, hcl_palettes, plot = "True")

    # custom must be one of the allowed types; e.g.,
    # an object of class defaultpalette or list.
    raises(TypeError, hcl_palettes, custom = "Foo")
    raises(TypeError, hcl_palettes, custom = 3)

    # type_ must be None or string
    raises(TypeError, hcl_palettes, type_ = 123)
    raises(TypeError, hcl_palettes, type_ = ["foo"])

    # type_ given but no palettes available matching
    # this type (partial matching).
    raises(Exception, hcl_palettes, type_ = "Just a test")



# ------------------------------------------
# Default return
# ------------------------------------------
def test_default_return():
    pals = hcl_palettes()
    assert isinstance(pals, hclpalettes)
    assert pals.length() == 100

def test_get_palettes():
    pals = hcl_palettes()
    assert isinstance(pals.get_palettes(), list)
    assert len(pals.get_palettes()) == 100

def test_get_palette_types():
    types = hcl_palettes().get_palette_types()
    assert isinstance(types, list)
    assert np.all([isinstance(x, str) for x in types])
    assert len(types) == 7


# ------------------------------------------
# Filter by tyoe_ and name
# ------------------------------------------
def test_filter_by_one_type():
    res = hcl_palettes(type_ = "Basic: Qualitative")
    assert isinstance(res, hclpalettes)
    assert res.length() == 9
    assert len(res.get_palette_types()) == 1
    assert res.get_palette_types()[0] == "Basic: Qualitative"

def test_filter_by_name():
    res = hcl_palettes(name = "Purples")
    assert isinstance(res, hclpalettes)
    assert res.length() == 1
    assert res.get_palettes()[0].name() == "Purples"








