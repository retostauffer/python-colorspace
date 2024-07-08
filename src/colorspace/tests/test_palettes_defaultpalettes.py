
from colorspace import hcl_palettes, palettes
import pytest
from pytest import raises

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_defaultpalette_methods_agSunset():

    # Drawing a palette
    pal = hcl_palettes().get_palette("ag_Sunset")

    # 'pal' should be a defaultpalette object
    assert isinstance(pal, palettes.defaultpalette)

    # Testing call vs. .colors()
    assert pal() == pal.colors()   # By default there should be 11 colors
    assert pal(11) == pal.colors() # By default there should be 11 colors
    assert pal(5) == pal.colors(5) # Testing with 5 colors

    # .method() should deliver the name of the function the
    # palette is based on
    assert isinstance(pal.method(), str)
    assert pal.method() == "sequential_hcl"

    # .type() Type of palette
    assert isinstance(pal.type(), str)
    assert pal.type() == "Advanced: Sequential (multi-hue)"

    # Renaming for testing purposes
    new_name = "test renaming ag_Sunset"
    pal.rename(new_name)
    assert pal.name() == new_name

    # Setting invalid argument(s)
    raises(ValueError, pal.set, c1 = "bar") # Non-numeric


def test_defaultpalette_set_get_settings():

    pal = hcl_palettes().get_palette("ag_Sunset")

    # IF boolean it should be converted to 0/1 intenally.
    # For "c1" whihc is of type int it will be integer 0/1,
    # for p1 which is of type float it will be 0./1.
    pal.set(c1 = False)
    assert isinstance(pal.get("c1"), int)
    assert pal.get("c1") == 0
    pal.set(c1 = True)
    assert isinstance(pal.get("c1"), int)
    assert pal.get("c1") == 1

    pal.set(p1 = False)
    assert isinstance(pal.get("p1"), float)
    assert pal.get("p1") == 0.
    pal.set(p1 = True)
    assert isinstance(pal.get("p1"), float)
    assert pal.get("p1") == 1.

    # If we overwrite an integer, it will convert the input to
    # input as well (using c1 here). If the setting originally
    # is float, the new value will also be converted to float.
    # Using p1 here.
    pal.set(c1 = 100) # Handing over int -> stays int
    assert isinstance(pal.get("c1"), int)
    assert pal.get("c1") == 100
    pal.set(c1 = 100.1) # Handing over float -> gets int
    assert isinstance(pal.get("c1"), int)
    assert pal.get("c1") == 100

    pal.set(p1 = 2.) # Handing over float -> stays float
    assert isinstance(pal.get("p1"), float)
    assert pal.get("p1") == 2.
    pal.set(p1 = 2) # Handing over int -> gets float
    assert isinstance(pal.get("p1"), float)
    assert pal.get("p1") == 2.


def test_defaultpalette_standard_representation_agSunset():

    from re import match

    pal = hcl_palettes().get_palette("ag_Sunset")

    txt = repr(pal)

    pattern = ["^Palette Name: ag_Sunset",
               "\\s+Type: Advanced: Sequential \\(multi-hue\\)",
               "\\s+Inspired by: CARTO palettes",
               "\\s+c1.*?",
               "\\s+c2.*?",
               "\\s+cmax.*?",
               "\\s+fixup.*?",
               "\\s+gui.*?",
               "\\s+h1.*?",
               "\\s+h2.*?",
               "\\s+l1.*?",
               "\\s+l2.*?",
               "\\s+p1.*?",
               "\\s+p2.*?"]
    ####DEV####print("\n".join(pattern))

    match("\n".join(pattern), txt)

