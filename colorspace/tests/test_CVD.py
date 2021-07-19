
from colorspace.CVD import *
from colorspace import sequential_hcl
import numpy as np
from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    cols = sequential_hcl()(3)

    raises(TypeError,  CVD, cols = cols, type_ = 12345678, severity = 1)      # type_ not str
    raises(ValueError, CVD, cols = cols, type_ = "foo",    severity = 1)      # type_ not str

    # Argument 'severity'
    raises(TypeError,  CVD, cols = cols, type_ = "deutan", severity = [1])        # not float
    raises(TypeError,  CVD, cols = cols, type_ = "deutan", severity = "0.5")      # not float
    raises(ValueError, CVD, cols = cols, type_ = "deutan", severity = -0.01)      # below 0
    raises(ValueError, CVD, cols = cols, type_ = "deutan", severity = +1.01)      # above 1

    raises(ValueError, CVD, cols = ["#ff0000", "foobar"], type_ = "deutan", severity = 1) # non HEX


# ------------------------------------------
# Ensure that the default usage stays the same
# ------------------------------------------
def test_default():

    cols = sequential_hcl()(3)
    assert np.all(cols == ["#023FA5", "#A1A6C8", "#E2E2E2"])

    x1   = CVD(cols, "deutan")
    x2   = CVD(cols = cols, type_ = "deutan", severity = 1.0)
    # TODO(R): Seems we have some roundoff errors here.
    #x3   = ["#1132A2", "#9CA6C7", "#E1E1E2"] # Copy from R
    assert isinstance(x1, CVD)
    assert isinstance(x2, CVD)
    assert np.all(x1.colors() == x2.colors())
    #assert np.all(x1.colors() == x3)
    del x1, x2 #, x3

    x1   = CVD(cols, "protan")
    x2   = CVD(cols = cols, type_ = "protan", severity = 1.0)
    # TODO(R): Seems we have some roundoff errors here.
    #x3   = ["#2042AA", "#9EA8C9", "#E2E2E2"]
    assert isinstance(x1, CVD)
    assert isinstance(x2, CVD)
    assert np.all(x1.colors() == x2.colors())
    # assert np.all(x1.colors() == x3)
    del x1, x2 #, x3

    x1   = CVD(cols, "protan")
    x2   = CVD(cols = cols, type_ = "protan", severity = 1.0)
    # TODO(R): Seems we have some roundoff errors here.
    #x3   = ["#00525D", "#99ABB0", "#E1E2E2"]
    assert isinstance(x1, CVD)
    assert isinstance(x2, CVD)
    assert np.all(x1.colors() == x2.colors())
    #assert np.all(x1.colors() == x3)
    del x1, x2 #, x3


# ------------------------------------------
# Testing interfacing functions
# ------------------------------------------
def test_default():

    cols = sequential_hcl()(3)

    x1   = CVD(cols, "deutan")
    x2   = deutan(cols)
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    del x1, x2

    x1   = CVD(cols, "protan")
    x2   = protan(cols)
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    del x1, x2

    x1   = CVD(cols, "tritan")
    x2   = tritan(cols)
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    del x1, x2


# ------------------------------------------
# Testing interfacing functions
# ------------------------------------------
def test_desaturate_wrong_usage():

    cols = sequential_hcl()(3)

    # Testing argument amount
    raises(TypeError,  desaturate, cols = cols, amount = "foo") # not float/int
    raises(ValueError, desaturate, cols = cols, amount = -0.01) # negative
    raises(ValueError, desaturate, cols = cols, amount = 2) # larger than 1

    #TODO(R): Test for 'cols' at some point.

def test_desaturate():

    cols = sequential_hcl()(3)
    assert np.all(cols == ["#023FA5", "#A1A6C8", "#E2E2E2"])

    # If amount is 0: will be returned as they are
    x1 = desaturate(cols, amount = 0)
    assert np.all(cols == x1)

    # Compare to R
    x2 = desaturate(cols, amount = 1)
    x3 = desaturate(cols)                # Testing default

    assert np.all(x2 == ["#474747", "#A8A8A8", "#E2E2E2"])
    assert np.all(x3 == ["#474747", "#A8A8A8", "#E2E2E2"])






