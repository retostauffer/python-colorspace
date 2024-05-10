

import pytest
from pytest import raises
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from colorspace import *



# ---------------------------------
# Testing a series of swatchplot options
# ---------------------------------

# Single list of hex colors
@pytest.mark.mpl_image_compare
def test_swatchplot_single_hex_list():
    fig = swatchplot(diverging_hcl()(7))
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



