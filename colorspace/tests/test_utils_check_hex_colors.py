
from colorspace import check_hex_colors
import numpy as np

from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    # Input missing
    raises(TypeError,  check_hex_colors)

    # Input object(s) wrong
    raises(TypeError,  check_hex_colors, 1)
    raises(TypeError,  check_hex_colors, {"#ff0033", "#ff00ff"})
    raises(ValueError, check_hex_colors, [1, 2, 3])
    raises(ValueError, check_hex_colors, [1, 2, "foo"])

    # Non-boolean for allow_nan
    raises(TypeError,  check_hex_colors, "#ff0033", "foo")

    # Wrong hex color
    raises(ValueError, check_hex_colors, "#ff")
    raises(ValueError, check_hex_colors, "#ff00")
    raises(ValueError, check_hex_colors, "#ff00ADFASFD")
    raises(ValueError, check_hex_colors, "FF0")
    raises(ValueError, check_hex_colors, "FFFF00")


def test_return_value():

    x1 = check_hex_colors("#FF0")          # three digit hex
    x2 = check_hex_colors("#FFFF00")       # six digit hex
    x3 = check_hex_colors("#FFFF0033")     # eight digit hex

    assert isinstance(x1, list)
    assert isinstance(x2, list)
    assert isinstance(x3, list)

    assert len(x1) == len(x2) == len(x3) == 1
    assert len(x1[0]) == len(x2[0]) == 7
    assert len(x3[0]) == 9

    assert x1[0] == x2[0]                       # FF0 extended to FFFF00?
    assert x1[0] == x3[0][0:7]                  # Remove alpha - same right?


    x4 = check_hex_colors(["#000", "#F00", "#00FF00", "#0000FF"])

    assert isinstance(x4, list)
    assert len(x4) == 4
    assert np.all([len(x) == 7 for x in x4])





