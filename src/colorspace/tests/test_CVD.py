
from colorspace import deutan, protan, tritan, desaturate
from colorspace import sequential_hcl, diverging_hcl, palette
from colorspace import hexcols, compare_colors
from colorspace.CVD import CVD

import numpy as np
import pytest
from pytest import raises

try:
    import matplotlib
    _got_mpl = True
except:
    _got_mpl = False


# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    cols = sequential_hcl()(3)

    raises(TypeError,  CVD, cols = cols, type_ = 12345678, severity = 1)      # type_ not str
    raises(ValueError, CVD, cols = cols, type_ = "foo",    severity = 1)      # type_ not allowed

    # Argument 'severity'
    raises(TypeError,  CVD, cols = cols, type_ = "deutan", severity = [1])        # not float
    raises(TypeError,  CVD, cols = cols, type_ = "deutan", severity = "0.5")      # not float
    raises(ValueError, CVD, cols = cols, type_ = "deutan", severity = -0.01)      # below 0
    raises(ValueError, CVD, cols = cols, type_ = "deutan", severity = +1.01)      # above 1

    raises(ValueError, CVD, cols = ["#ff0000", "foobar"], type_ = "deutan", severity = 1) # non HEX

    # Argument 'linear'
    raises(TypeError, CVD, cols = ["#ff0000", "#00ff00"], type_ = "deutan", linear = [True]) # not bool
    raises(TypeError, CVD, cols = ["#ff0000", "#00ff00"], type_ = "deutan", linear = "foo")  # not bool
    raises(TypeError, CVD, cols = ["#ff0000", "#00ff00"], type_ = "deutan", linear = None)   # not bool

    # Input none of the allowed types
    raises(TypeError, CVD, cols = None, type_ = "deutan")
    raises(TypeError, CVD, cols = None, type_ = "protan")
    raises(TypeError, CVD, cols = None, type_ = "tritan")
    raises(TypeError, deutan, None)
    raises(TypeError, protan, None)
    raises(TypeError, tritan, None)


# ------------------------------------------
# Testing interfacing functions
# ------------------------------------------
def test_CVD_default():

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


# ------------------------------------------
# Input is a palette
# ------------------------------------------
def test_CVD_palette_input():

    cols = sequential_hcl()(3)
    pal = palette(cols)

    x1   = CVD(pal, "deutan")
    x2   = deutan(pal)
    R    = ["#0040A3", "#9BA6C7", "#E2E2E2"] # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    x1   = CVD(pal, "protan")
    x2   = protan(pal)
    R    = ["#004EA8", "#9DA9CA", "#E2E2E2"] # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    x1   = CVD(pal, "tritan")
    x2   = tritan(pal)
    R    = ["#005A6C", "#98ACB1", "#E2E2E2"] # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R


# ------------------------------------------
# Input is a string (single color)
# ------------------------------------------
def test_CVD_string_input():

    col = sequential_hcl()(3)[0] # Taking first color as str

    x1   = CVD(col, "deutan")
    x2   = deutan(col)
    R    = "#0040A3" # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == [R])
    del x1, x2, R

    x1   = CVD(col, "protan")
    x2   = protan(col)
    R    = "#004EA8" # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == [R])
    del x1, x2, R

    x1   = CVD(col, "tritan")
    x2   = tritan(col)
    R    = "#005A6C" # From R colorspace, severity = 1
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == [R])
    del x1, x2, R


# ------------------------------------------
# Input is a hexcolor object
# ------------------------------------------
def test_CVD_hexcols_input():

    cols = hexcols(diverging_hcl()(5))

    x1 = CVD(cols, "deutan")
    x2 = deutan(cols)
    assert compare_colors(x1.colors(), x2)
    del x1, x2


# ------------------------------------------
# Input is a matplotlib.colors.LinearSegmentedColormap
# ------------------------------------------
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_CVD_cmap_input():

    from matplotlib.colors import LinearSegmentedColormap

    # Allows for LinearSegmentedColormap objects as input
    x = CVD(sequential_hcl().cmap(), "tritan")
    assert isinstance(x, CVD)
    assert x.CMAP
    # Extracting colormap
    cmap = x.colors()
    assert isinstance(cmap, LinearSegmentedColormap)
    assert isinstance(cmap.name, str)
    assert cmap.name == "custom_hcl_cmap"


# ------------------------------------------
# Edge-case where severity is 50% (0.5)
# ------------------------------------------
def test_CVD_severity05():

    cols = sequential_hcl()(3)

    # Deutan for edge-case where severity is 0.5
    x1   = CVD(cols, "deutan", severity = 0.5)
    x2   = deutan(cols, severity = 0.5)
    R    = ["#0041A4", "#9DA7C8", "#E2E2E2"] # From R colorspace, severity = 0.5
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    # Protan for edge-case where severity is 0.5
    x1   = CVD(cols, "protan", severity = 0.5)
    x2   = protan(cols, severity = 0.5)
    R    = ["#0048A7", "#9EA8C9", "#E2E2E2"] # From R colorspace, severity = 0.5
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    # Tritan for edge-case where severity is 0.5
    x1   = CVD(cols, "tritan", severity = 0.5)
    x2   = tritan(cols, severity = 0.5)
    R    = ["#004893", "#9FA8C0", "#E2E2E2"] # From R colorspace, severity = 0.5
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R


# ------------------------------------------
# Edge case where severity is 0 (no correction)
# ------------------------------------------
def test_CVD_severity00():

    cols = sequential_hcl()(3)

    # Deutan for edge-case where severity is 0.0
    x1   = CVD(cols, "deutan", severity = 0.0)
    x2   = deutan(cols, severity = 0.0)
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == cols)
    assert np.all(x1.colors() == cols)
    del x1, x2

    # Protan for edge-case where severity is 0.0
    x1   = CVD(cols, "protan", severity = 0.0)
    x2   = protan(cols, severity = 0.0)
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == cols)
    assert np.all(x1.colors() == cols)
    del x1, x2

    # Tritan for edge-case where severity is 0.0
    x1   = CVD(cols, "tritan", severity = 0.0)
    x2   = tritan(cols, severity = 0.0)
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == cols)
    assert np.all(x1.colors() == cols)
    del x1, x2


# ------------------------------------------
# Edge case with severity = 0.55; mixes two transformation
# matrices in _interpolate_cvd_transform()
# ------------------------------------------
def test_CVD_severity55():

    cols = sequential_hcl()(3)

    # Deutan for edge-case where severity is 0.55
    x1   = CVD(cols, "deutan", severity = 0.55)
    x2   = deutan(cols, severity = 0.55)
    R    = ["#0041A4", "#9DA7C7", "#E2E2E2"]
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    # Protan for edge-case where severity is 0.55
    x1   = CVD(cols, "protan", severity = 0.55)
    x2   = protan(cols, severity = 0.55)
    R    = ["#0049A7", "#9EA8C9", "#E2E2E2"]
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    # Tritan for edge-case where severity is 0.55
    x1   = CVD(cols, "tritan", severity = 0.55)
    x2   = tritan(cols, severity = 0.55)
    R    = ["#004A91", "#9FA8BF", "#E2E2E2"]
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R


# ------------------------------------------
# Testing CVD with linear = FALSE (RGB instead of sRGB)
# ------------------------------------------
def test_CVD_severity55_nonlinear_RGB():

    cols = sequential_hcl()(3)

    # Deutan for edge-case where severity is 0.55
    x1   = CVD(cols, "deutan", severity = 0.55, linear = False)
    x2   = deutan(cols, severity = 0.55, linear = False)
    R    = ["#0E37A4", "#9EA6C7", "#E2E2E2"]
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    # Protan for edge-case where severity is 0.55
    x1   = CVD(cols, "protan", severity = 0.55, linear = False)
    x2   = protan(cols, severity = 0.55, linear = False)
    R    = ["#1640A8", "#9FA8C9", "#E2E2E2"]
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R

    # Tritan for edge-case where severity is 0.55
    x1   = CVD(cols, "tritan", severity = 0.55, linear = False)
    x2   = tritan(cols, severity = 0.55, linear = False)
    R    = ["#004687", "#9FA8BE", "#E2E2E2"]
    assert isinstance(x1, CVD)
    assert isinstance(x2, list)
    assert np.all(x1.colors() == x2)
    assert np.all(x1.colors() == R)
    del x1, x2, R


# ------------------------------------------
# Default order of arguments
# ------------------------------------------
def test_CVD_default_argument_order():
    
    cols = diverging_hcl().colors(5)

    x1 = deutan(cols = cols, severity = 0.66, linear = True)
    x2 = deutan(cols, 0.66, True)
    assert np.all(x1 == x2)
    del x1, x2

    x1 = protan(cols = cols, severity = 0.66, linear = True)
    x2 = protan(cols, 0.66, True)
    assert np.all(x1 == x2)
    del x1, x2

    x1 = tritan(cols = cols, severity = 0.66, linear = True)
    x2 = tritan(cols, 0.66, True)
    assert np.all(x1 == x2)
    del x1, x2


# ======================================================================
# ======================================================================


# ------------------------------------------
# Testing interfacing functions
# ------------------------------------------
def test_desaturate_wrong_usage():

    cols = sequential_hcl()(3)

    # Testing argument amount
    raises(TypeError,  desaturate, cols = cols, amount = "foo") # not float/int
    raises(ValueError, desaturate, cols = cols, amount = -0.01) # negative
    raises(ValueError, desaturate, cols = cols, amount = 2) # larger than 1

    # Input none of the allowed types
    raises(TypeError, desaturate, None)


# ------------------------------------------
# List of hex cols as input
# ------------------------------------------
def test_desaturate():

    cols = sequential_hcl()(3)
    R    = ["#474747", "#A8A8A8", "#E2E2E2"] # R solution

    # If amount is 0: will be returned as they are
    x1 = desaturate(cols, amount = 0)
    assert np.all(cols == x1)

    # Compare to R
    x2 = desaturate(cols = cols, amount = 1)
    x3 = desaturate(cols)                # Testing default

    assert np.all(x2 == R)
    assert np.all(x3 == R)


# ------------------------------------------
# Input is a palette
# ------------------------------------------
def test_desaturate_palette_input():

    cols = sequential_hcl()(3)
    pal  = palette(cols)
    R    = ["#474747", "#A8A8A8", "#E2E2E2"] # R solution

    x1   = desaturate(pal, amount = 0)
    x2   = desaturate(pal, amount = 1)
    x3   = desaturate(pal)
    assert isinstance(x1, list)
    assert isinstance(x2, list)
    assert isinstance(x3, list)
    assert np.all(x1 == cols)
    assert np.all(x2 == R)
    assert np.all(x3 == R)


# ------------------------------------------
# Desaturate by 1/4, 2/4, 3/5
# ------------------------------------------
def test_desaturate_odd_amount():

    cols = sequential_hcl()(3)

    # If amount is 0: will be returned as they are
    x1 = desaturate(cols, amount = 1 / 4)
    x2 = desaturate(cols, amount = 2 / 4)
    x3 = desaturate(cols, amount = 3 / 4)

    assert np.all(x1 == ["#2A428C", "#A3A6C0", "#E2E2E2"])
    assert np.all(x2 == ["#394475", "#A5A7B8", "#E2E2E2"])
    assert np.all(x3 == ["#41465E", "#A6A7B0", "#E2E2E2"])


# ------------------------------------------
# Input is a string (single color)
# ------------------------------------------
def test_desaturate_string_input():

    col = sequential_hcl()(3)[0] # Taking first color as str
    R    = "#474747"

    x1   = desaturate(col, amount = 0)
    x2   = desaturate(col, amount = 1)
    x3   = desaturate(col)
    assert np.all(x1 == [col])
    assert np.all(x2 == [R])
    assert np.all(x3 == [R])


# ------------------------------------------
# Input is a hexcolor object
# ------------------------------------------
def test_desaturate_hexcols_input():

    cols = hexcols(diverging_hcl()(3))
    R    = ["#474747", "#E2E2E2", "#464646"] # R solution

    x1 = desaturate(cols, amount = 0)
    x2 = desaturate(cols, amount = 1)
    x3 = desaturate(cols)
    assert np.all(x1 == cols.colors())
    assert np.all(x2 == R)
    assert np.all(x3 == R)


# ------------------------------------------
# Input is a hexcolor object
# ------------------------------------------
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_desaturate_cmap_input():

    from matplotlib.colors import LinearSegmentedColormap
    cmap = diverging_hcl().cmap()

    x1 = desaturate(cmap, amount = 0)
    x2 = desaturate(cmap, amount = 1)
    assert isinstance(x1, LinearSegmentedColormap)
    assert isinstance(x2, LinearSegmentedColormap)


