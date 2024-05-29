#!/usr/bin/env python3


import os
import subprocess as sub
import shutil
import yaml
import re


def main():

    from os.path import join, basename
    from pyp2qmd import Config, DocConverter

    # Absolute path of this script
    abspath = os.path.dirname(__file__)

    # Initialize Config; parses user arguments via argparse
    config  = Config()
    config.setup(action = "init", package = "colorspace",
                 output_dir = "_site", overwrite = True)

    # Initialize DocConverter; creates _quarto.yml,
    # pyp.sass, and index.qmd if needed.
    docconv = DocConverter(config)

    docconv.document()
    docconv.update_quarto_yml()

    # Quarto source folder for now
    qdir = os.path.join(abspath, "temporary_pages")

    # Adding test page
    qfiles = {"Home": "index.qmd",
              "Installation": "installation.qmd",
              "Get started": "getstarted.qmd",
              "API": "api.qmd",
              "Changelog": "changelog.qmd"}
    for k,f in qfiles.items():
        src = join(qdir, f)
        docconv.add_navbar_page(src, basename(src), k)


    # Adding a menu 'articles'
    docconv.add_navbar_menu("Articles")

    # Adding articles to Articles menu
    qfiles = {"Color spaces": "color_spaces.qmd",
              "HCL-Based Color Palettes": "hcl_palettes.qmd",
              "Palette Visualization and Assessment": "palette_visualization.qmd",
              "App for Choosing Palettes Interactively": "choose_palette.qmd",
              "Color Vision Deficiency Emulation": "cvd.qmd",
              "Color Manipulation and Utilities": "manipulation_utilities.qmd",
              "Approximate Colors from Other Packages": "approximations.qmd",
              "Classes and Methods": "classes_and_methods.qmd",
              "Somewhere over the Rainbow": "endrainbow.qmd"}

    for k,f in qfiles.items():
        src = join(qdir, f)
        docconv.add_navbar_page(src, join("articles", basename(src)), k, menu = "Articles")

    # Moving some images
    imgdir = join(docconv.config_get("quarto_dir"), "images")
    if not os.path.isdir(imgdir): os.makedirs(imgdir)

    for img in ["human-axes.svg", "hcl-projections-1.png", "img_gui.jpeg"]:
        shutil.copy(join(qdir, "images", img), join(imgdir, img))

    # Adding logo
    shutil.copy(join(qdir, "logo-wide.png"), "_quarto/logo-wide.png")
    docconv.add_logo("logo-wide.png", title = None)

    # Adding additional scss file for styling
    shutil.copy(join(qdir, "colorspace.scss"), "_quarto/colorspace.scss")
    docconv.add_scss("colorspace.scss")

    # Copy some static files around
    shutil.copy(join(qdir, "references.bib"), "_quarto/references.bib")
    shutil.copy(join(qdir, "python-logo.svg"), "_quarto/python-logo.svg")

    # Adding repo and issue URL + github icon
    repo_url    = "https://github.com/retostauffer/python-colorspace"
    repo_branch = "main"
    docconv.add_repo_url(repo_url, repo_branch)
    docconv.add_issue_url("https://github.com/retostauffer/python-colorspace/issues")

    docconv.add_navbar_right({"icon": "github", "href": f"{repo_url}/tree/{repo_branch}"})

    docconv.add_navbar_right({"text": "![](/python-logo.svg)",
                              "href": "https://pypi.org"})


if __name__ == "__main__":
    main()
