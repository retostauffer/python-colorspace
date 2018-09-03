
    
from cslogger import cslogger
log = cslogger(__name__)


def hcl_palettes(n = 7, type_ = None, name = None, plot = False, custom = None, *args):
    """TODO: write docstring.


    Parameters:
        n (int): number of colors to be plotted, default is 7. Only used
            if plot = True.
        type_: None (default), a string, or a list of strings. Can be used
            to display only a subset of the palettes. If not set all default
            palettes will be returned/plotted. Can be used in combination with
            input argument name.
        name: Similar to type_. If not specified all palettes will be returned.
            Can be set to a string or a list of strings containing the names
            of the palettes which should be returned/plotted.
        plot (bool): if False (default) a hclpalettes object will be returned
            containing the (subset) of default color palettes.
            Note that matplotlib has to be installed if plot is set to True.
        custom: one or multiple defaultpalettes can be provided in addition.

    Examples:

        >>> # Basic usage
        >>> from colorspace.hcl_palettes import hcl_palettes

        >>> print hcl_palettes()
        >>> print hcl_palettes(type_ = "Diverging")
        >>> print hcl_palettes(name = ["Oranges", "Tropic"]) 

        >>> print hcl_palettes(type_ = "Diverging", plot = True)
        >>> print hcl_palettes(name = ["Oranges", "Tropic"], plot = True) 
        >>> 
        >>> # Loading all available palettes (just to make custom palettes)
        >>> from colorspace.palettes import hclpalettes
        >>> pal = hclpalettes()
        >>> c1 = pal.get_palette("Oranges")
        >>> c2 = pal.get_palette("Greens")
        >>> 
        >>> # Modify the custom palettes
        >>> c1.set(h1 = 99, l2 = 30, l1 = 30)
        >>> c1.rename("Retos custom 1")
        >>> c2.set(h1 = -30, l1 = 40, l2 = 30, c1 = 30, c2 = 40)
        >>> c2.rename("Retos custom 1")

        >>> hcl_palettes(type_ = "Custom", custom = [c1, c2], plot = True)


    .. todo::
        Allow to forward **kwargs files with custom pre-defined
        palettes if this feature is getting a public thing.
    """

    
    # Loading pre-defined palettes from within the package
    from . import hclpalettes
    pals      = hclpalettes()                    # Loading palettes

    # If custom palettes have been added: add them as well (if
    # the types are correct, of course).
    if not custom is None:
        from numpy import all
        from palettes import defaultpalette
        def customerror():
            import inspect
            str = "list with custom palettes provided to {:s}".format(inspect.stack()[0][3])
            str += " but not all elements are of type defaultpalette"
            raise ValueError(str)

        if isinstance(custom, defaultpalette):
            pals._palettes_["Custom"] = [custom]
        # Check if all inputs are of correct type
        elif isinstance(custom, list):
            if not all([isinstance(x, defaultpalette) for x in custom]):
                    customerror()
            pals._palettes_["Custom"] = custom
        # Else append pals._palettes_["Custom"] = custom
        else:
            raise ValueError("input custom to {:s} misspecified".format(self.__class__.__name__))


    if not type_ is None:
        if isinstance(type_, str): type_ = [type_]
        
        # Drop palettes from hclpalettes object not requested
        # by the user.
        for t in pals.get_palette_types():
            if not t.upper() in [x.upper() for x in type_]:
                del pals._palettes_[t]
    else:
        type_ = pals.get_palette_types()

    # Now dropping all color maps not matching a name, if the
    # user has set a name.
    if not name is None:
        if isinstance(name, str): name = [name]
        # Looping over palette types
        for t in pals.get_palette_types():
            palettenames = [p.name() for p in pals.get_palettes(t)]
            drop = []
            for i in range(0, len(palettenames)):
                if not palettenames[i] in name: drop.append(i)
            # Drop all?
            if len(drop) == len(palettenames):
                del pals._palettes_[t]
            else:
                drop.sort(reverse = True)
                for i in drop: del pals._palettes_[t][i]

    # No palettes survived?
    if len(pals.get_palettes()) == 0:
        import inspect
        raise Exception("no palettes found in {:s} matching one of: {:s}".format(
                inspect.stack()[0][3], ", ".join(type_)))

    # Return if plot is not required
    if not plot: return pals


    # If plot is True: proceed.
    # Requires matpotlib, a suggested package. If not avialable
    # raise an import error.
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        import inspect
        msg = "{:s} with plot=True requires matplotlib to be installed: {:s}".format(
                inspect.stack()[0][3], e)
        raise ImportError(msg)



    # Draw the colormap
    def cmap(ax, cols, ylo, yhi, xmin, xmax, boxedupto = 15):

        from numpy import linspace
        from matplotlib.patches import Rectangle
        if len(cols) == 1:
            space     = 0.
            step      = xmax - xmin
            xlo       = [xmin]
            edgecolor = "#cecece"

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
            n         = len(cols)
            deltax    = float(xmax - xmin)
            space     = deltax * 0.05 / (n - 1)
            step      = (deltax - float(n - 1.) * space) / float(n)
            xlo       = linspace(xmin, xmax - step + space, n)
            edgecolor = "#cecece"

        # Else it is a bit simpler
        else:
            n         = len(cols)
            space     = 0.
            step      = float(xmax - xmin) / float(n)
            xlo       = linspace(xmin, xmax - float(xmax - xmin) / (n), n)
            edgecolor = None

        # Plotting the rectangles
        for i in range(0, len(cols)):
            rect = Rectangle((xlo[i], ylo), (step - space), yhi - ylo,
                    facecolor = cols[i], edgecolor = edgecolor)
            ax.add_patch(rect)


    # Make figure
    import numpy as np

    # Initialize new figure
    fig, ax = plt.subplots()

    # Plotting the different color maps
    npals  = len(pals.get_palettes())
    ydelta = 1. / float(npals + 1.4 * float(len(pals.get_palette_types())))
    ypos   = 1. + ydelta / 2. # Initial value, starting top down

    print ypos
    print ydelta

    # Adjusting outer margins
    fig.subplots_adjust(left = 0., bottom = 0., right  = 1.,
                        top  = 1., wspace = 0., hspace = 0.)
    ax.axis("off")
    # Small white margin around the plot
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)

    type_args = {"weight": "bold", "va": "center", "ha": "left"}
    pal_args  = {"va": "center", "ha": "left"}
    for type_ in pals.get_palette_types():

        # Adding palette type label
        ypos -= 1.4 * ydelta
        ax.text(0., ypos, type_, type_args)

        for pal in pals.get_palettes(type_):

            # Adding text
            ypos -= ydelta
            ax.text(0.02, ypos, pal.name(), pal_args)

            # Getting colors, plotting color bar
            cols = pal.colors(n)
            cmap(ax, cols, ypos - 0.8 * ydelta / 2.,
                 ypos + 0.8 * ydelta / 2., 0.35, 0.99) 

    plt.show()


    return


    



