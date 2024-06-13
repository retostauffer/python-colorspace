
# -------------------------------------------------------------------
# Install and test the package
# -------------------------------------------------------------------


venv: requirements_devel.txt
	-rm -rf venv
	virtualenv -p 3 venv
	venv/bin/pip install -r requirements_devel.txt

install: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE *********"
	python setup.py clean --all && \
	pip install -e .

document:
	@echo "********* CREATE (OVERWRITE) QMD FILES ************"
	pyp2qmd document --package colorspace

examples:
	@echo "********* CREATE (EXAMPLES) QMD FILES *************"
	rm -rf _examples
	pyp2qmd examples --package colorspace
	cd _examples && for file in *.qmd; do quarto render $$file; done

render:
	@echo "********* RENDERING QUARTO WEBSITE ****************"
	(cd _quarto && quarto render)

develop: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE *********"
	python setup.py clean --all && \
	pip install -e .[dev]

# Prepare for PyPI
check:
	python setup.py check

sdist:
	-rm -rf dist
	python setup.py sdist

wheel:
	python setup.py bdist_wheel --universal


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

test:
	pip install -e .
	pytest -s

doctest:
	pip install -e .
	pytest src/colorspace --doctest-modules

cov:
	(pytest --cov=src/colorspace --cov-report html)
	###(pytest --cov=src/colorspace --cov-report html:htmlcov/ --cov-report xml:coverage.xml && \
	###	firefox htmlcov/index.html)

.PHONY: clean
clean:
	-rm -rf src/colorspace.egg-info




