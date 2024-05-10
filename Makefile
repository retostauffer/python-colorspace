
# -------------------------------------------------------------------
# Install and test the package
# -------------------------------------------------------------------


venv: requirements.txt
	-rm -rf venv
	virtualenv -p 3 venv
	venv/bin/pip install -r requirements.txt

install: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE *********"
	python setup.py clean --all && \
	pip install -e .

develop: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE *********"
	python setup.py clean --all && \
	pip install -e .[dev]

# Prepare for PyPI
check:
	python setup.py check

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel --universal

testpypi:
	make sdist
	$(eval VERSION = $(shell cat colorspace/version.py | egrep "^version" | egrep -oE "[0-9\.]+"))
	@echo "********** Uploading dist/colorspace-$(VERSION).tar.gz **********"
	#twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/colorspace-$(VERSION).tar.gz


# Creates baseimages
.PHONY: baseline
baseline:
	pytest --mpl-generate-path=baseline

test:
	pytest -s

cov:
	(cd colorspace && \
		coverage run --source colorspace -m pytest && \
		coverage html --directory=../coverage)
		##chromium-browser htmlcov/index.html)

.PHONY: clean
clean:
	-rm -rf src/colorspace.egg-info




