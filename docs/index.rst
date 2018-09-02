.. python-colorspace documentation master file, created by
   sphinx-quickstart on Fri Aug 31 21:18:17 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Modules

    modules/colorlib.rst
    modules/palettes.rst
    modules/gui.rst

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Examples

    examples/colorlib.rst
    examples/transform.rst
    examples/hcl_palettes.rst

Welcome to python-colorspace's documentation!
=============================================

Hy :)

.. Contents:
   .. toctree::
       :maxdepth: 2
   .. Indices and tables
   ==================
   
   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`

Logging
=======

The `python-colorspace` package uses `logging`, default log level is `WARNING`.
The logging level can be controlled by setting an environment variable called
`CSLOGLEVEL` (e.g, on unix systems `export CSLOGLEVEL=DEBUG`).

Basic Objects
=============

There to types of objects: :class:`hclpalette`'s and :class:`colorobject`'s.
:class:`hclpalettes` contain a set of parameters which specify the color palette
and can be used to retrieve a set of `N` colors which can be defined by the user.
A :class:`colorobject` contains a set of `N` colors, but `N` is fixed (depending
on how the object has been created). :class:`colorobject`'s provide the methods
to convert colors from one color space to another (e.g., from `hex` to `sRGB`,
`HCL` or `CIEXZY`.

* Add some links here ...

Known issues
============

.. _index-known-issues:

.. warning::
    Gamma and alpha handling not yet implemented.

.. warning::
    White point implemented but might require some additional testing.


Full TODO list
==============

.. todolist::



