
.. _article-color_spaces:


Color Spaces: Classes and Utilities
===================================

Overview
--------

At the core of the *colorspace* package are various utilities for computing with
color spaces :cite:`cs-color:Wiki+Colorspace`, as the name conveys. Thus, the package helps to
map various three-dimensional representations of color to each other :cite:`cs-color:Ihaka:2003`.
A particularly important mapping is the one from the perceptually-based
and device-independent color model HCL (Hue-Chroma-Luminance) to standard
Red-Green-Blue (sRGB) which is the basis for color specifications in many
systems based on the corresponding hex codes :cite:`cs-color:Wiki+Webcolors`, e.g., in HTML
but also in Python. For completeness further standard color models are included as
well in the package. Their connections are illustrated in the following graph:


.. image:: images/colorspaces.png
    :width: 80%
    :alt: Color spaces and their connection.
    :align: center

.. currentmodule:: colorspace.colorlib

Color models that are (or try to be) perceptually-based are displayed with
circles and models that are not are displayed with rectangles. The
corresponding classes in *colorspace* are:


* :py:class:`RGB`
  for the classic Red-Green-Blue color model, which mixes three primary
  colors with different intensities to obtain a spectrum of colors. The
  advantage of this color model is (or was) that it corresponded to how
  computer and TV screens generated colors, hence it was widely adopted and
  still is the basis for color specifications in many systems. For example, hex
  color codes are employed in HTML but also in Python. However, the RGB model also
  has some important drawbacks: It does not take into account the output device
  properties, it is not perceptually uniform (a unit step within RGB does not
  produce a constant perceptual change in color), and it is unintuitive for
  humans to specify colors (say brown or pink) in this space.
  :cite:`cs-color:Wiki+Colorspace`
* :py:class:`sRGB`
  addresses the issue of device dependency by adopting a so-called
  gamma correction. Therefore, the gamma-corrected standard RGB (sRGB), as
  opposed to the linearized RGB above, is a good model for specifying colors in
  software and for hardware. But it is still unintuitive for humans to work
  directly with this color space. Therefore, sRGB is a good place to end up in
  a color space manipulation but it is not a good place to start.
  :cite:`cs-color:Wiki+sRGB`
* :py:class:`HSV`
  is a simple transformation of the (s)RGB space that tries to capture
  the perceptual axes: hue (dominant wavelength, the type of color), saturation
  (colorfulness), and value (brightness, i.e., light vs. dark). Unfortunately,
  the three axes in the HSV model are confounded so that, e.g., brightness
  changes dramatically with hue. :cite:`cs-color:Wiki+Webcolors`
* :py:class:`HSL`
  (Hue-Lightness-Saturation) is another transformation of (s)RGB that
  tries to capture the perceptual axes. It does a somewhat better job but the
  dimensions are still strongly confounded.
  :cite:`cs-color:Wiki+HSV`
* :py:class:`CIEXYZ`
  was established by the CIE (Commission Internationale de l’Eclairage)
  based on experiments with human subjects. It provides a unique triplet of XYZ
  values, coding the standard observer’s perception of the color. It is
  device-independent but it is not perceptually uniform and the XYZ coordinates
  have no intuitive meaning.
  :cite:`cs-color:Wiki+CIEXYZ`
* :py:class:`CIELUV` and :py:class:`CIELAB`
  were therefore proposed by the CIE as perceptually
  uniform color spaces where the former is typically preferred for emissive
  technologies (such as screens and monitors) whereas the latter is usually
  preferred when working with dyes and pigments. The L coordinate in both
  spaces has the same meaning and captures luminance (light-dark contrasts).
  Both the U and V coordinates as well as the A and B coordinates measure
  positions on red/green and yellow/blue axes, respectively, albeit in somewhat
  different ways. While this corresponds to how human color vision likely
  evolved (see the next section), these two color models still not correspond
  to perceptual axes that humans use to describe colors.
  :cite:`cs-color:Wiki+HSV,color:Wiki+CIELAB`
* :py:class:`polarLUV` (= :py:class:`HCL`) and :py:class:`polarLAB`
  therefore take polar coordinates in the UV plane
  and AB plane, respectively. Specifically, the polar coordinates of the LUV
  model are known as the HCL (Hue-Chroma-Luminance) model (see :cite:t:`cs-color:Wiki+HCL`,
  which points out that the LAB-based polar coordinates are also sometimes
  referred to as HCL). The HCL model captures the human perceptual axes very
  well without confounding effects as in the HSV or HLS approaches (more
  details follow below).


Human color vision and the HCL color model
------------------------------------------

It has been hypothesized that human color vision has evolved in three distinct stages:

1. Perception of light/dark contrasts (monochrome only).
2. Yellow/blue contrasts (usually associated with our notion of warm/cold colors).
3. Green/red contrasts (helpful for assessing the ripeness of fruit).

See :cite:t:`cs-color:Kaiser+Boynton:1996,cs-color:Knoblauch:2002,cs-color:Ihaka:2003,cs-color:dichromat`
and/or :cite:t:`color:Zeileis+Hornik+Murrell:2007` for more details and references.
Thus, colors can be described using a 3-dimensional space:



.. image:: images/human-axes.svg
    :width: 50%
    :alt: Representation of the three axis of human color vision.
    :align: center

However, for describing colors in such a space, it is more natural for humans
to employ polar coordinates in the color plane (yellow/blue vs. green/red,
visualized by the dashed circle above) plus a third light/dark axis. Hence,
color models that attempt to capture these perceptual axes are also called
perceptually-based color spaces. As already argued above, the HCL model
captures these dimensions very well, calling them: hue, chroma, and luminance.

The corresponding sRGB gamut, i.e., the HCL colors that can also be represented
in sRGB, is visualized in the animation below :cite:p:`cs-color:Horvath+Lipka:2016`.

* `Link to video (wikimedia.org) <https://upload.wikimedia.org/wikipedia/commons/transcoded/8/8d/SRGB_gamut_within_CIELCHuv_color_space_mesh.webm/SRGB_gamut_within_CIELCHuv_color_space_mesh.webm.480p.vp9.webm>`_


The shape of the HCL space is a distorted double cone which is seen best by
looking at vertical slices, i.e., chroma-luminance planes for given hues. For
example, the left panel below depicts the chroma-luminance plane for a certain
blue (hue = 255). Along with luminance the colors change from dark to light.
With increasing chroma the colors become more colorful, where the highest
chroma is possible for intermediate luminance.

As some colors are relatively dark (e.g., blue and red assume their maximum
chroma for relatively low luminances) while others are relatively light (e.g.,
yellow and green), horizontal slices of hue-chroma planes for given hue have
somewhat irregular shapes. The right panel below shows such a hue-chroma plane
for moderately light colors (luminance = 70). At that luminance, green and
orange can become much more colorful compared to blue or red.


.. image:: images/hcl-projections-1.png
    :width: 100%
    :align: center


Illustration of basic *colorspace* functionality
------------------------------------------------

As an example a vector of colors x can be specified in the HCL (or polar LUV)
model:

.. ipython:: python
    :okwarning:

    from colorspace.colorlib import HCL
    x = HCL(H = [0, 120, 240], C = [50.] * 3, L = [70.] * 3)
    print(x)

The resulting three colors are pastel red (hue = 0), green (hue = 120), and
blue (hue = 240) with moderate chroma and luminance. For display in other
systems an sRGB representation might be needed:

.. ipython:: python
    :okwarning:

    x.to("sRGB")    # Convert to sRGB coordinates
    print(x)

The displayed coordinates can also be extracted as numeric matrices by
:py:func:`x.get() <colorobject.get>` to get the values of all or a specific
coordinate of the color space the :py:class:`colorobject` is currently in.
As an example we convert the three colors to the :py:class:`HSV` color space
and extract the saturation coordinate only by calling :py:func:`x.get("S") <HSV.get>`:

.. ipython:: python
    :okwarning:

    x.to("HSV")
    print(x)
    print(x.get("S"))     # Saturation dimension only

For display in many systems hex color codes based on the
sRGB coordinates can be created:

.. ipython:: python
    :okwarning:

    print(x.colors())     # Automatically converts to hex


Color library
-------------

The workhorse of these transformations is the
:py:class:`colorlib` class which allows to transform
:py:class:`colorobject` objects into each other.

.. autosummary::
    :toctree: ../colorlib/
    :nosignatures:

    colorlib
    colorobject

The following classes (all inheriting from :py:class:`colorobject`) are
available to create colors in different color spaces. Colors can be transformed
from and to (mostly all) color spaces using the
``.to(\<name of color space\>)`` method (see e.g., :py:func:`hexcols.to`).

.. currentmodule:: colorspace.colorlib

.. autosummary::
    :toctree: ../colorlib/
    :nosignatures:

    CIELAB
    CIELUV
    CIEXYZ
    HLS
    HSV
    RGB
    hexcols
    polarLAB
    HCL
    polarLUV
    sRGB


Matplotlib color maps
---------------------

In addition many objects provided by the *colorspace* package allow to convert a
series of colors (color palette) into a
:py:class:`matplotlib.colors.LinearSegmentedColormap`
'cmap' used by matplotlib. As an example using the object ``x`` from above:

.. ipython:: python
    :okwarning:

    from colorspace import palette
    cmap = palette(x, "custom palette").cmap()
    print(cmap.N)


Please note that matplotlib performs linear interpolation in the sRGB color
space between the colors specified. This allows us to draw more than 3 colors
from the color map above. However, this may result in skewed color gradients!

.. currentmodule:: colorspace

The better way to go is to define/design your custom palette in the
HCL color space using :py:class:`qualitative_hcl`,
:py:class:`diverging_hcl`, :py:class:`sequential_hcl` among others
(see :ref:`HCL-Based Color Palettes <article-hcl_palettes>` for details).

These classes define color palettes via functions in the HCL color space
and allow to draw large numbers of colors along the function space.
The :py:func:`.cmap() <colorspace.palettes.hclpalette.cmap>` method will still return a 
:py:class:`LinearSegmentedColormap <matplotlib.colors.LinearSegmentedColormap>`
but (by default) based on ``N = 101`` distinct colors which will require
less linear interpolation.

.. ipython:: python
    :okwarning:

    from colorspace import diverging_hcl
    pal  = diverging_hcl("Green-Orange")
    cmap = pal.cmap()
    print(cmap.N)

A simple example using :py:func:`matplotlib.pyplot.contourf`
with a custom HCL based color palette
(``sequential_hcl("Rocket").cmap()``):

.. plot::
    :align: center
    :width: 70%

    import matplotlib.pyplot as plt
    import numpy as np
    from numpy import ma
    from matplotlib import ticker, cm

    # Custom color map
    from colorspace import sequential_hcl
    cmap = sequential_hcl("Rocket").cmap()

    N = 100
    x = np.linspace(-3.0, 3.0, N)
    y = np.linspace(-2.0, 2.0, N)
    X, Y = np.meshgrid(x, y)

    # A low hump with a spike coming out.
    # Needs to have z/colour axis on a log scale so we see both hump and spike.
    # linear scale only shows the spike.
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X * 10)**2 - (Y * 10)**2)
    z = Z1 + 50 * Z2

    # Put in some negative values (lower left corner) to cause trouble with logs:
    z[:5, :5] = -1

    # The following is not strictly essential, but it will eliminate
    # a warning.  Comment it out to see the warning.
    z = ma.masked_where(z <= 0, z)

    # Automatic selection of levels works; setting the
    # log locator tells contourf to use a log scale:
    # Matlplotlib.contourf decides to draw 9 levels
    fig, ax = plt.subplots()
    cs = ax.contourf(X, Y, z, locator=ticker.LogLocator(), cmap=cmap)

    plt.show()



References
----------

.. bibliography:: ../references.bib
    :cited:
    :style: plain
    :labelprefix: CS
    :keyprefix: cs-


