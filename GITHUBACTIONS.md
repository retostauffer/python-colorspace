

# Local Testing and GitHub Workflow Pipeline

Our GitHub repository comes with a `Makefile` (GNU make utility) as well
pip requirement files allowing for local testing and building the documentation.
These rules are also used for the GitHub actions (see `.github/workflow`)
used for continuous integration.

This file gives a brief overview of how to (i) run local tests and how
(ii) the GitHub workflow is set up.

**PLEASE NOTE:** If you are not a developer wishing to use our package, please refer to the
[Package Installation](https://retostauffer.github.io/python-colorspace/installation.html)
article available via the documentation. The following is intended
for contributors and developers, focusing on console users.


# Local Development and Testing

## (1) Clone git repository

The following requires a local copy (i.e., clone) of our GitHub repository.
To clone the head branch (the current development version) all you need is:

```
git clone https://github.com/retostauffer/python-colorspace.git
cd python-colorspace
```

## (1) Setup

Tough trying to limit the dependencies for our `colorspace` package, a series
of additional python packages is required for testing and building the documentation.
The pip requirements file `requirements_devel.txt` provides all required packages which
is also use for CI.

With `virtualenv` (Python virtual environment creator) installed, the easiest way
to set up the environment to run the test is as follows:

```
# Creates python3 virtualenv 'venv' and installs all packages
# listed in requirements_devel.txt
make venv
```

## (2) Activating Virtual Environment

To activate the virtual environment simply call:

```
source venv/bin/activate   # Activate the virtual environment
```

## (3) Installing `colorspace` from local git clone

Once all dependencies (as well as those needed for testing) are installed,
the `colorspace` package can be installed into your virtual environment
(`venv`; for development) using:

```
make install               # Installs colorspace from local git clone
```

## (3) Local testing

We use `pytest` to test our software. For local testing, simply call:

```
make test
```

## (4) Building Documentation

For our documentation we use [`pyp2qmd`](https://github.com/retostauffer/pyp2qmd)
to automatically generate documentation for all exported classes, functions and methods
(installed via `requirements_devel.txt`; see step (1)) and [`quarto`](https://quarto.org/)
to render the HTML documentation. To update the documentation, run:

```
make document
```

To build (render) the documentation use:

```
make render
```

... which renders all `.qmd` (Quarto Markdown) files located in the `_quarto` folder into
static HTML files stored under `_quarto/_site`. `make render` also calls `make document`,
so that the latest man pages are always available when rendering.

Important to note: All automatically generated quarto man pages (`_quarto/man`)
use `#| error: True` and `#| warning True` so hat if an 'Example' from the Python
docstrings throws an error or warning, the documentation will still be built. See
the next section for more information.


## (5) Running Examples

In addition to rendering the documentation (see section above) the Makefile
provides a rule to run only the 'Examples' from the Python dostrings of all
exported classes, functions, and methods.
In contrast to rendering the entire documentation, this rule only extracts the examples
from all exported classes, functions and methods using
[`pyp2qmd`](https://github.com/retostauffer/pyp2qmd) and creates `.qmd` 
(Quarto Markdown) files for all the 'Examples', which are run one by one.

This time, however (see 'Building Documentation') all the Examples are executed
using `#| error: False` and `#| warning: False` such that, in case there are
any errors or warnings, execution will fail and an error is thrown. This is also
used for testing the 'Examples' during CI.

```
make examples     # Extract and run/render all 'Examples'
```

## (6) Coverage

As for testing, `pytest` (pytest coverage) is used. We do not run any doctests
(for now), but have a set of test files located in `src/colorspace/tests` that
are run when calling:

```
make cov
```

Creates an HTML coverage report located stored in `htmlcov`, also used during CI.



# GitHub Actions

While the sections above outline local testing, this section gives an
insights into our CI (Continuous Integration) and GitHub Actions setup. The
configuration for all steps can be found in `.github/workflow/`.

Overall, we have a number of workflows in use with a series of dependencies
(via workflow execution) outlined by the nested list below.

* [1] `.github/workflow/pytest.yml`: Running "Tests"
    * [2] `.github/workflow/quartoexamples.yml`: Testing "Examples"
    * [3] ``.github/workflow/quartodoc.yml`: Rendering "Documentation"
        * [4] `.github/workflow/coverage.yml`: Running "Coverage"

Using GitHub's `workflow_run` they are not independent.

## (1) Testing

When pushed to our main branch, our "Test" action (1) will be triggered first
(basically `make test`). If successful, this will trigger both "Examples" (2) and
"Documentation" (3) (in parallel).

This ensures that (i) our tests run successfully and the documentation can be rendered
without problems (tough, the Examples are allowed to fail) and that
our Examples can be executed without issues.

If step (3), rendering the documentation, was successful, it will be pushed
to GitHub pages, triggering Coverage (4). Using `pytest` all tests will be run
again, pushing the current coverage report and creating the coverage
badge shown on the [README](https://github.com/retostauffer/python-colorspace).


















