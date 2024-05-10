

import pytest
import colorspace
import matplotlib
import numpy as np



# ------------------------------------------
# Testing usage of 'palette()'
# ------------------------------------------
def test_palette_valid_list():
    x = colorspace.palettes.palette(["#00ff00", "#ff00ff"], name = "test")
    pass

def test_palette_name_no_inputs():
    with pytest.raises(TypeError):
        colorspace.palettes.palette()

def test_palette_invalid_hex_values():
    with pytest.raises(ValueError):
        colorspace.palettes.palette(["a", "#00ff00"], name = "test")

def test_palette_invalid_type_name():
    with pytest.raises(TypeError):
        colorspace.palettes.palette(["#ff0000", "#00ff00"], name = 123)

def test_palette_invalid_type_color():
    with pytest.raises(ValueError):
        colorspace.palettes.palette([123, "#00ff00"], name = "test")

def test_palette_repr():
    assert isinstance(repr(colorspace.palettes.palette(["#00ff00"], name = "test")), str)

def test_palette_name_and_rename():
    x =  colorspace.palettes.palette(["#00ff00"], name = "test")
    assert isinstance(x.name(), str)
    assert x.name() == "test"
    x.rename("foo")
    assert isinstance(x.name(), str)
    assert x.name() == "foo"

def test_palette_invalid_rename():
    with pytest.raises(ValueError):
        x =  colorspace.palettes.palette(["#00ff00"], name = "test")
        x.rename(123)

# ------------------------------------------
# Testing colorspace.palettes.palette.cmap() method
# ------------------------------------------
def test_palette_cmap_class():
    x = colorspace.palettes.palette(["#00ff00"], name = "test")
    assert isinstance(x.cmap(), matplotlib.colors.LinearSegmentedColormap)

def test_palette_cmap_class_rev_False():
    x = colorspace.palettes.palette(["#00ff00"], name = "test")
    assert isinstance(x.cmap(rev = False), matplotlib.colors.LinearSegmentedColormap)

def test_palette_cmap_param_n():
    x = colorspace.palettes.palette(["#00ff00"], name = "test")
    cm = x.cmap(n = 10)
    assert isinstance(cm, matplotlib.colors.LinearSegmentedColormap)
    assert cm.N == 10

# ------------------------------------------
# ------------------------------------------
def test_hclpalettes_class():
    x = colorspace.palettes.hclpalettes()
    assert isinstance(x, colorspace.palettes.hclpalettes)
    assert x.length() > 0

def test_hclpalettes_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        colorspace.palettes.hclpalettes(files = "foo")

def test_hclpalettes_file_no_file():
    with pytest.raises(ValueError):
        colorspace.palettes.hclpalettes(files = [])

def test_hclpalettes_repr():
    assert isinstance(repr(colorspace.palettes.hclpalettes()), str)

def test_hclpalettes_get_palette_types():
    pals  = colorspace.palettes.hclpalettes()
    # Getting loaded palette types; list of character strings
    types = pals.get_palette_types()
    assert isinstance(types, list)
    assert len(types) > 0
    assert np.all([isinstance(x, str) for x in types])
    # Loading palettes of one specific type
    type_pals = pals.get_palettes(types[0])
    assert isinstance(type_pals, list)
    assert len(type_pals) > 0
    assert np.all([isinstance(x, colorspace.palettes.defaultpalette) for x in type_pals])

def test_hclpalettes_get_palettes_invalid_type_name():
    with pytest.raises(ValueError):
        colorspace.palettes.hclpalettes().get_palettes("foo")

def test_hclpalettes_get_palettes_invalid_type_type():
    with pytest.raises(ValueError):
        colorspace.palettes.hclpalettes().get_palettes(123)

def test_hclpalettes_get_palettes_type_none():
    # Testig default (type_ = None)
    x = colorspace.palettes.hclpalettes().get_palettes(type_ = None)
    assert isinstance(x, list)
    assert len(x) > 0
    # Explicitly testing for type_ = None
    x = colorspace.palettes.hclpalettes().get_palettes(type_ = None)
    x = colorspace.palettes.hclpalettes().get_palettes(type_ = None)
    assert isinstance(x, list)
    assert len(x) > 0


# ------------------------------------------
# Testing colorspace.palettes.hclpalettes.get_palette()
# ------------------------------------------
def test_hclpalettes_get_palette():
    pals  = colorspace.palettes.hclpalettes()
    # Getting first type of palettes
    first = pals.get_palettes(pals.get_palette_types()[0])
    assert isinstance(first, list)
    # Getting first palette of first type of palettes
    pal_name = first[0].name()
    assert isinstance(pal_name, str)
    # Getting this specific palette
    pal      = pals.get_palette(pal_name)
    assert isinstance(pal, colorspace.palettes.defaultpalette)
    assert isinstance(pal.name(), str)
def test_hclpalettes_get_palette_invalid_name():
    pals  = colorspace.palettes.hclpalettes()
    with pytest.raises(ValueError):
        pals.get_palette("this_is_a_test_foo_bar")










# ------------------------------------------
# ------------------------------------------
# types = ["diverging", "sequential", "qualitative", "heat", "rainbow", "terrain"]
