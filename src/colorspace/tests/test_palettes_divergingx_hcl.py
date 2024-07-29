

import pytest
from pytest import raises
import numpy as np
from colorspace import divergingx_hcl, hcl_palettes, divergingx_palettes

# All parameters; special for divergingx
_all_parameters = ["foo", "h1", "h2", "c1", "c2", "c3",
        "l1", "l2", "l3", "l4", "p1", "p2",
        "p3", "p4", "cmax1", "cmax2"]

# ---------------------------------------------
# Default settings
# ---------------------------------------------
def test_divergingx_hcl_defaults():
    expected_defaults = {"h1": 192, "h2": 77, "h3": 21,
                         "c1": 40, "c2": 35, "c3": 100,
                         "cmax1": 20, "cmax2": np.nan,
                         "l1": 50, "l2": 95, "l3": 50,
                         "p1": 1.0, "p2": 1.0, "p3": 1.2, "p4": 1.0,
                         "fixup": True, "rev": False}
    pal = divergingx_hcl()
    for k,v in expected_defaults.items():
        if np.isnan(v):
            assert np.isnan(pal.get(k))
        else:
            assert pal.get(k) == v

# ---------------------------------------------
# Getting named palette via divergingx_hcl
# ---------------------------------------------
def test_divergingx_hcl_named_palette():
    # hcl_palettes does not return DivergingX palettes
    raises(Exception, hcl_palettes, name = "ArmyRose")

    # Instead, go via divergingx_palettes
    armyrose1 = divergingx_palettes(name = "ArmyRose").get_palettes()[0]
    armyrose2 = divergingx_hcl("ArmyRose")

    # Must have identical settings as coming from the same source
    for k,v in armyrose1.get_settings().items():
        assert armyrose2.get(k) == v

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_divergingx_hcl_wrong_usage_h():
    # Testing argument 'h'
    raises(ValueError, divergingx_hcl, h = "name of non-existing palette")
    raises(ValueError, divergingx_hcl, h = None) # None not allowed
    raises(ValueError, divergingx_hcl, h = {1, 2}) # invalid type
    raises(ValueError, divergingx_hcl, h = [1, 2, 3, 4]) # length > 3
    raises(ValueError, divergingx_hcl, h = np.asarray([1, 2, 3, 4])) # length > 3
    raises(ValueError, divergingx_hcl, h = np.asarray([])) # length < 1
    raises(ValueError, divergingx_hcl, h = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, divergingx_hcl, h = np.asarray([1, np.nan])) # nan not allowed

def test_divergingx_hcl_wrong_usage_c():
    # Testing argument 'c'
    raises(ValueError, divergingx_hcl, c = "foo") # not numeric
    raises(ValueError, divergingx_hcl, c = None) # None not allowed
    raises(ValueError, divergingx_hcl, c = {1, 2}) # invalid type
    raises(ValueError, divergingx_hcl, c = [1, 2, 3, 4]) # length > 3
    raises(ValueError, divergingx_hcl, c = np.asarray([1, 2, 3, 4])) # length > 3
    raises(ValueError, divergingx_hcl, c = np.asarray([])) # length < 1
    raises(ValueError, divergingx_hcl, c = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, divergingx_hcl, c = np.asarray([1, np.nan])) # nan not allowed

def test_divergingx_hcl_wrong_usage_cmax():
    # Testing argument 'cmax'
    raises(TypeError, divergingx_hcl, cmax = "foo") # invalid type
    raises(TypeError, divergingx_hcl, cmax = {1, 2}) # invalid type
    raises(ValueError, divergingx_hcl, cmax = []) # length < 1
    raises(ValueError, divergingx_hcl, cmax = [1, 2, 3]) # length > 2
    raises(ValueError, divergingx_hcl, cmax = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, divergingx_hcl, cmax = np.asarray([])) # length < 1

def test_divergingx_hcl_wrong_usage_l():
    # Testing argument 'l'
    raises(ValueError, divergingx_hcl, l = "foo") # not numeric
    raises(ValueError, divergingx_hcl, l = None) # None not allowed
    raises(ValueError, divergingx_hcl, l = {1, 2}) # invalid type
    raises(ValueError, divergingx_hcl, l = 1) # length <2
    raises(ValueError, divergingx_hcl, l = [1]) # length <2
    raises(ValueError, divergingx_hcl, l = np.asarray([1])) # length <2
    raises(ValueError, divergingx_hcl, l = [1, 2, 3, 4]) # length > 3
    raises(ValueError, divergingx_hcl, l = np.asarray([1, 2, 3, 4])) # length > 3
    raises(ValueError, divergingx_hcl, l = np.asarray([])) # length < 1
    raises(ValueError, divergingx_hcl, l = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, divergingx_hcl, l = np.asarray([1, np.nan])) # nan not allowed

def test_divergingx_hcl_wrong_usage_power():
    # Testing argument 'power'
    raises(ValueError, divergingx_hcl, power = "foo") # not numeric
    raises(ValueError, divergingx_hcl, power = None) # None not allowed
    raises(ValueError, divergingx_hcl, power = {1, 2}) # invalid type
    raises(ValueError, divergingx_hcl, power = 1) # length <2
    raises(ValueError, divergingx_hcl, power = [1]) # length <2
    raises(ValueError, divergingx_hcl, power = np.asarray([1])) # length <2
    raises(ValueError, divergingx_hcl, power = [1, 2, 3, 4, 5]) # length > 4
    raises(ValueError, divergingx_hcl, power = np.asarray([1, 2, 3, 4, 5])) # length > 4
    raises(ValueError, divergingx_hcl, power = np.asarray([])) # length < 1
    raises(ValueError, divergingx_hcl, power = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, divergingx_hcl, power = np.asarray([1, np.nan])) # nan not allowed

def test_divergingx_hcl_wrong_usage_fixup():
    # 'fixup' must be bool
    raises(TypeError, divergingx_hcl, fixup = None)

def test_divergingx_hcl_wrong_usage_palette():
    # Must be None or str, name of palette to load
    raises(TypeError, divergingx_hcl, palette = 3)
    raises(TypeError, divergingx_hcl, palette = ["foo", "bar"])

def test_divergingx_hcl_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, divergingx_hcl, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_divergingx_hcl_colors():

    pal = divergingx_hcl()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = divergingx_hcl()(5)
    col2 = divergingx_hcl().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = divergingx_hcl().colors(5, fixup = "foo")
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
def test_divergingx_hcl_named_palette():
    # Both ways of specifying the palette should lead to the same result
    pal1 = divergingx_hcl("ArmyRose")
    pal2 = divergingx_hcl(palette = "ArmyRose")
    assert isinstance(pal1, divergingx_hcl)
    assert isinstance(pal2, divergingx_hcl)
    assert pal1.settings == pal2.settings

# Testing unallowed parameters
def test_divergingx_hcl_invalid_kwargs():
    pal1 = divergingx_hcl()

    not_allowed = []
    for p in _all_parameters:
        if not p in divergingx_hcl._allowed_parameters:
            not_allowed.append(p)

    for k in not_allowed:
        raises(ValueError, divergingx_hcl, **{k: 0.})

# Testing allowed parameters
def test_divergingx_hcl_allowed_kwargs_unnamed():
    # Test settings
    settings = {"h1": 11, "h2": 12, "h3": 13,
                "c1": 14, "c2": 15, "c3": 16,
                "cmax1": 17, "cmax2": 18,
                "l1": 19, "l2": 20, "l3": 21,
                "p1": 22, "p2": 23, "p3": 24, "p4": 25}

    # Ensure I test all allowed parameters
    for k in divergingx_hcl._allowed_parameters:
        if not k in settings.keys():
            raise Exception(f"missing allowed parameter \"{k}\" in test settings")

    # Reference palette
    ref = divergingx_hcl(h     = [settings[k] for k in ["h1", "h2", "h3"]],
                         c     = [settings[k] for k in ["c1", "c2", "c3"]],
                         cmax  = [settings[k] for k in ["cmax1", "cmax2"]],
                         l     = [settings[k] for k in ["l1", "l2", "l3"]],
                         power = [settings[k] for k in ["p1", "p2", "p3", "p4"]])

    # Settings; will be tested one-by-one first
    for k,v in settings.items():
        args = {k: v}
        tmp  = divergingx_hcl(**args)
        assert ref.get(k) == tmp.get(k)

    # All together
    tmp = divergingx_hcl(**settings)
    for k in settings.keys():
        assert ref.get(k) == tmp.get(k)

# Using named palette (should be overwritten)
def test_divergingx_hcl_allowed_kwargs_named():
    # Test settings
    settings = {"h1": 11, "h2": 12, "h3": 13,
                "c1": 14, "c2": 15, "c3": 16,
                "cmax1": 17, "cmax2": 18,
                "l1": 19, "l2": 20, "l3": 21,
                "p1": 22, "p2": 23, "p3": 24, "p4": 25}

    # As we overwrite all settings, it should not matter that the
    # first one starts with the settings of the Red-Green instead
    # of the default palette.
    pal1 = divergingx_hcl(**settings, palette = "ArmyRose")
    pal2 = divergingx_hcl(**settings)

    for k in settings.keys():
        assert pal1.get(k) == pal2.get(k)

# Handling of missing colors if fixup = FALSE
def test_divergingx_hcl_missing_colors_fixup():

    pal1 = divergingx_hcl(cmax1 = 100).colors(11)
    pal2 = divergingx_hcl(cmax1 = 100).colors(11, fixup = False)

    assert len(pal1) == len(pal2)
    assert pal2[0] is None
    assert pal2[1] is None
    assert pal2[2] is None

    assert np.all(pal2[3:] == pal1[3:])


# Testing the edge case where we have only one color (n = 1)
# Also testing n = 5, 4, 3, 2, 1 just to check that the center
# color and the distance is as expected.
def test_divergingx_hcl_one_color_only():

    R = ["#008585", "#9BBAA0", "#FBF2C4", "#DEA868", "#C7522B"]
    assert np.all(divergingx_hcl()(5) == R)

    R = ["#008585", "#B8CDAE", "#E6C186", "#C7522B"]
    assert np.all(divergingx_hcl()(4) == R)

    R = ["#008585", "#FBF2C4", "#C7522B"]
    assert np.all(divergingx_hcl()(3) == R)

    R = ["#008585", "#C7522B"]
    assert np.all(divergingx_hcl()(2) == R)
    
    R = ["#FBF2C4"]
    assert np.all(divergingx_hcl()(1) == R)

# Testing argument 'palette'
def test_divergingx_hcl_argument_palette():

    ref = divergingx_palettes().get_palette("ArmyRose").get_settings()
    
    # By name
    pal = divergingx_hcl("ArmyRose")
    assert ref == pal.settings
    del pal
    
    # By name using palette argument
    pal = divergingx_hcl(palette = "ArmyRose")
    assert ref == pal.settings
    del pal


# Testing argument 'h'
def test_divergingx_hcl_argument_h():

    # Testing h: Must be three values
    settings = divergingx_hcl(h = [180, 90, 0]).settings
    assert np.equal(settings["h1"], 180)
    assert np.equal(settings["h2"], 90)
    assert np.equal(settings["h3"], 0)
    del settings


# Testing argument 'cmax'
def test_divergingx_hcl_argument_cmax():

    # Default palette only has cmax1 = 20.
    settings = divergingx_hcl().settings
    assert np.equal(settings["cmax1"], 20.)
    assert np.isnan(settings["cmax2"])
    del settings

    # Single int: cmax1 = cmax, cmax2 is nan
    settings = divergingx_hcl(cmax = 22).settings
    assert np.equal(settings["cmax1"], 22.)
    assert np.isnan(settings["cmax2"])
    del settings

    # Single float: cmax1 = cmax, cmax2 is nan
    settings = divergingx_hcl(cmax = 22.2).settings
    assert np.equal(settings["cmax1"], 22.2)
    assert np.isnan(settings["cmax2"])
    del settings

    # List of single int: cmax1 = cmax[0], cmax2 is nan
    settings = divergingx_hcl(cmax = [33]).settings
    assert np.equal(settings["cmax1"], 33.)
    assert np.isnan(settings["cmax2"])
    del settings

    # List of single float: cmax1 = cmax[0], cmax2 is nan
    settings = divergingx_hcl(cmax = [33.3]).settings
    assert np.equal(settings["cmax1"], 33.3)
    assert np.isnan(settings["cmax2"])
    del settings

    # If cmax = None, both are nan
    settings = divergingx_hcl(cmax = None).settings
    assert np.isnan(settings["cmax1"])
    assert np.isnan(settings["cmax2"])
    del settings

    # List with mixed None and float
    settings = divergingx_hcl(cmax = [None, 44.4]).settings
    assert np.isnan(settings["cmax1"])
    assert np.equal(settings["cmax2"], 44.4)
    del settings

    settings = divergingx_hcl(cmax = [55.5, None]).settings
    assert np.equal(settings["cmax1"], 55.5)
    assert np.isnan(settings["cmax2"])
    del settings

    # List with two values float/int
    settings = divergingx_hcl(cmax = [66.6, 77]).settings
    assert np.equal(settings["cmax1"], 66.6)
    assert np.equal(settings["cmax2"], 77.0)
    del settings

    settings = divergingx_hcl(cmax = [88, 88.1]).settings
    assert np.equal(settings["cmax1"], 88.0)
    assert np.equal(settings["cmax2"], 88.1)
    del settings
    

# Testing argument 'c'
def test_divergingx_hcl_argument_c():

    # Testing c: two values. First will be used as c1, c3, the second for c2
    settings = divergingx_hcl(c = [50, 20]).settings
    assert np.equal(settings["c1"], 50)
    assert np.equal(settings["c2"], 20)
    assert np.equal(settings["c3"], 50)
    del settings
    
    # Testing c: three values [c1, c2, c3]
    settings = divergingx_hcl(c = [30, 40, 50]).settings
    assert np.equal(settings["c1"], 30)
    assert np.equal(settings["c2"], 40)
    assert np.equal(settings["c3"], 50)
    del settings


# Testing argument 'l'
def test_divergingx_hcl_argument_l():

    # Testing l: two values. First will be used as l1, l3, the second for l2
    settings = divergingx_hcl(l = [50, 20]).settings
    assert np.equal(settings["l1"], 50)
    assert np.equal(settings["l2"], 20)
    assert np.equal(settings["l3"], 50)
    del settings
    
    # Testing l: three values [l1, l2, l3]
    settings = divergingx_hcl(l = [30, 40, 50]).settings
    assert np.equal(settings["l1"], 30)
    assert np.equal(settings["l2"], 40)
    assert np.equal(settings["l3"], 50)
    del settings


# Testing argument 'power'
def test_divergingx_hcl_argument_power():

    # Testing power: two values. First will be used as p1 and p4, the second for p2 and p3
    settings = divergingx_hcl(power = [0.7, 1.2]).settings
    assert np.equal(settings["p1"], 0.7)
    assert np.equal(settings["p2"], 1.2)
    assert np.equal(settings["p3"], 1.2)
    assert np.equal(settings["p4"], 0.7)
    del settings
    
    # Testing power: three values, acts like only two would be there
    settings = divergingx_hcl(power = [0.7, 1.2, 1.8]).settings
    assert np.equal(settings["p1"], 0.7)
    assert np.equal(settings["p2"], 1.2)
    assert np.equal(settings["p3"], 1.2)
    assert np.equal(settings["p4"], 0.7)
    del settings

    # Testing power: four values [p1, p2, p3, p4]
    settings = divergingx_hcl(power = [1.1, 1.2, 1.3, 1.4]).settings
    assert np.equal(settings["p1"], 1.1)
    assert np.equal(settings["p2"], 1.2)
    assert np.equal(settings["p3"], 1.3)
    assert np.equal(settings["p4"], 1.4)
    del settings


# Testing alpha handling
def test_divergingx_hcl_argument_alpha():

    # First testing misuse
    pal = divergingx_hcl()
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

    # divergingx_hcl, 5 colors, no alpha
    x = divergingx_hcl().colors(5) 
    R = ["#008585", "#9BBAA0", "#FBF2C4", "#DEA868", "#C7522B"]
    assert np.all(x == R)
    
    # divergingx_hcl, 5 colors, constant alpha = 0.3
    x = divergingx_hcl().colors(5, alpha = 0.3) 
    R = ["#0085854D", "#9BBAA04D", "#FBF2C44D", "#DEA8684D", "#C7522B4D"]
    assert np.all(x == R)
    
    # divergingx_hcl, 6 colors with alpha [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    x = divergingx_hcl().colors(6, alpha = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    R = ["#00858500", "#85AF9733", "#D0DCB566", "#EDD59F99", "#DA9857CC", "#C7522B"]
    assert np.all(x == R)
    
    
    







