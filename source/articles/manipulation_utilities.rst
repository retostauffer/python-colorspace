
.. _article-manipulation_utilities:

Manipulation Utilities
======================

Template. TODO


Desaturation in HCL space
-------------------------

Desaturation should map a given color to the gray with the same "brightness".
In principle, any perceptually-based color model (HCL, HLS, HSV, ...) could be
employed for this but HCL works particularly well because its coordinates
capture the perceptual properties better than most other color models.

The :py:func:`desaturate <colorspace.desaturate>` function converts any given
hex color code to the corresponding HCL coordinates and sets the chroma to
zero. Thus, only the luminance matters which captures the "brightness"
mentioned above. Finally, the resulting HCL coordinates are transformed back to
hex color codes.

For illustration, a few simple examples are presented below. More examples in
the context of palettes for statistical graphics are discussed along with the
color vision deficiency article.


.. todo:: The function also allows to convert `colorobject`s and cmaps. Extend description.

.. ipython:: python
    :okwarning:

    from colorspace import rainbow, desaturate
    rainbow().colors(3)
    desaturate(rainbow().colors(3))

Even this simple example suffices to show that the three RGB rainbow colors
have very different grayscale levels. This deficiency is even clearer when
using a full color wheel (of colors with hues in `[0, 360]` degrees). While the
RGB :py:func:`rainbow <colorspace.rainbow>` is very unbalanced the HCL
:py:func:`rainbow_hcl <colorspace.rainbow_hcl>` (or also
:py:func:`qualitative_hcl <colorspace.qualitative_hcl>`)
is (by design) balanced with respect to luminance.

.. ipython:: python
    :okwarning:

    from matplotlib import pyplot as plt
    from colorspace import rainbow, rainbow_hcl, desaturate
    from numpy import repeat

    def wheel(ax, col): ax.pie(repeat(1, len(col)), colors = col, labels = range(len(col)))

    col     = rainbow()(8)
    col_hcl = rainbow_hcl()(8)

    fig, axes = plt.subplots(2, 2, figsize = (8, 8))
    wheel(axes[0, 0], col)
    wheel(axes[0, 1], desaturate(col))
    wheel(axes[1, 0], col_hcl)
    wheel(axes[1, 1], desaturate(col_hcl))

    fig.tight_layout()
    @savefig manipulation_utilities_pie.png align=center width=60%
    fig.show()




Lighten and darken colors
-------------------------

In principle, a similar approach for lightening and darkening colors can be
employed as for desaturation above. The colors can simply be transformed to HCL
space and then the luminance can either be decreased (turning the color darker)
or increased (turning it lighter) while preserving the hue and chroma
coordinates.

This strategy typically works well for lightening colors, although in some
situations the result can be rather colorful. Conversely, when darkening rather
light colors with little chroma, this can result in rather gray colors.

In these situations, an alternative might be to apply the analogous strategy in
HLS space which is frequently used in HTML style sheets. However, this strategy
may also yield colors that are either too gray or too colorful. A compromise
that sometimes works well is to adjust the luminance coordinate in HCL space
but to take the chroma coordinate corresponding to the HLS transformation.

We have found that typically the HCL-based transformation performs best for
lightening colors and this is hence the default in lighten(). For darkening
colors, the combined strategy often works best and is hence the default in
darken(). In either case it is recommended to try the other available
strategies in case the default yields unexpected results.

Regardless of the chosen color space, the adjustment of the L component can
occur by two methods, relative (the default) and absolute. For example
`L - 100 * amount` is used for absolute darkening, or `L * (1 - amount)` for relative
darkening. See :py:func:`lighten <colorspace.lighten>` and
:py:func:`darken <colorspace.darken>` for more details.

For illustration a qualitative palette (Okabe-Ito) is transformed by two levels
of both lightening and darkening, respectively.


.. ipython:: python
    :okwarning:

    from colorspace import palette, swatchplot, lighten, darken
    oi = ["#61A9D9", "#ADD668", "#E6D152", "#CE6BAF", "#797CBA"]

    @savefig manipulation_utilities_okabeito.png align=center width=60%
    swatchplot([palette(lighten(oi, 0.4), "-40%"),
                palette(lighten(oi, 0.2), "-20%"),
                palette(oi, "0%"),
                palette(darken(oi, 0.2), "+20%"),
                palette(darken(oi, 0.4), "+40%")])





