

import pytest


from colorspace import hexcols, sRGB, mixcolor

# Via sRGB, mimiking R's example
def test_mixcolor_sRGB_in_sRGB():
    mix = mixcolor(0.2, sRGB(1, 0, 0), sRGB(0, 1, 0), "sRGB")
    assert mix.colors()[0] == "#CC3300"

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
