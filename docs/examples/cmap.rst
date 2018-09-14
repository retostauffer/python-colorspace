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
:py:func:`palettes.hclpalette.cmap` method which returns a matplotlib color map with ``n``
colors (default ``51``).

The example below shows the demo with the "Green-Orange" :py:class:`diverging_hcl`
color palette and the "Purple-Orange" :py:class:`sequential_hcl` color palette in
the top row, and the "Set 2" :py:class:`qualitative_hcl` and a matplotlib default
color map called ``gist_ncar`` in the bottom row.

**Please note:** that none of the two shown in the bottom row should be used to
plut such a data set. The :py:class:`qualitative_hcl` color map has iso-chroma
(color intensity) and iso-luminance (lightness) and only varies in hue (the color itself).
Such palettes are made for classification tasks and not to display a data set as shown
in the demo plot. The ``gist_ncar`` palette should also not be used due to the
immense discontinuity across the palette. More information about
:ref:`effective color palettes <effective-color-palettes>` can be found
:ref:`on this page <effective-color-palettes>`.

.. raw:: html
    :file: example_cmap2.html

Color Vision Deficiency
-----------------------

The CVD toolbox of the colorspace package also allowes to
simulate color vision deficiencies on ``matplotlib.colors.LinearSegmentedColormap``
color maps.

.. raw:: html
    :file: example_cmap3.html


.. _cmap-demofun:

The Demo Function
-----------------

The output below shows the ``demo`` function used on this page.
It is a modified version of the
`3D surface <https://matplotlib.org/examples/mplot3d/surface3d_demo.html>`_ example.

.. literalinclude:: example_cmap_demo.py
   :language: python

