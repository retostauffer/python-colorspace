# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
try:
    import matplotlib
    matplotlib.use('TkAgg')
    print("matplotlib: %s, %s" % (matplotlib.__version__, matplotlib.__file__))
except ImportError:
    print("no matplotlib")
try:
    import sphinx_bootstrap_theme
    print("sphinx_bootstrap_thme: %s, %s" %
          (sphinx_bootstrap_theme.__version__, sphinx_bootstrap_theme.__file__))
except ImportError:
    print("no sphinx_bootstrap_theme")
    raise Exception("Problems importing sphinx_bootstrap_theme!")

try:
    import IPython
    print("ipython: %s, %s" % (IPython.__version__, IPython.__file__))
except ImportError:
    print("no ipython")
try:
    import numpy
    print("numpy: %s, %s" % (numpy.__version__, numpy.__file__))
except ImportError:
    print("no numpy")

import colorspace
# print("colorspace: %s, %s" % (colorspace.__version__, colorspace.__file__))



# -- Project information -----------------------------------------------------

project   = "colorspace-pythondoc"
author    = "Reto Stauffer"
copyright = "2021, {:s}".format(author)

# The short X.Y version
version = colorspace.__version__
# The full version, including alpha/beta/rc tags.
release = colorspace.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'matplotlib.sphinxext.mathmpl',
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    ####'numpydoc',
    ####'sphinx.ext.ifconfig',
    'IPython.sphinxext.ipython_directive',
    'IPython.sphinxext.ipython_console_highlighting'
    ####'sphinx.ext.doctest',
    #'sphinx.ext.todo',
    ####'sphinx.ext.coverage',
    ####'sphinx.ext.viewcode',
    #####'sphinx.ext.githubpages',
    #'sphinxcontrib.bibtex'
]

ipython_warning_is_error = True

#napoleon_include_private_with_doc = True
#napoleon_include_special_with_doc = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Bibtex configuration ----------------------------------------------------

bibtex_bibfiles      = ['references.bib']
bibtex_default_style = 'label'
bibtex_encoding      = 'latin'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages. See the documentation for a
# list of builtin themes.
html_theme      = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
html_logo       = '_static/logo_wide.png'

html_css_files = ['css/colorspace.css']

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    'navbar_title': ' ', # empty by design! colorspace',

    # Tab name for entire site. (Default: "Site")
    'navbar_site_name': "Articles",

    # A list of tuples containing pages or urls to link to.
    # Valid tuples should be in the following forms:
    #    (name, page)                 # a link to a page
    #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
    #    (name, "http://example.com", True) # arbitrary absolute url
    # Note the "1" or "True" value above as the third argument to indicate
    # an arbitrary url.
    'navbar_links': [
        ("Get started", "getstarted"),
        ("News", "news"),
        ("API Reference", "api", False),
    ],

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,

    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': False,

    # Tab name for the current pages TOC. (Default: "Page")
    'navbar_pagenav_name': "Page",

    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': 2,

    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    'globaltoc_includehidden': "false",

    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    # 'navbar_class': "navbar navbar-inverse",

    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    'navbar_fixed_top': "true",

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    'source_link_position': "exclude",

    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing (default) or the name of a valid theme
    # such as "cosmo" or "sandstone".
    #
    # The set of valid themes depend on the version of Bootstrap
    # that's used (the next config option).
    #
    # Currently, the supported themes are:
    # - Bootstrap 2: https://bootswatch.com/2
    # - Bootstrap 3: https://bootswatch.com/3
    'bootswatch_theme': "sandstone",

    # Choose Bootstrap version.
    # Values: "3" (default) or "2" (in quotes)
    'bootstrap_version': "3",
}


# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}
html_sidebars = {"**": ["localtoc.html", "sourcelink.html", "searchbox.html"]}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Autodoc configuration

###autosummary_generate = True
###autodoc_default_flags = ['members', 'show-inheritance', 'inherited-members']
###autodoc_default_options = {
###    'members': True,
###    'member-order': 'bysource',
###    'special-members': '__init__',
###    'undoc-members': True,
###    'exclude-members': '__weakref__'
###}


# -- Extension configuration -------------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

intersphinx_mapping = {'numpy': ('http://docs.scipy.org/doc/numpy/', None),
                       'scipy': ('http://docs.scipy.org/doc/scipy/reference/', None),
                       'matplotlib': ('http://matplotlib.org/', None),
                       'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None)
                       }





