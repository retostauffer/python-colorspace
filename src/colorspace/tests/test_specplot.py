

import pytest
from pytest import raises
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from colorspace import diverging_hcl, specplot, rainbow
cols = diverging_hcl()(7)


# ---------------------------------
# Wrong use
# ---------------------------------
def test_wrong_usage():
    raises(ValueError, specplot, x = cols, hcl = False, palette = False, rgb = False)

    # If y is set (not None) it must be a list
    raises(TypeError, specplot, x = cols, y = "foo")

    # If y is set it is first tested if it contains valid
    # hex colors.
    raises(ValueError, specplot, x = cols, y = ["#ff00ff", "00ff00"])

    # Next we ensure that len(x) equals len(y)
    raises(ValueError, specplot, x = cols, y = cols[:-1])

    # Argument 'title' must be None or str
    raises(TypeError, specplot, x = cols, title = ["foo"])
    raises(TypeError, specplot, x = cols, title = 1000)
    raises(TypeError, specplot, x = cols, title = False)



# ---------------------------------
# Testing different plots
# ---------------------------------
@pytest.mark.mpl_image_compare
def test_specplot_default():
    fig = specplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_specplot_hcl_palette_rgb():
    fig = specplot(cols, rgb = True)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_specplot_nohcl_palette_rgb():
    fig = specplot(cols, hcl = False, rgb = True)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_specplot_nohcl_nopalette_rgb():
    fig = specplot(cols, hcl = False, palette = False, rgb = True)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_specplot_hcl_nopalette_rgb():
    fig = specplot(cols, hcl = True, palette = False, rgb = True)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_specplot_nohcl_palette_norgb():
    fig = specplot(cols, hcl = False, palette = True, rgb = False)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_specplot_hcl_nopalette_norgb():
    fig = specplot(cols, hcl = True, palette = False, rgb = False)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_specplot_default_with_title():
    fig = specplot(cols, title = "Test Title")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Testing another color palette where heu-axis should be adjusted to 0-360 only
@pytest.mark.mpl_image_compare
def test_specplot_adjust_hueaxis():
    cols = rainbow(start = 0, end= 1/3)(51)
    fig = specplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Testing another color palette where heu-axis should be adjusted to 0-360 only
@pytest.mark.mpl_image_compare
def test_specplot_provide_figure_obj():
    import matplotlib.pyplot as plt

    fig  = plt.figure(figsize = (4, 6))
    cols = rainbow(start = 0, end= 1/3)(51)
    fig  = specplot(cols, fig = fig)
    assert isinstance(fig, Figure)
    # Ensure we got our custom figure object back
    assert fig.get_figwidth() == 4.
    assert fig.get_figheight() == 6.
    plt.show()
    plt.close() # Closing figure instance

