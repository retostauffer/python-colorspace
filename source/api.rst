#############
API Reference
#############


.. _sec-references:


Color palettes
==============


Most functions listed above are exported and can be accessed
directly via the `colorspace` package, such as 
`colorspace.hcl_palettes()`, `colorspace.qualitative_hcl()` and more.

.. currentmodule:: colorspace

.. autosummary::
    :toctree: api/
    :nosignatures:

    hcl_palettes
    qualitative_hcl
    sequential_hcl
    diverging_hcl
    rainbow_hcl
    heat_hcl
    terrain_hcl
    rainbow
    palette
    diverging_hsv


GUI for choosing color palettes
================================

Exported function, can be accessed via `colorspace.choose_palette()`.


.. currentmodule:: colorspace.choose_palette

.. autosummary::
    :toctree: api/
    :nosignatures:

    choose_palette


Assessing colors and palettes
=============================

.. currentmodule:: colorspace

.. autosummary::
    :toctree: api/
    :nosignatures:

    specplot
    swatchplot


Color vision defficiency
========================

.. currentmodule:: colorspace.CVD

.. autosummary::
    :toctree: api/
    :nosignatures:

    CVD
    desaturate
    deutan
    protan
    tritan


Color manipulation
==================

.. currentmodule:: colorspace

.. autosummary::
    :toctree: api/
    :nosignatures:

    max_chroma
    contrast_ratio
    lighten
    darken

Color library/color transformations
===================================

.. currentmodule:: colorspace.colorlib

.. autosummary::
    :toctree: api/
    :nosignatures:

    polarLUV
    HCL
    CIELUV
    CIEXYZ
    RGB
    sRGB
    CIELAB
    polarLAB
    HSV
    HLS
    hexcols
