

import pytest
from pytest import raises
import numpy as np
from colorspace import sequential_hcl, hcl_palettes

# All parameters
_all_parameters = ["foo", "h1", "h2", "c1", "cmax", "c3", "l1", "l2", "p1", "p2"]

# ---------------------------------------------
# Default settings
# ---------------------------------------------
def test_sequential_hcl_defaults():
    expected_defaults = {"h1": 260, "h2": 260, "c1": 80, "c2": 0,
                         "l1": 30, "l2": 90, "p1": 1.5, "fixup": True, "rev": False}
    pal = sequential_hcl()
    for k,v in expected_defaults.items():
        assert pal.get(k) == v

# ---------------------------------------------
# Getting named palette via sequential_hcl
# ---------------------------------------------
def test_sequential_hcl_named_palette():
    trop1 = hcl_palettes(name = "Inferno").get_palettes()[0]
    trop2 = sequential_hcl("Inferno")

    # Must have identical settings as coming from the same source
    for k,v in trop1.get_settings().items():
        assert trop2.get(k) == v

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_sequential_hcl_wrong_usage_h():
    # Testing argument 'h'
    raises(ValueError, sequential_hcl, h = "name of non-existing palette")
    raises(ValueError, sequential_hcl, h = None) # None not allowed
    raises(ValueError, sequential_hcl, h = {1, 2}) # invalid type
    raises(ValueError, sequential_hcl, h = [1, 2, 3]) # length > 2
    raises(ValueError, sequential_hcl, h = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, sequential_hcl, h = np.asarray([])) # length < 1
    raises(ValueError, sequential_hcl, h = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, sequential_hcl, h = np.asarray([1, np.nan])) # nan not allowed

def test_sequential_hcl_wrong_usage_c():
    # Testing argument 'c'
    raises(ValueError, sequential_hcl, c = "foo") # not numeric
    raises(ValueError, sequential_hcl, c = None) # None not allowed
    raises(ValueError, sequential_hcl, c = {1, 2}) # invalid type
    raises(ValueError, sequential_hcl, c = [1, 2, 3, 4]) # length > 3
    raises(ValueError, sequential_hcl, c = np.asarray([1, 2, 3, 4])) # length > 3
    raises(ValueError, sequential_hcl, c = np.asarray([])) # length < 1
    raises(ValueError, sequential_hcl, c = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, sequential_hcl, c = np.asarray([1, np.nan])) # nan not allowed

def test_sequential_hcl_wrong_usage_l():
    # Testing argument 'l'
    raises(ValueError, sequential_hcl, l = "foo") # not numeric
    raises(ValueError, sequential_hcl, l = None) # None not allowed
    raises(ValueError, sequential_hcl, l = {1, 2}) # invalid type
    raises(ValueError, sequential_hcl, l = [1, 2, 3]) # length > 2
    raises(ValueError, sequential_hcl, l = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, sequential_hcl, l = np.asarray([])) # length < 1
    raises(ValueError, sequential_hcl, l = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, sequential_hcl, l = np.asarray([1, np.nan])) # nan not allowed

def test_sequential_hcl_wrong_usage_power():
    # Testing argument 'power'
    raises(ValueError, sequential_hcl, power = "foo") # not numeric
    raises(ValueError, sequential_hcl, power = None) # None not allowed
    raises(ValueError, sequential_hcl, power = {1, 2}) # invalid type
    raises(ValueError, sequential_hcl, power = [1, 2, 3]) # length > 2
    raises(ValueError, sequential_hcl, power = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, sequential_hcl, power = np.asarray([])) # length < 1
    raises(ValueError, sequential_hcl, power = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, sequential_hcl, power = np.asarray([1, np.nan])) # nan not allowed

def test_sequential_hcl_wrong_usage_fixup():
    # 'fixup' must be bool
    raises(TypeError, sequential_hcl, fixup = None)

def test_sequential_hcl_wrong_usage_palette():
    # Must be None or str, name of palette to load
    raises(TypeError, sequential_hcl, palette = 3)
    raises(TypeError, sequential_hcl, palette = ["foo", "bar"])

def test_sequential_hcl_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, sequential_hcl, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_sequential_hcl_colors():

    pal = sequential_hcl()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = sequential_hcl()(5)
    col2 = sequential_hcl().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = sequential_hcl().colors(5, fixup = "foo")
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
def test_sequential_hcl_named_palette():
    # Both ways of specifying the palette should lead to the same result
    pal1 = sequential_hcl("Purple-Orange")
    pal2 = sequential_hcl(palette = "Purple-Orange")
    assert isinstance(pal1, sequential_hcl)
    assert isinstance(pal2, sequential_hcl)
    assert pal1.settings == pal2.settings

# Testing unallowed parameters
def test_sequential_hcl_invalid_kwargs():
    pal1 = sequential_hcl()
    not_allowed = []
    for p in _all_parameters:
        if not p in sequential_hcl._allowed_parameters:
            not_allowed.append(p)

    for k in not_allowed:
        raises(ValueError, sequential_hcl, **{k: 0.})

# Testing allowed parameters
def test_sequential_hcl_allowed_kwargs_unnamed():
    # Test settings
    settings = {"h1": 11, "h2": 12, "c1": 13, "c2": 14,
                "l1": 15, "l2": 16, "p1": 17, "p2": 18}

    # Ensure I test all allowed parameters
    for k in sequential_hcl._allowed_parameters:
        # Skipping 'cmax', only testing 'basic' sequential palettes.
        # There are dedicated tests for advanced palettes below
        if k in ["cmax"]: continue
        if not k in settings.keys():
            raise Exception(f"missing allowed parameter \"{k}\" in test settings")

    # Reference palette
    ref = sequential_hcl(h =     [settings["h1"], settings["h2"]],
                         c =     [settings["c1"], settings["c2"]],
                         l =     [settings["l1"], settings["l2"]],
                         power = [settings["p1"], settings["p2"]])

    # Settings; will be tested one-by-one first
    for k,v in settings.items():
        args = {k: v}
        tmp  = sequential_hcl(**args)
        assert ref.get(k) == tmp.get(k)

    # All together
    tmp = sequential_hcl(**settings)
    for k in settings.keys():
        assert ref.get(k) == tmp.get(k)

# Using named palette (should be overwritten)
def test_sequential_hcl_allowed_kwargs_named():
    # Test settings
    settings = {"h1": 11, "h2": 12, "c1": 13, "c2": 14,
                "l1": 15, "l2": 16, "p1": 17, "p2": 18}

    # As we overwrite all settings, it should not matter that the
    # first one starts with the settings of the Red-Green instead
    # of the default palette.
    pal1 = sequential_hcl(**settings, palette = "Purple-Orange")
    pal2 = sequential_hcl(**settings)

    for k in settings.keys():
        assert pal1.get(k) == pal2.get(k)

# Building advanced sequential multi-hue (BuPu) "by hand" to
# cover the options/arguments required for advanced palettes,
# namely cmax (c of length 3)
def test_sequential_hcl_BuPu():

    # Reference palette
    ref = sequential_hcl(palette = "BuPu")

    # Building it via named kwargs
    settings = {"h1": 320, "h2": 200,
                "c1": 40,  "cmax": 65, "c2": 5,
                "l1": 15,  "l2": 98,
                "p1": 1.2, "p2": 1.3}
    tmp = sequential_hcl(**settings)
    for k,v in settings.items():
        assert tmp.get(k) == v
        assert ref.get(k) == tmp.get(k)

    # Buliding it over h, c, l, power
    tmp = sequential_hcl(h =     [settings["h1"], settings["h2"]],
                         c =     [settings["c1"], settings["cmax"], settings["c2"]],
                         l =     [settings["l1"], settings["l2"]],
                         power = [settings["p1"], settings["p2"]])
    for k,v in settings.items():
        assert tmp.get(k) == v
        assert ref.get(k) == tmp.get(k)

# Handling of missing colors if fixup = FALSE
def test_sequential_hcl_missing_colors_fixup():

    pal1 = sequential_hcl(c1 = 100).colors(11)
    pal2 = sequential_hcl(c1 = 100).colors(11, fixup = False)

    assert len(pal1) == len(pal2)
    assert pal2[0] is None

    assert np.all(pal2[1:] == pal1[1:])


# Testing argument 'palette'
def test_sequential_hcl_argument_palette():
    ref = hcl_palettes().get_palette("viridis").get_settings()
    
    # By name
    pal = sequential_hcl("viridis")
    assert ref == pal.settings
    del pal
    
    # By name using palette argument
    pal = sequential_hcl(palette = "viridis")
    assert ref == pal.settings
    del pal

# Testing argument 'h'
def test_sequential_hcl_argument_h():

    # Testing h: single int
    settings = sequential_hcl(h = 30).settings
    assert np.equal(settings["h1"], 30)
    assert np.equal(settings["h2"], 30)
    del settings
    
    settings = sequential_hcl(h = [30]).settings
    assert np.equal(settings["h1"], 30)
    assert np.equal(settings["h2"], 30)
    del settings
    
    # Testing h: single float
    settings = sequential_hcl(h = 30.5).settings
    assert np.equal(settings["h1"], 30)
    assert np.equal(settings["h2"], 30)
    del settings
    
    # Testing h as list of [h1, h2]
    settings = sequential_hcl(h = [40, 50]).settings
    assert np.equal(settings["h1"], 40)
    assert np.equal(settings["h2"], 50)
    del settings

# Testing argument 'c'
def test_sequential_hcl_argument_c():

    # Testing c: single numeric (linear to zero)
    settings = sequential_hcl(c = 30.).settings
    assert np.equal(settings["c1"], 30)
    assert np.equal(settings["c2"], 0)
    assert not "cmax" in settings.keys() # no cmax
    del settings
    
    settings = sequential_hcl(c = [30.]).settings
    assert np.equal(settings["c1"], 30)
    assert np.equal(settings["c2"], 0)
    assert not "cmax" in settings.keys() # no cmax
    del settings
    
    # Testinc c: list of two numerics ([c1, c2])
    settings = sequential_hcl(c = [35, 45]).settings
    assert np.equal(settings["c1"], 35)
    assert np.equal(settings["c2"], 45)
    assert not "cmax" in settings.keys() # no cmax
    del settings
    
    # Testinc c: list of three numerics ([c1, cmax, c2])
    settings = sequential_hcl(c = [30, 50, 10]).settings
    assert np.equal(settings["c1"], 30)
    assert np.equal(settings["cmax"], 50)
    assert np.equal(settings["c2"], 10)

# Testing argument 'l'
def test_sequential_hcl_argument_l():

    # Testing c: single numeric (linear to zero)
    settings = sequential_hcl(l = 10.).settings
    assert np.equal(settings["l1"], 10)
    assert np.equal(settings["l2"], 10)
    del settings
    
    settings = sequential_hcl(l = [10.]).settings
    assert np.equal(settings["l1"], 10)
    assert np.equal(settings["l2"], 10)
    del settings
    
    # Testing c: single numeric (linear to zero)
    settings = sequential_hcl(l = 20.).settings
    assert np.equal(settings["l1"], 20)
    assert np.equal(settings["l2"], 20)
    del settings
    
    # Testing c: single numeric (linear to zero)
    settings = sequential_hcl(l = [11, 12]).settings
    assert np.equal(settings["l1"], 11)
    assert np.equal(settings["l2"], 12)
    del settings

# Testing argument 'power'
def test_sequential_hcl_argument_power():

    # Testing power: single numeric (recycled)
    settings = sequential_hcl(power = 1.1).settings
    assert np.equal(settings["p1"], 1.1)
    assert np.equal(settings["p2"], 1.1)
    del settings
    
    settings = sequential_hcl(power = [1.1]).settings
    assert np.equal(settings["p1"], 1.1)
    assert np.equal(settings["p2"], 1.1)
    del settings
    
    # Testing power: two numeric values
    settings = sequential_hcl(power = [0.5, 0.7]).settings
    assert np.equal(settings["p1"], 0.5)
    assert np.equal(settings["p2"], 0.7)
    del settings


# Testing alpha handling
def test_sequential_hcl_argument_alpha():

    # First testing misuse
    pal = sequential_hcl()
    raises(TypeError, pal.colors, n = 2, alpha = "foo") # must be float
    raises(TypeError, pal.colors, n = 2, alpha = 0) # must be float

    raises(ValueError, pal.colors, n = 2, alpha = -0.0001) # must be [0, 1]
    raises(ValueError, pal.colors, n = 2, alpha =  1.0001) # must be [0, 1]

    raises(ValueError, pal.colors, n = 2, alpha =  [0.3, 1.0001]) # must be [0, 1]
    raises(ValueError, pal.colors, n = 2, alpha =  [1.0001, 0.3]) # must be [0, 1]
    raises(ValueError, pal.colors, n = 2, alpha =  [0.3, -0.0001]) # must be [0, 1]
    raises(ValueError, pal.colors, n = 2, alpha =  [-0.0001, 0.3]) # must be [0, 1]

    raises(ValueError, pal.colors, n = 2, alpha = [0.1, 0.2, 0,3]) # length mismatch
    raises(ValueError, pal.colors, n = 3, alpha = [0.1, 0.2]) # length mismatch

    # 'R' is the solution from the same call in R to be compared against

    # sequential_hcl, 5 colors, no alpha
    x = sequential_hcl().colors(5)
    R = ["#023FA5", "#6A76B2", "#A1A6C8", "#CBCDD9", "#E2E2E2"]
    assert np.all(x == R)
     
    # sequential_hcl, 5 colors, constant alpha = 0.3
    x = sequential_hcl().colors(5, alpha = 0.3)
    R = ["#023FA54D", "#6A76B24D", "#A1A6C84D", "#CBCDD94D", "#E2E2E24D"]
    assert np.all(x == R)
    
    # sequential_hcl, 6 colors with alpha [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    R = ["#023FA500", "#5D6CAE33", "#8C94BF66", "#B3B7CF99", "#D2D3DCCC", "#E2E2E2"]
    x = sequential_hcl().colors(6, alpha = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    assert np.all(x == R)




