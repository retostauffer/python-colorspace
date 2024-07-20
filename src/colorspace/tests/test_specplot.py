

import pytest
from pytest import raises
from colorspace import diverging_hcl, specplot, rainbow
cols = diverging_hcl()(7)

try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    _got_mpl = True
except:
    _got_mpl = False

# ---------------------------------
# Wrong use
# ---------------------------------
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_wrong_usage():
    raises(ValueError, specplot, x = cols, hcl = False, palette = False, rgb = False)

    # x not list or LinearSegmentedColormap
    raises(TypeError, specplot, x = "foo")
    raises(TypeError, specplot, x = 123)

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
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_default():
    fig = specplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_hcl_palette_rgb():
    fig = specplot(cols, rgb = True)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_nohcl_palette_rgb():
    fig = specplot(cols, hcl = False, rgb = True)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_nohcl_nopalette_rgb():
    fig = specplot(cols, hcl = False, palette = False, rgb = True)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_hcl_nopalette_rgb():
    fig = specplot(cols, hcl = True, palette = False, rgb = True)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_nohcl_palette_norgb():
    fig = specplot(cols, hcl = False, palette = True, rgb = False)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_hcl_nopalette_norgb():
    fig = specplot(cols, hcl = True, palette = False, rgb = False)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_default_with_title():
    fig = specplot(cols, title = "Test Title")
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Testing another color palette where heu-axis should be adjusted to 0-360 only
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_adjust_hueaxis():
    cols = rainbow(start = 0, end= 1/3)(51)
    fig = specplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Testing another color palette where heu-axis should be adjusted to 0-360 only
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
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

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_input_LinearSegmentedColormap():
    cmap = diverging_hcl().cmap() # Default, n = 256
    specplot(cmap)
    plt.close()
    del cmap

    cmap = diverging_hcl().cmap(n = 5) # With n = 5
    specplot(cmap)
    plt.close()
    del cmap

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_input_ListedColormap():
    from matplotlib.colors import ListedColormap
    specplot(ListedColormap(diverging_hcl().colors(10)))
    plt.close()

# Testing another color palette where heu-axis should be adjusted to 0-360 only
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
@pytest.mark.mpl_image_compare
def test_specplot_input_list_plus_cmap():
    # Providing a series of colors as list (length 5)
    # and a cmap (n = 256); `specplot` should draw n = 5
    # colors from the LinearSegmentedColormap
    cols = diverging_hcl(c1 = 50).colors(5)
    cmap = diverging_hcl().cmap() # Default, n = 256
    specplot(cols, cmap)
    plt.close()

    # The other way around it must fail, as y (n = 5)
    # does not match the length of x (n = 256) in this case.
    raises(ValueError, specplot, cmap, cols)
    del cmap

    # However, if the LinearSegmentedColormap also only has
    # exactly n = 5 colors it should work.
    cmap = diverging_hcl().cmap(n  = 5)
    specplot(cols, cmap)
    plt.close()
    del cmap, cols



