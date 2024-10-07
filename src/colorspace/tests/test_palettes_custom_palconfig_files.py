# -------------------------------------------------------
# Note: To be complient with Windows, NamedTemporaryFiles
# are closed and deleted manually to avoid file permission
# errors (delete = False; manually .close() and os.remove()
# them when no longer needed).
# -------------------------------------------------------

import os
import pytest
from pytest import raises
from colorspace import hclpalettes
import numpy as np
from tempfile import NamedTemporaryFile
import os

# Content used below to create custom temporary palconfig files
good_custom_div = """
[main]
type   = Custom diverging
method = diverging_hcl

[palette Barcelona]
desc  =  Modified Lisbon palette for testing
h1    =  180
h2    =  300
c1    =   25
l1    =   85
l2    =   16
p1    =  1.0
cmax  =   45
fixup =    1
gui   =    0
"""

good_custom_seq = """
[main]
type   = Custom qualitative
method = qualitative_hcl

[palette Darkwarmish]
desc  =  Customized 'Warm' palette
h1    =   90
h2    =  lambda x: -x / 2.0
c1    =   60
l1    =   60
fixup =    1
gui   =    0

[palette Darkcold]
desc  =  ...
h1    =  270
h2    =  150
c1    =   50
l1    =   30
fixup =    1
gui   =    1
"""


# ------------------------------------------
# ------------------------------------------
def test_hclpalettes_custom_palconfig_wrong_usage():

    # Wrong type for 'files'
    raises(TypeError, hclpalettes, files = 3)
    raises(TypeError, hclpalettes, 3)
    raises(TypeError, hclpalettes, [3, "foo"])

    # Wrong use of 'files_regex'
    raises(TypeError, hclpalettes, files_regex = 3)
    raises(TypeError, hclpalettes, files_regex = ["foo", "bar"])

    # Using methods wrongly
    pals = hclpalettes()
    raises(TypeError, pals.get_palettes, 3)
    raises(TypeError, pals.get_palettes, True)
    raises(TypeError, pals.get_palettes, ["foo"])
    raises(TypeError, pals.get_palettes, exact = 3)
    raises(TypeError, pals.get_palettes, exact = None)



# ------------------------------------------
# ------------------------------------------
def test_hclpalettes_custom_palconfig_good_custom_div():

    tmpfile = NamedTemporaryFile(delete = False)
    with open(tmpfile.name, "w") as fid: fid.write(good_custom_div)

    pals1 = hclpalettes(files = tmpfile.name)
    pals2 = hclpalettes(files = [tmpfile.name])

    tmpfile.close()
    os.unlink(tmpfile.name)

    # Should both return the same, testing both
    for pals in [pals1, pals2]:
        assert isinstance(pals, hclpalettes)
        assert isinstance(pals.get_palette_types(), list)
        assert len(pals.get_palette_types()) == 1
        assert isinstance(pals.get_palette_types()[0], str)
        assert pals.get_palette_types()[0] == "Custom diverging"
        tmp = pals.get_palettes()
        assert isinstance(tmp, list)
        assert len(tmp) == 1
        tmp = tmp[0]
        assert tmp.name() == "Barcelona"
        assert tmp == pals.get_palette("Barcelona")

        # Testing settings
        expecting = {"h1":  180, "h2":  300, "c1":  25, "l1":  85, "l2":  16,
                    "p1":   1.0, "cmax":  45, "fixup":  1, "gui": 0}
        tmp = tmp.get_settings()
        for k,v in expecting.items():
            assert isinstance(tmp[k], type(v))
            assert tmp[k] == v

    # Closing file connection and delete temporary file
    tmpfile.close()
    os.remove(tmpfile.name)


# ------------------------------------------
# We have tested a lot of things in custom_div, so we can
# reduce the test set a bit here and focus on the main things:
# we have two palettes, and the first one has a lambda function
# on h2.
# ------------------------------------------
def test_hclpalettes_custom_palconfig_good_custom_seq():

    tmpfile = NamedTemporaryFile(delete = False)
    with open(tmpfile.name, "w") as fid: fid.write(good_custom_seq)

    pals = hclpalettes(files = tmpfile.name)

    tmpfile.close()
    os.unlink(tmpfile.name)

    assert len(pals.get_palettes()) == 2
    pal = pals.get_palette("Darkwarmish")
    assert callable(pal.get_settings()["h2"])
    assert pal.get_settings()["h2"](100) == -50.

    # Closing file connection and delete temporary file
    tmpfile.close()
    os.remove(tmpfile.name)

# ------------------------------------------
# Reading both at the same time
# ------------------------------------------
def test_hclpalettes_custom_palconfig_good_custom_seq_and_div():

    # Write and read both files at once
    tmpfile_div = NamedTemporaryFile(delete = False)
    with open(tmpfile_div.name, "w") as fid: fid.write(good_custom_div)
    tmpfile_seq = NamedTemporaryFile(delete = False)
    with open(tmpfile_seq.name, "w") as fid: fid.write(good_custom_seq)

    # Reading palette config
    pals = hclpalettes(files = [tmpfile_div.name, tmpfile_seq.name])

    ptypes = pals.get_palette_types()
    assert isinstance(ptypes, list)
    assert len(ptypes) == 2
    assert np.all(ptypes == ["Custom qualitative", "Custom diverging"])

    assert isinstance(pals.get_palettes("Custom qualitative"), list)
    assert len(pals.get_palettes("Custom qualitative")) == 2
    assert isinstance(pals.get_palettes("Custom diverging"), list)
    assert len(pals.get_palettes("Custom diverging")) == 1

    # get_palettes with exact match
    assert isinstance(pals.get_palettes("Custom qualitative", exact = True), list)
    assert len(pals.get_palettes("Custom qualitative", exact = True)) == 2

    # Closing file connection and delete temporary file
    tmpfile_div.close()
    os.remove(tmpfile_div.name)
    tmpfile_seq.close()
    os.remove(tmpfile_seq.name)

# ------------------------------------------
# Bad custom palconfig file: Missing [main]
# ------------------------------------------
bad_custom1 = """
[palette Barcelona]
desc  =  Modified Lisbon palette for testing
h1    =  180
h2    =  300
c1    =   25
l1    =   85
l2    =   16
p1    =  1.0
cmax  =   45
fixup =    1
gui   =    0
"""

bad_custom2 = """
[main]
type  = Custom palette

[palette Barcelona]
desc  =  Modified Lisbon palette for testing
h1    =  180
h2    =  300
c1    =   25
l1    =   85
l2    =   16
p1    =  1.0
cmax  =   45
fixup =    1
gui   =    0
"""

bad_custom3 = """
[main]
method = diverging_hcl

[palette Barcelona]
desc  =  Modified Lisbon palette for testing
h1    =  180
h2    =  300
c1    =   25
l1    =   85
l2    =   16
p1    =  1.0
cmax  =   45
fixup =    1
gui   =    0
"""

bad_custom4 = """
[main]
type   = Custom palette
method = diverging_hcl

[palette Barcelona]
desc  =  Modified Lisbon palette for testing
h1    =  foo bar
h2    =  300
c1    =   25
l1    =   85
l2    =   16
p1    =  1.0
cmax  =   45
fixup =    1
gui   =    0
"""

def test_hclpalettes_custom_palconfig_broken_palconfig():

    tmpfile = NamedTemporaryFile(delete = False)
    with open(tmpfile.name, "w") as fid: fid.write(bad_custom1)

    raises(Exception, hclpalettes, tmpfile.name)
    tmpfile.close() # Closing file connection

    with open(tmpfile.name, "w") as fid:
        fid.write(bad_custom2)
    raises(Exception, hclpalettes, tmpfile.name)
    tmpfile.close() # Closing file connection

    with open(tmpfile.name, "w") as fid:
        fid.write(bad_custom3)
    raises(Exception, hclpalettes, tmpfile.name)
    tmpfile.close() # Closing file connection

    with open(tmpfile.name, "w") as fid:
        fid.write(bad_custom4)
    raises(ValueError, hclpalettes, tmpfile.name)

    # Closing file connection and delete temporary file
    tmpfile.close()
    os.remove(tmpfile.name)


empty_palconf = """

[main]
type   = Custom palette
method = diverging_hcl

"""

def test_hclpalettes_custom_palconfig_empty_palconfig():

    tmpfile = NamedTemporaryFile(delete = False)
    with open(tmpfile.name, "w") as fid: fid.write(empty_palconf)

    pals = hclpalettes(tmpfile.name)

    tmpfile.close()
    os.unlink(tmpfile.name)

    assert isinstance(pals.get_palettes(), list)
    assert len(pals.get_palettes()) == 0

    # Closing file connection and delete temporary file
    tmpfile.close()
    os.remove(tmpfile.name)

