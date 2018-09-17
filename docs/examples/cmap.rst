Matolotlib cmaps
================

For demonstration the `3D surface demo <https://matplotlib.org/examples/mplot3d/surface3d_demo.html>`_
is used to demonstrate the colorspace cmap functionality.
The code for the demo can be :ref:`a the end of this page <cmap-demofun>`.

HCL Color Palettes
------------------

.. raw:: html
    :file: example_cmap1.html

All :py:class:`palettes.hclpalette` objects provide a method called
:py:func:`palettes.hclpalette.cmap` method which returns a matplotlib color map
with ``n`` colors (default ``51``).

The example below shows the demo with the "Green-Orange" :py:class:`palettes.diverging_hcl`
color palette and the "Purple-Orange" :py:class:`palettes.sequential_hcl` color palette in
the top row, and the "Set 2" :py:class:`palettes.qualitative_hcl` and a matplotlib default
color map called ``gist_ncar`` in the bottom row.

**Please note:** that none of the two shown in the bottom row should be used to
illustrate such a data set. The :py:class:`palettes.qualitative_hcl` color map
has iso-chroma (constant color intensity) and iso-luminance (constant
lightness) and only varies in the hue dimension (the color itself).  Such
palettes are made for classification tasks and not to display a data set as
shown in the demo.  The ``gist_ncar`` palette should also not be used due to
the immense discontinuity across the palette (I've chosen this as one of the
worst examples among the matplotlib color maps). More information about
:ref:`effective color palettes <effective-color-palettes>` can be found
:ref:`on this page <effective-color-palettes>`.

.. raw:: html
    :file: example_cmap2.html

Color Vision Deficiency
-----------------------

The color vision deficiency (CVD) toolbox of the colorspace package also
allows to simulate color vision deficiencies on
``matplotlib.colors.LinearSegmentedColormap`` color maps.

.. raw:: html
    :file: example_cmap3.html

The figure above shows the very same color map (the "Blue-Red" default
:py:class:`palettes.diverging_hcl` palette) in four different versions.
Top left is the original color map as people without visual constraints
perceive the colors. Top right is a desaturated version where all the
color information is removed. This yields a pure gray scale color map, and
as the diverging color maps are well balanced, to equal gray on both ends
of the spectrum.

The bottom row shows how people with a deuteranomaly (commonly known as "red-green
blindness"; left) and protanomaly (less common, known as "blue-yellow blindness"; right)
perceive the very same color map. Except for the desaturated version the color
map works quite well and even under visual constraints the association between
color and the actual value is possible without any problem.
For other color maps this might not be true and the effectiveness of a color map
can rapidly collapse under certain visual constraints. Thus, always think of who
receives the figures and graphs, and whether or not it is important that
color vision deficiency has to be considered or not (most often the answer is: yes!).

.. _cmap-demofun:

The Demo Function
-----------------

The output below shows the ``demo`` function used on this page.
It is a modified version of the
`3D surface <https://matplotlib.org/examples/mplot3d/surface3d_demo.html>`_ example.

.. literalinclude:: example_cmap_demo.py
   :language: python


