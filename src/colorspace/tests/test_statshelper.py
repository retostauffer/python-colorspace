
from colorspace import *
from pytest import raises
import numpy as np


def test_nprange_wrong_usage():
    from colorspace.statshelper import nprange
    raises(TypeError, nprange) # Missing argument
    raises(TypeError, nprange, y = np.repeat(1, 3)) # Wrong name
    raises(TypeError, nprange, x = 1.0) # fnot ndarray
    raises(TypeError, nprange, x = 1) # int, not ndarray
    raises(TypeError, nprange, x = [1, 2, 3]) # list, not ndarray

def test_nprange_wrong_ndarray():
    from colorspace.statshelper import nprange
    raises(TypeError,  nprange, np.repeat("foo", 3)) # Unicode 
    raises(ValueError, nprange, np.repeat(1.0, 0)) # Empty
    raises(ValueError, nprange, np.ones((2, 2))) # 2x2 array of ones

def test_nprange_return():
    from colorspace.statshelper import nprange
    x = nprange(np.asarray([1, 2, 3, 4]))
    assert all(np.isclose(x, [1, 4]))
    x = nprange(np.asarray([-10.5, 0, 10.5]))
    assert all(np.isclose(x, [-10.5, 10.5]))
    x = nprange(np.asarray([1234567.8]))
    assert all(np.isclose(x, np.repeat(1234567.8, 2)))


if __name__ == "__main__":
    # nprange
    test_nprange_wrong_usage()
    test_nprange_wrong_ndarray()
    test_nprange_return()

    # standard deviation with N - 1
