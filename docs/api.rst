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

    colorspace.cls.cls
    colorspace.hcl_palettes
    colorspace.qualitative_hcl
    colorspace.sequential_hcl
    colorspace.diverging_hcl
    colorspace.rainbow_hcl
    colorspace.heat_hcl
    colorspace.terrain_hcl
    colorspace.palette
    colorspace.diverging_hsv
    colorspace.palettes.defaultpalette

GUI for choosing color palettes
================================

Exported function, can be accessed via `colorspace.choose_palette()`.

.. autosummary::
    :toctree: api/
    :nosignatures:
    
    colorspace.choose_palette.choose_palette


Assessing colors and palettes
=============================

.. autosummary::
    :toctree: api/
    :nosignatures:

    colorspace.specplot.specplot
    colorspace.swatchplot.swatchplot


Color vision defficiency
========================

.. autosummary::
    :toctree: api/
    :nosignatures:

    colorspace.CVD.CVD
    colorspace.CVD.desaturate
    colorspace.CVD.deutan
    colorspace.CVD.protan
    colorspace.CVD.tritan


Color library/color transformations
===================================

.. autosummary::
    :toctree: api/
    :nosignatures:

    colorspace.colorlib

