

import pytest
from pytest import raises
import numpy as np

from colorspace import diverging_hsv, hcl_palettes

# All parameters
_all_parameters = ["foo", "h1", "h2", "c1", "c2", "l1", "l2", "s", "v", "p1", "p2", "power"]

# ---------------------------------------------
# Default settings
# ---------------------------------------------
def test_diverging_hsv_defaults():
    expected_defaults = {"h1": 240, "h2": 0, "s": 1, "v": 1,
                         "power": 1, "fixup": True, "rev": False}
    pal = diverging_hsv()
    for k,v in expected_defaults.items():
        assert pal.get(k) == v

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_diverging_hsv_wrong_usage_h():
    # Testing argument 'h'
    raises(ValueError, diverging_hsv, h = "name of non-existing palette")
    raises(ValueError, diverging_hsv, h = None) # None not allowed
    raises(ValueError, diverging_hsv, h = {1, 2}) # invalid type
    raises(ValueError, diverging_hsv, h = [1, 2, 3]) # length > 2
    raises(ValueError, diverging_hsv, h = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, diverging_hsv, h = np.asarray([])) # length < 1
    raises(ValueError, diverging_hsv, h = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, diverging_hsv, h = np.asarray([1, np.nan])) # nan not allowed

def test_diverging_hsv_wrong_usage_s():
    # Testing argument 's'
    raises(TypeError, diverging_hsv, s = "name of non-existing palette")
    raises(TypeError, diverging_hsv, s = None) # None not allowed
    raises(TypeError, diverging_hsv, s = {1, 2}) # invalid type
    raises(TypeError, diverging_hsv, s = [1]) # invalid type

    raises(ValueError, diverging_hsv, s = -0.00001) # invalid value
    raises(ValueError, diverging_hsv, s = +1.00001) # invalid value

def test_diverging_hsv_wrong_usage_v():
    # Testing argument 'v'
    raises(TypeError, diverging_hsv, v = "name of non-existing palette")
    raises(TypeError, diverging_hsv, v = None) # None not allowed
    raises(TypeError, diverging_hsv, v = {1, 2}) # invalid type
    raises(TypeError, diverging_hsv, v = [1]) # invalid type

    raises(ValueError, diverging_hsv, v = -0.00001) # invalid value
    raises(ValueError, diverging_hsv, v = +1.00001) # invalid value

def test_diverging_hsv_wrong_usage_power():
    # Testing argument 'power'
    raises(ValueError, diverging_hsv, power = "foo") # not numeric
    raises(ValueError, diverging_hsv, power = None) # None not allowed
    raises(ValueError, diverging_hsv, power = {1, 2}) # invalid type
    raises(ValueError, diverging_hsv, power = [1, 2]) # length > 1
    raises(ValueError, diverging_hsv, power = np.asarray([1, 2])) # length > 1
    raises(ValueError, diverging_hsv, power = np.asarray([])) # length < 1
    raises(ValueError, diverging_hsv, power = np.asarray([np.nan])) # nan not allowed

def test_diverging_hsv_wrong_usage_fixup():
    # 'fixup' must be bool
    raises(TypeError, diverging_hsv, fixup = None)

def test_diverging_hsv_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, diverging_hsv, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_diverging_hsv_colors():

    pal = diverging_hsv()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = diverging_hsv()(5)
    col2 = diverging_hsv().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = diverging_hsv().colors(5, fixup = "foo")
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


# Testing alpha handling
def test_diverging_hsv_argument_alpha():

    # First testing misuse
    pal = diverging_hsv()
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

    # diverging_hsv, 5 colors, no alpha
    x = diverging_hsv().colors(5) 
    R = ["#0000FF", "#BCBCFF", "#FFFFFF", "#FFBCBC", "#FF0000"]
    assert np.all(x == R)
    
    # diverging_hsv, 5 colors, constant alpha = 0.3
    x = diverging_hsv().colors(5, alpha = 0.3) 
    R = ["#0000FF4D", "#BCBCFF4D", "#FFFFFF4D", "#FFBCBC4D", "#FF00004D"]
    assert np.all(x == R)
    
    # diverging_hsv, 6 colors with alpha [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    x = diverging_hsv().colors(6, alpha = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    R = ["#0000FF00", "#AAAAFF33", "#E7E7FF66", "#FFE7E799", "#FFAAAACC", "#FF0000"] 
    assert np.all(x == R)


