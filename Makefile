
install: setup.py
	$(info ********* REMOVE AND REINSTALL PY PACKAGE *********)
	python setup.py clean --all && \
	python setup.py install

develop: setup.py
	$(info ********* REMOVE AND REINSTALL PY PACKAGE *********)
	python setup.py clean --all && \
	python setup.py develop

