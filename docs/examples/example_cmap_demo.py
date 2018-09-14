def demo(*args):
    """demo(*args)

    3D surface (color map) example from matplotlib.org

    Parameters
    ----------
    args : ...
        a set of LinearSegmentedColormap our custom
        matplotlib.color.LinearSegmentedColormap.
    """

    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import numpy as np

    # Subplot config
    nsubplots = len(args)
    fig = plt.figure()

    # Make data.
    X    = np.arange(-5, 5, 0.01)
    Y    = np.arange(-5, 5, 0.01)
    X, Y = np.meshgrid(X, Y)
    R    = np.sqrt(X**2 + Y**2)
    Z    = np.sin(R)

    # Disable axis
    def disable_axis(ax):
        for a in (ax.w_xaxis, ax.w_yaxis, ax.w_zaxis):
            for t in a.get_ticklines()+a.get_ticklabels():
                t.set_visible(False)
            a.pane.set_visible(False)
    
    # Plotting surface(s)
    for i,cmap in enumerate(args):
        
        # Plot the surface.
        ax   = fig.add_subplot(np.ceil(nsubplots/2.), 2, i+1, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap = cmap,
                               linewidth=0, antialiased=False)
        
        # Customize the z axis.
        ax.set_title(cmap.name)
        ax.set_zlim(-1.01, 1.01)
        disable_axis(ax)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        
        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)
        
    fig.tight_layout()
    plt.show()

