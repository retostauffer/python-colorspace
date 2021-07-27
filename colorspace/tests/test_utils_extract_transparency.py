
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
    raises(TypeError,  extract_transparency, x, x)

    # Wrong input type. Testing some generic
    # types first and then colorspace objects which not yet work
    # but may be added in the future.
    raises(TypeError,  extract_transparency, x = "foo")
    raises(TypeError,  extract_transparency, x = 3)
    raises(TypeError,  extract_transparency, x = None)

    # hclpalette object
    raises(TypeError,  extract_transparency, x = diverging_hcl())
    # A custom palette
    raises(TypeError,  extract_transparency, x = palette(diverging_hcl().colors(3)))


# ------------------------------------------
# Wrong usage
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










