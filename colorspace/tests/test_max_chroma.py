
from colorspace.utils import max_chroma
import numpy as np
from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():
    raises(TypeError, max_chroma, H = "foo", L = 10)          # H wrong type
    raises(TypeError, max_chroma, H = 10,    L = "foo")       # L wrong type
    raises(TypeError, max_chroma, H = 10, L = 10, floor = 10) # float not boolean
    raises(TypeError, max_chroma, H = 10, L = 10, fooo = "bar") # non-existing argument

def test_correct_usage():

    # Two single values (float/integer)
    x1 = max_chroma(H = 10,  L = 10., floor = False)
    x2 = max_chroma(H = 10., L = 10,  floor = False)

    # Testing default
    x3 = max_chroma(H = 10,  L = 10.)
    x4 = max_chroma(H = 10., L = 10)
    x5 = max_chroma(10., 10)

    x6 = max_chroma(H = np.asarray(10), L = 10)
    x7 = max_chroma(H = 10., L = np.asarray(10))

    # All 4 calls above do the very same; check result
    assert x1 == 33.66
    for x in [x2, x3, x4, x5, x6, x7]: assert x1 == x


# -------------------------------------------------------------------
# Testing different combinations of allowed input types and lengths.
# -------------------------------------------------------------------
def test_input_length():

    # Above we have seen what happens if both inputs for H and L
    # are of the same length. The function also allows for two
    # lists/numpy arrays of the same length or mixed length - if
    # one of the two has length 1.
    x1 = max_chroma([10, 180], [10, 99])
    assert isinstance(x1, np.ndarray)
    assert len(x1) == 2
    assert np.all(x1 == np.asarray([33.66, 8.42]))

    x2 = max_chroma([10, 180], [10, 10])
    x3 = max_chroma([10, 180], 10)
    x4 = max_chroma(np.asarray([10, 180], dtype = "int"), 10.)
    assert np.all(x2 == x3)
    assert np.all(x2 == x4)

    x5 = max_chroma([10], [40, 10])
    x6 = max_chroma(10,   [40, 10])
    x7 = max_chroma(10.,  np.asarray([40, 10], dtype = "float"))
    assert np.all(x5 == x6)
    assert np.all(x5 == x7)

    # In case H and L are both > 1 and do not match we expect an error
    raises(ValueError, max_chroma, H = [1, 2, 3], L = [10, 20])
















