
.. currentmodule:: python-colorspace

.. _article-colorspace:

colorspace
============

Template. TODO

Testing ipython
===============

.. ipython:: python
    :okwarning:

    from colorspace import palette, sequential_hcl, swatchplot
    H = palette(sequential_hcl(h = [0, 300], c = 60, l = 65).colors(5), "Hue")
    C = palette(sequential_hcl(h = 0, c = [0, 100], l = 65).colors(5), "Chroma")
    L = palette(sequential_hcl(h = 0, c = 0, l = [90, 25]).colors(5), "Luminance")

    @savefig hcl_dimensions.png scale=100% align=center
    swatchplot([H, C, L], figsize = (3, 1.5))

.. ipython:: python
    :okwarning:

    from colorspace import hcl_palettes

    hcl_palettes()

    @savefig hcl_palettes.png scale=100% width=900px height=600px
    hcl_palettes(plot = True, figsize = (15, 10))

