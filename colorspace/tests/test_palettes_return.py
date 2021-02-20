
import colorspace
import numpy as np

types = ["diverging", "sequential", "qualitative", "heat", "rainbow", "terrain"]

# Test that the return values for ...()(3) and ...().colors(3) is always
# of type list and of length 3 (hex colors).

def test_list_return():
    res   = [isinstance(eval("colorspace.{:s}_hcl()(3)".format(x)), list) for x in types]
    assert np.all(res)
def test_list_return_length1():
    res   = [len(eval("colorspace.{:s}_hcl()(3)".format(x))) == 3 for x in types]
    assert np.all(res)
def test_list_return_length2():
    res   = [len(eval("colorspace.{:s}_hcl().colors(3)".format(x))) == 3 for x in types]
    assert np.all(res)


