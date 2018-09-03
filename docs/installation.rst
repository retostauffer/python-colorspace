
.. _page-installation:

Installation
============

The package is available [on github](https://github.com/retostauffer/python-colorspace) and
can thus simply be installed via ``pip``.
The package is tested against Python `2.7` and Python `3.6+` requiring only `numpy` to be
installed on the system.

* ``pip install https://github.com/retostauffer/python-colorspace``,
* Or clone the repository and use the good old ``python setup.py install``.

Some of the functions (those creating plots and manipulating images) depend on
``matplotlib`` and ``imageio``. The package will raise an error and inform you about
the dependency as soon as you run into them. However, depending on what want to do
there is no need for these two additional modules.

After successfully installing the package you might want to have a look into our
:ref:`page-gettingstarted` section of this documentation.



