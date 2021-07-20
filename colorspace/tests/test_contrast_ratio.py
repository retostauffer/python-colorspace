
from colorspace.colorlib import hexcols
from colorspace import palette, contrast_ratio
import numpy as np

from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    # Input missing
    raises(TypeError,  contrast_ratio)

    # Argument 'cols'
    raises(TypeError,  contrast_ratio, cols = 1) # integer
    raises(ValueError, contrast_ratio, cols = "foo")                # no hex color
    raises(ValueError, contrast_ratio, cols = ["#FF00FF", "foo"])   # invalid hex

    # Argument 'bg'
    raises(TypeError,  contrast_ratio, cols = "#FF00FF", b = "foo") # no hex color
    raises(TypeError,  contrast_ratio, cols = "#FF00FF", b = ["#FF00FF", "foo"]) # invalid hex

    # Argument 'plot'
    raises(TypeError,  contrast_ratio, cols = "#FF00FF", plot = "foo")



# ------------------------------------------
# Checking return values.
# ------------------------------------------
def test_result():

    # Checking against black
    cols = hexcols(["#FF0000", "#FFBF00", "#80FF00", "#00FF40",
                    "#00FFFF", "#0040FF", "#8000FF", "#FF00BF"])

    # Testing proper usage
    res_white1 = contrast_ratio(cols)
    res_white2 = contrast_ratio(cols, "#FFFFFF")
    sol_white  = np.asarray([3.998477, 1.652981, 1.294551, 1.365584,
                             1.253881, 6.609264, 6.246581, 3.497483])

    assert isinstance(res_white1, np.ndarray)
    assert isinstance(res_white2, np.ndarray)
    assert np.all(res_white1 == res_white2)
    assert np.all(np.isclose(res_white1, sol_white))

    res_bw = contrast_ratio(cols, ["#FFFFFF", "#000000"])
    sol_bw = np.asarray([3.998477, 12.704321, 1.294551, 15.378033,
                         1.253881,  3.177358, 6.246581, 6.004318])

    res_bw = contrast_ratio(cols, ["#FFFFFF", "#000000"], plot = True)
    assert isinstance(res_bw, np.ndarray)
    assert np.all(np.isclose(res_bw, sol_bw))


