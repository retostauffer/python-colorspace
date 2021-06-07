

def cvd_emulator(image = "DEMO", cvd = "desaturate", severity = 1.0,
        output = None, dropalpha = False):
    """Simulate color deficiencies on png/jpg/jpeg figures.
    Takes an existing pixel image and simulates different color vision
    deficiencies.

    The function displays a matplotlib figure if output is set to None.
    If the parameter output is set, the converted figure will be stored.
    If only one color vision deficiency is defined (e.g., ``cvd = "desaturate"``)
    a figure of the same type and size as the input figure will be saved to
    the disc. If multiple cvd's are specified a multi-panel plot will be
    stored under `output`.

    Args:
        image (str): Name of the figure which should be converted
            (png/jpg/jpeg).  If ``image = "DEMO"`` the package demo figure will be
            used.
        cvd (str, list): The color vision deficiency. Allowed types are
            deutanope, protanope, tritanope, and desaturated.  Input is either a
            single string or a list of strings which define the cvd's which should
            be simulated.
        severity (float): How severe the color vision deficiency is
            (``[0.,1.]``).  Also used as the amount of desaturation if ``cvd =
            "desaturate"``.
        output (string): Optional. It None an interactive plotting window will
            be opened. If a string is given the figure will be written to
            ``output``.
        dropalpha (bool): Whether or not to drop the alpha channel.  Only
            useful for figures having an alpha channel (png w/ alpha).

    Example:

        >>> from colorspace.cvd_emulator import cvd_emulator
        >>> cvd_emulator("DEMO", "deutan", 0.5)
        >>> cvd_emulator("DEMO", "desaturate", 1.0, "output.png")
        >>> cvd_emulator("DEMO", ["original", "deutan", "protan"], 0.5, dropalpha = True)

    .. note::
        Requires the modules ``matplotlib`` and ``imageio``.
    """

    import os
    import inspect

    # Conver to ..?
    allowed = ["protan", "tritan", "deutan", "desaturate", "original"]
    tmp     = []
    if isinstance(cvd, str): cvd = [cvd]
    for c in cvd:
        if c in allowed:
            tmp.append(c)
        else:
            raise ValueError("cvd type {:s} not allowed. ".format(cvd) + \
                    "Use {:s}".format(", ".join(allowed)))
    if len(cvd) == 0:
        raise ValueError("no valid \"cvd\" methods")
    cvd = tmp; del tmp

    # If image = "DEMO": use package demo image.
    if image == "DEMO":
        resource_package = os.path.dirname(__file__)
        image = os.path.join(resource_package, "data", "colorful.png")

    # Check if file exists
    if not os.path.isfile(image):
        raise Exception("method {:s}".format(inspect.stack()[0][3]) + \
                "cannot find image file {:s}".format(image))

    # Wrong input for output
    if not output is None and not isinstance(output, str):
        raise ValueError("output has to be None or a string (file name)")

    # Import imageio
    try:
        import imageio
    except Exception as e:
        raise Exception("the {:s} requires the ".format(inspect.stack()[0][3]) + \
                "python module imageio to be installed: {:s}".format(str(e)))


    # Read image data
    try:
        img = imageio.imread(image)
    except Exception as e:
        raise Exception(str(e))

    # Extracting colors (scale from [0,255] to [0.,1.])
    data = {}
    if img.shape[2] == 3:
        [data["R"], data["G"], data["B"]] = \
                [img[:,:,i].flatten() / 255. for i in [0,1,2]]
    elif img.shape[2] == 4:
        [data["R"], data["G"], data["B"], data["alpha"]] = \
                [img[:,:,i].flatten() / 255. for i in [0,1,2,3]]

    # Create sRGB with or without
    from .colorlib import sRGB
    if not "alpha" in data.keys():
        rgba = sRGB(data["R"], data["G"], data["B"])
    else:
        rgba = sRGB(data["R"], data["G"], data["B"], data["alpha"])


    # Drop alpha
    if dropalpha: rgba.dropalpha()

    # Apply color deficiency
    from . import CVD
    import matplotlib.pyplot as plt

    from numpy import ceil
    if len(cvd) <= 3: [nrow, ncol] = [1, len(cvd)]
    else:             [nrow, ncol] = [ceil(len(cvd)/2.), 2]

    # Start plotting
    for c in range(0, len(cvd)):

        # Start plotting
        if len(cvd) == 1:
            fig = plt.figure()
        else:
            fig = plt.subplot(nrow, ncol, c + 1)

        if cvd[c] == "original":
            cols = rgba
        else:
            fun  = getattr(CVD, cvd[c])
            cols = fun(rgba, severity)

        # Convert RGB [0.-1.] to [0,255], uint8
        def fun(x, shape):
            from numpy import fmin, fmax
            x = fmax(0, fmin(255, x*255))
            return x.reshape(shape)

        # Shape of the new figure
        if cols.hasalpha():  shape = [img.shape[0],img.shape[1],4]
        else:                shape = [img.shape[0],img.shape[1],3]

        # Create new image matrix and fill in the data
        from numpy import ndarray, uint8
        imnew = ndarray(shape, dtype = uint8)
        imnew[:,:,0] = fun(cols.get("R"), shape[0:2])
        imnew[:,:,1] = fun(cols.get("G"), shape[0:2])
        imnew[:,:,2] = fun(cols.get("B"), shape[0:2])
        if cols.hasalpha():
            imnew[:,:,3] = fun(cols.get("alpha"), shape[0:2])

        import matplotlib.pyplot as plt
        plt.imshow(imnew)
        plt.axis("off")

    # Adjusting outer margins
    plt.subplots_adjust(left = 0., right = 1., top = 1., bottom = 0.1)

    # Show or save image.
    if output is None:
        plt.show()
    else:
        # Write a simple figure:
        if len(cvd) == 1:
            imageio.imwrite(output, imnew)
        # Save matplotlib panel plot
        else:
            plt.savefig(output)



