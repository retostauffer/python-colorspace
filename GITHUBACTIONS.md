

# Local Testing and GitHub Workflow Pipeline

Our GitHub repository comes with a `Makefil` (GNU make utility) as well
as files (pip requirement files) to run the commands alongside with a series
of `.github/workflow/`s for continuous integration.

This file gives a brief overview of how to (i) run local tests and how
(ii) the GitHub workflow is set up. This file is focusing on console users
in the 'Local Development and Testing' section.

**PLEASE NOTE:** If you are not a developer who wants to use our package, please
refer to the [Package Installation](https://retostauffer.github.io/python-colorspace/installation.html) article provided via our documentation. The following is intended
for contributors and developers.


# Local Development and Testing

## (1) Clone git repository

The following requires a local copy (i.e., clone) of our GitHub repository.
To clone the head branch (current development version) all you needed is:

```
git clone https://github.com/retostauffer/python-colorspace.git
cd python-colorspace
```

## (1) Setup

Tough trying to limit the dependencies for our `colorspace` package, a series
of packages are required for testing full functionality and running the tests.
Alongside this file, our GitHub repository provides a file called
`requirements_devel.txt` containing all packages for CI.

If `virtualenv` (Python virtual environment creator) is installed, the easiest
to set up the environment for running the tests is the following:

```
make venv                  # Creates python3 virtualenv 'venv'
```

## (2) Activating Virtual Environment

Simply call:

```
source venv/bin/activate   # Activate the virtual environment
```

## (3) Installing `colorspace` from local git clone

Once all dependencies (as well as those needed for testing) are installed,
the `colorspace` package can be installed into your virtual environment
(`venv`; for development) using:

```
make install
```

## (3) Local testing

We are using `pytest` to test our software. For local testing, simply call:

```
make test
```

## (4) Building Documentation

For our documentation we are using [`pyp2qmd`](https://github.com/retostauffer/pyp2qmd)
to automatically create the documentation for all exported classes, functions and methods
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
static HTML files stored under `_quarto/_site`. `make render` also calls `make document`
to always have the latest man pages when rendering.

Important to mention: All auto-generated man quarto documents (man pages; `_quarto/man`)
use `#| error: True` and `#| warning True` such hat, if an Example from the python
docstrings throws an error or warning, the documentation is still built. See next
section for more information.


## (5) Running Examples

Besides rendering the documentation (see section above) the Makefile provides a rule
to solely run all the Examples of all exported classes, functions, and methods. In
contrast to rendering the entire documentation, this rule only extracts the examples
from all exported classes, functions and methods using
[`pyp2qmd`](https://github.com/retostauffer/pyp2qmd) and creates a `.qmd` 
(Quarto Markdown) file for all examples; running them one by one.

This time, however (see 'Building Documentation') all the Examples are executed
using `#| error: False` and `#| warning: False` such that, in case there are
any errors or warnings, execution will fail.

## (6) Coverage

As for testing, `pytest` (pytest coverage) is used. We (for now) do not run
any doctests, but having a series of test files located under
`src/colorspace/tests` which will be run when calling:

```
make cov
```

This will create an HTML coverage report located under `htmlcov`.




# GitHub Actions

Whilst the sections above outline local testing, this section will provide
insights our CI (Continuous Integration) and GitHub Actions setup. The
configuration for all steps can be found under `.github/workflow/`.

Overall, we have a series of workflows in use:

1. `.github/workflow/pytest.yml`: Running "Tests"
2. `.github/workflow/quartoexamples.yml`: Testing "Examples"
3. `.github/workflow/quartodoc.yml`: Rendering "Documentation"
4. `.github/workflow/coverage.yml`: Running "Coverage"

Using GitHub's `workflow_run` they are not independent.

## (1) Testing

When pushed to our main branch, our "Test" (1) action will be triggered first
(basically `make test`). If successful, this will trigger "Examples" (2) as well
as "Documentation" (3) (in parallel).

This ensures that (i) our tests run successful, the documentation can be rendered
without issues (tough some of the Examples are allowed to fail) and that
our Examples can be executed without issues (tough the Documentation may show
issues).

If step (3), rendering the Documentation, was run successfully, it is pushed
to GitHub pages, triggering (4) Coverage. Using `pytest` all tests will be run
again, pushing the current coverage report as well as creating the coverage
badge shown on the [README](https://github.com/retostauffer/python-colorspace).


















