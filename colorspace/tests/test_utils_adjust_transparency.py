
from colorspace import *
from colorspace.colorlib import hexcols
import numpy as np

from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    # Input missing
    raises(TypeError,  adjust_transparency)

    # Too many inputs
    x = hexcols("#ff0033")
    raises(TypeError,  adjust_transparency, x, x, x)

    # Wrong inputs
    raises(TypeError,  adjust_transparency, colors = x, alpha = None)

    # Wrong input type. Testing some generic
    # types first and then colorspace objects which not yet work
    # but may be added in the future.
    raises(TypeError,  adjust_transparency, x = "foo", alpha = None)
    raises(TypeError,  adjust_transparency, x = 3,     alpha = None)
    raises(TypeError,  adjust_transparency, x = None,  alpha = None)

    # hclpalette object
    raises(TypeError,  adjust_transparency, x = diverging_hcl(), alpha = None)
    # A custom palette
    raises(TypeError,  adjust_transparency, x = palette(diverging_hcl().colors(3)), alpha = None)

    # Wrong arguments on alpha
    raises(TypeError,  adjust_transparency, x = x, alpha = "foo")
    raises(TypeError,  adjust_transparency, x = x, alpha = {"foo": None})
    raises(TypeError,  adjust_transparency, x = x, alpha = {"foo": None})

# ------------------------------------------
# Invalid values for alpha
# ------------------------------------------
def test_invalid_alpha_values():

    x = hexcols(['#023FA5CC', '#E2E2E266', '#8E063BCC'])

    # Constant alpha but below 0
    raises(ValueError, adjust_transparency, x = x, alpha = -0.0000001)
    # Constant alpha but above 1
    raises(ValueError, adjust_transparency, x = x, alpha =  1.0000001)
    # Constant alpha, integer, below 0 and above 1
    raises(ValueError, adjust_transparency, x = x, alpha = -1)
    raises(ValueError, adjust_transparency, x = x, alpha = +2)

    # Our object 'x' is of length 3. Thus if we provide alist
    # we also have to provide 3 values in our list which all
    # need to be able to be converted to floating point numbers
    # in the range of [0., 1.]. Let's test this ...
    raises(ValueError, adjust_transparency, x = x, alpha = [0.8, 0.4])            # Not enough
    raises(ValueError, adjust_transparency, x = x, alpha = [0.8, 0.4, 0.4, 0.8])  # Too many
    raises(ValueError, adjust_transparency, x = x, alpha = [0.8, "foo", 0.8])     # Not float
    raises(ValueError, adjust_transparency, x = x, alpha = [-0.0001, 0.4, 0.8])   # Below 0
    raises(ValueError, adjust_transparency, x = x, alpha = [1.00001, 0.4, 0.8])   # Above 1

    # Same yields for inputs of type np.ndarray
    raises(ValueError, adjust_transparency, x = x, alpha = np.asarray([0.8, 0.4]))            # Not enough
    raises(ValueError, adjust_transparency, x = x, alpha = np.asarray([0.8, 0.4, 0.4, 0.8]))  # Too many
    raises(ValueError, adjust_transparency, x = x, alpha = np.asarray([0.8, "foo", 0.8]))     # Not float
    raises(ValueError, adjust_transparency, x = x, alpha = np.asarray([-0.0001, 0.4, 0.8]))   # Below 0
    raises(ValueError, adjust_transparency, x = x, alpha = np.asarray([1.00001, 0.4, 0.8]))   # Above 1


# ------------------------------------------
# Invalid values for alpha
# ------------------------------------------
def test_remove_transparency():

    x   = hexcols(['#023FA5CC', '#E2E2E266', '#8E063BCC'])
    res = adjust_transparency(x, None)

    assert isinstance(extract_transparency(x), np.ndarray)
    assert len(extract_transparency(x)) == 3
    assert isinstance(extract_transparency(res), type(None))
    assert res.get("alpha") is None

# ------------------------------------------
# Add constant transparency
# ------------------------------------------
def test_add_constant_transparency():

    x   = hexcols(['#023FA5', '#E2E2E2', '#8E063B']) # No transparency

    x2  = adjust_transparency(x, 0.5)
    res = extract_transparency(x2)

    assert isinstance(extract_transparency(x), type(None))
    assert isinstance(res, np.ndarray)
    assert len(res) == 3
    assert np.all(np.isclose(res, 0.5))
    del x2, res

    x2  = adjust_transparency(x, int(1))
    res = extract_transparency(x2)

    assert isinstance(extract_transparency(x), type(None))
    assert isinstance(res, np.ndarray)
    assert len(res) == 3
    assert np.all(np.isclose(res, 1.0))
    del x2, res

# ------------------------------------------
# Overwrite transparency with constant
# ------------------------------------------
def test_overwrite_with_constant_transparency():

    x   = hexcols(['#023FA5CC', '#E2E2E266', '#8E063BCC'])
    x2  = adjust_transparency(x, 0.5)
    res = extract_transparency(x2)

    assert isinstance(extract_transparency(x), np.ndarray)
    assert isinstance(res, np.ndarray)
    assert len(res) == 3
    assert np.all(np.isclose(res, 0.5))
    del x2, res


# ------------------------------------------
# Change transparency
# ------------------------------------------
def test_change_transparency():

    x   = hexcols(['#023FA5CC', '#E2E2E266', '#8E063BCC'])
    x2  = adjust_transparency(x, [0.4, 0.8, 0.4]) # With list
    x3  = adjust_transparency(x, np.asarray([0.4, 0.8, 0.4])) # With array

    assert np.all(np.isclose(extract_transparency(x),  [0.8, 0.4, 0.8]))
    assert np.all(np.isclose(extract_transparency(x2), [0.4, 0.8, 0.4]))
    assert np.all(np.isclose(extract_transparency(x3), [0.4, 0.8, 0.4]))







































