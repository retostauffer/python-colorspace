

import pytest
from pytest import raises
import numpy as np
from colorspace import qualitative_hcl, hcl_palettes

# All parameters
_all_parameters = ["foo", "h1", "h2", "c1", "cmax", "c3", "l1", "l2", "p1", "p2"]

# ---------------------------------------------
# Helper function to compare settings. Some allow
# to be lambda functions; this function tries to
# take care of comparing the return of these
# functions properly.
# ---------------------------------------------
def get_setting_values(a, b, name, n = 10):
    from colorspace.palettes import defaultpalette

    def get_entry(x, name):
        if isinstance(x, qualitative_hcl):
            return x.get(name)
        elif isinstance(x, defaultpalette):
            return x.get_settings()[name]
        elif isinstance(x, dict):
            return x[name]
        else:
            raise TypeError(f"unknown type: {type(x)}")

    a = get_entry(a, name)
    b = get_entry(b, name)

    if callable(a) and callable(b):
        return a(n), b(n)
    elif not callable(a) and not callable(b):
        return a, b
    else:
        raise Exception("issues comparing settings; not both callable/not callable")


# ---------------------------------------------
# Default settings
# ---------------------------------------------
def test_qualitative_hcl_defaults():
    expected_defaults = {"h1": 0, "h2": lambda n: 360. * (n - 1) / n,
                         "c1": 80, "l1": 60., "fixup": True, "rev": False}
    pal = qualitative_hcl()
    for k in expected_defaults.keys():
        a,b = get_setting_values(pal, expected_defaults, k, n = 10)

# ---------------------------------------------
# Getting named palette via qualitative_hcl
# ---------------------------------------------
def test_qualitative_hcl_named_palette():
    set21 = hcl_palettes(name = "Set 2").get_palettes()[0]
    set22 = qualitative_hcl("Set 2")

    # Must have identical settings as coming from the same source
    for k in set21.get_settings().keys():
        a,b = get_setting_values(set21, set22, k, n = 10)

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_qualitative_hcl_wrong_usage_h():
    # Testing argument 'h'
    raises(ValueError, qualitative_hcl, h = "name of non-existing palette")
    raises(ValueError, qualitative_hcl, h = None) # None not allowed
    raises(ValueError, qualitative_hcl, h = {1, 2}) # invalid type
    raises(ValueError, qualitative_hcl, h = [1, 2, 3]) # length > 2
    raises(ValueError, qualitative_hcl, h = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, qualitative_hcl, h = np.asarray([])) # length < 1
    raises(ValueError, qualitative_hcl, h = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, qualitative_hcl, h = np.asarray([1, np.nan])) # nan not allowed

    # inappropriate type
    raises(TypeError, qualitative_hcl, h = [3, "foo"])
    raises(TypeError, qualitative_hcl, h = ["foo", 3])
    raises(ValueError, qualitative_hcl, h = ["foo"])


def test_qualitative_hcl_wrong_usage_c():
    # Testing argument 'c'
    raises(ValueError, qualitative_hcl, c = "foo") # not numeric
    raises(ValueError, qualitative_hcl, c = None) # None not allowed
    raises(ValueError, qualitative_hcl, c = {1, 2}) # invalid type
    raises(ValueError, qualitative_hcl, c = [1, 2, 3]) # length > 2
    raises(ValueError, qualitative_hcl, c = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, qualitative_hcl, c = np.asarray([])) # length < 1
    raises(ValueError, qualitative_hcl, c = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, qualitative_hcl, c = np.asarray([1, np.nan])) # nan not allowed

def test_qualitative_hcl_wrong_usage_l():
    # Testing argument 'l'
    raises(ValueError, qualitative_hcl, l = "foo") # not numeric
    raises(ValueError, qualitative_hcl, l = None) # None not allowed
    raises(ValueError, qualitative_hcl, l = {1, 2}) # invalid type
    raises(ValueError, qualitative_hcl, l = [1, 2, 3]) # length > 2
    raises(ValueError, qualitative_hcl, l = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, qualitative_hcl, l = np.asarray([])) # length < 1
    raises(ValueError, qualitative_hcl, l = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, qualitative_hcl, l = np.asarray([1, np.nan])) # nan not allowed

def test_qualitative_hcl_wrong_usage_fixup():
    # 'fixup' must be bool
    raises(TypeError, qualitative_hcl, fixup = None)

def test_qualitative_hcl_wrong_usage_palette():
    # Must be None or str, name of palette to load
    raises(TypeError, qualitative_hcl, palette = 3)
    raises(TypeError, qualitative_hcl, palette = ["foo", "bar"])

def test_qualitative_hcl_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, qualitative_hcl, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_qualitative_hcl_colors():

    pal = qualitative_hcl()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = qualitative_hcl()(5)
    col2 = qualitative_hcl().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = qualitative_hcl().colors(5, fixup = "foo")
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
def test_qualitative_hcl_named_palette():
    # Both ways of specifying the palette should lead to the same result
    pal1 = qualitative_hcl("Harmonic")
    pal2 = qualitative_hcl(palette = "Harmonic")
    assert isinstance(pal1, qualitative_hcl)
    assert isinstance(pal2, qualitative_hcl)
    assert pal1.settings == pal2.settings

# Testing unallowed parameters
def test_qualitative_hcl_invalid_kwargs():
    pal1 = qualitative_hcl()

    not_allowed = []
    for p in _all_parameters:
        if not p in qualitative_hcl._allowed_parameters:
            not_allowed.append(p)

    for k in not_allowed:
        raises(ValueError, qualitative_hcl, **{k: 0.})

# Allowed are: "h1", "h2", "c1", "l1"
# Testing allowed parameters
def test_qualitative_hcl_allowed_kwargs_unnamed():
    # Test settings
    settings = {"h1": 11, "h2": 12, "c1": 13, "l1": 14}

    # Ensure I test all allowed parameters
    for k in qualitative_hcl._allowed_parameters:
        if not k in settings.keys():
            raise Exception(f"missing allowed parameter \"{k}\" in test settings")

    # Reference palette
    ref = qualitative_hcl(h = [settings["h1"], settings["h2"]],
                          c = settings["c1"],
                          l = settings["l1"])

    # Settings; will be tested one-by-one first
    for k,v in settings.items():
        args = {k: v}
        tmp  = qualitative_hcl(**args)
        assert ref.get(k) == tmp.get(k)

    # All together
    tmp = qualitative_hcl(**settings)
    for k in settings.keys():
        assert ref.get(k) == tmp.get(k)

# Using named palette (should be overwritten)
def test_qualitative_hcl_allowed_kwargs_named_nolambda():
    # Reference palette
    settings = {"h1": 270, "h2": 150, "c1": 50, "l1": 70}

    # As we overwrite all settings, it should not matter that the
    # first one starts with the settings of the Cold instead
    # of the default palette.
    pal1 = qualitative_hcl(**settings, palette = "Cold")
    pal2 = qualitative_hcl(**settings)

    for k in settings.keys():
        assert pal1.get(k) == pal2.get(k)

# Same as above, but going for a slithly more complex function,
# namely Set 3 which has a lambda function on 'h2' using two
# inputs (h1, n). When specifying h2.
def test_qualitative_hcl_allowed_kwargs_named_lambda():
    # Reference palette
    settings = {"h1": 0,
                "h2": lambda x,h1: 360. * (n - 1.) / n - h1,
                "c1": 50,
                "l1": 80}

    # As we overwrite all settings, it should not matter that the
    # first one starts with the settings of the Set 3 instead
    # of the default palette.
    pal1 = qualitative_hcl(**settings, palette = "Set 3")
    pal2 = qualitative_hcl(**settings)

    for k in settings.keys():
        assert pal1.get(k) == pal2.get(k)


# Handling of missing colors if fixup = FALSE
def test_qualitative_hcl_missing_colors_fixup():

    pal1 = qualitative_hcl("Dark 3").colors(7)
    pal2 = qualitative_hcl("Dark 3").colors(7, fixup = False)

    assert len(pal1) == len(pal2)
    assert pal2[1] is None
    assert pal2[2] is None
    assert pal2[3] is None
    assert pal2[4] is None

    assert np.all(pal2[5:] == pal1[5:])
    assert np.all(pal2[5:] == pal1[5:])


# Testing argument 'palette'
def test_qualitative_hcl_argument_palette():

    ref = hcl_palettes().get_palette("Warm").get_settings()
    
    # By name
    pal = qualitative_hcl("Warm")
    assert ref == pal.settings
    del pal
    
    # By name using palette argument
    pal = qualitative_hcl(palette = "Warm")
    assert ref == pal.settings
    del pal

# Testing argument 'h'
def test_qualitative_hcl_argument_h():

    # Testing h: single int
    settings = qualitative_hcl(h = [90, 270]).settings
    assert np.equal(settings["h1"], 90)
    assert np.equal(settings["h2"], 270)
    del settings


# Testing argument 'c'
def test_qualitative_hcl_argument_c():

    # Testing c: single numeric (linear to zero)
    settings = qualitative_hcl(c = 30.).settings
    assert np.equal(settings["c1"], 30)
    assert not "c2" in settings.keys() # no cmax
    assert not "cmax" in settings.keys() # no cmax
    del settings
    
    settings = qualitative_hcl(c = [30.]).settings
    assert np.equal(settings["c1"], 30)
    assert not "c2" in settings.keys() # no cmax
    assert not "cmax" in settings.keys() # no cmax
    del settings


# Testing argument 'l'
def test_qualitative_hcl_argument_l():

    # Testing c: single numeric (linear to zero)
    settings = qualitative_hcl(l = 10.).settings
    assert np.equal(settings["l1"], 10)
    assert not "l2" in settings.keys()
    del settings
    
    settings = qualitative_hcl(l = [10.]).settings
    assert np.equal(settings["l1"], 10)
    assert not "l2" in settings.keys()
    del settings


# Testing alpha handling
def test_sequential_hcl_argument_alpha():

    # First testing misuse
    pal = qualitative_hcl()
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

    # qualitative_hcl, 5 colors, no alpha
    x = qualitative_hcl().colors(5)
    R = ["#E16A86", "#AA9000", "#00AA5A", "#00A6CA", "#B675E0"]
    assert np.all(x == R)
    
    # qualitative_hcl, 5 colors, constant alpha = 0.3
    x = qualitative_hcl().colors(5, alpha = 0.3)
    R = ["#E16A864D", "#AA90004D", "#00AA5A4D", "#00A6CA4D", "#B675E04D"]
    assert np.all(x == R)
    
    # qualitative_hcl, 6 colors with alpha [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    x = qualitative_hcl().colors(6, alpha = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    R = ["#E16A8600", "#B88A0033", "#50A31566", "#00AD9A99", "#009ADECC", "#C86DD7"]
    assert np.all(x == R)


