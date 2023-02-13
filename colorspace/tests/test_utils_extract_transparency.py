
from colorspace import *
from colorspace.colorlib import hexcols
import numpy as np

from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    # Input missing
    raises(TypeError,  extract_transparency)

    # Too many inputs
    x = hexcols("#ff0033")
    raises(TypeError,  extract_transparency, x, x, x)

    # Wrong input on 'mode'
    raises(TypeError,  extract_transparency, x = x, mode = 12345) # no string
    raises(ValueError, extract_transparency, x = x, mode = "foo") # does not exist

    # Wrong input type. Testing some generic
    # types first and then colorspace objects which not yet work
    # but may be added in the future.
    raises(TypeError,  extract_transparency, x = "foo")
    raises(TypeError,  extract_transparency, x = 3)
    raises(TypeError,  extract_transparency, x = None)

    # hclpalette object
    raises(TypeError,  extract_transparency, x = diverging_hcl())


# ------------------------------------------
# Default extraction
# ------------------------------------------
def test_extract_transparency():

    # Three colors without alpha
    x1 = hexcols(['#023FA5',   '#E2E2E2',   '#8E063B'])
    # Same colors with transparency 80%, 40%, 80%
    x2 = hexcols(['#023FA5CC', '#E2E2E266', '#8E063BCC'])

    # Convert hex color lists to colorobjects
    assert isinstance(x1, hexcols)
    assert len(x1) == 3
    res1 = extract_transparency(x1)
    assert isinstance(res1, type(None))

    # Convert hex color lists to colorobjects
    assert isinstance(x2, hexcols)
    assert len(x2) == 3
    res2 = extract_transparency(x2)
    assert isinstance(res2, np.ndarray)
    assert np.all(np.isclose(res2, [.8, .4, .8]))

    # Testing custom palettes
    res3 = extract_transparency(palette(x1, name = "custom palette"))
    assert isinstance(res3, type(None))

    # Convert hex color lists to colorobjects
    res4 = extract_transparency(palette(x2, name = "custom palette"))
    assert isinstance(res4, np.ndarray)
    assert np.all(np.isclose(res4, [.8, .4, .8]))


# ------------------------------------------
# Testing the different return modes
# ------------------------------------------
def test_extract_transparency_modes():

    # Three colors without alpha
    x1 = hexcols(['#023FA5',   '#E2E2E2',   '#8E063B'])
    # Same colors with transparency 80%, 40%, 80%
    x2 = hexcols(['#023FA5CC', '#E2E2E266', '#8E063BCC'])

    # Convert hex color lists to colorobjects
    assert extract_transparency(x1, mode = "float") is None
    assert extract_transparency(x1, mode = "int")   is None
    assert extract_transparency(x1, mode = "str")   is None

    assert np.all(np.isclose(extract_transparency(x2, mode = "float"), [0.8, 0.4, 0.8]))
    assert np.all(np.isclose(extract_transparency(x2, mode = "int"), [0.8 * 255, 0.4 * 255, 0.8 * 255]))
    assert np.all(extract_transparency(x2, mode = "str") == ["CC", "66", "CC"])









