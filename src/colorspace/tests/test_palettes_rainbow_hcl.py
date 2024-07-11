

import pytest
from pytest import raises
import numpy as np

import matplotlib.pyplot as plt
from colorspace import rainbow_hcl, hcl_palettes

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
        if isinstance(x, rainbow_hcl):
            return x.get(name)
        elif isinstance(x, defaultpalette):
            return x.get_settings()[name]
        elif isinstance(x, dict):
            return x[name]
        elif isinstance(x, (float, int)):
            return x
        else:
            raise TypeError(f"unknown type: {name} = {type(x)}")

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
def test_rainbow_hcl_defaults():
    expected_defaults = {"c1": 50, "l1": 70, "h1": 0,
                         "h2": lambda n: 360 * (n - 1) / n,
                         "fixup": True, "rev": False}
    pal = rainbow_hcl()
    for k in expected_defaults.keys():
        a,b = get_setting_values(pal, expected_defaults, k, n = 10)
        assert a == b

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_rainbow_hcl_wrong_usage_c():
    # Testing argument 'c'
    raises(ValueError, rainbow_hcl, c = "name of non-existing palette")
    raises(ValueError, rainbow_hcl, c = None) # None not allowed
    raises(ValueError, rainbow_hcl, c = {1, 2}) # invalid type
    raises(ValueError, rainbow_hcl, c = [1, 2, 3]) # length > 2
    raises(ValueError, rainbow_hcl, c = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, rainbow_hcl, c = np.asarray([])) # length < 1
    raises(ValueError, rainbow_hcl, c = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, rainbow_hcl, c = np.asarray([1, np.nan])) # nan not allowed

def test_rainbow_hcl_wrong_usage_l():
    # Testing argument 'l'
    raises(ValueError, rainbow_hcl, l = "foo") # not numeric
    raises(ValueError, rainbow_hcl, l = None) # None not allowed
    raises(ValueError, rainbow_hcl, l = {1, 2}) # invalid type
    raises(ValueError, rainbow_hcl, l = [1, 2, 3]) # length > 2
    raises(ValueError, rainbow_hcl, l = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, rainbow_hcl, l = np.asarray([])) # length < 1
    raises(ValueError, rainbow_hcl, l = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, rainbow_hcl, l = np.asarray([1, np.nan])) # nan not allowed

def test_rainbow_hcl_wrong_usage_start():
    # Testing argument 'start'
    raises(TypeError, rainbow_hcl, start = "foo") # not numeric
    raises(TypeError, rainbow_hcl, start = None) # None not allowed
    raises(TypeError, rainbow_hcl, start = {1, 2}) # invalid type
    raises(TypeError, rainbow_hcl, start = [1, 2, 3]) # length > 2
    raises(TypeError, rainbow_hcl, start = np.asarray([1, 2, 3])) # length > 2
    raises(TypeError, rainbow_hcl, start = np.asarray([])) # length < 1
    raises(TypeError, rainbow_hcl, start = np.asarray([np.nan])) # nan not allowed
    raises(TypeError, rainbow_hcl, start = np.asarray([1, np.nan])) # nan not allowed

def test_rainbow_hcl_wrong_usage_end():
    # Testing argument 'end'
    raises(TypeError, rainbow_hcl, end = "foo") # not numeric
    raises(TypeError, rainbow_hcl, end = None) # None not allowed
    raises(TypeError, rainbow_hcl, end = {1, 2}) # invalid type
    raises(TypeError, rainbow_hcl, end = [1, 2, 3]) # length > 2
    raises(TypeError, rainbow_hcl, end = np.asarray([1, 2, 3])) # length > 2
    raises(TypeError, rainbow_hcl, end = np.asarray([])) # length < 1
    raises(TypeError, rainbow_hcl, end = np.asarray([np.nan])) # nan not allowed
    raises(TypeError, rainbow_hcl, end = np.asarray([1, np.nan])) # nan not allowed

def test_rainbow_hcl_lambda_start_and_end():

    # Simply returning constant 50/100
    pal1 = rainbow_hcl(start = 50,           end = lambda n: 100)
    pal2 = rainbow_hcl(start = lambda n: 50, end = 100)
    pal3 = rainbow_hcl(start = lambda n: 50, end = lambda n: 100)

    assert isinstance(pal1.get("h1"), int)
    assert callable(pal1.get("h2"))
    assert pal1.get("h1") == 50
    assert pal1.get("h2")(1) == 100

    assert callable(pal2.get("h1"))
    assert isinstance(pal2.get("h2"), int)
    assert pal2.get("h1")(1) == 50
    assert pal2.get("h2") == 100

    assert callable(pal3.get("h1"))
    assert callable(pal3.get("h2"))
    assert pal3.get("h1")(1) == 50
    assert pal3.get("h2")(1) == 100

def test_rainbow_hcl_lambda_invalid():
    # lambda functions are only allowed to have one argument here.
    raises(Exception, rainbow_hcl, start = lambda: -999) # Not enouth args
    raises(Exception, rainbow_hcl, end   = lambda: -999) # Not enough args
    raises(Exception, rainbow_hcl, start = lambda a,b: -999) # Too many args
    raises(Exception, rainbow_hcl, end   = lambda a,b: -999) # Too many args

def test_rainbow_hcl_wrong_usage_fixup():
    # 'fixup' must be bool
    raises(TypeError, rainbow_hcl, fixup = None)

def test_rainbow_hcl_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, rainbow_hcl, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_rainbow_hcl_colors():

    pal = rainbow_hcl()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = rainbow_hcl()(5)
    col2 = rainbow_hcl().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = rainbow_hcl().colors(5, fixup = "foo")
    assert np.all(col1 == col3)

# Allowed are: "h1", "h2", "c1", "l1", "l2", "p1"
# Testing allowed parameters
def test_rainbow_hcl_allowed_kwargs_unnamed():
    # Test settings
    settings = {"h1": 11, "h2": 12, "c1": 13, "l1": 14}

    # Ensure I test all allowed parameters
    for k in rainbow_hcl._allowed_parameters:
        if not k in settings.keys():
            raise Exception(f"missing allowed parameter \"{k}\" in test settings")

    # Reference palette
    ref = rainbow_hcl(c1 = settings["c1"],
                      l1 = settings["l1"],
                      h1 = settings["h1"],
                      h2 = settings["h2"])

    # Settings; will be tested one-by-one first
    for k,v in settings.items():
        args = {k: v}
        tmp  = rainbow_hcl(**args)
        assert ref.get(k) == tmp.get(k)

    # All together
    tmp = rainbow_hcl(**settings)
    for k in settings.keys():
        assert ref.get(k) == tmp.get(k)

