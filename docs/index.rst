.. python-colorspace documentation master file, created by
   sphinx-quickstart on Fri Aug 31 21:18:17 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Getting started

    installation.rst
    gettingstarted.rst
    logenvir.rst
    releasenotes.rst

.. toctree::
    :maxdepth: 1
    :hidden:

    examples/hcl_palettes.rst
    examples/transform.rst
    examples/colorlib.rst
    examples/hcl_converter.rst

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: References

    userapi.rst
    modules/gui.rst
    modules/palettes.rst


.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Objects

    modules/colorlib.rst



Welcome to python-colorspace's documentation!
=============================================

Hy :)

Basic Objects
=============

There to types of objects: :class:`hclpalette`'s and :class:`colorobject`'s.
:py:class:`hclpalettes` contain a set of parameters which specify the color palette
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



