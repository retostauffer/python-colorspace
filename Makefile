
# -------------------------------------------------------------------
# Install and test the package
# -------------------------------------------------------------------
#
#  Imageio does not longer exist for python 2.7 via pip.
#  Can we already neglect python2?
#venv2: requirements.txt
#	-rm -rf venv2
#	virtualenv -p python2 venv2
#	venv2/bin/pip install -r requirements.txt

venv3: requirements.txt
	-rm -rf venv3
	virtualenv -p python3 venv3
	venv3/bin/pip install -r requirements.txt

install: setup.py
	$(info ********* REMOVE AND REINSTALL PY PACKAGE *********)
	python setup.py clean --all && \
	python setup.py install

develop: setup.py
	$(info ********* REMOVE AND REINSTALL PY PACKAGE *********)
	python setup.py clean --all && \
	python setup.py develop

test:
	pytest -s

cov:
	(cd colorspace && \
		coverage run --source colorspace -m pytest && \
		coverage html --directory=../coverage)
		##chromium-browser htmlcov/index.html)

.PHONY: clean
clean:
	-rm -rf build
	-rm source/api/*
	-rm source/colorlib/*

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile
	#-rm -rf build
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

