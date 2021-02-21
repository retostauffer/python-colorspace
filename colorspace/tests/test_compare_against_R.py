
from colorspace import *
import pytest
import json

import os
path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path, "R_test_solution.json")) as fid:
    content = "\n".join(fid.readlines())
    data    = json.loads(content)

def wrapper(fun, kwargs, n): return fun(**kwargs)(n)


def test_against_R():

    for i in range(0, len(data)):
        # Getting current record for convenience
        rec = data[i]

        # Print for debugging shown when running pytest -s
        print("[compare against R]: {:s}".format(rec["id"]))
        fun = eval(rec["fun"])
        arg = rec["args"]
        n   = arg["n"]
        del arg["n"] # Not an argument for the python function itself
        # Create colors
        sol = fun(**arg)(n)
    
        # Compare solution of R colorspace against python colorspace
        assert len(rec["colors"]) == len(sol)
        assert all([rec["colors"][i].upper() == sol[i].upper() for i in range(len(sol))])
    
    
    
    
    
