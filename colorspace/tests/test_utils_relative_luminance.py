
from colorspace.utils import relative_luminance
from colorspace.colorlib import hexcols
from colorspace import palette
import numpy as np

from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    # Input missing
    raises(TypeError,  relative_luminance)

    # Too many inputs
    raises(TypeError,  relative_luminance, 1, 2)

    # Input object(s) wrong
    raises(TypeError,  relative_luminance, colors = 1234)
    raises(TypeError,  relative_luminance, colors = {"#FFFFFF", "#000000"})


def test_return_values():

    colors = hexcols(["#FF0000", "#FFBF00", "#80FF00", "#00FF40",
                    "#00FFFF", "#0040FF", "#8000FF", "#FF00BF"])

    # Testing proper usage
    res1 = relative_luminance(colors)
    res2 = relative_luminance(colors = colors)

    # What R gives us
    sol  = np.asarray([0.2126000, 0.5852160, 0.7610919, 0.7189017,
                       0.7874000, 0.1088679, 0.1180919, 0.2502159])

    assert isinstance(res1, np.ndarray)
    assert isinstance(res2, np.ndarray)
    assert np.all(res1 == res2)
    assert np.all(np.isclose(res1, sol))

# ------------------------------------------
# Test that all different input types work.
# ------------------------------------------
def test_input_types():

    colors_str         = "#FF0000"
    colors_list        = ["#FF0000", "#FFBF00", "#80FF00", "#00FF40",
                          "#00FFFF", "#0040FF", "#8000FF", "#FF00BF"]
    colors_palette     = palette(colors_list)
    colors_object      = hexcols(colors_list)

    # Now calling relative_luminance, compare outputs
    x1 = relative_luminance(colors_str)
    assert isinstance(x1, np.ndarray)
    assert len(x1) == 1

    x2 = relative_luminance(colors_list)
    x3 = relative_luminance(colors_palette)
    x4 = relative_luminance(colors_object)

    assert isinstance(x2, np.ndarray)
    assert isinstance(x3, np.ndarray)
    assert isinstance(x4, np.ndarray)
    assert len(x2) == len(x3) == len(x4) == len(colors_list)












