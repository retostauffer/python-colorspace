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

    shutil.copy(join(qdir, "references.bib"), "_quarto/references.bib")




if __name__ == "__main__":
    main()

#    if not os.path.isdir("_quarto"):
#        action = "init"
#    else:
#        action = "document"
#    sub.call(["python", "makedocs.py", action, "-p", "colorspace"])
#
#    print("\n\n")
#            
#    # Checking for temporary_quarto_pages
#    def get_pages(dir = "temporary_quarto_pages"):
#        assert os.path.isdir(dir)
#        from glob import glob
#        tmp = glob(f"{dir}/*", recursive = True)
#        qmdfiles = []
#        for f in tmp:
#            if not re.match(".*\.qmd$", f): continue
#            qmdfiles.append(f)
#        return qmdfiles
#
#    # copy qmd files over to the new folder
#    qmdfiles   = get_pages()
#    naventries = [{"text": "Home", "file": "index.qmd"}]
#    if not os.path.isdir("_quarto/articles"):
#        os.mkdir("_quarto/articles")
#    for f in qmdfiles:
#        print(f"Copy template to: _quarto/{os.path.basename(f)}")
#        shutil.copy(f, f"_quarto/articles/{os.path.basename(f)}")
#        naventries.append({"text": re.sub("\.qmd$", "", os.path.basename(f)),
#                           "file": os.path.join("articles", os.path.basename(f))})
#
#    # Copy image folder
#    shutil.copytree("temporary_quarto_pages/images", "_quarto/articles/images",
#                     dirs_exist_ok = True)
#    shutil.copy("temporary_quarto_pages/references.bib", "_quarto/references.bib")
#
#    # Adding to _quarto.yml
#    print("Updating _quarto/_quarto.yml")
#    with open("_quarto/_quarto.yml", "r") as fid:
#        yml = yaml.safe_load(fid)
#
#    yml['website']['navbar']['left'] = naventries
#    with open("_quarto/_quarto.yml", "w") as fid:
#        yaml.dump(yml, fid)
#
