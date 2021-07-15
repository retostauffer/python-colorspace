
.. _article-palette_visualization:

Palette Visualization and Assessment
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

* *Hue*: Only the hue (= type of color) changes from `H = 0` (red) via `60`
  (yellow), etc. to `300` (purple) while chroma and luminance are fixed to
  moderate values of `C = 60` and `L = 65`, respectively.
* *Chroma*: Only the chroma (= colorfulness) changes from `C = 0` (gray) to `100`
  (colorful) while hue and luminance are fixed to `H = 0` (red) and `L = 65`,
  respectively.
* *Luminance*: Only the luminance (= brightness) changes from `L = 90` (light) to
  `25` (dark) while hue and chroma are fixed to `H = 260` (blue) and `C = 25` (low,
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



Moreover, the `cvd` argument can be set to a vector of transformation names,
indicating which deficiencies to emulate. In the example below this is used to
compare the Viridis and YlGnBu palettes under deuteranopia and desaturation.


.. ipython:: python
    :okwarning:

    pal1 = sequential_hcl("YlGnBu")(7)
    pal2 = sequential_hcl("Viridis")(7)

    @savefig palette_visualization_cvd_option.png width=70% align=center
    swatchplot([palette(pal1, "YlGnBu"), palette(pal2, "Viridis")],
                cvd = ["protan", "desaturate"], nrow = 4, figsize = (8, 2.5))



HCL (and RGB) spectrum
----------------------

As the properties of a palette in terms of the perceptual dimensions *hue*,
*chroma*, and *luminance* are not always clear from looking just at color swatches
or (statistical) graphics based on these palettes, the :py:func:`specplot<colorspace.specplot.specplot>`
function provides an explicit display for the coordinates of the HCL trajectory
associated with a palette. This can bring out clearly various aspects, e.g.,
whether hue is constant, whether chroma is monotonic or triangular, and whether
luminance is approximately constant (as in many qualitative palettes),
monotonic (as in sequential palettes), or diverging.

The function first transforms a given color palette to its HCL (polarLUV)
coordinates. As the hues for low-chroma colors are not (or only poorly)
identified, they are smoothed by default. Also, to avoid jumps from `0` to `360` or
vice versa, the hue coordinates are shifted suitably.

By default, the resulting trajectories in the HCL spectrum are visualized by a
simple line plot:

* *Hue* is drawn in red and coordinates are indicated on the axis on the right
  with range `[-360, 360]`.
* *Chroma* is drawn in green with coordinates on the
  left axis.  The range `[0, 100]` is used unless the palette necessitates higher
  chroma values.
* *Luminance* is drawn in blue with coordinates on the left axis in the
range `[0, 100]`.

Additionally, a color swatch for the palette is included.
Optionally, a second spectrum for the corresponding trajectories of RGB
coordinates can be included. However, this is usually just of interest for
palettes created in RGB space (or simple transformations of RGB).

The illustrations below show how basic qualitative, sequential, and diverging
palettes are constructed in HCL space (the corresponding mathematical equations
are provided in the
:ref:`construction details<article-section-construction_details>`).
In the qualitative `"Set 2"` palette below, the hue traverses the entire color
"wheel" (from `0` to `360` degrees) while keeping chroma and luminance (almost)
constant (`C = 60` and `L = 70`).

.. ipython:: python
    :okwarning:

    from colorspace import specplot, qualitative_hcl
    @savefig palette_visualization_specplot_set2.png width=70% align=center
    specplot(qualitative_hcl("Set 2").colors(100))


Note that due to the restrictions of the HCL color space, some of the
green/blue colors have a slightly smaller maximum chroma resulting in a small
dip in the chroma curve. This is fixed automatically (by default) and is hardly
noticable in visualizations, though.

The sequential `"Blues 2"` palette below employs a single hue (`H = 260`) and a
monotonically increasing luminance trajectory (from dark to light). Chroma
simply decreases monotonically along with increasing luminance.

.. ipython:: python
    :okwarning:

    from colorspace import specplot, sequential_hcl
    @savefig palette_visualization_specplot_blues2.png width=70% align=center
    specplot(sequential_hcl("Blues 2").colors(100))


Finally, the diverging `"Blue-Red"` palette is depicted below. It simply combines
a blue and a red sequential single-hue palette (similar to the `"Blues 2"`
palette discussed above). Hue is constant in each “arm” of the palette and the
chroma/luminance trajectories are balanced between both arms. In the center the
palette passes through a light gray (with zero chroma) as the neutral value.

.. ipython:: python
    :okwarning:

    from colorspace import specplot, diverging_hcl
    @savefig palette_visualization_specplot_bluered.png width=70% align=center
    specplot(diverging_hcl("Blue-Red").colors(100))



.. todo:: Add RGB rainbow example here (`gist_rainbow` from matplotlib?).


Trajectories in HCL space
-------------------------

.. todo:: Section must be written.


Demonstration of statistical graphics
-------------------------------------

To demonstrate how different kinds of color palettes work in different kinds of
statistical displays, demoplot() provides a simple convenience interface to
some base graphics with (mostly artificial) data sets. As a first overview, all
built-in demos are displayed with the same sequential heat colors palette:
`sequential_hcl("Heat")(7)`.

.. ipython:: python
    :okwarning:

    from matplotlib import pyplot as plt
    from colorspace import demoplot, sequential_hcl

    colors = sequential_hcl("Heat").colors(5)
    fig, axes = plt.subplots(2, 3)

    demo_types = ["Bar", "Heatmap", "Lines", "Matrix", "Pie", "Spine"]
    for i in range(0, len(demo_types)):
        demoplot(colors, type_ = demo_types[i], title = demo_types[i], ax = axes.flatten()[i])

    @savefig palette_visualization_demonstration.png width=100% align=center
    fig.show()


All types of demos can, in principle, deal with arbitrarily many colors from
any palette, but the graphics differ in various respects such as:

* Working best for fewer colors (e.g., bar, pie, scatter, lines, ...)
  vs. many colors (e.g., heatmap, perspective, ...).
* Intended for categorical data (e.g., bar, pie, ..)
  vs. continuous numeric data (e.g., heatmap, perspective, ...).
* Shading areas (e.g., map, bar, pie, …) vs. coloring points or lines (scatter, lines).

Hence, in the following some further illustrations are organized by type of
palette, using suitable demos for the particular palettes.


.. todo:: Some examples and demoplot types still missing.

