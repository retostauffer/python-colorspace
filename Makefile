
# -------------------------------------------------------------------
# Install and test the package
# -------------------------------------------------------------------

# Setting up a fresh virtualenv for running 'soft tests'.
# Only installs colorspace and the mandatory dependencies
# defined in setup.py (only `numpy`) plus `pytest` to run
# the tests.
.PHONY: softvenv
softvenv:
	-rm -rf softvenv
	virtualenv -p 3 softvenv
	softvenv/bin/pip install pytest
	softvenv/bin/pip install -e .

# Running soft tests with minimal requirements.
.PHONY: softtest
softtest:
	@echo "------ RUNNING TESTS WITH SOFT DEPENDENCIES -----"
	make softvenv
	softvenv/bin/pytest -s -m "not matplotlib and not pandas"

# Setting up virtual environment with all packages required
# for development and rendering the documentation. This is
# intended for developers only, not for 'users'.
venv: requirements_devel.txt
	-rm -rf venv
	virtualenv -p 3 venv
	venv/bin/pip install -r requirements_devel.txt
	(source venv/bin/activate && make install)
	
# Install Python colorspace.
install: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE *********"
	python setup.py clean --all && \
	pip install -e .

# Create man pages (_quarto/man/*.qmd) by extracting docstrings
# from python classes and functions. Requires pyp2qmd to be installed.
# - https://github.com/retostauffer/pyp2qmd
document:
	@echo "********* CREATE (OVERWRITE) QMD FILES ************"
	pyp2qmd document --package colorspace

# Uses `pyp2qmd` to extract all examples from the docstrings, and
# creates a series of quarto markdown files (qmd). Used for testing
# that the examples work as expected.
# - https://github.com/retostauffer/pyp2qmd
examples:
	@echo "********* CREATE (EXAMPLES) QMD FILES *************"
	rm -rf _examples
	pyp2qmd examples --package colorspace
	cd _examples && for file in *.qmd; do quarto render $$file || exit 99; done

# Render documentation. Requires quarto to be installed as well
# a series of python packages used in the documentation (see
# requirements_devel.txt; make venv).
# - https://quarto.org/
render:
	@echo "********* RENDERING QUARTO WEBSITE ****************"
	(make document && cd _quarto && quarto render)

# Prepare for PyPI
check:
	python setup.py check

sdist:
	-rm -rf dist
	python setup.py sdist

wheel:
	python setup.py bdist_wheel --universal


# Rules to push releases to PyPI test and PyPI.
# Makes use of the token/config stored in $HOME/.pypirc
testpypi:
	make sdist
	twine upload --verbose --repository testpypi dist/*

pypirelease:
	make sdist
	twine upload --verbose --repository pypi dist/*

# Creates baseimages
.PHONY: baseline
baseline:
	pytest --mpl-generate-path=baseline

# Running tests. Will first run soft tests and then
# the full tests with additional dependencies (matplotlib,
# pandas).
test:
	make softtest
	pip install -e .
	pytest -s

# Running pytest coverage analysis, creates coverage report
# in `htmlcov`. Also used by GitHub Action.
.PHONY: cov
cov:
	make venv
	make install
	(pytest --cov=src/colorspace --cov-report html)
	firefox htmlcov/index.html

.PHONY: clean
clean:
	-rm -rf src/colorspace.egg-info
	-find . -type d -name "__pycache__" -exec rm -rf {} \;

.PHONY: dockerpdf
dockerpdf:
	docker run --rm -it -v ${PWD}:/data -u $(id -u):$(id -g) \
	openjournals/inara -o pdf,crossref -p ./paper.md



