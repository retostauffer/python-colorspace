

import pytest
import numpy as np

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from colorspace import diverging_hcl, sequential_hcl, demoplot, palette
from colorspace.colorlib import hexcols
cols = sequential_hcl()(7)

from pytest import raises

plt.switch_backend("Agg")

# ---------------------------------
# Wrong use
# ---------------------------------
def test_wrong_usage():

    # Missing type
    raises(TypeError,  demoplot, colors = cols)

    # Non-existing type
    raises(TypeError,  demoplot, colors = cols, type_ = {"foo": "bar"})
    raises(ValueError, demoplot, colors = cols, type_ = "foo")

    # Wrong input for 'n'
    raises(TypeError,  demoplot, colors = cols, type_ = "Map", n = "foo")
    raises(ValueError, demoplot, colors = cols, type_ = "Map", n = -10)


# ---------------------------------
# Testing different input types for argument colors
# ---------------------------------
def test_input_hex_list():
    fig = demoplot(cols, "Lines")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance
def test_input_colorobject():
    x = hexcols(cols)
    x.to("HCL")
    fig = demoplot(x, "Lines")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance
def test_input_palette():
    x = palette(cols, "test palette")
    fig = demoplot(x, "Lines")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance
def test_input_hclpalette():
    fig = demoplot(diverging_hcl(), "Lines")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# ---------------------------------
# Testing different plots
# ---------------------------------
# Here testing non case-sensitivity as well
@pytest.mark.mpl_image_compare
def test_demoplot_Bar():
    fig = demoplot(cols, "bAr")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_demoplot_Heatmap():
    fig = demoplot(cols, "Heatmap")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_demoplot_Lines():
    fig = demoplot(cols, "Lines")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_demoplot_Map():
    fig = demoplot(cols, "Map")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_demoplot_Matrix():
    fig = demoplot(cols, "Matrix")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_demoplot_Pie():
    fig = demoplot(cols, "Pie")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_demoplot_Spectrum():
    fig = demoplot(cols, "Spectrum")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_demoplot_Spine():
    fig = demoplot(cols, "Spine")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# ---------------------------------
# Testing ax option
# ---------------------------------
def test_demoplot_single_subplot():
    fig = plt.subplot()
    res = demoplot(cols, "Map", ax = fig)
    assert isinstance(res, Axes)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_demoplot_multi_subplots():
    fig,axes = plt.subplots(2, 2)
    ax1 = demoplot(diverging_hcl("Red-Green")(10), "Bar", ax = axes[0, 0])
    ax2 = demoplot(diverging_hcl("Tofino")(5),     "Bar", ax = axes[0, 1])
    ax3 = demoplot(sequential_hcl("Peach")(5),     "Bar", ax = axes[1, 0])
    ax4 = demoplot(sequential_hcl("Heat 2")(8),    "Bar", ax = axes[1, 1])
    assert isinstance(ax1, Axes)
    assert isinstance(ax2, Axes)
    assert isinstance(ax3, Axes)
    assert isinstance(ax4, Axes)
    plt.close() # Closing figure instance

# ---------------------------------
# Adding title and labels (**kwargs)
# ---------------------------------
@pytest.mark.mpl_image_compare
def test_demoplot_title_and_labels():
    fig = demoplot(cols, "Spine",
                   title = "Custom Title",
                   xlabel = "custom x label",
                   ylabel = "custom y label")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance


# ---------------------------------
# Adding title and labels (**kwargs)
# ---------------------------------
def test_invalid_ax_object():
    types = ["Bar", "Pie", "Spine", "Heatmap", "Matrix", "Lines", "Map"]
    for x in types:
        raises(TypeError, demoplot, colors = cols, type_ = x, ax = "foo")

def test_return_Axis_object():
    ax = plt.subplot()
    types = ["Bar", "Pie", "Spine", "Heatmap", "Matrix", "Lines", "Map"]
    for x in types:
        res = demoplot(cols, type_ = x, ax = ax)
        assert isinstance(res, Axes)


# ---------------------------------
# Testing the two functions to load some data sets for the demo plots
# ---------------------------------
def test_get_volcano_data():
    from colorspace.demos import get_volcano_data

    # Wrong usage
    raises(ValueError, get_volcano_data, array = "foo")

    # Testing returns
    x = get_volcano_data()
    assert isinstance(x, list)
    assert len(x) == 61
    assert np.all([len(x) == 87 for x in x])

    x = get_volcano_data(array = True)
    assert isinstance(x, np.ndarray)
    assert x.shape == (61, 87)
    assert x.dtype == np.int64


def test_get_map_data():
    from colorspace.demos import get_map_data
    from matplotlib.collections import PatchCollection

    # Wrong usage
    raises(TypeError, get_map_data, some = "thing")

    # Testing returns
    mapdata = get_map_data()
    assert isinstance(mapdata, list)
    assert len(mapdata) == 2

    assert type(mapdata[0]) == PatchCollection
    assert len(mapdata[1]) == 272
    assert mapdata[1].dtype == np.float64














