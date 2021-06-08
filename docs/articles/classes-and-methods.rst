


.. _article-classes-and-methods:


Classes and methods
===================

:py:class:`colorspace.palettes.palette` is used to create custom named palettes
based on a fixed number of hex colors. Used to provide the same functionality
for non-colorspace palettes such as creating a ``specplot()`` or ``swatchplot()``.

.. todo::
    Not working as expected, rethink. ``cmap()`` and ``swatchplot()`` not woking.

.. ipython::

    import colorspace
    pal = colorspace.palette(["#c3c3c3", "#DD0000"])


.. autosummary::
    :toctree: ../generated/
    :nosignatures:

    colorspace.qualitative_hcl
    colorspace.sequential_hcl
    colorspace.diverging_hcl
    colorspace.rainbow_hcl
    colorspace.heat_hcl
    colorspace.terrain_hcl
    colorspace.diverging_hsv

:py:class:`colorspace.palettes.defaultpalette` not intended to be used by the user.
Reads the config files (shipped with the python package) and returns all available
default palettes. Called by :py:class:`colorspace.palettes.hclplaettes`.


:py:class:`colorspace.palettes.hclpalette` serves as the parent class for the
following color palettes.

:py:class:`colorspace.palettes.qualitative_hcl`

:py:class:`colorspace.palettes.diverging_hcl`

:py:class:`colorspace.palettes.sequential_hcl`


:py:class:`colorspace.palettes.rainbow_hcl` convenience palette for qualitative HCL rainbow.
:py:class:`colorspace.palettes.heat_hcl` HCL approximation of Rs old heat palette.
:py:class:`colorspace.palettes.terrain_hcl` HCL approxmation of Rs terrain palette.

:py:class:`colorspace.palettes.diverging_hsv` HSV based diverging color palette.

