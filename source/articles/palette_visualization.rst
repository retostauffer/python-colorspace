
.. _article-palette_visualization:

Palette visualization and Assessment
====================================


Overview
--------

.. currentmodule:: colorspace

.. autosummary::
    :toctree: ../api/

    swatchplot
    specplot
    demoplot


Color swatches
--------------

The function :py:class:`swatchplot <colorspace.swatchplot>` is a convenience
function for displaying collections
of palettes that can be specified as lists or matrices of hex color codes.
Essentially, it is just a call to the base graphics rect() function but with
heuristics for choosing default labels, margins, spacings, borders, etc. These
heuristics are selected to work well for hcl_palettes() and might need further
tweaking in future versions of the package.



.. ipython:: python
    :okwarning:

    from colorspace import swatchplot, sequential_hcl, palette

    hue       = sequential_hcl(h = [0, 360], c = 60, l = 65)
    chroma    = sequential_hcl(h = 0, c = [100, 0], l = 65, rev = True, power = 1)
    luminance = sequential_hcl(h = 260, c = 25, l = [25, 90], rev = True, power = 1)

    @savefig palette_visualization_swatchplot.png align=center
    swatchplot([palette(hue(5), "Hue"),
                palette(chroma(5), "Chroma"),
                palette(luminance(5), "Luminance")],
                figsize = (6, 1.5))


This shows the following:

* *Hue*: Only the hue (= type of color) changes from H = 0 (red) via 60
  (yellow), etc. to 300 (purple) while chroma and luminance are fixed to
  moderate values of C = 60 and L = 65, respectively.
* *Chroma*: Only the chroma (= colorfulness) changes from C = 0 (gray) to 100
  (colorful) while hue and luminance are fixed to H = 0 (red) and L = 65,
  respectively.
* *Luminance*: Only the luminance (= brightness) changes from L = 90 (light) to
  25 (dark) while hue and chroma are fixed to H = 260 (blue) and C = 25 (low,
  close to gray), respectively.

Next, we demonstrate a more complex example of a
:py:class:`swatchplot <colorspace.swatchplot>` with three matrices of
sequential color palettes of blues, purples, reds, and greens. For all
palettes, luminance increases monotonically to yield a proper sequential
palette. However, the hue and chroma handling is somewhat different to
emphasize different parts of the palette.

* *Single-hue*: In each palette the hue is fixed and chroma decreases
  monotonically (along with increasing luminance). This is typically sufficient
  to clearly bring out the extreme colors (dark/colorful vs. light gray).
* *Single-hue* (advanced): The hue is fixed (as above) but the chroma
  trajectory is triangular. Compared to the basic single-hue palette above,
  this better distinguishes the colors in the middle and not only the extremes.
* *Multi-hue* (advanced): As in the advanced single-hue palette, the chroma
  trajectory is triangular but additionally the hue varies slightly. This can
  further enhance the distinction of colors in the middle of the palette.


.. ipython:: python
    :okwarning:

    from colorspace import swatchplot, sequential_hcl

    @savefig palette_visualization_sequential_examples.png align=center
    swatchplot({"Single-hue":           [sequential_hcl(x) for x in ["Blues 2", "Purples 2", "Reds 2", "Greens 2"]],
               "Single-hue (advanced)": [sequential_hcl(x) for x in ["Blues 3", "Purples 3", "Reds 3", "Greens 3"]],
               "Multi-hue (advanced)":  [sequential_hcl(x) for x in ["Blues", "Purples", "Reds", "Greens"]]},
               n = 7, show_names = False, nrow = 5, figsize = (12, 3))


.. todo::
    :py:func:`swatchplot<colorspace.swatchplot.swatchplot>` requires
    an optional argument `cvd` analogous to the R package.











