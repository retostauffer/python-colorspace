
from colorspace import hcl_palettes, palettes, diverging_hcl, divergingx_hcl
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


# Testing standard representation of Pastel 1 (qualitative
# palette) as it has a lambda function on 'h2'.
def test_defaultpalette_standard_representation_Pastel1():

    from re import match
    pal = hcl_palettes().get_palette("Pastel 1")
    txt = repr(pal)

    pattern = ["^Palette Name: Pastel 1",
            "\\s+Type: Basic: Qualitative", 
               "\\s+Inspired by: \\.\\.\\.",
               "\\s+c1.*?",   
               "\\s+fixup.*?",
               "\\s+gui.*?",
               "\\s+h1.*?",
               "\\s+h2\\s+<function\\s<lambda>\\sat\\s.*?>", 
               "\\s+l1.*?"]
    ####DEV####print("\n".join(pattern))

    match("\n".join(pattern), txt)


# ---------------------------------------------------
# Testing methods from superclass
# ---------------------------------------------------
def test_diverging_hcl_methods():

    # Capturing stdout for show_settings
    import io
    from contextlib import redirect_stdout

    # Using the diverging_hcl palette for testing
    x = diverging_hcl()
    capture = io.StringIO()
    with redirect_stdout(capture): x.show_settings()
    txt = capture.getvalue()

    # Representation of show_settings
    from re import match
    pattern = ["Class:\\s+diverging_hcl",
               "h1\\s+[0-9\\.-]+",
               "h2\\s+[0-9\\.-]+",
               "c1\\s+[0-9\\.-]+",
               "cmax\\s+[0-9\\.-]+",
               "c2\\s+[0-9\\.-]+",
               "l1\\s+[0-9\\.-]+",
               "l2\\s+[0-9\\.-]+",
               "p1\\s+[0-9\\.-]+",
               "p2\\s+[0-9\\.-]+",
               "fixup\\s+(True|False)"]

    match("\n".join(pattern), txt)

    # Using diverging_hcl again but replacing h2 with a lambda function
    # and h1 with an integer 50 to test show_settings()
    x = diverging_hcl(h1 = 50, h2 = lambda x: -x / 2.0)
    capture = io.StringIO()
    with redirect_stdout(capture): x.show_settings()
    txt = capture.getvalue()

    # Representation of show_settings
    from re import match
    pattern = ["Class:\\s+diverging_hcl",
               "h1\\s+50",
               "h2\\s+<lambda>",
               "c1\\s+[0-9\\.-]+",
               "cmax\\s+[0-9\\.-]+",
               "c2\\s+[0-9\\.-]+",
               "l1\\s+[0-9\\.-]+",
               "l2\\s+[0-9\\.-]+",
               "p1\\s+[0-9\\.-]+",
               "p2\\s+[0-9\\.-]+",
               "fixup\\s+(True|False)"]

    match("\n".join(pattern), txt)

    # DivergingX palette; has some more output
    x = divergingx_hcl()
    capture = io.StringIO()
    with redirect_stdout(capture): x.show_settings()
    txt = capture.getvalue()

    # Representation of show_settings
    from re import match
    parms = ["h1", "h2", "h3", "c1", "cmax1", "c2", "cmax2", "c3", 
                    "l1", "l2", "l3", "p1", "p2", "p3", "p4"]
    pattern = ["Class:\\s+divergingx_hcl"] + \
              [f"{x}\\s+[0-9\\.-]+" for x in parms] + \
              ["fixup\\s+(True|False)"]

    match("\n".join(pattern), txt)


