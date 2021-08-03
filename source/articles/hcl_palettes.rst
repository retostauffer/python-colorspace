
.. _article-hcl_palettes:

HCL-Based Color Palettes
========================

.. currentmodule:: colorspace

As motivated in the previous article (:ref:`article-color_spaces`),
the HCL space is particularly useful for specifying individual colors and
color palettes, as its three axes match those of the human visual system very
well. Therefore, the *colorspace* package provides three types of palettes based
on the HCL model:

* *Qualitative:* Designed for coding categorical information, i.e., where no
  particular ordering of categories is available and every color should receive
  the same perceptual weight.
* *Sequential:* Designed for coding ordered/numeric information, i.e., going
  from high to low (or vice versa).
* *Diverging:* Designed for coding ordered/numeric information around a central
  neutral value, i.e., where colors diverge from neutral to two extremes.

The corresponding classes are :py:class:`qualitative_hcl`,
:py:class:`sequential_hcl`, and :py:class:`diverging_hcl`.
Their construction principles are exemplified in the following
color swatches and explained in more detail below. The desaturated palettes
bring out clearly that luminance differences (light-dark contrasts) are crucial
for sequential and diverging palettes while qualitative palettes are balanced
at the same luminance.

.. plot::

    from colorspace import *

    qual_pal = qualitative_hcl("Set 2")
    qual1 = palette(qual_pal(5), "Color")
    qual2 = palette(desaturate(qual_pal(5)), "Desaturated")

    seq_pal = sequential_hcl("Blues 3")
    seq1 = palette(seq_pal(7), "Color")
    seq2 = palette(desaturate(seq_pal(7)), "Desaturated")

    div_pal = diverging_hcl("Green-Brown")
    div1 = palette(div_pal(7), "Color")
    div2 = palette(desaturate(div_pal(7)), "Desaturated")

    swatchplot({"Qualitative (Set 2)":     [qual1, qual2],
                "Sequential (Blues 3)":    [seq1, seq2],
                "Diverging (Green-Brown)": [div1, div2]},
                nrow = 3, figsize = (12, 1.5))


More details about the construction of such palettes is provided in the
following while the article on :ref:`article-palette_visualization`
introduces further tools to better understand the properties of color palettes.

To facilitate obtaining good sets of colors, HCL parameter combinations that
yield useful palettes are accessible by name. These can be listed using the
function :py:func:`hcl_palettes`:

.. ipython:: python
    :okwarning:

    from colorspace import hcl_palettes
    hcl_palettes()

To inspect the HCL parameter combinations for a specific palette simply include
the palette name where upper- vs. lower-case, spaces, etc. are ignored for
matching the label, e.g., ``"set2"`` matches ``"Set 2"`` as well as ``"SET2"`` will.

.. ipython:: python
    :okwarning:

    from colorspace import hcl_palettes
    pal = hcl_palettes().get_palette(name = "SET2")
    print(pal)
    print(pal.get_settings())


Calling :py:class:`qualitative_hcl`, :py:class:`sequential_hcl`, and
:py:class:`diverging_hcl` respectively, will return an object of class
:py:class:`hclpalette` defined by a series of parameters which specify
the color palette.
All parameters can either be specified "by hand"
through the HCL parameters, an entire palette can be specified "by name", or
the name-based specification can be modified by a few HCL parameters. In case
of the HCL parameters, either a vector-based specification such as
``h = [0, 270]`` or individual parameters ``h1 = 0`` and ``h2 = 270`` can be used.

To compute the actual color hex codes (representing sRGB coordinates), the
method :py:func:`hclpalette.colors()` or :py:func:`hclpalette.__call__` are used
which return a list of :math:`N` colors along the coordinates defined by parameters
specified when constructing the object.

The first three of the following commands lead to equivalent output. The fourth
command yields a modified set of colors (lighter due to a luminance of ``80``
instead of ``70``).

.. ipython:: python
    :okwarning:

    from colorspace import qualitative_hcl
    qualitative_hcl(h = [0, 270], c = 60, l = 70)(4)
    qualitative_hcl(h1 = 0, h2 = 270, c1 = 60, l1 = 70)(4)
    qualitative_hcl("set2").colors(4)
    qualitative_hcl("Set 2", l = 80).colors(4)


.. todo::
    Incorrect description. Missing support for the lambda function which, here,
    controls ``h2`` by default. Once implemented please check code/result/text.


Qualitative palettes
--------------------
:py:class:`qualitative_hcl` distinguishes
the underlying categories by a sequence of hues while keeping both chroma and
luminance constant, to give each color in the resulting palette the same
perceptual weight. Thus, ``h`` should be a pair of hues (or equivalently ``h1`` and ``h2``
can be used) with the starting and ending hue of the palette. Then, an
equidistant sequence between these hues is employed, by default spanning the
full color wheel (i.e., the full ``360`` degrees). Chroma ``c`` (or equivalently ``c1``)
and luminance ``l`` (or equivalently ``l1``) are constants. Finally, fixup indicates
whether colors with out-of-range coordinates should be corrected.

In the following graphic the available named palettes are shown. The first five
palettes are close to the ColorBrewer.org palettes of the same name
:cite:p:`HCL-color:Harrower+Brewer:2003`.
They employ different levels of chroma and luminance and, by default, span the
full hue range. The remaining four palettes are taken from
:cite:t:`HCL-color:Ihaka:2003`. They are based on the same chroma (``50``) and
luminance (``70``) but the hue is restricted to different intervals.

.. ipython:: python
    :okwarning:

    from colorspace import hcl_palettes
    @savefig hcl_palettes_qualitative.png width=400px height=350px align=center
    hcl_palettes(5, "Qualitative", plot = True, ncol = 1)

When palettes are employed for shading areas in statistical displays (e.g., in
bar plots, pie charts, or regions in maps), lighter colors (with moderate
chroma and high luminance) such as "Pastel 1" or "Set 3" are typically less
distracting. By contrast, when coloring points or lines, more flashy colors
(with high chroma) are often required: On a white background a moderate
luminance as in "Dark 2" or "Dark 3" usually works better while on a black/dark
background the luminance should be higher as in "Set 2" for example.



Sequential palettes (single-hue)
--------------------------------

:py:class:`sequential_hcl` codes the underlying numeric values by a monotonic
sequence of increasing (or decreasing) luminance. Thus, the function's ``l``
argument should provide a vector of length :math:`2` with starting and ending luminance
(equivalently, ``l1`` and ``l2`` can be used).  Without chroma (i.e., ``c = 0``),
this simply corresponds to a gray-scale palette, see "Grays" and "Light Grays"
below.

.. ipython:: python
    :okwarning:

    from colorspace import hcl_palettes
    @savefig hcl_palettes_sequential_singlehue.png width=50% align=center
    hcl_palettes(7, "Sequential (single-hue)", plot = True,
                 ncol = 1, figsize = (6, 7.5))

All except the last are inspired by the `ColorBrewer.org <http://ColorBrewer.org>`_
palettes with the same base name :cite:p:`HCL-color:Harrower+Brewer:2003` but
restricted to a single hue only. They are intended for a white/light
background. The last palette (Oslo) is taken from the scientific color maps of
:cite:t:`HCL-color:Crameri:2018` and is intended for a black/dark background
and hence the order is reversed starting from a light blue (not a light gray).

To distinguish many colors in a sequential palette it is important to have a
strong contrast on the luminance axis, possibly enhanced by an accompanying
pronounced variation in chroma. When only a few colors are needed (e.g., for
coding an ordinal categorical variable with few levels) then a lower luminance
contrast may suffice.



Sequential palettes (multi-hue)
-------------------------------

To not only bring out extreme colors in a sequential palette but also better
distinguish middle colors it is a common strategy to employ a sequence of hues.
Thus, the basis of such a palette is still a monotonic luminance sequence as
above (combined with a monotonic or triangular chroma sequence). But rather
than using a single hue, an interval of hues in ``h`` (or beginning hue ``h1`` and
ending hue ``h2``) can be specified.

:py:class:`sequential_hcl` allows combined variations in hue (``h`` and
``h1``/``h2``, respectively), chroma (``c`` and ``c1``/``c2``/``cmax``,
respectively), luminance (``l`` and ``l1``/``l2``, respectively), and power
transformations for the chroma and luminance trajectories (power and
``p1``/``p2``, respectively). This yields a broad variety of sequential
palettes, including many that closely match other well-known color palettes.
The plot below shows all the named multi-hue sequential palettes in *colorspace*:

* "Purple-Blue" to "Terrain 2" are various palettes created during the
  development of *colorspace*, e.g., by :cite:t:`HCL-color:Zeileis+Hornik+Murrell:2009` or
  :cite:t:`HCL-color:Stauffer+Mayr+Dabernig:2015` among others.
* "Viridis" to "Inferno" closely match the palettes that
  :cite:t:`HCL-color:Smith+VanDerWalt:2015`
  developed for matplotlib and that gained popularity recently.
* "Dark Mint" to "BrwnYl" closely match palettes provided in :cite:t:`HCL-color:CARTO`
* "YlOrRd" to "Blues" closely match ColorBrewer.org palettes
  :cite:p:`HCL-color:Harrower+Brewer:2003`.
* "Lajolla" to "Batlow" closely match the scientific color maps of the same
  name by :cite:t:`HCL-color:Crameri:2018` and the first two of these are intended for a
  black/dark background.

.. todo::
    I do not have the same order as I do not mix basic and advanced.
    Thus, this list above is invalid for the python package. Fix this.

.. ipython:: python
    :okwarning:

    @savefig hcl_palettes_sequential_multihue.png width=100% align=center
    hcl_palettes(7, "Sequential (multi-hue)", plot = True,
                 ncol = 3, figsize = (10, 8))

Note that the palettes differ substantially in the amount of chroma and
luminance contrasts. For example, many palettes go from a dark high-chroma
color to a neutral low-chroma color (e.g., "Reds", "Purples", "Greens",
"Blues") or even light gray (e.g., "Purple-Blue"). But some palettes also
employ relatively high chroma throughout the palette (e.g., the viridis and
many CARTO palettes). To emphasize the extremes the former strategy is
typically more suitable while the latter works better if all values along the
sequence should receive some more perceptual weight.


Diverging palettes
------------------

:py:class:`diverging_hcl` codes the underlying numeric values by a triangular
luminance sequence with different hues in the left and in the right "arms" of
the palette. Thus, it can be seen as a combination of two sequential palettes
with some restrictions: (a) a single hue is used for each arm of the palette,
(b) chroma and luminance trajectory are balanced between the two arms, (c) the
neutral central value has zero chroma. To specify such a palette a vector of
two hues h (or equivalently ``h1`` and ``h2``), either a single chroma value
``c`` (or ``c1``) or a vector of two chroma values ``c`` (or ``c1`` and
``cmax``), a vector of two luminances ``l`` (or ``l1`` and ``l2``), and power
parameter(s) power (or ``p1`` and ``p2``) are used.
For more flexible diverging palettes without the restrictions above (and
consequently more parameters) see the :py:class:`divergingx_hcl` palettes
introduced below.

The plot below shows all such diverging palettes that have been named in *colorspace*:

* "Blue-Red" to "Cyan-Magenta" have been developed for *colorspace* starting from
  Zeileis, Hornik, and Murrell (2009), taking inspiration from various other
  palettes, including more balanced and simplified versions of several
  ColorBrewer.org palettes :cite:p:`HCL-color:Harrower+Brewer:2003`.
* "Tropic" closely matches the palette of the same name from CARTO :cite:p:`HCL-color:CARTO`.
* "Broc" to "Vik" and "Berlin" to "Tofino" closely match the scientific color
  maps of the same name by :cite:t:`HCL-color:Crameri:2018`, where the first three are intended
  for a white/light background and the other three for a black/dark background.

.. todo::
    I do not have the same order as I do not mix basic and advanced.
    Thus, this list above is invalid for the python package. Fix this.

.. ipython:: python
    :okwarning:

    @savefig hcl_palettes_diverging.png width=60% align=center
    hcl_palettes(7, "Diverging", plot = True,
                 ncol = 1, figsize = (6, 10))

When choosing a particular palette for a display similar considerations apply
as for the sequential palettes. Thus, large luminance differences are important
when many colors are used while smaller luminance contrasts may suffice for
palettes with fewer colors etc.



.. _article-hcl_palettes-section-construction-details:

Construction details
--------------------

The three different types of palettes (qualitative, sequential, and diverging)
are all constructed by combining three different types of trajectories
(constant, linear, triangular) for the three different coordinates (hue H,
chroma C, luminance L):

+---------------+---------------------------+-----------------------------+--------------------+
|**Type**       | **H**                     | **C**                       | **L**              |
+---------------+---------------------------+-----------------------------+--------------------+
| Qualitative   | Linear                    | Constant                    | Constant           |
+---------------+---------------------------+-----------------------------+--------------------+
| | Sequential  | | Constant (single-hue)   | | Linear (+ power)          | | Linear (+ power) |
| |             | | *or* Linear (multi-hue) | | *or* Triangular (+ power) | |                  |
+---------------+---------------------------+-----------------------------+--------------------+
| | Diverging   | | Constant (2x)           | | Linear (+ power)          | | Linear (+ power) |
| |             | |                         | | *or* Triangular (+ power) | |                  |
+---------------+---------------------------+-----------------------------+--------------------+


As pointed out initially in this article, luminance is probably the most
important property for defining the type of palette. It is constant for
qualitative palettes, monotonic for sequential palettes (linear or a power
transformation), and uses two monotonic trajectories (linear or a power
transformation) diverging from the same neutral value.

Hue trajectories are also rather intuitive and straightforward for the three
different types of palettes. However, chroma trajectories are probably the most
complicated and least obvious from the examples above. Hence, the exact
mathematical equations underlying the chroma trajectories are given in the
following (i.e., using the parameters ``c1``, ``c2``, ``cmax``, and ``p1``, respectively).
Analogous equations apply for the other two coordinates.

The trajectories are functions of the intensity :math:`i \in [0,1]` where :math:`1`
corresponds to the full intensity:

.. math::
   :nowrap:

   \begin{gather*}
   \text{Constant}: c_1 \\

   \text{Linear}: c_2 - (c_2 - c_1) \times i \\

   \text{Triangular}: \begin{cases}
           c_2 - (c_2 - c_{max}) \times \frac{i}{j}  & \text{if}~~~~i \le j \\
           c_{max} - (c_{max} - c_1) \times \frac{i - j}{1 - j} & \text{else}
   \end{cases}
   \end{gather*}


where :math:`j` is the intensity at which :math:`c_{max}` is assumed.
It is constructed such that the slope to the left is the negative of
the slope to the right of :math:`j`:

.. math::
    :nowrap:

    \begin{gather*}
    j = \Big(1 + \frac{|c_{max} - c_1|}{|c_{max} - c_2|}\Big)^{-1}
    \end{gather*}

Instead of using a linear intensity :math:`i` going from :math:`1` to :math:`0`,
one can replace :math:`i` with :math:`i ^{p_1}` in the equations above.
This then leads to power-transformed curves that add or remove chroma more
slowly or more quickly depending on whether the power
parameter :math:`p_1` is :math:`< 1` or :math:`> 1`.


The three types of trajectories are also depicted below. Note that full
intensity :math:`i = 1` is on the left and zero intensity :math:`i = 0` is on
the right of each panel.

.. plot::
    :align: center
    :width: 100%

    from matplotlib import pyplot as plt
    import numpy as np

    fig, [ax1, ax2, ax3] = plt.subplots(1, 3, figsize = (10, 3.5))
    i = np.linspace(0, 1, 51) # intensity
    bbox = dict(edgecolor = "black", facecolor = "white", alpha = 0.5) # Box style

    # Setting title and axis labels
    for t,a in {"Constant": ax1, "Linear": ax2, "Triangular": ax3}.items():
        a.set_title(t); a.set_xlabel("Intensity (i)"); a.set_ylabel("Coordinate")
        a.set_xlim(1, 0); a.set_ylim(0, 100)

    # ---------------------
    # First subplot
    # ---------------------
    y = np.repeat(80, len(i))
    ax1.plot(i, y, color = "black", linestyle = "-")

    # ---------------------
    # Second subplot
    # ---------------------
    y1 = 10 - (10 - 80) * i**1.0
    y2 = 10 - (10 - 80) * i**1.6
    ax2.plot(i, y1, color = "black", linestyle = "-")  # linear
    ax2.plot(i, y2, color = "black", linestyle = "--") # power-transformed

    # Adding texts and labels
    ax2.text(0.96, 82, "c1", va = "bottom", ha = "left",  bbox = bbox)
    ax2.text(0.04,  8, "c2", va = "top",    ha = "right", bbox = bbox)
    ax2.text(0.5,  52, "p1 = 1.0", va = "bottom", ha = "left",  bbox = bbox)
    ax2.text(0.55, 30, "p1 = 1.6", va = "top",    ha = "right", bbox = bbox)

    # ---------------------
    # Third subplot
    # ---------------------
    def get_coord(c1, c2, cmax, p1):
        j = (1. + np.abs(cmax - c1) / np.abs(cmax - c2))**(-1.)
        return np.where(i**p1 <= j,
                        c2   - (c2   - cmax) * i**p1 / j,
                        cmax - (cmax - c1)   * (i**p1 - j) / (1 - j))
    y1 = get_coord(60, 10, 80, 1.0)
    y2 = get_coord(60, 10, 80, 1.6)
    ax3.plot(i, y1, color = "black", linestyle = "-")  # linear
    ax3.plot(i, y2, color = "black", linestyle = "--") # power-transformed

    # Adding texts and labels
    ax3.text(0.96, 54, "c1",   va = "top",    ha = "left",   bbox = bbox)
    ax3.text(0.04,  8, "c2",   va = "top",    ha = "right",  bbox = bbox)
    ax3.text(0.70, 81, "cmax", va = "bottom", ha = "left",   bbox = bbox)
    ax3.text(0.45, 58, "p1 = 1.0", va = "bottom", ha = "left",  bbox = bbox)
    ax3.text(0.55, 35, "p1 = 1.6", va = "top",    ha = "right", bbox = bbox)

    # Tighten up and display
    plt.tight_layout()
    fig.show()

The concrete parameters in the plot above are:

* Constant: ``c1 = 80``.
* Linear: ``c1 = 80``, ``c2 = 10``, ``p1 = 1`` (solid) vs. ``p1 = 1.6`` (dashed).
* Triangular: ``c1 = 60``, ``cmax = 80``, ``c2 = 10``, ``p1 = 1`` (solid) vs. ``p1 = 1.6`` (dashed).

Further discussion of these trajectories and how they can be visualized and
assessed for a given color palette is provided in the article
:ref:`article-palette_visualization`.



Registering your own palettes
-----------------------------

.. todo:: Registering new palettes not yet implemented.


Flexible diverging palettes
---------------------------

The :py:class:`divergingx_hcl` function provides more flexible diverging palettes by
simply calling :py:class:`sequential_hcl` twice with prespecified sets of hue, chroma,
and luminance parameters. Thus, it does not pose any restrictions that the two
"arms" of the palette need to be balanced and also may go through a non-gray
neutral color (typically light yellow). Consequently, the chroma/luminance
paths can be rather unbalanced.

The plot below shows all such flexible diverging palettes that have been named in *colorspace*:

* "ArmyRose" to "Tropic" closely match the palettes of the same name from CARTO
  :cite:p:`color:CARTO`.
* "PuOr" to "Spectral" closely match the palettes of the same name from
  ColorBrewer.org :cite:p:`color:Harrower+Brewer:2003`.
* "Zissou 1" closely matches the palette of the same name from wesanderson
  :cite:p:`color:wesanderson`
* "Cividis" closely matches the palette of the same name from the viridis
  family (Garnier 2018). Note that despite having two "arms" with blue vs.
  yellow colors and a low-chroma center color, this is probably better
  classified as a sequential palette due to the monotonic chroma going from
  dark to light. (See Approximating Palettes from Other Packages for more
  details.)
* "Roma" closely matches the palette of the same name by
  :cite:t:`color:Crameri:2018`.

.. plot::
    :width: 60%
    :align: center

    from colorspace import divergingx_palettes
    divergingx_palettes(ncol = 1, plot = True, figsize = (5, 8))

Typically, the more restricted :py:class:`diverging_hcl` palettes should be preferred
because they are more balanced. However, by being able to go through light
yellow as the neutral color warmer diverging palettes are available.



References
----------

.. bibliography:: ../references.bib
    :cited:
    :style: plain
    :labelprefix: HCL
    :keyprefix: HCL-

