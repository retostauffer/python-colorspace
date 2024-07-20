
from colorspace.colorlib import hexcols
from colorspace import palette, contrast_ratio
import numpy as np

import pytest
from pytest import raises

try:
    from matplotlib import pyplot as plt
    from matplotlib.axes import Axes
    _got_mpl = True
except:
    _got_mpl = False

# ------------------------------------------
# Wrong usage
# ------------------------------------------
def test_wrong_usage():

    # Input missing
    raises(TypeError,  contrast_ratio)

    # Unknown argument
    raises(TypeError,  contrast_ratio, cols = "#ff0033")

    # Argument 'cols'
    raises(TypeError,  contrast_ratio, colors = 1) # integer
    raises(ValueError, contrast_ratio, colors = "foo")                # no hex color
    raises(ValueError, contrast_ratio, colors = ["#FF00FF", "foo"])   # invalid hex

    # Argument 'bg'
    raises(ValueError,  contrast_ratio, colors = "foo") # invalid hex
    raises(ValueError,  contrast_ratio, colors = "#FF00") # invalid hex
    raises(ValueError,  contrast_ratio, colors = ["#FF00FF", "foo"]) # invalid hex


@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_wrong_usage_plot():
    # Argument 'plot'
    raises(TypeError,  contrast_ratio, colors = "#FF00FF", plot = "foo")
    # Testint argument 'ax'; wrong type of object
    raises(TypeError,  contrast_ratio, colors = "#F00", bg = "#000", plot = True, ax = "foo")


# ------------------------------------------
# Checking return values.
# ------------------------------------------

# Testing multiple colors on white bg.
# Testing len(colors) > len(bg)
def test_result_on_white_bg():

    # Checking against black
    cols = hexcols(["#FF0000", "#FFBF00", "#80FF00", "#00FF40",
                    "#00FFFF", "#0040FF", "#8000FF", "#FF00BF"])

    res_white1 = contrast_ratio(cols)
    res_white2 = contrast_ratio(cols, "#FFFFFF")
    sol_white  = np.asarray([3.998477, 1.652981, 1.294551, 1.365584,
                             1.253881, 6.609264, 6.246581, 3.497483])

    assert isinstance(res_white1, np.ndarray)
    assert isinstance(res_white2, np.ndarray)
    assert np.all(res_white1 == res_white2)
    assert np.all(np.isclose(res_white1, sol_white))


# Taking one main color but 5 different shaded of gray for background
# Testing len(colors) < len(bg)
def test_result_varying_bg():

    # Define background colors (shades of gray)
    cols_bg = ["#4D4D4D", "#888888", "#AEAEAE", "#CCCCCC", "#E6E6E6"]
    res = contrast_ratio("#ff0000", cols_bg)
    sol = np.asarray([2.114101, 1.127956, 1.802238, 2.489822, 3.203724])

    assert isinstance(res, np.ndarray)
    assert np.all(np.isclose(res, sol))


# ------------------------------------------
# Testing plot options
# ------------------------------------------
# Testing multiple colors on alternating white/black background.
# Testing auto-repeat, len(colors) > len(bg)
@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_result_on_bw_bg():

    # Checking against black
    cols = hexcols(["#FF0000", "#FFBF00", "#80FF00", "#00FF40",
                    "#00FFFF", "#0040FF", "#8000FF", "#FF00BF"])

    res_bw = contrast_ratio(cols, ["#FFFFFF", "#000000"])
    sol_bw = np.asarray([3.998477, 12.704321, 1.294551, 15.378033,
                         1.253881,  3.177358, 6.246581, 6.004318])

    res_bw = contrast_ratio(cols, ["#FFFFFF", "#000000"], plot = True)
    assert isinstance(res_bw, np.ndarray)
    assert np.all(np.isclose(res_bw, sol_bw))

@pytest.mark.skipif(not _got_mpl, reason = "Requires matplotlib")
def test_plot_options():

    from colorspace.colorlib import hexcols
    from colorspace import palette, contrast_ratio
    from matplotlib import pyplot as plt
    import numpy as np
    from matplotlib.axes import Axes
    from pytest import raises

    # Single axis
    fig, ax = plt.subplots()
    res = contrast_ratio("#F00", bg = "#000", plot = True, ax = ax)
    assert isinstance(res, Axes)
    plt.close()
    del fig, ax, res

    # Multiple subplots
    fig, axes = plt.subplots(2, 2)
    res = contrast_ratio("#F00", bg = "#000", plot = True, ax = axes[0, 0])
    assert isinstance(res, Axes)
    plt.close()
    del fig, axes, res

    # In case plot = False 'ax' should not be checked (object type neglected)
    res = contrast_ratio("#F00", bg = "#000", plot = False, ax = "foo")
    assert isinstance(res, np.ndarray)
    plt.close()
    del res

    # Plot set to True but ax = None (default)
    res = contrast_ratio("#F00", bg = "#000", plot = True, ax = None)
    assert isinstance(res, np.ndarray)
    plt.close()
    del res






