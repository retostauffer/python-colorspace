
from colorspace import sequential_hcl
from colorspace import deutan, protan, tritan, desaturate
from colorspace.CVD import CVD
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
# Testing interfacing functions
# ------------------------------------------
def test_default():

    cols = sequential_hcl()(3)

    x1   = CVD(cols, "deutan")
    x2   = deutan(cols)
    R    = ["#0040A3", "#9BA6C7", "#E2E2E2"] # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    x1   = CVD(cols, "protan")
    x2   = protan(cols)
    R    = ["#004EA8", "#9DA9CA", "#E2E2E2"] # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    x1   = CVD(cols, "tritan")
    x2   = tritan(cols)
    R    = ["#005A6C", "#98ACB1", "#E2E2E2"] # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R


#def test_cvd_severity05():
#
#    cols = sequential_hcl()(3)
#
#    # TODO: Small round-off problems it seems!
#    x1   = CVD(cols, "deutan", severity = 0.5)
#    x2   = deutan(cols, severity = 0.5)
#    R    = ["#0041A4", "#9DA7C8", "#E2E2E2"] # From R colorspace, severity = 0.5
#    assert isinstance(x1, CVD)
#    assert isinstance(x2, list)
#    assert np.all(x1.colors() == x2)
#    assert np.all(x1.colors() == R)
#    del x1, x2, R
#
#    # TODO: Small round-off problems it seems!
#    x1   = CVD(cols, "protan", severity = 0.5)
#    x2   = protan(cols, severity = 0.5)
#    R    = ["#0048A7", "#9EA8C9", "#E2E2E2"] # From R colorspace, severity = 0.5
#    assert isinstance(x1, CVD)
#    assert isinstance(x2, list)
#    assert np.all(x1.colors() == x2)
#    assert np.all(x1.colors() == R)
#    del x1, x2, R
#
#    # TODO: Small round-off problems it seems!
#    x1   = CVD(cols, "tritan", severity = 0.5)
#    x2   = tritan(cols, severity = 0.5)
#    R    = ["#004893", "#9FA8C0", "#E2E2E2"] # From R colorspace, severity = 0.5
#    assert isinstance(x1, CVD)
#    assert isinstance(x2, list)
#    assert np.all(x1.colors() == x2)
#    assert np.all(x1.colors() == R)
#    del x1, x2, R

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






