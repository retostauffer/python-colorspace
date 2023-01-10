
.. _article-choose_palette:

.. currentmodule:: colorspace

Apps for Choosing Colors and Palettes Interactively
===================================================

To facilitate exploring the package and employing it when working with colors,
a Tcl/Tk based is provided within the package using pythons
`tkinter <https://docs.python.org/3/library/tkinter.html>`_ interface.

``choose_palette()``.

.. image:: ../_static/img_gui.jpeg


Web App
-------

A web-app to explore the capabilities based on the R implementation
`colorspace <https://cran.r-project.org/package=colorspace>`_ is available
via `<https://hclwizard.org>`_.

1. `Palette Creator <http://hclwizard.org:3000/hclwizard/>`_
2. `Deficiency Emulator <http://hclwizard.org:3000/cvdemulator/>`_
3. `Color Picker <http://hclwizard.org:3000/hclcolorpicker/>`_

The latter two do not exist as GUIs in the python implementation, however,
the function :py:ref:`cvd_emulator` allows to emulate color vision
deficiencies from within the python package. For more information please
have a look at the article
:ref:`article-color_vision_deficiency_emulation_cvd_emulator`.


