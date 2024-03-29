
.. _article-approximations:

Approximating Palettes from Other Packages
==========================================



.. todo::
    Article about color map approximations must be written or referred to
    the R colorspace website.


.. plot::
    :width: 80%

    from colorspace import specplot, sequential_hcl

    # From RColorBrewer
    brewer_YlGnBu   = ['#0C2C84', '#225EA8', '#1D91C0', '#41B6C4', '#7FCDBB', '#C7E9B4', '#FFFFCC']

    # Comparing against colorspace YlGnBu
    specplot(brewer_YlGnBu,
             sequential_hcl("YlGnBu").colors(7),
             title = "ColorBrewer.org: YlGnBu")

.. plot::
    :width: 80%

    from colorspace import specplot, sequential_hcl

    # From R package viridis
    viridis_viridis = ['#440154', '#443A83', '#31688E', '#21908C', '#35B779', '#8FD744', '#FDE725']

    # Comparing against colorspace Viridis
    specplot(viridis_viridis,
             sequential_hcl("Viridis").colors(7),
             title = "viridis: Viridis")

.. plot::
    :align: center
    :width: 80%

    from colorspace import specplot, sequential_hcl

    # From R package rcartocolor
    carto_agsunset  = ['#4B2991', '#872CA2', '#C0369D', '#EA4F88', '#FA7876', '#F6A97A', '#EDD9A3']

    # Comparing against colorspace ag_Sunset
    specplot(carto_agsunset,
             sequential_hcl("ag_Sunset").colors(7),
             title = "CARTO: ag_Sunset")

.. plot::
    :align: center
    :width: 80%

    from colorspace import specplot, sequential_hcl

    # From R package viridis
    viridis_plasma  = ['#0D0887', '#5D01A6', '#9C179E', '#CC4678', '#ED7953', '#FDB32F', '#F0F921']

    # Comparing against colorspace Plasma
    specplot(viridis_plasma,
             sequential_hcl("Plasma").colors(7),
             title = "viridis: Plasma")

             
