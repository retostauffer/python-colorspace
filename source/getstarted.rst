

colorspace: A Toolbox for Manipulating and Assessing Colors and Palettes
========================================================================


Overview The colorspace package provides a broad toolbox for selecting
individual colors or color palettes, manipulating these colors, and employing
them in various kinds of visualizations.

At the core of the package there are various utilities for computing with color
spaces (as the name of the package conveys). Thus, the package helps to map
various three-dimensional representations of color to each other. A
particularly important mapping is the one from the perceptually-based and
device-independent color model HCL (Hue-Chroma-Luminance) to standard
Red-Green-Blue (sRGB) which is the basis for color specifications in many
systems based on the corresponding hex codes (e.g., in HTML but also in R). For
completeness further standard color models are included as well in the package:
:py:class:`polarLUV<colorspace.colorlib.polarLUV>` (= :py:class:`HCL<colorspace.colorlib.HCL>`),
:py:class:`CIELUV<colorspace.colorlib.CIELUV>`,
:py:class:`polarLAB<colorspace.colorlib.polarLAB>`,
:py:class:`CIELAB<colorspace.colorlib.CIELAB>`,
:py:class:`CIEXYZ<colorspace.colorlib.CIEXYZ>`,
:py:class:`RGB<colorspace.colorlib.RGB>`,
:py:class:`sRGB<colorspace.colorlib.sRGB>`,
:py:class:`HLS<colorspace.colorlib.HLS>`,
:py:class:`HSV<colorspace.colorlib.HSV>`.

The HCL space (= polar coordinates in CIELUV) is particularly useful for
specifying individual colors and color palettes as its three axes match those
of the human visual system very well: Hue (= type of color, dominant
wavelength), chroma (= colorfulness), luminance (= brightness).

.. ipython:: python
    :okwarning:

    from colorspace import palette, sequential_hcl, swatchplot
    H = palette(sequential_hcl(h = [0, 300], c = 60, l = 65).colors(5), "Hue")
    C = palette(sequential_hcl(h = 0, c = [0, 100], l = 65).colors(5), "Chroma")
    L = palette(sequential_hcl(h = 0, c = 0, l = [90, 25]).colors(5), "Luminance")

    @savefig hcl_dimensions.png scale=100% align=center
    swatchplot([H, C, L], figsize = (3, 1.5))


The colorspace package provides three types of palettes based on the HCL model:

* _Qualitative_: Designed for coding categorical information, i.e., where no
  particular ordering of categories is available and every color should receive
  the same perceptual weight.
  Class: :py:class:`qualitative_hcl <colorspace.qualitative_hcl>`.
* _Sequential_: Designed for coding ordered/numeric information, i.e., where
  colors go from high to low (or vice versa).
  Class: :py:class:`sequential_hcl <colorspace.sequential_hcl>`.
* _Diverging_: Designed for coding ordered/numeric information around a central
  neutral value, i.e., where colors diverge from neutral to two extremes.
  Class: :py:class:`diverging_hcl <colorspace.diverging_hcl>`.

To aid choice and application of these palettes there are: scales for use with
matplotlib and an app for interactive exploration; visualizations of
palette properties; accompanying manipulation utilities (like desaturation,
lighten/darken, and emulation of color vision deficiencies).

.. todo:: Darken and lighten not yet implemented.

More detailed overviews and examples are provided in the articles:

.. toctree::
    :maxdepth: 1

    api
    articles/classes-and-methods
    articles/installation
    articles/color_spaces
    articles/colorlib
    articles/hcl_palettes
    articles/palette_visualization
    articles/hclwizard
    articles/color_vision_deficiency
    articles/manipulation_utilities
    articles/approximations
    articles/endrainbow

Installation
============

At the moment the package is available via [github](github)
`github.com/retostauffer/python-colorspace <https://https://github.com/retostauffer/python-colorspace>`_.
Note that `numpy <https://pypi.org/project/numpy/>`_ needs to be installed to be able to
use the package.
A `PyPI <https://pypi.org>`_ release is planned in the future.

**Requirements**:

* Python 2.7+ or Python 3+
* `numpy`

**Install via pip**

The package can be installed via `pip <https://pypi.org/project/pip/>`_ using
the following command:

.. code-block:: console

    pip install https://github.com/retostauffer/python-colorspace


**Clone git Repository**

Alternatively, clone the git repository and install the package:

.. code-block:: console

    git clone https://github.com/retostauffer/python-colorspace.git
    cd python-colorspace && python setup.py install


.. todo:: Update once released on PyPI.

Choosing HCL-based color palettes
=================================

The colorspace package ships with a wide range of predefined color palettes,
specified through suitable trajectories in the HCL (hue-chroma-luminance) color
space. A quick overview can be gained easily with the
:py:func:`hcl_palettes<colorspace.hcl_palettes>` function:


.. ipython:: python
    :okwarning:

    from colorspace import hcl_palettes
    @savefig hcl_palettes.png scale=100% width=900px height=600px
    hcl_palettes(plot = True, figsize = (15, 10))


A suitable palette object can be easily computed by specifying the desired
palette name (see the plot above), e.g.,

.. ipython:: python
    :okwarning:

    from colorspace import qualitative_hcl
    pal = qualitative_hcl("Dark 3")
    pal(4)  # Draw list of 4 colors across the palette


The functions :py:func:`sequential_hcl<colorspace.sequential_hcl>` and
:py:func:`diverging_hcl<colorspace.diverging_hcl>` work analogously.
Additionally, their hue/chroma/luminance parameters can be modified, thus
allowing for easy customization of each palette. Moreover, the
:py:func:`choose_palette<colorspace.choose_palette>` app provides a convenient user interfaces to perform
palette customization interactively.

.. todo::
    Adjust text when adding `divergingx_hcl()` (_Finally, even more
    flexible diverging HCL palettes are provided by divergingx_hcl()


Use with matplotlib graphics
============================

All color palettes come with a `cmap()` method to generate objects
of class `LinearSegmentedColormap` as used by the `matplotlib` and can
thus usually be passed directly to most matplotlib plotting functions, typically
trough the `cmap` argument. Here, a `pcolormesh()` example is shown using
the diverging HCL color palette "_Blue-Red__3_".

.. ipython:: python
    :okwarning:

    import matplotlib.pyplot as plt
    import numpy as np

    from colorspace import diverging_hcl
    pal = diverging_hcl("Blue-Red 3")

    np.random.seed(19680801)
    Z = np.random.rand(6, 10)
    x = np.arange(-0.5, 10, 1)  # len = 11
    y = np.arange(4.5, 11, 1)  # len = 7

    fig, ax = plt.subplots()
    dead_end = ax.pcolormesh(x, y, Z, cmap = pal.cmap())

    @savefig matplotlib_cmap.png scale=70% width=900px height=600px align=center
    plt.show()


As another example for a sequential palette, we demonstrate how to create a
line plot using `rainbowplot()` provided by the `statsmodels` package.
The Purples 3 palette is used which is quite similar to the
`ColorBrewer2.org<https://colorbrewer2.org/>`_ palette Purples.
Here, only two colors are employed, yielding a dark purple and a light gray.

.. todo::
    Currently using 'Purple' not 'Purple 3' as this is an advanced
    palette which is not yet implemented!

.. ipython:: python
    :okwarning:

    import numpy as np
    import matplotlib.pyplot as plt
    import statsmodels.api as sm
    data = sm.datasets.elnino.load(as_pandas = False)

    from colorspace import sequential_hcl
    #pal = sequential_hcl("Purples 3")
    pal = sequential_hcl("Purples")

    fig = plt.figure()
    ax = fig.add_subplot(111)
    res = sm.graphics.rainbowplot(data.raw_data[:, 1:], ax = ax, cmap = pal.cmap())
    dead_end = ax.set_xlabel("Month of the year")
    dead_end = ax.set_ylabel("Sea surface temperature (C)")
    dead_end = ax.set_xticks(np.arange(13, step=3) - 1)
    dead_end = ax.set_xticklabels(["", "Mar", "Jun", "Sep", "Dec"])
    dead_end = ax.set_xlim([-0.2, 11.2])

    @savefig statsmodels_purples.png scale=60% width=900px height=600px align=center
    plt.show()


Palette visualization and assessment
====================================

The colorspace package also provides a number of functions that aid
visualization and assessment of its palettes.


.. currentmodule:: colorspace.demos

.. autosummary::
    :toctree: demos/

    Bar
    Pie
    Spine
    Heatmap
    Matrix
    Lines
    Spectrum

.. currentmodule:: colorspace.specplo

.. autosummary::
    :toctree: demos/

    specplot







