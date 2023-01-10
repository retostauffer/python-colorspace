
.. _article-installation:

Package Installation
====================

At the moment the package is available via
`<https://https://github.com/retostauffer/python-colorspace>`_.
A few requirements are needed to be able to use the package and all its features.

* Python ``3.10+``
* `numpy <https://pypi.org/project/numpy/>`_
* `matplotlib <https://pypi.org/project/matplotlib/>`_
* `imageio <https://pypi.org/project/imageio/>`_ (optional).

A release of the *colorspace* package on `PyPi <https://pypi.org>`_ is planned
in the near future. Please use the
`git issues <https://github.com/retostauffer/python-colorspace/issues>`_
to report bugs and issues as well as feature requests. There is no
guarantee that feature requests can be accommodated, especially as we try to
keep both, the R and Python version of the package, around the same level.


**Installing via pip**

The package can be installed via `pip <https://pypi.org/project/pip/>`_ using the following command:

.. code-block:: console

    pip install https://github.com/retostauffer/python-colorspace


**Cloning the git repository**

Alternatively, clone the git repository and install the package:

.. code-block:: console

    git clone https://github.com/retostauffer/python-colorspace.git
    cd python-colorspace && python setup.py install

**Using a virtual environment**

The repository contains a ``Makefile`` and requirements files to set up virtual
environments.  Note that this requires ``make`` and ``virtualenv`` to be
installed.

To set up a virtual environments the git repository must be cloned first;
afterwards you should be able to set up the virtual environment
and install the *colorspace* package.

.. code-block:: console

    # Using the binary 'python3'
    git clone https://github.com/retostauffer/python-colorspace.git
    cd python-colorspace
    make venv3
    make install

This will set up a virtual environment and also install the required
python packages before installing the latest version of the *colorspace*
package from the repository.



