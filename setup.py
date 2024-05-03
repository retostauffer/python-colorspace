# -------------------------------------------------------------------
# - NAME:        setup.py
# - AUTHOR:      Reto Stauffer
# - LICENSE:     GPL-2, Reto Stauffer, copyright 2022
# -------------------------------------------------------------------
# - DESCRIPTION: The python-colorpsace package.
# -------------------------------------------------------------------


import os
from setuptools import setup

ISRELEASED    = False
VERSION       = "0.4.1"
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

# Write version information
if WRITE_VERSION:
    write_version_py()

# Reading 'README.md'; replaces Markdown-style hyperrefs with rst style
# links as expected by PyPI for the long description of the package.
def README():
    from re import findall, match
    content  = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
    return content

    ## Find markdown links; replace them with rst-compatible links
    #md_links = findall("\[.*?[^\]].*?(?<=\))", content)
    #def md_to_rst(x):
    #    link = match("\[(.*?)\]\((.*?)\)", x).groups()
    #    if not link: raise ValueError(f"Problems encoding {x} (changing link format).")
    #    return f"`{link[0]} <{link[1]}>_`"
    #for x in md_links: content = content.replace(x, md_to_rst(x))
    #return content

# Setup
setup(name="colorspace",     # This is the package name
      version = VERSION,     # Current package version, what else
      description = "Color space package for python",
      long_description = README(),
      long_description_content_type = "text/markdown",
      url = "https://github.com/retostauffer/python-colorspace",
      author = "Reto Stauffer [aut,cre], Ross Ihaka [ctb], Paul Murrell [ctb], Kurt Hornik [ctb], Jason C. Fisher [ctb], Claus O. Wilke [ctb], Claire D. Mc White [ctb], Achim Zeileis [ctb]",
      author_email = "Reto.Stauffer@uibk.ac.at",
      maintainer = "Reto Stauffer",
      maintainer_email = "reto.stauffer@uibk.ac.at",
      license = "GPL-2",
      keywords = "colors HCL",
      classifiers = [
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Programming Language :: Python :: 3.11"
      ],
      install_requires = ["numpy"],

      packages = ["colorspace"],
      include_package_data = True)

