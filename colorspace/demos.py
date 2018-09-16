# -------------------------------------------------------------------
# - NAME:        demos.py
# - AUTHOR:      Reto Stauffer
# - DATE:        2018-09-15
# -------------------------------------------------------------------
# - DESCRIPTION:
# -------------------------------------------------------------------
# - EDITORIAL:   2018-09-15, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2018-09-16 19:08 on marvin
# -------------------------------------------------------------------


def Bar(colors, fig = None):

    import matplotlib.pyplot as plt
    import numpy as np

    
    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Get random data
    np.random.seed(1)
    width = 0.9 / len(colors)

    lower  = [1.1, 1.9, 0.7, 0.3]
    offset = [0.5, 1.1, 1.5, 0.8]

    ax = plt.subplot2grid((1, 1), (0, 0))
    for i in range(0, len(lower)):
        x = i + np.arange(0, len(colors)) * width
        y = lower[i] + np.abs(np.sin(offset[i] + 1 + \
            np.arange(0, len(colors), dtype = float))) / 3
        ax.bar(x, y, color = colors, width = width)

    # Plot
    #ax.bar(range(0, len(colors)), x, color = colors)
    plt.axis("off")
    plt.tight_layout()

    if not showfig:
        return fig
    else:
        fig.show()


def Pie(colors, fig = None):

    import matplotlib.pyplot as plt
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Axis
    ax = plt.subplot2grid((1, 1), (0, 0))

    # Data
    x = 0.01 + np.abs(np.sin(1.5 + np.arange(0, len(colors))))
    plt.pie(x, colors = colors)
    plt.axis("off")
    plt.tight_layout()

    if not showfig:  return fig
    else:            fig.show()

def Spine(colors, fig = None):

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Data
    offset  = 0.015
    widths  = [0.05, 0.1, 0.15, 0.1, 0.2, 0.08, 0.12, 0.16, 0.04]
    k       = len(widths)
    n       = len(colors)
    heights = [np.power(np.arange(1, n + 1, dtype = float) / n, 1. / p) for p in \
              [2.5, 1.2, 2.7, 1, 1.3, 0.7, 0.4, 0.2, 1.7]]

    # Axis
    ax = plt.subplot2grid((1, 1), (0, 0))

    # Plot
    x = 0.
    for i in range(0,k):
        y = 0.
        heights[i] = heights[i] / sum(heights[i]) # Scale
        for j in range(0,n):
            rect = Rectangle((x,y), widths[i], heights[i][j], color = colors[j])
            ax.add_patch(rect)
            y += heights[i][j]
        x += offset + widths[i]

    plt.axis("off")
    plt.tight_layout()

    if not showfig:  return fig
    else:            fig.show()


def Matrix(colors, fig = None):

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    import numpy as np

    
    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Get random data
    np.random.seed(1)
    x = np.random.uniform(0., float(len(colors)), 100)
    x = np.floor(x)

    ax = plt.subplot2grid((1, 1), (0, 0))
    for i in range(0, 10):
        for j in range(0, 10):
            rect = Rectangle((i / 10.,j / 10.), 0.1, 0.1,
                             color = colors[int(x[i + 10*j])])
            ax.add_patch(rect)

    # Plot
    plt.axis("off")
    plt.tight_layout()

    if not showfig:
        return fig
    else:
        fig.show()

#def Scatter(colors, fig = None):
#
#    import matplotlib.pyplot as plt
#    import numpy as np
#
#    # Open figure if input "fig" is None, else use
#    # input "fig" handler.
#    if fig is None:
#        fig = plt.figure()
#        showfig = True
#    else:
#        showfig = False
#
#    # Data
#    x0 = np.sin(np.pi * np.arange(1,61) / 30) / 5
#    y0 = np.cos(np.pi * np.arange(1,61) / 30) / 5
#    xr = [0.1, -0.6, -0.7, -0.9,  0.4,  1.3, 1.0]
#    yr = [0.3,  1.0,  0.1, -0.9, -0.8, -0.4, 0.6]
#
#    # Requires scipy
#
#    x = 0.01 + np.abs(np.sin(1.5 + np.arange(0, len(colors))))
#    plt.pie(x, colors = colors)
#    plt.axis("off")
#    plt.tight_layout()
#
#    if not showfig:  return fig
#    else:            fig.show()

def Lines(colors, fig = None):

    import matplotlib.pyplot as plt
    import numpy as np

    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None:
        fig = plt.figure()
        showfig = True
    else:
        showfig = False

    # Data
    n = len(colors)
    s = range(2, n + 2)

    lwd = 6
    if n > 5:  lwd -= 1
    if n > 15: lwd -= 1
    if n > 25: lwd -= 1

    ax = plt.subplot2grid((1, 1), (0, 0))
    for i in range(0, len(colors)):
        j = n - 1 - i
        ax.plot([1 / s[i], 2. + 1. / s[j]],
                [s[i], s[j]],
                color = colors[i], linewidth = lwd)
        ax.plot([2. + 1. / s[i], 4. - 1. / s[i], 6. - 1 / s[i]],
                [s[i], s[i], s[j]],
                color = colors[j], linewidth = lwd)
    plt.axis("off")
    plt.tight_layout()

    if not showfig:  return fig
    else:            fig.show()


def Spectrum(*args, **kwargs):

    from colorspace import specplot
    specplot(*args, **kwargs)

