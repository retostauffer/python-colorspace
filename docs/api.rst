#############
API Reference
#############

.. currentmodule:: python-colorspace

.. _sec-references:



Color palettes
==============

Most functions listed above are exported and can be accessed
directly via the `colorspace` package, such as 
`colorspace.hcl_palettes()`, `colorspace.qualitative_hcl()` and more.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    colorspace.hcl_palettes.hcl_palettes
    colorspace.palettes.qualitative_hcl
    colorspace.palettes.sequential_hcl
    colorspace.palettes.diverging_hcl
    colorspace.palettes.rainbow_hcl
    colorspace.palettes.heat_hcl
    colorspace.palettes.terrain_hcl
    colorspace.palettes.palette
    colorspace.palettes.diverging_hsv
    colorspace.palettes.defaultpalette

GUI for choosing color palettes
================================

Exported function, can be accessed via `colorspace.choose_palette()`.

.. autosummary::
    :toctree: generated/
    :nosignatures:
    
    colorspace.choose_palette.choose_palette


Assessing colors and palettes
=============================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    colorspace.specplot.specplot
    colorspace.swatchplot.swatchplot


Color vision defficiency
========================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    colorspace.CVD.CVD
    colorspace.CVD.desaturate
    colorspace.CVD.deutan
    colorspace.CVD.protan
    colorspace.CVD.tritan


Color library/color transformations
===================================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    colorspace.colorlib

