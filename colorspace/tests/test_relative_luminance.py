
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

    # Input object(s) wrong
    raises(TypeError,  relative_luminance, cols = "#FFFFFF")
    raises(TypeError,  relative_luminance, cols = palette(["#FF0000", "#00FF00"], "test"))


def test_return_values():

    cols = hexcols(["#FF0000", "#FFBF00", "#80FF00", "#00FF40",
                    "#00FFFF", "#0040FF", "#8000FF", "#FF00BF"])

    # Testing proper usage
    res1 = relative_luminance(cols)
    res2 = relative_luminance(cols = cols)

    # What R gives us
    sol  = np.asarray([0.2126000, 0.5852160, 0.7610919, 0.7189017,
                       0.7874000, 0.1088679, 0.1180919, 0.2502159])

    assert isinstance(res1, np.ndarray)
    assert isinstance(res2, np.ndarray)
    assert np.all(res1 == res2)
    assert np.all(np.isclose(res1, sol))



