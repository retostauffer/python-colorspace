
.. _article-hcl_palettes:

HCL based color palettes
========================


As motivated in the previous article (:ref:`article-color_spaces`),
the HCL space is particularly useful for specifying individual colors and
color palettes, as its three axes match those of the human visual system very
well. Therefore, the *colorspace* package provides three types of palettes based
on the HCL model:

* *Qualitative*: Designed for coding categorical information, i.e., where no
  particular ordering of categories is available and every color should receive
  the same perceptual weight.
* *Sequential*: Designed for coding ordered/numeric information, i.e., going
  from high to low (or vice versa).
* *Diverging*: Designed for coding ordered/numeric information around a central
  neutral value, i.e., where colors diverge from neutral to two extremes.


The corresponding functions are
:py:func:`qualitative_hcl<colorspace.palettes.qualitative_hcl>`,
:py:func:`sequential_hcl<colorspace.palettes.sequential_hcl>`, and
:py:func:`diverging_hcl<colorspace.palettes.diverging_hcl>`.
Their construction principles are exemplified in the following
color swatches and explained in more detail below. The desaturated palettes
bring out clearly that luminance differences (light-dark contrasts) are crucial
for sequential and diverging palettes while qualitative palettes are balanced
at the same luminance.

.. ipython:: python
    :okwarning:

    from colorspace import *

    qual_pal = qualitative_hcl("Set 2")
    qual1 = palette(qual_pal(5), "Color")
    qual2 = palette(desaturate(qual_pal(5)), "Desaturated")

    seq_pal = sequential_hcl("Blues")
    seq1 = palette(seq_pal(5), "Color")
    seq2 = palette(desaturate(seq_pal(5)), "Desaturated")

    div_pal = diverging_hcl("Green-Brown")
    div1 = palette(div_pal(5), "Color")
    div2 = palette(desaturate(div_pal(5)), "Desaturated")

    @savefig hcl_palettes_dimensions.png width=600px height=90px align=center
    swatchplot({"Qualitative (Set 2)":     [qual1, qual2],
                "Sequential (Blues 3)":    [seq1, seq2],
                "Diverging (Green-Brown)": [div1, div2]},
                nrow = 3, figsize = (10, 1.5))


More details about the construction of such palettes is provided in the
following while the article on :ref:`article-palette_visualization` Palette
Visualization and Assessment introduces further tools to better understand the
properties of color palettes.

To facilitate obtaining good sets of colors, HCL parameter combinations that yield useful palettes are accessible by name. These can be listed using the function hcl_palettes():

Graphical user interface (GUI)
==============================

``choose_palette()``.

.. image:: ../_static/img_gui.jpeg

Create custom palettes
----------------------

Function reference
------------------

.. autofunction:: colorspace.choose_palette
    :noindex:

