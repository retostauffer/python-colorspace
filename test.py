
# Loading package
from colorspace import *
from colorspace.colorlib import *

# Generate a set of colors
cols = hexcols(["#023FA5", "#A1A6C8", "#E2E2E2", "#CA9CA4", "#8E063B"])

# Convert colors
cols.to("HCL")
print(cols)

cols.to("hex")
print(cols)

