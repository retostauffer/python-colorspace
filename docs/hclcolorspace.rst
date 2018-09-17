
.. _page-hclcolorspace:

The HCL Color Space
====================

The most well known color space is the Red-Green-Blue (RGB) color
space. The RGB color space is based the technical demand of 
digital screens such as computer monitors or TVs.
The color of each individual pixel on a screen is created by mixing
intensities of red, green, and blue (additive color mixture) to create
the picture we can see.

In contrast, the Hue-Chroma-Luminance color space is based on how
human color perception works. In contrast to computer screens our visual
system (eye-brain) is processing visual information in the dimension of
luminance (the lightness of an object), chroma (the colorfulness) and hue
(the actual color tone).

The Hue-Chroma-Luminance color space allows us to directly control each
of these three dimensions. The swatch plot below illustrates how this works.
Each of the three swatches varies only one specific dimension (hue, chroma,
and luminance) while all others are held constant.
Thus, all colors in the top swatch exhibit the same lightness and same color
intensity while only the hue changes from left to right from reddish over greenish,
blueish, back to red.
The second swatch has constant luminance and hue, but varies from zero chroma
(pure gray) on the left hand side to a vivid red.
The last swatch goes from black (zero luminance) to white (full luminance)
with zero chroma which yields pure gray scale colors.

.. raw:: html
    :file: examples/example_hclspace.html

.. _hcl-dimensions:


Path trough the HCL space
-------------------------

The properties of the HCL color space allows to draw well-defined
and effective color palettes from the HCL color space. One example
are the :ref:`diverging-color-palettes`.
The design principle of diverging color palettes is that both ends
of the spectrum have the same luminance and chroma to not distort the
data and add artificial weight to one side or the other.
The only property which changes from one end to the other is the hue
(e.g., from red to blue).


The animation below shows the HCL color space as a volume and the path of the
default :ref:`diverging-color-palettes` ("Blue-Red") trough the space. The
vertical axis shows the luminance dimension from ``L=0`` (black) to ``L=100``
(white), hue and chroma are shwon on the XY plane. The angle (from ``H=0`` to
``H=360``; cyclic) defines the hue, the radial distance to the center the
chroma.

.. image:: _static/HCL_space.gif

The solid line inside the volume shows the path of the "Blue-Red" color
palette with 11 unique colors.
Both sides of the palette proceed linearly from a neutral center point
with 90% luminance (``L=90``) and no chroma to a dark blue (``H=260``; constant)
and a dark red (``H=0``; constant) with equal luminance (``L=30``) and equal
chroma (``C=80``). 

This yields a well balanced diverging color map shown in the top left
corner of the animation with equal weights on both ends which can easily
be adjusted by adjusting the start and end point of the path without
and preserve the well defined and monotonic behavior of the overall palette.
Variations of the "Blue-Red" diverging color map can be found on the
":ref:`default color palette page <page-defaultpalettes>`".


.. _apple-example:

Why is the Luminance Important
------------------------------

The following non-technical example illustrates why it is beneficial to have
direct control over the luminance dimension.  The image below shows a juicy and
delicious apple. Our visual system needs only the blink of an eye to identify
the object as what it is.

.. raw:: html
    :file: examples/example_apple.html

This simple example illustrates how false or missing luminance information
can quickly obscure the information of a figure or graph.
Even with additional attributes on top (hue/chroma) the underlying luminance
information is processed by our visual system and helps us to gather the
information we are looking at. If used in a wrong way, colors can easily
wreck the effectiveness of a (scientific) visualization and might, in a
worst case, even mislead the reader in a way that he is perceiving something
else or at least focussing on the wrong aspects of the image.

And here the python-colorspace package can help you out with designing
effective color maps, investigate the properties of a new or existing
color palette, and more.


.. _effective-color-palettes:

Effective Color Palettes
------------------------

.. todo::
    Introduction to the three basic principles of the
    diverging, sequential, and qualitative color maps.









