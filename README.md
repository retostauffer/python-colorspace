<img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-wide.png" width="350" alt="python-colorspace"/>

## A Python toolbox for manipulating and assessing colors and palettes

[![Documentation](https://github.com/retostauffer/python-colorspace/actions/workflows/quartodoc.yml/badge.svg?branch=main)](https://github.com/retostauffer/python-colorspace/actions/workflows/quartodoc.yml)
[![Examples](https://github.com/retostauffer/python-colorspace/actions/workflows/quartoexamples.yml/badge.svg?branch=main)](https://github.com/retostauffer/python-colorspace/actions/workflows/quartoexamples.yml)
[![Testing](https://github.com/retostauffer/python-colorspace/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/retostauffer/python-colorspace/actions/workflows/pytest.yml)
[![Coverage](https://github.com/retostauffer/python-colorspace/actions/workflows/coverage.yml/badge.svg?branch=main)](https://github.com/retostauffer/python-colorspace/actions/workflows/coverage.yml)
[![](https://retostauffer.github.io/python-colorspace/coverage.svg)](https://retostauffer.github.io/python-colorspace/coverage/)
[![status](https://joss.theoj.org/papers/94041eecfa4b186c7c07252875817578/status.svg)](https://joss.theoj.org/papers/94041eecfa4b186c7c07252875817578)

The package provides a Python 3 version of the
[R colorspace](http://colorspace.R-Forge.R-project.org/) package comprising:

- **Color spaces:** Conversions and manipulations of RGB, HSV, CIEXYZ, CIELAB, CIELUV, HCL etc.
- **HCL-based palettes:** Qualitative, sequential, and diverging color maps constructed
  using the HCL (hue-chroma-luminance) color model. These can closely approximate palettes
  from ColorBrewer.org, CARTO, viridis, or Crameri's scientific color maps.
- **matplotlib color maps:** Integration with [matplotlib](https://matplotlib.org/) for
  use in standard plotting functions.
- **Palette visualization:** Plotting palettes in color swatches, spectrums of HCL and/or
  RGB trajectories, and illustrations of typical data visualizations.
- **Interactive palette chooser:** App for exploring, modifying, and picking color
  palettes interactively.
- **Color vision deficiency:** Emulation of different kinds of color blindness.
- **Utilities:** Various color manipulations including tools to desaturate, lighten, darken,
  adjust the transparency, or compute the contrast ratio.


## Links

- **PyPI:** <https://pypi.org/project/colorspace/>
- **GitHub:** <https://github.com/retostauffer/python-colorspace/>
- **Documentation:** <https://retostauffer.github.io/python-colorspace/>
- **Bug reports:** <https://github.com/retostauffer/python-colorspace/issues>
  _Bug reports and suggestions are welcome and very much appreciated!_


## Contributors

- [Reto Stauffer](https://retostauffer.org/)
  <a target="_new" href="https://orcid.org/0000-0002-3798-5507"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
  (_principal author & maintainer_), Universität Innsbruck, Austria
- [Achim Zeileis](https://www.zeileis.org/)
  <a target="_new" href="https://orcid.org/0000-0003-0918-3766"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
  Universität Innsbruck, Austria

We would like to thank the following individuals for their contributions to the
review process for this software, as part of the submission to
[The Journal of Open Source Software](https://joss.theoj.org/) (JOSS):
[Julia Romanowska @jromanowska, Editor](https://github.com/jromanowska)
  <a target="_new" href="https://orcid.org/0000-0001-6733-1953"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
[Daniel S. Katz @danielskatz, Editor](https://github.com/danielskatz)
  <a target="_new" href="https://orcid.org/0000-0001-5934-7525"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
[David Reagan @dmreagan, Reviewer](https://github.com/dmreagan)
  <a target="_new" href="https://orcid.org/0000-0002-8359-7580"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
[Andrew Ting @hollowscene, Reviewer](https://github.com/hollowscene).

Furthermore, the Python package implements the functionality from the R package
that is co-written with
[Ross Ihaka](https://www.stat.auckland.ac.nz/~ihaka/),
[Paul Murrell](https://www.stat.auckland.ac.nz/~paul/)
  <a target="_new" href="https://orcid.org/0000-0002-3224-8858"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
[Kurt Hornik](https://statmath.wu.ac.at/~hornik/)
  <a target="_new" href="https://orcid.org/0000-0003-4198-9911"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
[Jason C. Fisher](https://www.usgs.gov/staff-profiles/jason-c-fisher)
  <a target="_new" href="https://orcid.org/0000-0001-9032-8912"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
[Claus O. Wilke](https://clauswilke.com/)
  <a target="_new" href="https://orcid.org/0000-0002-7470-9261"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>,
[Claire D. McWhite](https://clairemcwhite.github.io/)
  <a target="_new" href="https://orcid.org/0000-0001-7346-3047"><img src="https://raw.githubusercontent.com/retostauffer/python-colorspace/main/_quarto/logo-orcid.svg" width="16px" alt="ORCID iD"/></a>.


## Citations

Stauffer, R. and Zeileis A. (2024). "colorspace: A Python Toolbox for Manipulating
and Assessing Colors and Palettes." _The Journal of Open Source Software_,
9(102), 7120, doi:[10.21105/joss.07120](https://doi.org/10.21105/joss.07120).

Stauffer, R. and Zeileis, A. (2024). "colorspace: A Python Toolbox for Manipulating and Assessing Colors and Palettes (v1.0.0)". _Zenodo_.
doi:[10.5281/zenodo.14004295](https://doi.org/10.5281/zenodo.14004295).

## Development notes

### Community guidelines

If you encountery any bugs or issues, or are interested in contributing
to Python _colorspace_, please have a look at our
[Community guidelines](https://retostauffer.github.io/python-colorspace/community.html).

### Test and development

More detailed information on how to run automated tests, create coverage reports,
test examples and render the documentation can be found on our 
[Installation](https://retostauffer.github.io/python-colorspace/installation.html#test-and-development) page.

### GitHub Action integration (CI)

Additional notes about development and deployment are documented in
[GITHUBACTIONS.md](https://github.com/retostauffer/python-colorspace/blob/main/GITHUBACTIONS.md).
