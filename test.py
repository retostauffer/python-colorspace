


from colorspace.colorlib import hexcols

x1 = hexcols(["#ff00ff", "#00ff00", "#0000ff"])
print(x1)
x2 = hexcols(["#f0f", "#00ff00", "#0000ff"])
print(x2)
import sys; sys.exit(3)

from colorspace import check_hex_colors

#check_hex_colors("#ff003311")
#check_hex_colors("#ff0033")
#check_hex_colors("#f03")
#check_hex_colors(["#f0f", "#00F", "#00FFFF", "#ff003311"])
#import sys; sys.exit(3)


from colorspace.palettes import palette
colors = ["#070707", "#690056", "#C30E62", "#ED8353", "#FDF5EB"]
custom_pal = palette(colors, "test palette")
print(custom_pal)

## Testing different input types (str, list, colorobject)
from colorspace.colorlib import hexcols
from colorspace import palette
hexcols = hexcols(colors)

pal1 = palette("#ff0033")
pal2 = palette("#ff0033", name = "custom name")
pal3 = palette(colors, name = "custom 1.1")
pal4 = palette(hexcols, name = "custom 1.2")
print(pal1)
print(pal2)
print(pal3)
print(pal4)

from colorspace import swatchplot
swatchplot([pal3, pal4])


