

from pytest import raises
from colorspace import hexcols, sRGB, mixcolor, compare_colors

def test_mixcolor_wrong_usage():

    # Alpha wrong type
    c1 = sRGB(1, 0, 0)
    c2 = sRGB(0, 1, 0)

    raises(TypeError, mixcolor, alpha = [1, 2, 3], color1 = c1, color2 = c2, where = "sRGB")
    # Alpha out of allowed range
    raises(ValueError, mixcolor, alpha = -0.000001, color1 = c1, color2 = c2, where = "sRGB")
    raises(ValueError, mixcolor, alpha = +1.000001, color1 = c1, color2 = c2, where = "sRGB")

    # where not string
    raises(TypeError, mixcolor, alpha = 0.5, color1 = c1, color2 = c2, where = None)

    # where not among the allowed types
    raises(ValueError, mixcolor, alpha = 0.5, color1 = c1, color2 = c2, where = "foo")

    # object 'color1' cannot be converted to a hexcolor object.
    # Using the 'min' function for this test.
    raises(Exception, mixcolor, alpha = 0.5, color1 = min, color2 = c2,  where = "sRGB")
    raises(Exception, mixcolor, alpha = 0.5, color1 = c1,  color2 = min, where = "sRGB")


# Recycling shorter object (color1)
def test_mixcolor_recycling_color1():
    res = mixcolor(0.5, ["#FF00FF", "#FF0000"], "#00FF00", "sRGB")
    assert isinstance(res, sRGB)
    assert len(res) == 2

# Recycling shorter object (color2)
def test_mixcolor_recycling_color2():
    res = mixcolor(0.5, "#FF00FF", ["#FF0000", "#00FF00"], "sRGB")
    assert isinstance(res, sRGB)
    assert len(res) == 2

# Via sRGB, mimiking R's example
def test_mixcolor_sRGB_in_sRGB():
    # Testing with named and unnamed argumnets to check position
    mix1 = mixcolor(0.2, sRGB(1, 0, 0), sRGB(0, 1, 0), "sRGB")
    mix2 = mixcolor(alpha = 0.2, color1 = sRGB(1, 0, 0),
                    color2 = sRGB(0, 1, 0), where = "sRGB")
    assert mix1.colors()[0] == "#CC3300"
    assert compare_colors(mix1, mix2)


# Same but mixing in the CIEXYZ color space
def test_mixcolor_sRGB_in_CIEXYZ():
    mix = mixcolor(0.2, sRGB(1, 0, 0), sRGB(0, 1, 0), "CIEXYZ")
    assert mix.colors()[0] == "#E77C00"


# Mising two hex colors via sRGB
def test_mixcolor_hex_in_sRGB():
    mix = mixcolor(0.2, hexcols("#FF0000"), hexcols("#00FF00"), "sRGB")
    assert mix.colors()[0] == "#CC3300"


# Mising two hex colors via CIEXYZ
def test_mixcolor_hex_in_CIEXYZ():
    mix = mixcolor(0.2, hexcols("#FF0000"), hexcols("#00FF00"), "CIEXYZ")
    assert mix.colors()[0] == "#E77C00"



