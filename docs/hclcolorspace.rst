
.. _page-hclcolorspace:

The HCL Color Space
====================

The most well known color space is the Red-Green-Blue (RGB) color
space. The RGB color space is mainly based on the technical
specification of digital screens such as computer screens or TVs.
The color of each individual pixel on a screen is created by mixing
intensities of red, green, and blue (additive color mixture).

In contrast, the Hue-Chroma-Luminance color space is based on how
human color perception works.

.. raw:: html
    :file: examples/example_hclspace.html

.. _hcl-dimensions:

Path trough the HCL space
-------------------------

The animation shows the HCL color space as a volume. The vertical
axis shows the luminance dimension from ``L=0`` (black) to ``L=100`` (white),
hue and chroma are shwon on the XY plane. The angle (from ``H=0`` to ``H=360``; cyclic)
shows defines the hue, the radial distance to the center the chroma.

.. image:: _static/HCL_space.gif

The solid line inside the volume shows the path of the default
:py:class:`diverging_hcl` color map (with ``n=11`` colors) trough the HCL
color space. 


.. _apple-example:

Importance of the luminance dimension
-------------------------------------

.. raw:: html
    :file: examples/example_apple.html

This simple example shows the effect of the luminance information.
Even if additional color coding is used on top the luminance information
is still processed by our brain and can either support the reader if used
in an effective way, or make it hard or even impossible to gather the
most important information if used without caution.

.. _effective-color-palettes:

Effective Color Palettes
------------------------

The colorspace package provides an easy to use interface to choose effective
color maps based on the HCL color space.

.. todo::
    To be done ...


