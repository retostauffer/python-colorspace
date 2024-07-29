# -------------------------------------------------------------------
# - NAME:        setup.py
# - AUTHOR:      Reto Stauffer
# - LICENSE:     GPL-2 | GPL-3, Reto Stauffer, copyright 2022-2024
# -------------------------------------------------------------------
# - DESCRIPTION: The python-colorpsace package.
# -------------------------------------------------------------------


import os
from setuptools import setup, find_packages

ISRELEASED    = False
VERSION       = "0.5.0"
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
        filename = path.join(path.dirname(__file__), "src", "colorspace", "version.py")

    a = open(filename, "w")
    try:
        a.write(cnt % (FULLVERSION, VERSION, ISRELEASED))
    finally:
        a.close()

# Write version information
if WRITE_VERSION:
    write_version_py()

# Reading 'README.md'; replaces Markdown-style hyperrefs with rst style
# links as expected by PyPI for the long description of the package.
def README():
    from re import findall, match
    content  = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
    return content

# Setup
setup(name="colorspace",     # This is the package name
      version = VERSION,     # Current package version, what else
      description = "A Python toolbox for manipulating and assessing colors and palettes",
      project_urls = {
          "Documentation": "https://retostauffer.github.io/python-colorspace/",
          "Repository": "https://github.com/retostauffer/python-colorspace/",
          "Issues": "https://github.com/retostauffer/python-colorspace/issues/",
          "HCL Wizard": "https://hclwizard.org/"
      },
      long_description = README(),
      long_description_content_type = "text/markdown",
      url = "https://github.com/retostauffer/python-colorspace",
      author               = "Reto Stauffer, Achim Zeileis",
      author_email         = "Reto.Stauffer@uibk.ac.at, Achim.Zeileis@uibk.ac.at",
      maintainer           = "Reto Stauffer",
      maintainer_email     = "reto.stauffer@uibk.ac.at",
      license              = "GPL-2 | GPL-3",
      keywords             = "colors, color palettes, color spaces, manipulate colors, HCL, HCL colors, color vision deficiencies",
      classifiers = [
          "Topic :: Scientific/Engineering :: Visualization",
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Programming Language :: Python :: 3.11"
      ],
      install_requires     = ["numpy"],
      packages             = find_packages("src"),
      package_dir          = {"": "src"},
      include_package_data = True)

