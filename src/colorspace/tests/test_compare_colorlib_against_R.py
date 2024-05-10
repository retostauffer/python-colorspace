
from colorspace import *
import pytest
import json
import numpy as np

import os
path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path, "R_test_colorlib_solution.json")) as fid:
    content = "\n".join(fid.readlines())
    data    = json.loads(content)

# Just testing if the content we got from the json file is
# as expected.
def test_solution_file_content():
    assert isinstance(data, dict)
    assert "meta" in data.keys()
    assert "colors" in data.keys()
    
    for x in ["sRGB", "RGB", "HLS", "HSV", "CIEXYZ", "CIELAB",
              "CIELUV", "polarLAB", "polarLUV", "hexcols"]:
        assert x in data["colors"].keys()

def test_hexcols():
    c = hexcols(data["colors"]["hexcols"])
    x = c.get("hex_")
    assert np.all(x == data["colors"]["hexcols"])

def test_sRGB():
    to = "sRGB"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    for k,v in c._data_.items():
        assert np.allclose(v, data["colors"][to][k])

def test_RGB():
    to = "RGB"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    for k,v in c._data_.items():
        if k == "alpha":   assert v is None
        else:              assert np.allclose(v, data["colors"][to][k])

def test_HLS():
    to = "HLS"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    for k,v in c._data_.items():
        if k == "alpha":   assert v is None
        else:              assert np.allclose(v, data["colors"][to][k])

def test_HSV():
    to = "HSV"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    for k,v in c._data_.items():
        if k == "alpha":   assert v is None
        else:              assert np.allclose(v, data["colors"][to][k])

def test_CIEXYZ():
    to = "CIEXYZ"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    for k,v in c._data_.items():
        if k == "alpha":   assert v is None
        else:              assert np.allclose(v, data["colors"][to][k])

def test_CIELUV():
    to = "CIELUV"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    for k,v in c._data_.items():
        if k == "alpha":   assert v is None
        else:              assert np.allclose(v, data["colors"][to][k])

def test_CIELAB():
    to = "CIELAB"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    for k,v in c._data_.items():
        if k == "alpha":   assert v is None
        else:              assert np.allclose(v, data["colors"][to][k])

def test_polarLUV():
    to = "polarLUV"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    for k,v in c._data_.items():
        if k == "alpha":   assert v is None
        else:              assert np.allclose(v, data["colors"][to][k])

def test_polarLAB():
    to = "polarLAB"
    c = hexcols(data["colors"]["hexcols"])
    c.to(to)
    # R colorspace works with L, C, H
    # python with             L, A, B
    # -> translating
    lookup = {"L": "L", "A": "C", "B": "H"}

    for k,v in c._data_.items():
        if k == "alpha":   assert v is None
        else:              assert np.allclose(v, data["colors"][to][lookup[k]])


