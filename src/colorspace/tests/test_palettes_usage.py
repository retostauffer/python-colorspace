

import pytest
from pytest import raises
import colorspace
from colorspace import palette, hclpalettes
from colorspace.palettes import defaultpalette
import matplotlib
import numpy as np
import matplotlib.pyplot as plt



# ------------------------------------------
# Testing usage of 'palette()'
# ------------------------------------------
def test_palette_valid_list():
    x = palette(["#00ff00", "#ff00ff"], name = "test")
    pass

def test_palette_name_no_inputs():
    with pytest.raises(TypeError):
        palette()

def test_palette_invalid_hex_values():
    with pytest.raises(ValueError):
        palette(["a", "#00ff00"], name = "test")

def test_palette_invalid_type_name():
    with pytest.raises(TypeError):
        palette(["#ff0000", "#00ff00"], name = 123)

def test_palette_invalid_type_color():
    with pytest.raises(ValueError):
        palette([123, "#00ff00"], name = "test")

def test_palette_repr():
    assert isinstance(repr(palette(["#00ff00"], name = "test")), str)

def test_palette_name_and_rename():
    x =  palette(["#00ff00"], name = "test")
    assert isinstance(x.name(), str)
    assert x.name() == "test"
    x.rename("foo")
    assert isinstance(x.name(), str)
    assert x.name() == "foo"

def test_palette_invalid_rename():
    with pytest.raises(ValueError):
        x =  palette(["#00ff00"], name = "test")
        x.rename(123)

# ------------------------------------------
# Testing palette.cmap() method
# ------------------------------------------
def test_palette_cmap_class():
    x = palette(["#00ff00"], name = "test")
    assert isinstance(x.cmap(), matplotlib.colors.LinearSegmentedColormap)

def test_palette_cmap_class_rev_False():
    x = palette(["#00ff00"], name = "test")
    assert isinstance(x.cmap(rev = False), matplotlib.colors.LinearSegmentedColormap)

def test_palette_cmap_param_n():
    x = palette(["#00ff00"], name = "test")
    cm = x.cmap(n = 10)
    assert isinstance(cm, matplotlib.colors.LinearSegmentedColormap)
    assert cm.N == 10

# ------------------------------------------
# ------------------------------------------
def test_hclpalettes_get_palettes_wrong_usage():

    # Incorrect first argument (type_)
    pals = hclpalettes()
    raises(TypeError, pals.get_palette, type_ = 3)
    raises(TypeError, pals.get_palette, type_ = ["Qualitative"])

    # Incorrect type for 'exact' (must be bool)
    raises(TypeError, pals.get_palette, type_ = "Qualitative", exact = 3)
    raises(TypeError, pals.get_palette, type_ = "Qualitative", exact = None)
    raises(TypeError, pals.get_palette, type_ = "Qualitative", exact = [False])

def test_hclpalettes_class():
    x = hclpalettes()
    assert isinstance(x, hclpalettes)
    assert x.length() > 0

def test_hclpalettes_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        hclpalettes(files = "foo")

def test_hclpalettes_file_no_file():
    with pytest.raises(ValueError):
        hclpalettes(files = [])

def test_hclpalettes_repr():
    assert isinstance(repr(hclpalettes()), str)

def test_hclpalettes_get_palette_types():
    pals  = hclpalettes()
    # Getting loaded palette types; list of character strings
    types = pals.get_palette_types()
    assert isinstance(types, list)
    assert len(types) > 0
    assert np.all([isinstance(x, str) for x in types])
    # Loading palettes of one specific type
    type_pals = pals.get_palettes(types[0])
    assert isinstance(type_pals, list)
    assert len(type_pals) > 0
    assert np.all([isinstance(x, defaultpalette) for x in type_pals])

def test_hclpalettes_get_palettes_invalid_type_name():
    with pytest.raises(ValueError):
        hclpalettes().get_palettes("foo")

def test_hclpalettes_get_palettes_invalid_type_type():
    with pytest.raises(TypeError):
        hclpalettes().get_palettes(123)

def test_hclpalettes_get_palettes_type_none():
    # Testig default (type_ = None)
    x = hclpalettes().get_palettes(type_ = None)
    assert isinstance(x, list)
    assert len(x) > 0
    # Explicitly testing for type_ = None
    x = hclpalettes().get_palettes(type_ = None)
    x = hclpalettes().get_palettes(type_ = None)
    assert isinstance(x, list)
    assert len(x) > 0


# ------------------------------------------
# Testing hclpalettes.get_palettes(),
# hclpalettes.get_palette(), and some features
# of the object returned.
# ------------------------------------------
def test_hclpalettes_get_palette():
    pals  = hclpalettes()
    # Getting first type of palettes
    first = pals.get_palettes(pals.get_palette_types()[0])
    assert isinstance(first, list)
    # Getting first palette of first type of palettes
    pal_name = first[0].name()
    assert isinstance(pal_name, str)
    # Getting this specific palette
    pal      = pals.get_palette(pal_name)
    assert isinstance(pal, defaultpalette)
    assert isinstance(pal.name(), str)


def test_hclpalettes_get_palettes():
    from re import compile

    hclpals = hclpalettes()
    assert isinstance(hclpals, hclpalettes)

    # Getting all available palettes
    pals = hclpals.get_palettes()
    assert len(pals) == 115
    del pals

    # Get all Diverging (no exact match)
    pat  = compile(r".*?Diverging.*?")
    pals = hclpals.get_palettes("Diverging")
    assert len(pals) == 36
    for p in pals: assert pat.match(p.type())
    del pals

    # Get all 'Advanced: Diverging' (no exact match).
    # This will also include 'Advanced: DivergingX'.
    pat  = compile(r"^Advanced: Diverging.*?")
    pals = hclpals.get_palettes("Advanced: Diverging")
    assert len(pals) == 29
    for p in pals: assert pat.match(p.type())
    del pals

    # Get all 'Advanced: Diverging' (exact match).
    # No longer includes 'Advanced: DivergingX'.
    pat  = compile(r"^Advanced: Diverging$")
    pals = hclpals.get_palettes("Advanced: Diverging", exact = True)
    assert len(pals) == 11
    for p in pals: assert pat.match(p.type())

    # Testing order of arguments
    assert pals == hclpals.get_palettes("Advanced: Diverging", True)


def test_hclpalettes_get_palette_invalid_name():
    pals  = hclpalettes()
    with pytest.raises(ValueError):
        pals.get_palette("this_is_a_test_foo_bar")


def test_hclpalettes_get_palette_methods():

    pal = hclpalettes().get_palette("Teal")
    pal_settings = pal.get_settings()
    assert isinstance(pal_settings, dict)

    expected = ["desc", "h1", "h2", "c1", "c2", "l1",
                "l2", "p1", "p2", "cmax", "fixup", "gui"]
    assert all([x in expected for x in pal_settings.keys()])


@pytest.mark.mpl_image_compare
def test_hclpalettes_plot_method():
    pals = hclpalettes()
    pals.plot()
    plt.close()

    # Wrong argument 'n' (must be positive int)
    raises(TypeError, pals.plot, n = None)
    raises(TypeError, pals.plot, n = 10.0)
    raises(ValueError, pals.plot, n = 0)
    raises(ValueError, pals.plot, n = -1)

# --------------------------------------------
# Plotting ..
# --------------------------------------------
# Testing another color palette where heu-axis should be adjusted to 0-360 only
@pytest.mark.mpl_image_compare
def test_colorlib_specplot_method():
    cols = colorspace.diverging_hcl()
    cols.specplot()
    plt.close()
    cols.specplot(n = 15)
    plt.close()

@pytest.mark.mpl_image_compare
def test_colorlib_swatchplot_method():
    cols = colorspace.diverging_hcl()
    cols.swatchplot()
    plt.close()
    cols.swatchplot(n = 15)
    plt.close()

@pytest.mark.mpl_image_compare
def test_colorlib_hclplot_method():
    cols = colorspace.diverging_hcl()
    cols.hclplot()
    plt.close()
    cols.hclplot(n = 15)
    plt.close()

