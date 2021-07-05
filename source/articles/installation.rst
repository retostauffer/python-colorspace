
.. _article-installation:

Package Installation
====================


At the moment the package is available via [github](github)
`github.com/retostauffer/python-colorspace <https://https://github.com/retostauffer/python-colorspace>`_.
Note that `numpy <https://pypi.org/project/numpy/>`_ needs to be installed to be able to
use the package.
A `PyPI <https://pypi.org>`_ release is planned in the future.


**Requirements**:

.. todo::
    Python 2.7+ support questionable as `imageio` is no longer available.
    I think it would be nice to have support for 2.7 if it can be done
    easily; else ignore and support 3+ only.

* Python 2.7+ or Python 3+
* `numpy`

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

.. todo::
    Update installation notes once the package has been released on
    `PyPi.org <https://pypi.org/>`_.
