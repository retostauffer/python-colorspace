
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


#natural_cubic_splines(x, y, xout)
def test_spline_wrong_usage():
    import numpy as np
    from colorspace.statshelper import natural_cubic_spline as ncs
    raises(TypeError, ncs) # No input args

    # Creating correct inputs
    x    = np.asarray([1, 2, 3, 5.5, 6.5])
    y    = np.asarray([6.5, 5.5, 5., 8.5, 9.5])
    xout = np.asarray([-1, 0, 1, 2, 3, 4, 5, 6, 7])

    raises(TypeError, ncs, x = x, y = y, xout = "foo")
    raises(TypeError, ncs, x = x, y = "foo", xout = xout)
    raises(TypeError, ncs, x = "foo", y = y, xout = xout)
    raises(TypeError, ncs, x = 1, y = 2, xout = 3)

    # Empty array on x or xout
    raises(ValueError, ncs, x = np.asarray([]), y = y, xout = xout)
    raises(ValueError, ncs, x = x, y = y, xout = np.asarray([]))

    # Length of x and y mismatch
    raises(ValueError, ncs, x = x[:-1], y = y, xout = xout)

    # Using non-numeric vectors for x, y
    tmp = np.asarray(["A", "B", "C", "D", "E"]) # Same length as x
    raises(TypeError, ncs, x = tmp, y = y, xout = xout)
    raises(TypeError, ncs, x = x, y = tmp, xout = xout)
    raises(TypeError, ncs, x = x, y = y,   xout = tmp)

def test_spline_return():
    import numpy as np
    from colorspace.statshelper import natural_cubic_spline as ncs

    # Creating correct inputs
    x    = np.asarray([1, 2, 3, 5.5, 6.5])
    y    = np.asarray([6.5, 5.5, 5., 8.5, 9.5])
    xout = np.asarray([-1, 0, 1, 2, 3, 4, 5, 6, 7])

    # Predicting on the original data (xout = x)
    res = ncs(x = x, y = y, xout = x)
    assert isinstance(res, dict)
    assert len(res) == 2
    assert "x" in res.keys() and "y" in res.keys()
    assert all(res["x"] == x)
    assert all(res["y"] == y)

    # Unnamed
    res2 = ncs(x, y, x)
    assert all(res["x"] == res2["x"])
    assert all(res["y"] == res2["y"])
    del res, res2

    # Predicting on new x (xout = xout)
    res = ncs(x, y, xout)

    # Testing against the return from R (spline(x, y, xout = xout, method = 'natural'))
    # using the same data as above.
    er = [8.586280, 7.543140, 6.500000, 5.500000,
          5.000000, 5.979726, 7.720427, 9.065282, 9.912957]
    assert all(np.abs(res["y"] - er) < 1e-5)
    del res

    # If x/y are of length one, the estimate for yout should always
    # be equal to y for each element of xout.
    xout = np.arange(-1, 5)
    res = ncs(x = np.ones(1), y = np.asarray([5.5]), xout = xout)
    assert np.array_equal(res["x"], xout)
    assert np.array_equal(res["y"], np.repeat(5.5, len(xout)))



# lm(y, X, Xout)
def test_lm_wrong_usage():
    from colorspace.statshelper import lm
    import numpy as np

    y = np.asarray([4.17, 5.58, 5.18, 6.11, 4.50, 4.61, 5.17, 4.53, 5.33, 5.14])
    X = np.transpose([np.repeat(1, len(y)), np.repeat([0, 1], 5)])
    Xout = np.transpose([np.repeat(1, 4), np.repeat([1, 0], 2)])

    # Testing wrong inputs, uses the test data above
    raises(TypeError, lm, y = [1, 2, 3], X = X, Xout = Xout) # y not ndarray
    raises(TypeError, lm, y = y, X = [1, 2, 3], Xout = Xout) # X not ndarray
    raises(TypeError, lm, y = y, X = X, Xout = [1, 2, 3]) # Xout not ndarray

    # X or Xout not two dimensional
    raises(ValueError, lm, y = y, X = X[:,1], Xout = Xout)
    raises(ValueError, lm, y = y, X = X, Xout = Xout[:,1])
    # Second dimension of X and Xout mismatch
    raises(ValueError, lm, y = y, X = X, Xout = np.concatenate([Xout, Xout], axis = 1))
    # length of y does not match first dimension of X
    raises(ValueError, lm, y = y[:-1], X = X, Xout = Xout)

def test_lm_return():
    from colorspace.statshelper import lm
    import numpy as np

    # Example from Rs stats::lm man page + additional linear effect.
    # Annette Dobson (1990) "An Introduction to Generalized Linear Models". 
    # Page 9: Plant Weight Data. 
    weight = np.asarray([4.17, 5.58, 5.18, 6.11, 4.50, 4.61, 5.17, 4.53, 5.33, 5.14,
                         4.81, 4.17, 4.41, 3.59, 5.87, 3.83, 6.03, 4.89, 4.32, 4.69])
    
    # Dummy variable for 'Treatment group' 
    trt = np.repeat([0., 1.], 10)
    
    # Alternating +/-0.1 'noise'
    rand = np.repeat(-0.1, 20)
    rand[::2] = +0.1
    rand   = weight / 2 + rand
    
    # Create model matrix
    from colorspace.statshelper import lm
    X = np.transpose([np.repeat(1., 20), rand, trt])        
    mod = lm(y = weight, X = X, Xout = X)

    # Testing return
    assert isinstance(mod, dict)
    assert len(mod) == 3
    assert "coef" in mod.keys()
    assert "sigma" in mod.keys()
    assert "Yout" in mod.keys()
    assert len(mod["Yout"]) == len(weight)

    # Coefficients from R
    cr = [0.63201454,  1.74880185, -0.04659726]
    assert all(np.abs(mod["coef"] - np.asarray(cr)) < 1e-6)

    # Standard error from R
    assert np.abs(mod["sigma"] - 0.1929574) < 1e-6
    
    # Fitted values from R (prediction)
    pr = [4.453147, 5.336292, 5.336292, 5.799724, 4.741699, 4.488123, 5.327548, 4.418171, 
          5.467452, 4.951555, 4.966166, 4.056789, 4.616406, 3.549636, 5.893031, 3.759493, 
          6.032935, 4.686358, 4.537709, 4.511477 ]
    assert all(mod["Yout"] - np.asarray(pr) < 1e-6)

    
def test_split_wrong_usage():
    from colorspace.statshelper import split
    import numpy as np

    # Both inputs must be numpy.ndarrays
    raises(TypeError, split, x = 1, y = np.ones(3))
    raises(TypeError, split, x = np.ones(3), y = 1)

    # If x is of length 0 (must be at least 1) or if lengths differ
    raises(ValueError, split, x = np.asarray([]), y = np.ones(3))
    raises(ValueError, split, x = np.ones(5), y = np.ones(4))

def test_split_return():
    from colorspace.statshelper import split
    import numpy as np

    # If 'x' is of length 1 a list [x] is returned
    x = np.asarray([3])
    y = np.asarray([True])
    res = split(x, y)
    assert isinstance(res, list)
    assert len(res) == 1
    assert np.array_equal(res[0], x)
    del res, x, y

    # x is [1, 2, 3, 4], y [True, True, False, False], so the
    # return should be [[1, 2], [3, 4]]
    x = np.arange(1, 5, 1, dtype = np.int16)
    y = np.repeat([True, False], 2)
    # Named and unnamed arguments to test order
    res1 = split(x, y)
    res2 = split(x = x, y = y)
    assert isinstance(res1, list)
    assert len(res1) == 2
    assert np.array_equal(res1[0], np.arange(1, 3, 1, dtype = np.int16))
    assert np.array_equal(res1[1], np.arange(3, 5, 1, dtype = np.int16))
    del res1, res2, x, y

    # x is ['A','B','C','D'] which we also use as y, so the value changes
    # every time and it should be split up into [['A'], ['B'], ['C'], ['D']]
    x = np.asarray(["A", "B", "C", "D"])
    res = split(x, x)
    assert isinstance(res, list)
    assert len(res) == 4
    for i in range(4):
        assert x[i] == res[i][0]


##if __name__ == "__main__":
##    # nprange
##    test_nprange_wrong_usage()
##    test_nprange_wrong_ndarray()
##    test_nprange_return()
##
##    # natural cubic spline
##    test_spline_wrong_usage()
##    test_spline_return()
##
##    # linear regression
##    test_lm_wrong_usage()
##    test_lm_return()
##
##    # split
##    test_split_wrong_usage()
##    test_split_return()





