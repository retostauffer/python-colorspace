

import pytest
from pytest import raises
import numpy as np
from colorspace import rainbow, hcl_palettes

# All parameters
_all_parameters = ["foo", "s", "v", "start", "end"]

# ---------------------------------------------
# Helper function to compare settings. Some allow
# to be lambda functions; this function tries to
# take care of comparing the return of these
# functions properly.
# ---------------------------------------------
def get_setting_values(a, b, name, n = 10):
    from colorspace.palettes import defaultpalette

    def get_entry(x, name):
        if isinstance(x, rainbow):
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
def test_rainbow_defaults():
    expected_defaults = {"s": 1, "v": 1,
            "start": 0, "end": lambda n: max(1., n - 1.) / n,
            "rev": False}
    pal = rainbow()
    for k in expected_defaults.keys():
        a,b = get_setting_values(pal, expected_defaults, k, n = 10)
        assert a == b

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_rainbow_wrong_usage_s():
    # Testing argument 's'
    raises(TypeError, rainbow, s = "name of non-existing palette")
    raises(TypeError, rainbow, s = None) # None not allowed
    raises(TypeError, rainbow, s = {1, 2}) # invalid type
    raises(TypeError, rainbow, s = [1]) # invalid type

    raises(ValueError, rainbow, s = -0.00001) # invalid value
    raises(ValueError, rainbow, s = +1.00001) # invalid value

def test_rainbow_wrong_usage_v():
    # Testing argument 'v'
    raises(TypeError, rainbow, v = "name of non-existing palette")
    raises(TypeError, rainbow, v = None) # None not allowed
    raises(TypeError, rainbow, v = {1, 2}) # invalid type
    raises(TypeError, rainbow, v = [1]) # invalid type

    raises(ValueError, rainbow, v = -0.00001) # invalid value
    raises(ValueError, rainbow, v = +1.00001) # invalid value

def test_rainbow_wrong_usage_start():
    # Testing argument 'start'
    raises(TypeError, rainbow, start = "foo") # not numeric
    raises(TypeError, rainbow, start = None) # None not allowed
    raises(TypeError, rainbow, start = {1}) # invalid type
    raises(TypeError, rainbow, start = [1]) # length > 2

def test_rainbow_wrong_usage_end():
    # Testing argument 'end'
    raises(TypeError, rainbow, end = "foo") # not numeric
    raises(TypeError, rainbow, end = None) # None not allowed
    raises(TypeError, rainbow, end = {1}) # invalid type
    raises(TypeError, rainbow, end = [1]) # length > 2

def test_rainbow_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, rainbow, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_rainbow_colors():

    pal = rainbow()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = rainbow()(5)
    col2 = rainbow().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = rainbow().colors(5, fixup = "foo")
    assert np.all(col1 == col3)

