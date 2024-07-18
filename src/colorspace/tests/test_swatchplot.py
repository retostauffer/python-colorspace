

import pytest
from pytest import raises, warns
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from colorspace import *

# ---------------------------------
# Wrong usage
# ---------------------------------
def test_swatchplot_wrong_usage():

    cols = diverging_hcl().colors(5)

    # Testing non-allowed cvd types
    raises(TypeError, swatchplot, cols, cvd = 3)
    raises(TypeError, swatchplot, cols, cvd = 3.)
    raises(TypeError, swatchplot, cols, cvd = True)
    raises(TypeError, swatchplot, cols, cvd = {"a":3})
    raises(TypeError, swatchplot, cols, cvd = (3))

    # If list, it must only contain str
    raises(ValueError, swatchplot, cols, cvd = [3])
    raises(ValueError, swatchplot, cols, cvd = ["foo", 3])
    raises(ValueError, swatchplot, cols, cvd = [True, False])
    raises(ValueError, swatchplot, cols, cvd = [None])

    # Invalid value(s) on cvd
    raises(ValueError, swatchplot, cols, cvd = "foo")
    raises(ValueError, swatchplot, cols, cvd = ["deutan", "foo"])

    # Figsize - if provided - must be a tuple of length 2 with int/float
    raises(ValueError, swatchplot, cols, figsize = 3)
    raises(ValueError, swatchplot, cols, figsize = [3, 5])
    raises(ValueError, swatchplot, cols, figsize = (3))
    raises(ValueError, swatchplot, cols, figsize = (3, "foo"))
    raises(ValueError, swatchplot, cols, figsize = (3, 3, 5))

    # Provide a colorobject with no colors at all; should
    # raise an error.
    raises(ValueError, swatchplot, hexcols([]))

    # Providing a list with a dictionary inside; a type which
    # is now allowed.
    raises(Exception, swatchplot, [{"a_dict": diverging_hcl()}])


# ---------------------------------
# Testing a series of swatchplot options
# ---------------------------------


# Single list of hex colors
@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list():
    fig = swatchplot(diverging_hcl()(7))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Colorobject as input
@pytest.mark.mpl_image_compare
def test_swatchplot_single_colorobject():
    x = hexcols(rainbow_hcl().colors(7))
    fig = swatchplot(x)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Single list of hex colors; suppress names
@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list_nonames():
    fig = swatchplot(diverging_hcl()(7), show_names = False)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Dictionary of single hex color list (adds title)
@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list_title():
    fig = swatchplot({"Default diverging": diverging_hcl()(7)})
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# List of list of hex colors
@pytest.mark.mpl_image_compare
def test_swatchplot_two_hex_lists_nonames():
    fig = swatchplot([diverging_hcl()(7), sequential_hcl()(5)], show_names = False)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Plotting two hclpalettes; no names, no title
@pytest.mark.mpl_image_compare
def test_swatchplot_two_hclpalettes_nonames():
    p1 = diverging_hcl()
    p2 = sequential_hcl()
    assert isinstance(p1, palettes.hclpalette)
    assert isinstance(p2, palettes.hclpalette)
    fig = swatchplot([p1, p2], show_names = False)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Plotting two hclpalettes; names and single title
@pytest.mark.mpl_image_compare
def test_swatchplot_two_hclpalettes_nonames_title():
    p1 = diverging_hcl()
    p2 = sequential_hcl()
    assert isinstance(p1, palettes.hclpalette)
    assert isinstance(p2, palettes.hclpalette)
    fig = swatchplot({"hclpalettes": [p1, p2]}, show_names = False)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Plotting two hclpalettes; names and two title
@pytest.mark.mpl_image_compare
def test_swatchplot_two_hclpalettes_two_titles():
    p1 = diverging_hcl()
    p2 = sequential_hcl()
    assert isinstance(p1, palettes.hclpalette)
    assert isinstance(p2, palettes.hclpalette)
    fig = swatchplot({"diverging_hcl()": p1, "sequential_hcl()": p2})
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance


# ---------------------------------------------------------
# Testing different inputs
# ---------------------------------------------------------

@pytest.mark.mpl_image_compare
def test_swatchplot_input_str():
    fig = swatchplot("#ff0033")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_input_dict():
    cols = {"test": diverging_hcl()(5)}
    fig = swatchplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.filterwarnings("ignore:swatchplot")
def test_swatchplot_input_dict_with_cvd():
    cols = {"test": diverging_hcl()(5)}
    fig = swatchplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_input_dict_in_dict():
    cols = {"outer": {"test": diverging_hcl()(5)}}
    fig = swatchplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.filterwarnings("ignore:swatchplot")
def test_swatchplot_input_dict_in_dict_with_cvd():
    cols = {"outer": {"test": diverging_hcl()(5)}}
    fig = swatchplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_input_palette():
    fig = swatchplot(palette(diverging_hcl().colors(5)))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_input_LinearSegmentedColormap():
    fig = swatchplot(diverging_hcl().cmap())
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_input_ListedColormap():
    from matplotlib.colors import ListedColormap
    fig = swatchplot(ListedColormap(diverging_hcl()(10)))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_input_dict():
    fig = swatchplot({"Diverging": diverging_hcl(),
                      "Sequential": sequential_hcl()})
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

    fig = swatchplot({"Diverging": diverging_hcl().colors(5),
                      "Sequential": sequential_hcl()})
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

    fig = swatchplot({"Diverging": [diverging_hcl().colors(5), rainbow()],
                      "Sequential": [sequential_hcl(), heat_hcl().colors(3)]})
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance


# ---------------------------------------------------------
# Providing 'cvd' argument; creates additional swatches
# with simulated CVD colors.
# ---------------------------------------------------------

# Single list of hex colors
@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list_CVD_deutan():
    fig = swatchplot(diverging_hcl()(7), cvd = "deutan")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list_CVD_protan():
    fig = swatchplot(diverging_hcl()(7), cvd = "protan")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list_CVD_tritan():
    fig = swatchplot(diverging_hcl()(7), cvd = "tritan")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list_CVD_desaturate():
    fig = swatchplot(diverging_hcl()(7), cvd = "desaturate")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list_CVD_desaturate():
    fig = swatchplot(diverging_hcl()(7), cvd = ["deutan", "protan", "tritan", "desaturate"])
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

