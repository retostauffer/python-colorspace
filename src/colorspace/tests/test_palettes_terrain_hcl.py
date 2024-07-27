

import pytest
from pytest import raises
import numpy as np
from colorspace import terrain_hcl, hcl_palettes

# All parameters
_all_parameters = ["foo", "h1", "h2", "c1", "cmax", "c3", "l1", "l2", "p1", "p2"]

# ---------------------------------------------
# Default settings
# ---------------------------------------------
def test_terrain_hcl_defaults():
    expected_defaults = {"h1": 130, "h2": 0, "c1": 80, "c2": 0,
            "l1": 60, "l2": 95, "p1": 0.1, "p2": 1.,
            "fixup": True, "rev": False}
    pal = terrain_hcl()
    for k,v in expected_defaults.items():
        assert pal.get(k) == v

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_terrain_hcl_wrong_usage_h():
    # Testing argument 'h'
    raises(ValueError, terrain_hcl, h = "name of non-existing palette")
    raises(ValueError, terrain_hcl, h = None) # None not allowed
    raises(ValueError, terrain_hcl, h = {1, 2}) # invalid type
    raises(ValueError, terrain_hcl, h = [1, 2, 3]) # length > 2
    raises(ValueError, terrain_hcl, h = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, terrain_hcl, h = np.asarray([])) # length < 1
    raises(ValueError, terrain_hcl, h = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, terrain_hcl, h = np.asarray([1, np.nan])) # nan not allowed

def test_terrain_hcl_wrong_usage_c():
    # Testing argument 'c'
    raises(ValueError, terrain_hcl, c = "foo") # not numeric
    raises(ValueError, terrain_hcl, c = None) # None not allowed
    raises(ValueError, terrain_hcl, c = {1, 2}) # invalid type
    raises(ValueError, terrain_hcl, c = [1, 2, 3, 4]) # length > 3
    raises(ValueError, terrain_hcl, c = np.asarray([1, 2, 3, 4])) # length > 3
    raises(ValueError, terrain_hcl, c = np.asarray([])) # length < 1
    raises(ValueError, terrain_hcl, c = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, terrain_hcl, c = np.asarray([1, np.nan])) # nan not allowed

def test_terrain_hcl_wrong_usage_l():
    # Testing argument 'l'
    raises(ValueError, terrain_hcl, l = "foo") # not numeric
    raises(ValueError, terrain_hcl, l = None) # None not allowed
    raises(ValueError, terrain_hcl, l = {1, 2}) # invalid type
    raises(ValueError, terrain_hcl, l = [1, 2, 3]) # length > 2
    raises(ValueError, terrain_hcl, l = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, terrain_hcl, l = np.asarray([])) # length < 1
    raises(ValueError, terrain_hcl, l = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, terrain_hcl, l = np.asarray([1, np.nan])) # nan not allowed

def test_terrain_hcl_wrong_usage_power():
    # Testing argument 'power'
    raises(ValueError, terrain_hcl, power = "foo") # not numeric
    raises(ValueError, terrain_hcl, power = None) # None not allowed
    raises(ValueError, terrain_hcl, power = {1, 2}) # invalid type
    raises(ValueError, terrain_hcl, power = [1, 2, 3]) # length > 2
    raises(ValueError, terrain_hcl, power = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, terrain_hcl, power = np.asarray([])) # length < 1
    raises(ValueError, terrain_hcl, power = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, terrain_hcl, power = np.asarray([1, np.nan])) # nan not allowed

def test_terrain_hcl_wrong_usage_fixup():
    # 'fixup' must be bool
    raises(TypeError, terrain_hcl, fixup = None)

def test_terrain_hcl_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, terrain_hcl, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_terrain_hcl_colors():

    pal = terrain_hcl()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = terrain_hcl()(5)
    col2 = terrain_hcl().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = terrain_hcl().colors(5, fixup = "foo")
    assert np.all(col1 == col3)

# ---------------------------------------------
# Testing options
# ---------------------------------------------
# Testing unallowed parameters
def test_terrain_hcl_invalid_kwargs():
    pal1 = terrain_hcl()
    not_allowed = []
    for p in _all_parameters:
        if not p in terrain_hcl._allowed_parameters:
            not_allowed.append(p)

    for k in not_allowed:
        raises(ValueError, terrain_hcl, **{k: 0.})

# Testing allowed parameters
def test_terrain_hcl_allowed_kwargs_unnamed():
    # Test settings
    settings = {"h1": 11, "h2": 12, "c1": 13, "c2": 14,
                "l1": 15, "l2": 16, "p1": 17, "p2": 18}

    # Ensure I test all allowed parameters
    for k in terrain_hcl._allowed_parameters:
        # Skipping 'cmax', only testing 'basic' sequential palettes.
        # There are dedicated tests for advanced palettes below
        if k in ["cmax"]: continue
        if not k in settings.keys():
            raise Exception(f"missing allowed parameter \"{k}\" in test settings")

    # Reference palette
    ref = terrain_hcl(h =     [settings["h1"], settings["h2"]],
                   c =     [settings["c1"], settings["c2"]],
                   l =     [settings["l1"], settings["l2"]],
                   power = [settings["p1"], settings["p2"]])

    # Settings; will be tested one-by-one first
    for k,v in settings.items():
        args = {k: v}
        tmp  = terrain_hcl(**args)
        assert ref.get(k) == tmp.get(k)

    # All together
    tmp = terrain_hcl(**settings)
    for k in settings.keys():
        assert ref.get(k) == tmp.get(k)

# Handling of missing colors if fixup = FALSE
def test_terrain_hcl_missing_colors_fixup():

    pal1 = terrain_hcl(c = [60, 60]).colors(5)
    pal2 = terrain_hcl(c = [60, 60]).colors(5, fixup = False)

    assert len(pal1) == len(pal2)
    assert pal2[3] is None
    assert pal2[4] is None

    assert np.all(pal2[:3] == pal1[:3])


# Testing alpha handling
def test_terrain_hcl_argument_alpha():

    # First testing misuse
    pal = terrain_hcl()
    raises(TypeError, pal.colors, n = 2, alpha = "foo") # must be float
    raises(TypeError, pal.colors, n = 2, alpha = 0) # must be float

    raises(ValueError, pal.colors, n = 2, alpha = -0.0001) # must be [0, 1]
    raises(ValueError, pal.colors, n = 2, alpha =  1.0001) # must be [0, 1]

    raises(ValueError, pal.colors, n = 2, alpha =  [0.3, 1.0001]) # must be [0, 1]
    raises(ValueError, pal.colors, n = 2, alpha =  [1.0001, 0.3]) # must be [0, 1]
    raises(ValueError, pal.colors, n = 2, alpha =  [0.3, -0.0001]) # must be [0, 1]
    raises(ValueError, pal.colors, n = 2, alpha =  [-0.0001, 0.3]) # must be [0, 1]

    raises(ValueError, pal.colors, n = 2, alpha = [0.1, 0.2, 0,3]) # length mismatch
    raises(ValueError, pal.colors, n = 3, alpha = [0.1, 0.2]) # length mismatch

    # 'R' is the solution from the same call in R to be compared against

    ## terrain_hcl, 5 colors, no alpha
    #x = terrain_hcl().colors(5) 
    #R = ["#26A63A", "#9BB306", "#E1BB4E", "#FFC59E", "#F1F1F1"]
    #assert np.all(x == R)
    #
    ## terrain_hcl, 5 colors, constant alpha = 0.3
    #x = terrain_hcl().colors(5, alpha = 0.3) 
    #R = ["#26A63A4D", "#9BB3064D", "#E1BB4E4D", "#FFC59E4D", "#F1F1F14D"]
    #assert np.all(x == R)
    #
    ## terrain_hcl, 6 colors with alpha [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    #x = terrain_hcl().colors(6, alpha = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]) 
    #R = ["#26A63A00", "#8AB00933", "#C7B82F66", "#F9BF6E99", "#FFC7AECC", "#F1F1F1"]
    #assert np.all(x == R)


