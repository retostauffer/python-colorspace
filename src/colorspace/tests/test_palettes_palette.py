
from colorspace import palette, diverging_hcl
from colorspace.colorlib import hexcols
from colorspace.colorlib import HCL
import numpy as np

import pytest
from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    # Input missing
    raises(TypeError,  palette)

    # Input object(s) wrong
    raises(ValueError, palette, colors = "foo")              # invalid hex
    raises(ValueError, palette, colors = ["#FF00FF", "foo"]) # invalid hex
    raises(TypeError,  palette, colors = {"foo": "bar"})     # invalid object

    # Input 'name' wrong.
    raises(TypeError,  palette, colors = "#FF00FF", name = 3)       # not string
    raises(TypeError,  palette, colors = "#FF00FF", name = ["foo"]) # not string

    # While numpy.ndarrays are allowed, the must be 1D. 2D will cause an error.
    raises(TypeError,  palette, colors = np.asarray([["#FF0000"], ["#00ff00", "#0ff"]], 
                                                    dtype = "object"))

# ------------------------------------------
# Testing different types of objects allowed
# as input 'colors'.
# ------------------------------------------
def test_input_types():

    # 'palettes' can take up
    # str: single hex color
    # list: list of hex colors
    # colorobject: any kind of colorobjects

    res1 = palette("#FF0033")
    assert isinstance(res1, palette)
    assert len(res1) == 1

    res2 = palette(["#FF0000", "#00ff00", "#0ff"])

    # Testing 1D and nD (2D) nd arrays
    res3 = palette(np.asarray(["#FF0000", "#00ff00", "#0ff"]))

    assert isinstance(res2, palette)
    assert isinstance(res3, palette)
    assert len(res3) == len(res2) == 3

    assert np.all(res2.colors() == res3.colors())


# ------------------------------------------
# Testing generic methods
# ------------------------------------------
def test_methods():

    # Unnamed palette
    x = palette(["#F00", "#00FF00", "#0000FF"])
    assert isinstance(x, palette)
    assert isinstance(x.name(), type(None))
    del x

    # Named palette
    x = palette(["#F00", "#00FF00", "#0000FF"], name = "demo palette")
    assert isinstance(x, palette)
    assert isinstance(x.name(), str)
    assert x.name() == "demo palette"

    # Rename palette
    x.rename("test palette")
    assert isinstance(x.name(), str)
    assert x.name() == "test palette"

    # Rename palette
    x.rename(None)
    assert isinstance(x.name(), type(None))

    # Checking length
    assert len(x) == 3

    # Getting colors
    cols = x.colors()
    assert isinstance(cols, list)
    assert len(cols) == 3

# ------------------------------------------
# Testing cmap functionality.
# ------------------------------------------
def test_cmap():

    from matplotlib.colors import LinearSegmentedColormap

    # Default
    x = palette(["#F00", "#00FF00", "#0000FF"])
    cmap = x.cmap()
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.N == len(x)
    assert isinstance(cmap.name, type(None))
    del x, cmap

    # Using custom N
    x = palette(["#F00", "#00FF00", "#0000FF"], name = "demo palette")
    cmap = x.cmap(n = 10)
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.N == 10
    assert isinstance(cmap.name, str)
    assert cmap.name == "demo palette"

    # Fails if we ask for less than n
    raises(ValueError, x.cmap, n = 2)
    del x, cmap


# ------------------------------------------
# Checking __repr__
# ------------------------------------------
def test_standard_representation():

    from re import match
    N    = 5
    name = "test"
    txt  = repr(palette(diverging_hcl().colors(N), name))
    assert match(f"^Palette Name: {name}\n\s+Type: Custom palette\n\s+Number of colors: {N}$", txt)

    N    = 20
    name = "my_palette"
    txt  = repr(palette(diverging_hcl().colors(N), name))
    assert match(f"^Palette Name: {name}\n\s+Type: Custom palette\n\s+Number of colors: {N}$", txt)

# ------------------------------------------
# Swatchplot feature
# ------------------------------------------
@pytest.mark.mpl_image_compare
def test_swatchplot():

    import matplotlib.pyplot as plt

    pal = palette(diverging_hcl(5), "test")
    assert isinstance(pal.name(), str)
    assert pal.name() == "test"

    # Plotting
    pal.swatchplot()
    plt.close()

    # Different figure size
    pal.swatchplot(figsize = (6, 2))
    plt.close()

    # Setting show_names; is deleted internally
    pal.swatchplot(figsize = (6, 2), show_names = "foo")
    plt.close()

