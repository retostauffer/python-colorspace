

import pytest
from pytest import raises
import numpy as np

import matplotlib.pyplot as plt
from colorspace import diverging_hcl, hcl_palettes


# ---------------------------------------------
# Default settings
# ---------------------------------------------
def test_diverging_hcl_defaults():
    expected_defaults = {"h1": 260, "h2": 0, "c1": 80, "l1": 30,
                         "l2": 90, "p1": 1.5, "fixup": True, "rev": False}
    pal = diverging_hcl()
    for k,v in expected_defaults.items():
        assert pal.get(k) == v

# ---------------------------------------------
# Getting named palette via diverging_hcl
# ---------------------------------------------
def test_diverging_hcl_named_palette():
    trop1 = hcl_palettes(name = "Tropic").get_palettes()[0]
    trop2 = diverging_hcl("Tropic")

    # Must have identical settings as coming from the same source
    for k,v in trop1.get_settings().items():
        assert trop2.get(k) == v

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_diverging_hcl_wrong_usage_h():
    # Testing argument 'h'
    raises(ValueError, diverging_hcl, h = "name of non-existing palette")
    raises(ValueError, diverging_hcl, h = None) # None not allowed
    raises(ValueError, diverging_hcl, h = {1, 2}) # invalid type
    raises(ValueError, diverging_hcl, h = [1, 2, 3]) # length > 2
    raises(ValueError, diverging_hcl, h = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, diverging_hcl, h = np.asarray([])) # length < 1
    raises(ValueError, diverging_hcl, h = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, diverging_hcl, h = np.asarray([1, np.nan])) # nan not allowed

def test_diverging_hcl_wrong_usage_c():
    # Testing argument 'c'
    raises(ValueError, diverging_hcl, c = "foo") # not numeric
    raises(ValueError, diverging_hcl, c = None) # None not allowed
    raises(ValueError, diverging_hcl, c = {1, 2}) # invalid type
    raises(ValueError, diverging_hcl, c = [1, 2, 3]) # length > 2
    raises(ValueError, diverging_hcl, c = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, diverging_hcl, c = np.asarray([])) # length < 1
    raises(ValueError, diverging_hcl, c = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, diverging_hcl, c = np.asarray([1, np.nan])) # nan not allowed

def test_diverging_hcl_wrong_usage_l():
    # Testing argument 'l'
    raises(ValueError, diverging_hcl, l = "foo") # not numeric
    raises(ValueError, diverging_hcl, l = None) # None not allowed
    raises(ValueError, diverging_hcl, l = {1, 2}) # invalid type
    raises(ValueError, diverging_hcl, l = [1, 2, 3]) # length > 2
    raises(ValueError, diverging_hcl, l = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, diverging_hcl, l = np.asarray([])) # length < 1
    raises(ValueError, diverging_hcl, l = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, diverging_hcl, l = np.asarray([1, np.nan])) # nan not allowed

def test_diverging_hcl_wrong_usage_power():
    # Testing argument 'power'
    raises(ValueError, diverging_hcl, power = "foo") # not numeric
    raises(ValueError, diverging_hcl, power = None) # None not allowed
    raises(ValueError, diverging_hcl, power = {1, 2}) # invalid type
    raises(ValueError, diverging_hcl, power = [1, 2, 3]) # length > 2
    raises(ValueError, diverging_hcl, power = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, diverging_hcl, power = np.asarray([])) # length < 1
    raises(ValueError, diverging_hcl, power = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, diverging_hcl, power = np.asarray([1, np.nan])) # nan not allowed

def test_diverging_hcl_wrong_usage_fixup():
    # 'fixup' must be bool
    raises(TypeError, diverging_hcl, fixup = None)

def test_diverging_hcl_wrong_usage_palette():
    # Must be None or str, name of palette to load
    raises(TypeError, diverging_hcl, palette = 3)
    raises(TypeError, diverging_hcl, palette = ["foo", "bar"])

def test_diverging_hcl_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, diverging_hcl, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_diverging_hcl_colors():

    pal = diverging_hcl()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = diverging_hcl()(5)
    col2 = diverging_hcl().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = diverging_hcl().colors(5, fixup = "foo")
    assert np.all(col1 == col3)

    # Alpha must be None, float, list (which can be converted)
    # to numpy array of dtype float), or numpy array. If array,
    # same length as n or 1. Values must be within 0-1
    # If input is a list or an array, the length must be 1 or equal to n.
    raises(TypeError, pal.colors, 3, alpha = "foo")
    raises(ValueError, pal.colors, 3, alpha = -0.01)
    raises(ValueError, pal.colors, 3, alpha = 1.01)
    raises(ValueError, pal.colors, 3, alpha = [-0.01])
    raises(ValueError, pal.colors, 3, alpha = [1.01])
    raises(ValueError, pal.colors, 3, alpha = [0.1, 0.1])
    raises(ValueError, pal.colors, 3, alpha = [0.1, 0.1, 0.1, 0.1])
    raises(ValueError, pal.colors, 3, alpha = np.repeat(0.3, 2))
    raises(ValueError, pal.colors, 3, alpha = np.repeat(0.3, 4))
    raises(ValueError, pal.colors, 3, alpha = np.repeat(-0.01, 3))
    raises(ValueError, pal.colors, 3, alpha = np.repeat(1.01, 3))

# ---------------------------------------------
# Testing options
# ---------------------------------------------

# Named palettes can be specified via first arg (h) or 'palette' arg.
def test_diverging_hcl_named_palette():
    # Both ways of specifying the palette should lead to the same result
    pal1 = diverging_hcl("Red-Green")
    pal2 = diverging_hcl(palette = "Red-Green")
    assert isinstance(pal1, diverging_hcl)
    assert isinstance(pal2, diverging_hcl)
    assert pal1.settings == pal2.settings

# Testing unallowed parameters
def test_diverging_hcl_invalid_kwargs():
    pal1 = diverging_hcl()
    not_allowed = ["foo", "c2"]
    for k in not_allowed:
        raises(ValueError, diverging_hcl, **{k: 0.})

# Testing allowed parameters
def test_diverging_hcl_allowed_kwargs_unnamed():
    # Reference palette
    settings = {"h1": 11, "h2": 12, "c1": 13, "l1": 14, "l2": 15, "p1": 16}
    ref = diverging_hcl(h = [settings["h1"], settings["h2"]],
                        c = settings["c1"],
                        l = [settings["l1"], settings["l2"]],
                        power = settings["p1"])

    # Settings; will be tested one-by-one first
    for k,v in settings.items():
        args = {k: v}
        tmp  = diverging_hcl(**args)
        assert ref.get(k) == tmp.get(k)

    # All together
    tmp = diverging_hcl(**settings)
    for k in settings.keys():
        assert ref.get(k) == tmp.get(k)

# Allowed are: "h1", "h2", "c1", "l1", "l2", "p1"
# Using named palette (should be overwritten)
def test_diverging_hcl_allowed_kwargs_named():
    # Reference palette
    settings = {"h1": 11, "h2": 12, "c1": 13, "l1": 14, "l2": 15, "p1": 16}

    # As we overwrite all settings, it should not matter that the
    # first one starts with the settings of the Red-Green instead
    # of the default palette.
    pal1 = diverging_hcl(**settings, palette = "Green-Orange")
    pal2 = diverging_hcl(**settings)

    for k in settings.keys():
        assert pal1.get(k) == pal2.get(k)

# Building advanced diverging (Tofino palette) "by hand" to
# cover the options/arguments required for advanced palettes,
# namely cmax/p2 (c of length 2, power of length 2)
def test_diverging_hcl_Tofino():

    # Reference palette
    ref = diverging_hcl(palette = "Tofino")

    # Building it via named kwargs
    settings = {"h1": 260, "h2": 120,
                "c1": 45, "cmax": 55,
                "l1": 90, "l2": 5,
                "p1": 0.8, "p2": 1.0}
    tmp = diverging_hcl(**settings)
    for k,v in settings.items():
        assert tmp.get(k) == v
        assert ref.get(k) == tmp.get(k)

    # Buliding it over h, c, l, power
    tmp = diverging_hcl(h = [settings["h1"], settings["h2"]],
                        c = [settings["c1"], settings["cmax"]],
                        l = [settings["l1"], settings["l2"]],
                        power = [settings["p1"], settings["p2"]])
    for k,v in settings.items():
        assert tmp.get(k) == v
        assert ref.get(k) == tmp.get(k)


## Testing another color palette where heu-axis should be adjusted to 0-360 only
#@pytest.mark.mpl_image_compare
#def test_specplot_provide_figure_obj():
#    import matplotlib.pyplot as plt
#
#    fig  = plt.figure(figsize = (4, 6))
#    cols = rainbow(start = 0, end= 1/3)(51)
#    fig  = specplot(cols, fig = fig)
#    assert isinstance(fig, Figure)
#    # Ensure we got our custom figure object back
#    assert fig.get_figwidth() == 4.
#    assert fig.get_figheight() == 6.
#    plt.show()
#    plt.close() # Closing figure instance

