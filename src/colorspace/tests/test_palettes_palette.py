
import numpy as np
import pytest
from pytest import raises

from colorspace import palette, diverging_hcl
from colorspace.colorlib import hexcols
from colorspace.colorlib import HCL

try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.colors import LinearSegmentedColormap
    _got_mpl = True
except:
    _got_mpl = False

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

    # Misuse of 'n'
    cols = diverging_hcl().colors(3)
    raises(TypeError, palette, cols, n = None) # Not integer
    raises(TypeError, palette, cols, n = 10.4) # Not integer
    raises(ValueError, palette, cols, n = 1) # <= 1


# ------------------------------------------
# Testing different types of objects allowed
# as input 'colors'.
# ------------------------------------------
def test_palette_input_types():

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

def test_palette_missing_colors():
    # Testing missing color inputs
    x = ["#ff0000", "#00ff00", "#0000ff", None, None]
    pal = palette(x)
    assert len(pal) == 5

    cols = pal.colors()
    assert cols[3] is None and cols[4] is None
    assert np.all(cols[:3] == [x.upper() for x in x[:3]])

    ref  = ["#00FF00", None, "#00FF00"]
    cols = palette(["#00ff00", None, "#0f0"]).colors()
    assert np.all(cols == ref)

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_palette_missing_colors():

    # For god sake, 'green' turns into #008000
    x = ["red", "lime", "#00f", "green", None, None]
    pal = palette(x)
    assert len(pal) == 6

    cols = pal.colors()
    assert cols[4] is None and cols[5] is None
    assert np.all(cols[:4] == ["#FF0000", "#00FF00", "#0000FF", "#008000"])


@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_palette_input_type_cmap():

    # Default number of colors
    x = diverging_hcl().cmap()
    assert isinstance(x, LinearSegmentedColormap)
    assert x.N == 256

    pal = palette(x)
    assert isinstance(pal, palette)
    assert len(pal.colors()) == 7
    pal = palette(x, n = 101)
    assert isinstance(pal, palette)
    assert len(pal.colors()) == 101

    del x, pal

    # Picking 100 colors
    x = diverging_hcl().cmap()
    assert isinstance(x, LinearSegmentedColormap)
    assert x.N == 256

    pal = palette(x)
    assert isinstance(pal, palette)
    assert len(pal.colors()) == 7
    pal = palette(x, n = 101)
    assert isinstance(pal, palette)
    assert len(pal.colors()) == 101

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
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_cmap():

    # Default
    x = palette(["#F00", "#00FF00", "#0000FF"])

    # Wrong input type
    raises(TypeError, x.cmap, continuous = 1)
    raises(TypeError, x.cmap, continuous = [True, False])

    # Non-continuous color map
    cmap = x.cmap(continuous = False)
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.N == len(x)
    assert isinstance(cmap.name, type(None))
    del x, cmap

    # Named palette
    x = palette(["#F00", "#00FF00", "#0000FF"], name = "demo palette")
    cmap = x.cmap(continuous = False)
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.N == 3
    assert isinstance(cmap.name, str)
    assert cmap.name == "demo palette"

    # Continous palette
    x = palette(["#F00", "#00FF00", "#0000FF"], name = "demo palette")
    cmap = x.cmap(continuous = True)
    assert isinstance(cmap, LinearSegmentedColormap)
    assert cmap.N == 256
    assert isinstance(cmap.name, str)
    assert cmap.name == "demo palette"


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
# Swatchplot method
# ------------------------------------------
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_swatchplot():

    pal = palette(diverging_hcl(5), "test")
    assert isinstance(pal.name(), str)
    assert pal.name() == "test"

    # Plotting
    fig = pal.swatchplot()
    assert isinstance(fig, Figure)
    plt.close()

    # Different figure size
    fig = pal.swatchplot(figsize = (6, 2))
    assert isinstance(fig, Figure)
    plt.close()

    # Setting show_names; is deleted internally
    fig = pal.swatchplot(figsize = (6, 2), show_names = "foo")
    assert isinstance(fig, Figure)
    plt.close()

# ------------------------------------------
# Specplot method
# ------------------------------------------
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot():

    pal = palette(diverging_hcl(5), "test")

    # Plotting
    fig = pal.specplot()
    assert isinstance(fig, Figure)
    plt.close()


# ------------------------------------------
# swatchplot method
# ------------------------------------------
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot():

    pal = palette(diverging_hcl(5), "test")

    # Plotting
    fig = pal.swatchplot()
    assert isinstance(fig, Figure)
    plt.close()


# ------------------------------------------
# hclplot method
# ------------------------------------------
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot():

    pal = palette(diverging_hcl(5), "test")

    # Plotting
    fig = pal.hclplot()
    assert isinstance(fig, Figure)
    plt.close()


