

def hcl_palettes(n = 16, type_ = None, *args):
    ###AAAA

    ###.. todo::
    ###    Allow to forward **kwargs files with custom pre-defined
    ###    palettes if this feature is getting a public thing.

    # Requires matpotlib, a suggested package. If not avialable
    # raise an import error.
    #try:
    #    from matplotlib import pyplot
    #except ImportError as e:
    #    import inspect
    #    msg = "{:s} requires matplotlib to be installed: {:s}".format(
    #            inspect.stack()[0][3], e)
    #    raise ImportError(msg)
    
    
    # Loading pre-defined palettes from within the package
    from . import palettes

    pals      = palettes()                    # Loading palettes
    alltypes_ = pals.get_palette_types()    # Number of different types

    # Evaluating type_ argument
    if type_ is None:
        type_ = alltypes_
    else:
        alltypes_ = [x.upper() for x in alltypes_]
        take_type = []
        for t in type_:
            if t.upper() in alltypes_: take_type.append(t)
        if len(take_type) == 0:
            import inspect
            msg = "esception from {:s}: ".format(inspect.stack()[0][3], e) + \
                  "none of {:s} is a valid palette type. ".format(", ".join(type_)) + \
                  "Available: {:s}".format(", ".join(alltypes_))
            raise ValueError(msg)
        # Else take these valid ones
        type_ = take_type


    npals  = 0
    for t in type_:
        npals += len(pals.get_palettes(t))
    
    print("Number of palette types {:d}".format(len(type_)))
    print("Number of palettes {:d}".format(npals))

    import matplotlib.pyplot as plt

    # Initialize new figure
    fig, ax = plt.subplots()

    # Plotting the different color maps
    ydelta = 1. / float(npals + 1.4 * len(type_))
    ypos   = 1. + ydelta / 2. # Initial value, starting top down

    # Adjusting outer margins
    fig.subplots_adjust(left = 0., bottom = 0., right  = 1.,
                        top  = 1., wspace = 0., hspace = 0.)
    ax.axis("off")
    ax.set_xlim(0., 1.)
    ax.set_ylim(- ydelta / 2, 1 + ydelta / 2.)

    # Draw the colormap
    def cmap(ax, cols, ylo, yhi, xmin, xmax, boxedupto = 15):

        from numpy import linspace
        from matplotlib.patches import Rectangle
        if len(cols) == 1:
            space  = 0.
            step   = xmax - xmin
            xlo    = [xmin]

        elif len(cols) <= boxedupto:
            # -----------------------------------------
            # For n = 2
            #    |<------------ deltax ------------>|
            #  xmin                                xmax
            #    | -------------------------------- |
            #    |#####COL1#######   ######COL2######
            #    |               >|-|< space        |
            #    |<--- step ------->|               |
            #    |xlo[0]            |xlo[1]         |
            #    |                |xhi[0]           |xhi[1]
            #    
            n      = len(cols)
            deltax = float(xmax - xmin)
            space  = deltax * 0.05 / (n - 1)
            step   = (deltax - float(n - 1.) * space) / float(n)
            xlo    = linspace(xmin, xmax - step + space, n)

        # Else it is a bit simpler
        else:
            n      = len(cols)
            space  = 0.
            step   = float(xmax - xmin) / float(n)
            xlo    = linspace(xmin, xmax - float(xmax - xmin) / (n), n)

        # Plotting the rectangles
        for i in range(0, len(cols)):
            rect = Rectangle((xlo[i], ylo), (step - space), yhi - ylo,
                    color = cols[i])
            ax.add_patch(rect)


    type_args = {"weight": "bold", "va": "center", "ha": "left"}
    pal_args  = {"va": "center", "ha": "left"}
    for type_ in type_:

        # Adding palette type label
        ypos -= 1.4 * ydelta
        ax.text(0.02, ypos, type_, type_args)

        for pal in pals.get_palettes(type_):

            # Adding text
            ypos -= ydelta
            ax.text(0.04, ypos, pal.name(), pal_args)

            # Getting colors, plotting color bar
            cols = pal.colors(n)
            cmap(ax, cols, ypos - 0.8 * ydelta / 2.,
                 ypos + 0.8 * ydelta / 2., 0.4, 0.99) 

    fig.show()


    



