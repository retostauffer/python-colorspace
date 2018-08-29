# -------------------------------------------------------------------
# - NAME:        setup.py
# - AUTHOR:      Reto Stauffer
# - DATE:        2017-02-05
# - LICENSE: GPL-2, Reto Stauffer, copyright 2014
# -------------------------------------------------------------------
# - DESCRIPTION: The python-colorpsace package.
# -------------------------------------------------------------------
# - EDITORIAL:   2017-02-05, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2018-08-28 15:45 on marvin
# -------------------------------------------------------------------
##from setuptools import setup
from distutils.core import setup, Extension

module1 = Extension('demo',
                    sources = ['src/demo.c'])

setup(name='colorspace',     # This is the package name
      version='0.0-1',            # Current package version, what else
      description='Color space package for python',
      long_description='No long description necessary',
      classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        'GNU Lesser General Public License v2 (GPL-2)',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='colors HCL',
      url='https://github.com/retostauffer/python-colorspace',
      author='Reto Stauffer',
      author_email='reto.stauffer@uibk.ac.at',
      license='GPL-2',
      packages=['colorspace'],
      #scripts=['bin/PyIGRA','bin/PyIGRA_search'],
      ext_modules = [module1],
      include_package_data=True,
      czip_safe=False)

