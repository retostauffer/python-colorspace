

import pytest
from pytest import raises
from colorspace.colorlib import *
from copy import deepcopy

import matplotlib.pyplot as plt
from colorspace import hexcols, polarLUV, diverging_hcl

all_models = ["polarLUV", "HCL", "CIELUV", "CIEXYZ", "CIELAB", "CIELUV", "RGB", \
              "sRGB", "polarLAB", "hex", "HLS", "HSV"]
colors_to_test            = hexcols(["#000000", "#ff0000", "#00ff00", "#0000ff",
                                     "#ff00ff", "#ffff00", "#00ffff", "#ffffff"])
colors_to_test_with_alpha = hexcols(["#00000010", "#ff0000ff", "#00ff0030", "#0000ffAA",
                                     "#ff00ffce", "#ffff0000", "#00ffffc3", "#ffffffD3"])

def test_HCL_to_RGB_black():
    x = HCL(0, 0, 0)
    required_HCL = ["H", "C", "L"]
    assert all(n in required_HCL for n in x._data_.keys())
    # Convert to rgbh
    x.to("RGB")
    required_RGB = ["R", "G", "B", "alpha"]
    assert all(n in required_RGB for n in x._data_.keys())

# --------------------------------------------
# Testing the 'compare colors' function
# --------------------------------------------

def test_hexcols_repr_alpha():
    from re import match, DOTALL
    # No alpha, there should be no 'alpha' in output
    x = repr(hexcols(["#ff0033", "#00ff00"]))
    assert isinstance(x, str)
    assert match(".*alpha.*", x, DOTALL) is None
    del x

    # With one alpha, we should find 'alpha' and '---' for the
    # second color which has no alpha.
    x = repr(hexcols(["#ff003310", "#00ff00"]))
    assert isinstance(x, str)
    assert match(".*alpha.*", x, DOTALL) is not None
    assert match(".*---.*", x, DOTALL) is not None
    del x

    # Two colors with alpha, so no more ---
    x = repr(hexcols(["#ff003310", "#00ff00CE"]))
    assert isinstance(x, str)
    assert match(".*alpha.*", x, DOTALL) is not None
    assert match(".*---.*", x, DOTALL) is None
    del x

# Compare hexcols objects
def test_compare_colors_hex():
    assert compare_colors(hexcols("#ff0000"), hexcols("#FF0000"))
    assert compare_colors(colors_to_test,     colors_to_test)

# Compare RGB objects
def test_compare_colors_RGB_no_alpha():
    assert compare_colors(RGB(1.0, 0.0, 0.5),
                          RGB(1.0, 0.0, 0.5))
    # Two identical objects
    assert compare_colors(RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1]),
                          RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1]))
    # One color slightly off but below tolerance (0.01)
    # Test nearly equal (exact = True)
    assert compare_colors(RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1]),
                          RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1005]))
    #  Test for exact = True (tolerance 1e-6)
    assert not compare_colors(RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1]),
                              RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1005]),
                              exact = True)

def test_compare_colors_RGB_with_alpha():
    # Two identical objects
    assert compare_colors(RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1], [0.5, 0.1]),
                          RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1], [0.5, 0.1]))
    # One color slightly off but below tolerance (0.01)
    # Test nearly equal (exact = True)
    assert compare_colors(RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1], [0.5, 0.1]),
                          RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1], [0.5, 0.10005]))
    #  Test for exact = True (tolerance 1e-6)
    assert not compare_colors(RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1], [0.5, 0.1]),
                              RGB([1.0, 0.5], [0.3, 0.5], [1.0, 0.1], [0.5, 0.10005]),
                              exact = True)

# Compare polarLUV (HCL) objects
def test_compare_colors_polarLUV():
    # Two identical objects
    assert compare_colors(HCL([0, 180, 270], [80, 60, 40], [30, 50, 70]),
                          HCL([0, 180, 270], [80, 60, 40], [30, 50, 70]))
    # One color slightly off but below tolerance (1.0)
    assert compare_colors(HCL([0, 180, 270], [80, 60, 40], [30, 50, 70]),
                          HCL([0, 180, 270], [80, 60, 40], [30, 50, 70]))
    # Test nearly equal (exact = True)
    #  Test for exact = True (tolerance 1e-6)
    assert compare_colors(HCL([0, 180, 270], [80, 60, 40], [30, 50, 70]),
                          HCL([0, 180, 270], [80, 60, 40], [30, 50, 70]))

# --------------------------------------------
# Testing conversion chain. the following chains
# should check all conversions
# * hexcols -> polarLUV;  polarLUV -> hexcols
# * hexcols -> polarLAB;  polarLAB -> hexcols
# * hexcols -> HSV;       HSV -> hexcols
# * hexcols -> HLS;       HLS -> hexcols
# --------------------------------------------
def convert_from_to(col, _from, _to):
    col2 = deepcopy(col)
    col2.to(_to)
    col2.to(_from)
    assert compare_colors(col, col2)

# ----------------------------------------------
# Convert colors
# ----------------------------------------------
def test_convert_polarLUV():
    col = polarLUV(50, 50, 50) # Basic color
    # ambigious conversion; skip
    ambigious = ["HLS", "HSV", "foo"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "polarLUV", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "polarLUV", _to)
            
def test_convert_CIELUV():
    col = CIELUV(50, 50, 50) # Basic color
    # ambigious conversion; skip
    ambigious = ["HLS", "HSV", "foo"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "CIELUV", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "CIELUV", _to)

def test_convert_CIELAB():
    col = CIELAB(50, 50, 50) # Basic color
    # ambigious conversion; skip
    ambigious = ["HLS", "HSV", "foo"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "CIELAB", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "CIELAB", _to)

def test_convert_CIEXYZ():
    col = CIEXYZ(50, 50, 50) # Basic color
    # ambigious conversion; skip
    ambigious = ["HLS", "HSV", "foo"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "CIEXYZ", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "CIEXYZ", _to)

def test_convert_RGB():
    col = RGB(0.5, 0.5, 0.5) # Basic color
    # ambigious conversion; skip
    ambigious = ["foo"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "RGB", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "RGB", _to)

def test_convert_sRGB():
    col = sRGB(0.5, 0.5, 0.5) # Basic color
    # ambigious conversion; skip
    ambigious = ["foo"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "sRGB", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "sRGB", _to)

def test_convert_polarLAB():
    col = polarLAB(50, 50, 50) # Basic color
    # ambigious conversion; skip
    ambigious = ["HLS", "HSV", "foo"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "polarLAB", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "polarLAB", _to)

def test_convert_HLS():
    col = HLS(180, 0.5, 0.5) # Basic color
    # ambigious conversion; skip
    ambigious = ["foo", "CIEXYZ","CIELUV","CIELAB","polarLUV","HCL","polarLAB"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "HLS", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "HLS", _to)

def test_convert_HSV():
    col = HSV(180, 0.5, 0.5) # Basic color
    # ambigious conversion; skip
    ambigious = ["foo", "CIEXYZ","CIELUV","CIELAB","polarLUV","HCL","polarLAB"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "HSV", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "HSV", _to)

def test_convert_hexcols():
    col = hexcols("#FF5733")
    # ambigious conversion; skip
    ambigious = ["foo"]
    for _to in all_models:
        if _to in ambigious: continue
        convert_from_to(col, "hex", _to)
    for _to in ambigious:
        with pytest.raises(Exception):
            convert_from_to(col, "hex", _to)


# ----------------------------------------------
# ----------------------------------------------
def test_convert_hex_to_polarLUV_to_hex():
    # Make a copy; convert hex -> polarLUV -> hex
    # polarLUV is identical to HCL
    x = deepcopy(colors_to_test); x.to("polarLUV"); x.to("hex")
    # Compare resulting hex colors
    assert compare_colors(colors_to_test, x)

def test_convert_hex_to_polarLAB_to_hex():
    # Make a copy; convert hex -> polarLAB -> hex
    x = deepcopy(colors_to_test); x.to("polarLAB"); x.to("hex")
    # Compare resulting hex colors
    assert compare_colors(colors_to_test, x)

def test_convert_hex_to_HSV_to_hex():
    # Make a copy; convert hex -> HSV -> hex
    x = deepcopy(colors_to_test); x.to("HSV"); x.to("hex")
    # Compare resulting hex colors
    assert compare_colors(colors_to_test, x)

def test_convert_hex_to_HLS_to_hex():
    # Make a copy; convert hex -> HLS -> hex
    x = deepcopy(colors_to_test); x.to("HLS"); x.to("hex")
    # Compare resulting hex colors
    assert compare_colors(colors_to_test, x)

## Additionally
def test_convert_color_spaces():
    x = deepcopy(colors_to_test); x.to("sRGB"); x.to("CIEXYZ")
    x.to("RGB"); x.to("HSV"); x.to("RGB"); x.to("HLS");
    x.to("hex")
    assert compare_colors(colors_to_test, x)


# Testing standard representation (only that we get a string)
def test_repr():
    color = hexcols("#ff0000")
    for x in ["CIELAB", "CIELUV", "HCL", "CIEXYZ", "RGB", "HSV", "HLS", "hex"]:
        color.to(x)
        assert isinstance(repr(color), str)
# Testing truncated output
def test_repr_truncation():
    colors = hexcols(["#000000"] * 100)
    assert isinstance(repr(colors), str)
def test_iterate():
    for col in colors_to_test:
        assert isinstance(col, type(colors_to_test))
        assert col.length() == 1
        assert isinstance(repr(col), str)
def test_getitem():
    assert isinstance(colors_to_test[0], type(colors_to_test))
    assert colors_to_test[0].length() == 1

    with pytest.raises(TypeError): colors_to_test["foo"]
    with pytest.raises(TypeError): colors_to_test[(1, 2, 3)]

# Testing that sRGB and RGB must be within [0, 1]
def test_sRGB_RGB_value_limits():
    assert isinstance(sRGB(0, 0, 0), sRGB)
    assert isinstance(sRGB(1, 1, 1), sRGB)
    assert isinstance(sRGB(1, 1, 1, alpha = 0), sRGB)
    assert isinstance(sRGB(1, 1, 1, alpha = 1), sRGB)

    assert isinstance(RGB(0, 0, 0), RGB)
    assert isinstance(RGB(1, 1, 1), RGB)
    assert isinstance(RGB(1, 1, 1, alpha = 0), RGB)
    assert isinstance(RGB(1, 1, 1, alpha = 1), RGB)

    with pytest.raises(ValueError): sRGB(-0.001, 0, 0)
    with pytest.raises(ValueError): sRGB( 1.001, 0, 0)
    with pytest.raises(ValueError): sRGB(0, 0, 0, alpha = -0.0001)
    with pytest.raises(ValueError): sRGB(0, 0, 0, alpha = 1.0001)

    with pytest.raises(ValueError): RGB(-0.001, 0, 0)
    with pytest.raises(ValueError): RGB( 1.001, 0, 0)
    with pytest.raises(ValueError): RGB(0, 0, 0, alpha = -0.0001)
    with pytest.raises(ValueError): RGB(0, 0, 0, alpha = 1.0001)

def test_check_for_alpha_values():
    a = RGB(0, 1, 0, alpha = 0.3)
    b = RGB(0, 1, 0)
    assert a.hasalpha() == True
    assert b.hasalpha() == False

def test_dropalpha_values():
    a = RGB(0, 1, 0, alpha = 0.3)
    assert a.hasalpha() == True
    a.dropalpha()
    assert a.hasalpha() == False

def test_get_colors():

    x = deepcopy(colors_to_test)

    # Take this hex color object and test .colors() method
    assert isinstance(x.colors(), list)
    assert all([isinstance(col, str) for col in x.colors()])
    assert x.length() == len(x.colors())

    # .colors is the same as the __call__ method
    assert isinstance(x(), list)
    assert all([isinstance(col, str) for col in x()])
    assert x.length() == len(x())

    # Convert to HCL and get colors (-> hex list)
    x.to("HCL")
    assert isinstance(x, polarLUV)
    assert isinstance(x.colors(), list)
    assert all([isinstance(col, str) for col in x.colors()])
    assert x.length() == len(x.colors())

    # Same with alpha values
    x = deepcopy(colors_to_test_with_alpha)

    # Take this hex color object and test .colors() method
    assert isinstance(x.colors(), list)
    assert all([isinstance(col, str) for col in x.colors()])
    assert x.length() == len(x.colors())

    # Convert to HCL and get colors (-> hex list)
    x.to("HCL")
    assert isinstance(x, polarLUV)
    assert isinstance(x.colors(), list)
    assert all([isinstance(col, str) for col in x.colors()])
    assert x.length() == len(x.colors())

def test_dimensions_must_be_of_same_length():

    with pytest.raises(ValueError): RGB(1, 0, [1, 0])
    with pytest.raises(ValueError): RGB(1, 0, 1, alpha = [.5, .3])
    with pytest.raises(ValueError): HCL([0, 90, 180], [40, 50], [50, 60, 70])


def test_get_and_set_method():

    x = RGB(1, 0.5, 0, alpha = 0.3)
    assert x.get("R")[0] == 1
    assert x.get("G")[0] == 0.5
    assert x.get("B")[0] == 0
    assert x.get("alpha")[0] == 0.3

    x.set(R = 0.2)
    x.set(G = 0.2, B = 0.2, alpha = 0.2)
    assert x.get("R")[0] == 0.2
    assert x.get("G")[0] == 0.2
    assert x.get("B")[0] == 0.2
    assert x.get("alpha")[0] == 0.2

def test_get_coords():
    cols = hexcols(["#00ff0010", "#ff0033"])

    # Testing the get method
    res = cols.get()
    assert isinstance(res, dict)
    assert "hex_" in res.keys() and "alpha" in res.keys()

    # Get specific coordinate
    res = cols.get("hex_")
    assert isinstance(res, np.ndarray)
    assert len(res) == 2

    raises(TypeError, cols.get, 1) # not string
    raises(ValueError, cols.get, "foo") # invalid dimension

def test_set_coords():
    cols = hexcols(["#00ff0010", "#ff0033"])

    raises(ValueError, cols.set, A = np.ones(2)) # A invalid dimension
    raises(ValueError, cols.set, hex_ = np.ones(3)) # Wrong length

    x = np.asarray(["#0000ff", "#CECECE"])
    cols.set(hex_ = x)
    assert np.array_equal(x, cols.get("hex_"))

    

def test_getset_whitepoint():
    # Get default whitepoint
    res = hexcols(["red", "blue"]).get_whitepoint()

    assert isinstance(res, dict)
    assert len(res) == 3
    assert all([x in res.keys() for x in ["X", "Y", "Z"]])
    for k,v in res.items():
        assert isinstance(v, float)
    assert res["X"] == 95.047
    assert res["Y"] == 100.0
    assert res["Z"] == 108.883
    del res

    # We can overwrite them (dummy variables)
    cols = hexcols(["red", "blue"])
    cols.set_whitepoint(X = 10., Y = 20., Z = 30.)
    res = cols.get_whitepoint()

    assert isinstance(res, dict)
    assert len(res) == 3
    assert all([x in res.keys() for x in ["X", "Y", "Z"]])
    for k,v in res.items():
        assert isinstance(v, float)
    assert res["X"] == 10.
    assert res["Y"] == 20.
    assert res["Z"] == 30.
    del res

    # Exception if we hand over anythihng not X, Z, Y to
    # the set_whitepoint method.
    raises(ValueError, cols.set_whitepoint, A = 3.)
    raises(ValueError, cols.set_whitepoint, X = "foo") # cannot conver to float
    raises(ValueError, cols.set_whitepoint, Y = "foo") # cannot conver to float
    raises(ValueError, cols.set_whitepoint, Z = "foo") # cannot conver to float

# --------------------------------------------
# Plotting ..
# --------------------------------------------
# Testing another color palette where heu-axis should be adjusted to 0-360 only
@pytest.mark.mpl_image_compare
def test_colorlib_specplot_method():
    # Create 'colorlib' based object
    cols = hexcols(diverging_hcl()(5))
    cols.specplot()
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_colorlib_swatchplot_method():
    # Create 'colorlib' based object
    cols = hexcols(diverging_hcl()(5))
    cols.swatchplot()
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_colorlib_hclplot_method():
    # Create 'colorlib' based object
    cols = hexcols(diverging_hcl()(5))
    cols.hclplot()
    plt.close() # Closing figure instance


