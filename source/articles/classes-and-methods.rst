


.. _article-classes-and-methods:


Main classes and methods
========================

Overview
--------

At the core of the *colorspace* package are various utilities for computing with
color spaces (:cite:Wikipedia 2020d), as the name conveys. Thus, the package helps to
map various three-dimensional representations of color to each other (Ihaka
2003). A particularly important mapping is the one from the perceptually-based
and device-independent color model HCL (Hue-Chroma-Luminance) to standard
Red-Green-Blue (sRGB) which is the basis for color specifications in many
systems based on the corresponding hex codes (Wikipedia 2020i), e.g., in HTML
but also in R. For completeness further standard color models are included as
well in the package. Their connections are illustrated in the following graph:

.. todo::
    colorspace.palette: rethink. ``cmap()`` and ``swatchplot()`` not woking as expected?

.. ipython:: python
    :okwarnings:

    import colorspace
    pal = colorspace.palette(["#c3c3c3", "#DD0000"])

.. currentmodule:: colorspace

.. autosummary::
    :toctree: ../api/
    :nosignatures:

    hclpalettes
    palette
    qualitative_hcl
    diverging_hcl
    sequential_hcl
    rainbow_hcl
    heat_hcl
    terrain_hcl
    diverging_hsv

    tritan
    protan
    deutan
    desaturate

    hcl_palettes
    swatchplot
    specplot
    choose_palette
    cvd_emulator



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

