



from colorspace import palette, sequential_hcl, swatchplot
H = palette(sequential_hcl(h = [0, 300], c = 60, l = 65).colors(5), "Hue")
C = palette(sequential_hcl(h = 0, c = [0, 100], l = 65).colors(5), "Chroma")
L = palette(sequential_hcl(h = 0, c = 0, l = [90, 25]).colors(5), "Luminance")


import matplotlib.pyplot as plt
fig = plt.figure()

swatchplot([H, C, L], figsize = (3, 1.5), fig = fig)

fig.imshow()

