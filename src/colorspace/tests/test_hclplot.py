

import pytest
from pytest import raises
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from colorspace import *


# Wrong use
def test_hclplot_wrong_usage():
    cols = diverging_hcl()(5)
    raises(TypeError, hclplot) # No args
    raises(TypeError, hclplot, x = cols, _type = 3) # _type must be None or str
    raises(ValueError, hclplot, x = cols, _type = "foo") # non-allowed type

    # 'c', 'l' must be None, int (>0), float (>0)
    raises(TypeError, hclplot, x = cols, c = True)
    raises(TypeError, hclplot, x = cols, c = "foo")
    raises(TypeError, hclplot, x = cols, c = np.asarray([1, 2, 3]))
    raises(ValueError, hclplot, x = cols, c = 0.0)

    raises(TypeError, hclplot, x = cols, l = True)
    raises(TypeError, hclplot, x = cols, l = "foo")
    raises(TypeError, hclplot, x = cols, l = np.asarray([1, 2, 3]))
    raises(ValueError, hclplot, x = cols, l = 0.0)

    # 'h' must be None, int, float, or a tuple. If tuple
    raises(TypeError, hclplot, x = cols, c = True)
    raises(TypeError, hclplot, x = cols, c = "foo")
    raises(TypeError, hclplot, x = cols, c = np.asarray([1]))
    raises(TypeError, hclplot, x = cols, c = [1, 2])

    # axes must be logical
    raises(TypeError, hclplot, x = cols, axes = None)
    raises(TypeError, hclplot, x = cols, axes = [True])
    raises(TypeError, hclplot, x = cols, axes = "Ja")

    # If 'h' is tuple: length must be 2, and both elements
    # inside the tuple must be int, float in range [-360, +360]
    raises(TypeError, hclplot, x = cols, h = True) # wrong type
    raises(TypeError, hclplot, x = cols, h = "foo") # wrong type
    raises(ValueError, hclplot, x = cols, h = ()) # length 0
    raises(ValueError, hclplot, x = cols, h = (1, 2, 3)) # length 3
    raises(TypeError, hclplot, x = cols, h = (True, False)) # Wrong content
    raises(ValueError, hclplot, x = cols, h = (-360.0001, 0)) # Lower bound violation
    raises(ValueError, hclplot, x = cols, h = (0, +360.0001)) # Upper bound violation
    # Single value boundary violation
    raises(ValueError, hclplot, x = cols, h = -360.0001) # Lower bound violation
    raises(ValueError, hclplot, x = cols, h = +360.0001) # Upper bound violation

    # 'x' can be a single hex colr (str) or a list of hex colors.
    # in case these are no valid colors, 'hexcols()' will complain.
    raises(ValueError, hclplot, x = "foo")
    raises(ValueError, hclplot, x = ["#00ff00", "red", "something"])

    # providing 'ax' which is not a matplotlib axis
    raises(TypeError, hclplot, x = cols, ax = True)

    # linewidth and s (scatter point size) can be provided. If probided,
    # must be None, or int/float >= 0.
    raises(TypeError, hclplot, x = cols, s = "foo")
    raises(TypeError, hclplot, x = cols, s = [1, 2, 3])
    raises(ValueError, hclplot, x = cols, s = -0.00001)
    raises(ValueError, hclplot, x = cols, s = -1)

    raises(TypeError, hclplot, x = cols, linewidth = "foo")
    raises(TypeError, hclplot, x = cols, linewidth = [1, 2, 3])
    raises(ValueError, hclplot, x = cols, linewidth = -0.00001)
    raises(ValueError, hclplot, x = cols, linewidth = -1)


# -------------------------------------------------------------------
# Conversion
# If first arg is str or list, an `hclcols()` object is created.
# Else we call `hclcols(x.colors())`. Testing this here.
@pytest.mark.mpl_image_compare
def test_hclplot_diverging_HSV_colorobject():
    x = hexcols(diverging_hcl()(7))
    x.to("HSV") # Now this is a hue-saturation-value object
    fig = hclplot(x)
    plt.close() # Closing figure instance


# -------------------------------------------------------------------
# Testing with colors with very low chroma
@pytest.mark.mpl_image_compare
def test_hclplot_qualitative_very_low_chroma():
    x = hexcols(rainbow_hcl()(7))
    x.to("HCL") # Now this is a hue-saturation-value object
    x.set(C = np.repeat(6, len(x)))
    fig = hclplot(x, _type = "qualitative")
    plt.close() # Closing figure instance


# -------------------------------------------------------------------
# Diverging
# -------------------------------------------------------------------
# Testing different plots
@pytest.mark.mpl_image_compare
def test_hclplot_diverging_simple():
    pal = diverging_hcl()
    fig = hclplot(pal(7))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_hclplot_diverging_largen():
    pal = diverging_hcl()
    fig = hclplot(pal(50))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_hclplot_diverging_h1():
    pal = diverging_hcl()
    fig = hclplot(pal(10), h = 0)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_hclplot_diverging_h2():
    pal = diverging_hcl()
    fig = hclplot(pal(10), h = (0, 180))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# DivergingX palette to test the title which is auto-generated
# as H = [a, b]/[c, d]
@pytest.mark.mpl_image_compare
def test_hclplot_divergingx_autotitle():
    cols = divergingx_palettes().get_palette("Geyser").colors(7)
    fig = hclplot(cols)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance


# Setting xlabel, ylabel, and title
@pytest.mark.mpl_image_compare
def test_hclplot_diverging_labels():
    pal = diverging_hcl()
    fig = hclplot(pal(7),
            xlabel = "testing xlabel",
            ylabel = "testing ylabel",
            title  = "testing title")
    plt.close() # Closing figure instance

# Specificly setting _type, suppressing axes
@pytest.mark.mpl_image_compare
def test_hclplot_diverging_noaxes():
    pal = diverging_hcl()
    fig = hclplot(pal(7), _type = "diverging", axes = False)
    plt.close() # Closing figure instance


# -------------------------------------------------------------------
# Sequential
# -------------------------------------------------------------------
# Testing different plots
@pytest.mark.mpl_image_compare
def test_hclplot_sequential_simple():
    pal = sequential_hcl()
    fig = hclplot(pal(7))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Manually setting hue level (where the pane slices trough the HCL space)
@pytest.mark.mpl_image_compare
def test_hclplot_qualitative_custom_h():
    pal = sequential_hcl()
    fig = hclplot(pal(7), h = 45)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_hclplot_sequential_h1():
    pal = sequential_hcl(h = 60)
    fig = hclplot(pal(7))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Setting xlabel, ylabel, and title
@pytest.mark.mpl_image_compare
def test_hclplot_sequential_labels():
    pal = sequential_hcl()
    fig = hclplot(pal(7),
            xlabel = "testing xlabel",
            ylabel = "testing ylabel",
            title  = "testing title")
    plt.close() # Closing figure instance

# Specificly setting _type, suppressing axes
@pytest.mark.mpl_image_compare
def test_hclplot_sequential_noaxes():
    pal = sequential_hcl()
    fig = hclplot(pal(7), _type = "sequential", axes = False)
    plt.close() # Closing figure instance

# -------------------------------------------------------------------
# Qualitative
# -------------------------------------------------------------------
# Testing different plots
@pytest.mark.mpl_image_compare
def test_hclplot_qualitative_simple():
    pal = qualitative_hcl()
    fig = hclplot(pal(7))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Manually setting chroma level (where the pane slices trough the HCL space)
@pytest.mark.mpl_image_compare
def test_hclplot_qualitative_custom_c():
    pal = qualitative_hcl()
    fig = hclplot(pal(7), c = 100)
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

@pytest.mark.mpl_image_compare
def test_hclplot_qualitative_h1():
    pal = qualitative_hcl(l = 60)
    fig = hclplot(pal(7))
    assert isinstance(fig, Figure)
    plt.close() # Closing figure instance

# Setting xlabel, ylabel, and title
@pytest.mark.mpl_image_compare
def test_hclplot_qualitative_labels():
    pal = qualitative_hcl()
    fig = hclplot(pal(7),
            xlabel = "testing xlabel",
            ylabel = "testing ylabel",
            title  = "testing title")
    plt.close() # Closing figure instance

# Specificly setting _type, suppressing axes
@pytest.mark.mpl_image_compare
def test_hclplot_qualitative_noaxes():
    pal = qualitative_hcl()
    fig = hclplot(pal(7), _type = "qualitative", axes = False)
    plt.close() # Closing figure instance

# Custom 'ax' argument
@pytest.mark.mpl_image_compare
def test_hclplot_qualitative_custom_ax():
    fig,ax = plt.subplots(1, 1)
    with pytest.warns(UserWarning, match = r"^cannot approximate L well as a linear function of C and H$"):
        ax = hclplot(rainbow()(10), ax = ax)
    assert isinstance(ax, plt.Axes)
    plt.show()  # Show custom figure
    plt.close() # Closing figure instance


