Palettes
========

The `palettes` module provides a user-friendly interface
to HCL based color palettes.

.. image:: ../_static/img_palettes.jpeg


Rainbow HCL
-----------

.. autoclass:: palettes.rainbow_hcl
    :members:

Qualitative HCL
---------------

.. autoclass:: palettes.qualitative_hcl
    :members:

Diverging HCL
-------------

.. autoclass:: palettes.diverging_hcl
    :members:

Sequential HCL
---------------

.. autoclass:: palettes.sequential_hcl
    :members:

HCL Palette Baseclass
---------------------

The different HCL color palettes
(:py:class:`palettes.rainbow_hcl`, :py:class:`palettes.diverging_hcl`,
:py:class:`palettes.qualitative_hcl`) are extending tihs
:py:class:`palettes.hclpalette` base class. 

The :py:class:`palettes.hclpalette` class provides several
methods to interact with the HCL palette objects
above to e.g., extract colors or check the current
palette settings.

.. autoclass:: palettes.hclpalette
    :members:


Other Methods
=============

.. autoclass:: palettes.palette

.. autoclass:: palettes.hclpalette
