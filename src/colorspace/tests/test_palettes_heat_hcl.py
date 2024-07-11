

import pytest
from pytest import raises
import numpy as np

import matplotlib.pyplot as plt
from colorspace import heat_hcl, hcl_palettes

# All parameters
_all_parameters = ["foo", "h1", "h2", "c1", "cmax", "c3", "l1", "l2", "p1", "p2"]

# ---------------------------------------------
# Default settings
# ---------------------------------------------
def test_heat_hcl_defaults():
    expected_defaults = {"h1": 0, "h2": 90, "c1": 100, "c2": 30,
            "l1": 50, "l2": 90, "p1": 0.2, "p2": 1.,
            "fixup": True, "rev": False}
    pal = heat_hcl()
    for k,v in expected_defaults.items():
        assert pal.get(k) == v

# ---------------------------------------------
# Testing sanity checks (misuse)
# ---------------------------------------------
def test_heat_hcl_wrong_usage_h():
    # Testing argument 'h'
    raises(ValueError, heat_hcl, h = "name of non-existing palette")
    raises(ValueError, heat_hcl, h = None) # None not allowed
    raises(ValueError, heat_hcl, h = {1, 2}) # invalid type
    raises(ValueError, heat_hcl, h = [1, 2, 3]) # length > 2
    raises(ValueError, heat_hcl, h = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, heat_hcl, h = np.asarray([])) # length < 1
    raises(ValueError, heat_hcl, h = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, heat_hcl, h = np.asarray([1, np.nan])) # nan not allowed

def test_heat_hcl_wrong_usage_c():
    # Testing argument 'c'
    raises(ValueError, heat_hcl, c = "foo") # not numeric
    raises(ValueError, heat_hcl, c = None) # None not allowed
    raises(ValueError, heat_hcl, c = {1, 2}) # invalid type
    raises(ValueError, heat_hcl, c = [1, 2, 3, 4]) # length > 3
    raises(ValueError, heat_hcl, c = np.asarray([1, 2, 3, 4])) # length > 3
    raises(ValueError, heat_hcl, c = np.asarray([])) # length < 1
    raises(ValueError, heat_hcl, c = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, heat_hcl, c = np.asarray([1, np.nan])) # nan not allowed

def test_heat_hcl_wrong_usage_l():
    # Testing argument 'l'
    raises(ValueError, heat_hcl, l = "foo") # not numeric
    raises(ValueError, heat_hcl, l = None) # None not allowed
    raises(ValueError, heat_hcl, l = {1, 2}) # invalid type
    raises(ValueError, heat_hcl, l = [1, 2, 3]) # length > 2
    raises(ValueError, heat_hcl, l = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, heat_hcl, l = np.asarray([])) # length < 1
    raises(ValueError, heat_hcl, l = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, heat_hcl, l = np.asarray([1, np.nan])) # nan not allowed

def test_heat_hcl_wrong_usage_power():
    # Testing argument 'power'
    raises(ValueError, heat_hcl, power = "foo") # not numeric
    raises(ValueError, heat_hcl, power = None) # None not allowed
    raises(ValueError, heat_hcl, power = {1, 2}) # invalid type
    raises(ValueError, heat_hcl, power = [1, 2, 3]) # length > 2
    raises(ValueError, heat_hcl, power = np.asarray([1, 2, 3])) # length > 2
    raises(ValueError, heat_hcl, power = np.asarray([])) # length < 1
    raises(ValueError, heat_hcl, power = np.asarray([np.nan])) # nan not allowed
    raises(ValueError, heat_hcl, power = np.asarray([1, np.nan])) # nan not allowed

def test_heat_hcl_wrong_usage_fixup():
    # 'fixup' must be bool
    raises(TypeError, heat_hcl, fixup = None)

def test_heat_hcl_wrong_usage_rev():
    # 'rev' must be bool
    raises(TypeError, heat_hcl, rev = None)


# ---------------------------------------------
# Testing methods on default palette
# ---------------------------------------------
def test_heat_hcl_colors():

    pal = heat_hcl()
    raises(TypeError, pal,  n = None)
    raises(TypeError, pal,  n = 15.3)
    raises(ValueError, pal, n = 0)
    raises(ValueError, pal, n = -1)

    col1 = heat_hcl()(5)
    col2 = heat_hcl().colors(5)

    assert isinstance(col1, list)
    assert isinstance(col2, list)
    assert len(col1) == 5
    assert len(col1) == 5
    assert np.all(col1 == col2)

    # 'fixup' is ignored if not boolean
    col3 = heat_hcl().colors(5, fixup = "foo")
    assert np.all(col1 == col3)

# ---------------------------------------------
# Testing options
# ---------------------------------------------
# Testing unallowed parameters
def test_heat_hcl_invalid_kwargs():
    pal1 = heat_hcl()
    not_allowed = []
    for p in _all_parameters:
        if not p in heat_hcl._allowed_parameters:
            not_allowed.append(p)

    for k in not_allowed:
        raises(ValueError, heat_hcl, **{k: 0.})

# Testing allowed parameters
def test_heat_hcl_allowed_kwargs_unnamed():
    # Test settings
    settings = {"h1": 11, "h2": 12, "c1": 13, "c2": 14,
                "l1": 15, "l2": 16, "p1": 17, "p2": 18}

    # Ensure I test all allowed parameters
    for k in heat_hcl._allowed_parameters:
        # Skipping 'cmax', only testing 'basic' sequential palettes.
        # There are dedicated tests for advanced palettes below
        if k in ["cmax"]: continue
        if not k in settings.keys():
            raise Exception(f"missing allowed parameter \"{k}\" in test settings")

    # Reference palette
    ref = heat_hcl(h =     [settings["h1"], settings["h2"]],
                   c =     [settings["c1"], settings["c2"]],
                   l =     [settings["l1"], settings["l2"]],
                   power = [settings["p1"], settings["p2"]])

    # Settings; will be tested one-by-one first
    for k,v in settings.items():
        args = {k: v}
        tmp  = heat_hcl(**args)
        assert ref.get(k) == tmp.get(k)

    # All together
    tmp = heat_hcl(**settings)
    for k in settings.keys():
        assert ref.get(k) == tmp.get(k)

