

import pytest
from pytest import raises
from matplotlib.figure import Figure
from colorspace import diverging_hcl, specplot, rainbow
cols = diverging_hcl()(7)


# ---------------------------------
# Wrong use
# ---------------------------------
def test_wrong_usage():
    raises(ValueError, specplot, hex_ = cols, hcl = False, palette = False, rgb = False)


# ---------------------------------
# Testing different plots
# ---------------------------------
@pytest.mark.mpl_image_compare
def test_specplot_default():
    fig = specplot(cols)
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_specplot_hcl_palette_rgb():
    fig = specplot(cols, rgb = True)
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_specplot_nohcl_palette_rgb():
    fig = specplot(cols, hcl = False, rgb = True)
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_specplot_nohcl_nopalette_rgb():
    fig = specplot(cols, hcl = False, palette = False, rgb = True)
    assert isinstance(fig, Figure)
    return fig

@pytest.mark.mpl_image_compare
def test_specplot_nohcl_palette_norgb():
    fig = specplot(cols, hcl = False, palette = True, rgb = False)
    assert isinstance(fig, Figure)
    return fig

# Testing another color palette where heu-axis should be adjusted to 0-360 only
@pytest.mark.mpl_image_compare
def test_specplot_adjust_hueaxis():
    cols = rainbow(start = 0, end= 1/3)(51)
    fig = specplot(cols)
    assert isinstance(fig, Figure)
    return fig

