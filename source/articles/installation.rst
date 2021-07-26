
.. _article-installation:

Package Installation
====================

At the moment the package is available via [github](github)
`github.com/retostauffer/python-colorspace <https://https://github.com/retostauffer/python-colorspace>`_.
A few requirements are needed to be able to use the package and all its features.

* Python ``3.4+`` or ``2.7`` (limited support)
* `numpy <https://pypi.org/project/numpy/>`_
* `imageio <https://pypi.org/project/imageio/>`_ (optional).
  Check the comment below in case you are still running Python ``2.7``.

A release of the ``colorspace`` package on `PyPi <https://pypi.org>`_ is planned
in the near future.

**Python 2.7**

Imageio has ended support for Python version ``2.7``. Imageio ``2.6.x`` is the last
release candidate to support Python ``2.7``. Make sure you install the correct version
in this case (``imageio==2.6.1``).


**Install via pip**

The package can be installed via `pip <https://pypi.org/project/pip/>`_ using
the following command:

.. code-block:: console

    pip install https://github.com/retostauffer/python-colorspace


**Clone git Repository**

Alternatively, clone the git repository and install the package:

.. code-block:: console

    git clone https://github.com/retostauffer/python-colorspace.git
    cd python-colorspace && python setup.py install

