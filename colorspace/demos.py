# -------------------------------------------------------------------
# - NAME:        demos.py
# - AUTHOR:      Reto Stauffer
# - DATE:        2018-09-15
# -------------------------------------------------------------------
# - DESCRIPTION:
# -------------------------------------------------------------------
# - EDITORIAL:   2018-09-15, RS: Created file on thinkreto.
# -------------------------------------------------------------------
# - L@ST MODIFIED: 2018-09-15 18:37 on marvin
# -------------------------------------------------------------------


def barplot(colors, fig = None):

    import matplotlib.pyplot as plt
    import numpy as np

    # Get random data
    np.random.seed(1)
    x = np.round(np.random.uniform(5, 20, len(colors)))
    
    # Open figure if input "fig" is None, else use
    # input "fig" handler.
    if fig is None: fig = plt.figure()


    # Plotting data
    #ax = fig.add_subplot(111)
    plt.bar(range(0, len(colors)), x, color = colors)
    plt.axis("off")
    plt.tight_layout()
    return fig
    #plt.show()


def specplot(*args, **kwargs):

    from colorspace import specplot
    specplot(*args, **kwargs)
