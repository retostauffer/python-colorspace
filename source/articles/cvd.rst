
.. _article-color_vision_deficiency_emulation:

Color Vision Deficiency Emulation
=================================

Different kinds of limitations can be emulated using the physiologically-based
model for simulating color vision deficiency (CVD) of
:cite:t:`color:Machado+Oliveira+Fernandes:2009`:
deuteranomaly (green cone cells defective), protanomaly (red
cone cells defective), and tritanomaly (blue cone cells defective). While most
other CVD simulations handle only dichromacy, where one of three cones is
non-functional, :cite:t:`color:Machado+Oliveira+Fernandes:2009` provides a unified
model of both dichromacy and anomalous trichromacy, where one cone has shifted
spectral sensitivity. As anomalous trichromacy is the most common form of color
vision deficiency, it is important to emulate along with the rarer, but more
severe dichromacy.

The workhorse function to emulate color vision deficiencies is simulate_cvd(),
which can take any vector of valid R colors and transform them according to a
certain CVD transformation matrix and transformation equation. The
transformation matrices have been established by
:cite:t:`color:Machado+Oliveira+Fernandes:2009` and are provided by methods
of the :py:func:`CVD<colorspace.CVD.CVD>`.
The convenience interfaces
:py:func:`deutan<colorspace.CVD.deutan>`,
:py:func:`protan<colorspace.CVD.protan>`,
:py:func:`tritan<colorspace.CVD.tritan>` are the high-level
functions for simulating the corresponding kind of color blindness with a given
severity. A severity of 1 corresponds to dichromacy, 0 to normal color vision,
and intermediate values to varying severities of anomalous trichromacy.

For further guidance on color blindness in relation to statistical graphics see
:cite:t:`color:dichromat` which accompanies the R package dichromat :cite:p:`color:dichromat`
and is based on earlier emulation techniques (:cite:t:`color:Vienot+Brettel+Ott:1995`;
:cite:t:`color:Brettel+Vienot+Mollon:1997`; :cite:t:`color:Vienot+Brettel+Mollon:1999`).
:cite:p:`color:Vienot+Brettel+Ott:1995,color:Brettel+Vienot+Mollon:1997,color:Vienot+Brettel+Mollon:1999`.

Illustration: Heatmap with sequential palette
---------------------------------------------

.. todo:: Heatmap example. Requires the rainbow again.

Demo plot based on the default diverging_hcl color palette
with 51 (default) distinct colors.
Normal color vision, a desaturated version, plus simulated
deuteranope and protanope color vision.

.. ipython:: python
    :okwarning:

    ###from colorspace import diverging_hcl, desaturate, deutan, protan
    ###from colorspace.demos import demo
    ###pal = diverging_hcl()

    ###@savefig cvd_heatmap.png width=100% align=center
    ###demo(pal.cmap(name = "Normal Color Vision"),
    ###     desaturate(pal.cmap(name = "Desaturated")),
    ###     deutan(pal.cmap(name = "Deuteranope Color Vision")),
    ###     protan(pal.cmap(name = "Protanope Color Vision")))



