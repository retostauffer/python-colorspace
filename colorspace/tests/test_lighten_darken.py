

from colorspace import lighten, darken
from pytest import raises
import numpy as np

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage(col = "#BB7784"):
    raises(TypeError,  lighten, col = 123)
    raises(TypeError,  lighten, col = col, method = ["foo"])
    raises(ValueError, lighten, col = col, method = "foo")
    raises(TypeError,  lighten, col = col, space = ["foo"])
    raises(ValueError, lighten, col = col, space = "foo")
    raises(TypeError,  lighten, col = col, fixup = "foo")


# ------------------------------------------
# Lighten colors
# ------------------------------------------
def test_lighten_relative_HCL(col = "#BB7784"):
    tmp = {"#C7828F": 0.1, "#D28E9A": 0.2, "#F6B0BD": 0.5}
    for sol,amount in tmp.items():
        x = lighten(col = col, amount = amount, method = "relative", space = "HCL")
        assert x == sol
def test_lighten_absolute_HCL(col = "#BB7784"):
    tmp = {"#D7929E": 0.1, "#F3ADB9": 0.2, "#FFFFFF": 0.5}
    for sol,amount in tmp.items():
        x = lighten(col = col, amount = amount, method = "absolute", space = "HCL")
        assert x == sol

## Seems I still have an issue with HLS -> hex
#def test_lighten_relative_HLS(col = "#BB7784"):
#    tmp = {"#C28590": 0.1, "#C9929D": 0.2, "#DDBBC2": 0.5}
#    for sol,amount in tmp.items():
#        x = lighten(col = col, amount = amount, method = "relative", space = "HLS")
#        assert x == sol
#def test_lighten_absolute_HLS(col = "#BB7784"):
#    tmp = {"#CC99A3": 0.1, "#DDBBC2": 0.2, "#FFFFFF": 0.5}
#    for sol,amount in tmp.items():
#        x = lighten(col = col, amount = amount, method = "absolute", space = "HLS")
#        assert x == sol

# TODO(R): missing 'combined' where I do have a similar/the same problem
#          as with absolute HLS -> seems my HLS to hex does not work as intended.



# ------------------------------------------
# Darkening colors
# ------------------------------------------
def test_darken_relative_HCL(col = "#BB7784"):
    tmp = {"#AC6875": 0.1, "#9C5967": 0.2, "#722D3D": 0.5}
    for sol,amount in tmp.items():
        x = darken(col = col, amount = amount, space = "HCL")
        assert x == sol

## Seems I still have an issue with HLS -> hex
#def test_darken_relative_HLS(col = "#BB7784"):
#    tmp = {"#C28590": 0.1, "#C9929D": 0.2, "#DDBBC2": 0.5}
#    for sol,amount in tmp.items():
#        x = darken(col = col, amount = amount, space = "HLS")
#        assert x == sol

# TODO(R): missing 'combined' where I do have a similar/the same problem
#          as with absolute HLS -> seems my HLS to hex does not work as intended.

# ------------------------------------------
# Testing returns
# ------------------------------------------
def test_return_str():
    col = "#BB7784"
    res = lighten(col)
    assert isinstance(res, str)

def test_return_list():
    from colorspace.palettes import palette
    pal = palette(["#023FA5", "#E2E2E2", "#8E063B"], "test_palette")
    res = lighten(pal)
    assert isinstance(res, palette)
    assert pal.name() == "test_palette"

def test_return_colorobject():
    from colorspace import lighten
    from colorspace.colorlib import colorobject, hexcols, RGB, HCL

    # Testing hexcols object
    col = hexcols(["#023FA5", "#E2E2E2", "#8E063B"])
    res = lighten(col)
    assert isinstance(res, colorobject)
    assert isinstance(res, type(col))
    assert col.length() == res.length()

    # RGB test .. note: lighten() returns colorobject of class hexcols
    col = RGB(R = [0.5, 0.8, 0], G = [0.5, 0, 0.8], B = [0, 0.8, 0.5])
    res = lighten(col)
    assert isinstance(res, colorobject)
    assert col.length() == res.length()

    # HCL test .. note: lighten() returns colorobject of class hexcols
    col = HCL(H = [-180, 0, 180], C = [30, 50, 30], L = [60, 40, 60])
    res = lighten(col)
    assert isinstance(res, colorobject)
    assert col.length() == res.length()


