
from colorspace import hcl_palettes, divergingx_palettes, rainbow
from colorspace.palettes import hclpalettes, defaultpalette
import numpy as np

import pytest
from pytest import raises

try:
    import matplotlib.pyplot as plt
    _got_mpl = True
except:
    _got_mpl = False

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
    assert pals.length() == 97

def test_get_palettes():
    pals = hcl_palettes()
    assert isinstance(pals.get_palettes(), list)
    assert len(pals.get_palettes()) == 97

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
    assert all([isinstance(x, defaultpalette) for x in res.get_palettes()])

def test_filter_by_name():
    res = hcl_palettes(name = "Purples")
    assert isinstance(res, hclpalettes)
    assert res.length() == 1
    assert res.get_palettes()[0].name() == "Purples"
    assert all([isinstance(x, defaultpalette) for x in res.get_palettes()])

# ------------------------------------------
# Custom feature
# ------------------------------------------
@pytest.mark.mpl_image_compare
def test_hcl_palettes_custom():
    # Extract specific palettes after loading
    palettes = hcl_palettes()
    c1 = palettes.get_palette("Oranges")
    c2 = palettes.get_palette("Greens")
    
    #: Modify palettes by overwriting palette settings
    c1.set(h1 = 99, l2 = 30, l1 = 30)
    c1.rename("Custom Palette #1")
    c2.set(h1 = -30, l1 = 40, l2 = 30, c1 = 30, c2 = 40)
    c2.rename("Custom Palette #2")

    # Misuse (wrong input object type)
    raises(TypeError, hcl_palettes, type_ = "Custom", custom = rainbow())
    raises(TypeError, hcl_palettes, type_ = "Custom", custom = rainbow()(10))

    # Custom palettes obj
    res = hcl_palettes(type_ = "Custom", custom = c1)
    assert isinstance(res.get_palette_types(), list)
    assert len(res.get_palette_types()) == 1
    assert res.get_palette_types()[0] == "Custom"
    assert isinstance(res, hclpalettes)
    assert isinstance(res.get_palettes(), list)
    assert len(res.get_palettes()) == 1
    del res
    
    # Custom palettes obj with two pals
    res = hcl_palettes(type_ = "Custom", custom = [c1, c2])
    assert isinstance(res.get_palette_types(), list)
    assert len(res.get_palette_types()) == 1
    assert res.get_palette_types()[0] == "Custom"
    assert isinstance(res, hclpalettes)
    assert isinstance(res.get_palettes(), list)
    assert len(res.get_palettes()) == 2
    del res
    

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_hcl_palettes_custom_plot():
    # Extract specific palettes after loading
    palettes = hcl_palettes()
    c1 = palettes.get_palette("Oranges")
    c2 = palettes.get_palette("Greens")

    # Visualize customized palettes
    res = hcl_palettes(type_ = "Custom", custom = [c1, c2],
                       plot = True, ncol = 1, figsize = (6, 1));
    assert isinstance(res, type(None))
    plt.close()

# ------------------------------------------
# Special wrapper function for divergingX palettes
# ------------------------------------------
def test_divergingx_palettes():
    res = divergingx_palettes()
    assert isinstance(res, hclpalettes)
    assert len(res.get_palette_types()) == 1
    assert res.get_palette_types()[0] == "Advanced: DivergingX"

    pals = res.get_palettes()
    assert isinstance(pals, list)
    assert len(pals) == 18
    assert all([isinstance(x, defaultpalette) for x in pals])





