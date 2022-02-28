# -------------------------------------------------------------------
# - NAME:        setup.py
# - AUTHOR:      Reto Stauffer
# - LICENSE: GPL-2, Reto Stauffer, copyright 2014
# -------------------------------------------------------------------
# - DESCRIPTION: The python-colorpsace package.
# -------------------------------------------------------------------
# - EDITORIAL:   2017-02-05, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2018-09-17 15:53 on marvin
# -------------------------------------------------------------------


from setuptools import setup

ISRELEASED    = False
VERSION       = "0.2.0"
FULLVERSION   = VERSION
WRITE_VERSION = True

# Write version string
def write_version_py(filename=None):
    cnt = """\
version = '%s'
short_version = '%s'
isreleased = %s
"""
    from os import path
    if not filename:
        filename = path.join(path.dirname(__file__), "colorspace", "version.py")

    a = open(filename, "w")
    try:
        a.write(cnt % (FULLVERSION, VERSION, ISRELEASED))
    finally:
        a.close()

if WRITE_VERSION:
    write_version_py()

# Setup

setup(name="colorspace",     # This is the package name
      version = VERSION,     # Current package version, what else
      description = "Color space package for python",
      long_description = "Provides a set of color transformation functions and an interface to chose efficient color maps based on the HCL color space. This package is inspired and based on the R package 'colorspace'.",
      url = "https://github.com/retostauffer/python-colorspace",
      author = "Reto Stauffer [aut,cre], Ross Ihaka [ctb], Paul Murrell [ctb], Kurt Hornik [ctb], Jason C. Fisher [ctb], Claus O. Wilke [ctb], Claire D. Mc White [ctb], Achim Zeileis [ctb]",
      author_email = "Reto.Stauffer@uibk.ac.at",
      maintainer = "Reto Stauffer",
      maintainer_email = "reto.stauffer@uibk.ac.at",
      license = "GPL-2",
      keywords = "colors HCL",
      classifiers = [
        "Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        "GNU Lesser General Public License v2 (GPL-2)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.8",
      ],
      install_requires = ["numpy"],

      packages = ["colorspace"],
      include_package_data = True)

