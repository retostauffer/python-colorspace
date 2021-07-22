

import pytest
from pytest import raises
from colorspace import sequential_hcl, demoplot
from matplotlib.figure import Figure
cols = sequential_hcl()(7)


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
    raises(TypeError,  demoplot, colors = cols, n = "foo")
    raises(TypeError,  demoplot, colors = cols, n = -10)


# ---------------------------------
# Testing different plots
# ---------------------------------
# Here testing non case-sensitivity as well
@pytest.mark.mpl_image_compare
def test_demoplot_Bar():
    fig = demoplot(cols, "bAr")
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_demoplot_Heatmap():
    fig = demoplot(cols, "Heatmap")
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_demoplot_Lines():
    fig = demoplot(cols, "Lines")
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_demoplot_Map():
    fig = demoplot(cols, "Map")
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_demoplot_Matrix():
    fig = demoplot(cols, "Matrix")
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_demoplot_Pie():
    fig = demoplot(cols, "Pie")
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_demoplot_Spectrum():
    fig = demoplot(cols, "Spectrum")
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_demoplot_Spine():
    fig = demoplot(cols, "Spine")
    assert isinstance(fig, Figure)
    return fig
