

from colorspace import check_hex_colors


print(check_hex_colors(["#FF0033", "#FFF", "#FF0033CC"]))

print(check_hex_colors(["red", "0", "#FFF"]))



import sys; sys.exit(0)


from colorspace import *
from colorspace.colorlib import hexcols
from colorspace.utils import extract_transparency, adjust_transparency
import numpy as np

# Three colors without alpha
cols1 = ['#023FA5',   '#E2E2E2',   '#8E063B']
# Same colors with transparency 80%, 40%, 80%
cols2 = ['#023FA5CC', '#E2E2E266', '#8E063BCC']

# Convert 'cols1' into a hexcols object and modify transparency
x1 = hexcols(cols1)
print(x1)
extract_transparency(x1)           # Extract transparency
x1 = adjust_transparency(x1, 0.5)  # Set constant transparency
print(x1)
x1 = adjust_transparency(x1, [0.8, 0.4, 0.8]) # Add transparency
print(x1)

# Convert 'cols2' into a hexcols object and extract/remove/add transparency
x2 = hexcols(cols2)
extract_transparency(x2)           # Extract current transparency
x2 = adjust_transparency(x2, None) # Remove transparency
print(x2)
extract_transparency(x2)
x2 = adjust_transparency(x2, np.asarray([0.8, 0.4, 0.8])) # Add again
print(x2)
extract_transparency(x2)

