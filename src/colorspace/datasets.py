

def _getdataset_volcano():
    """Topographic Information on Auckland's Maunga Whau Volcano

    Convenience function, for more details about this data set see
    man page for function :py:func:`get_volcano_data <colorspace.demos.get_volcano_data>`.
    """
    from .demos import get_volcano_data
    return get_volcano_data(array = True)


def _getdataset_HarzTraffic():
    """Daily Traffic Counts Sonnenberg

    Requires `pandas` to be installed.
    """
    try:
        import pandas as pd
    except:
        raise Exception("'HarzTraffic' requires `pandas` to be installed")
    import os
    import numpy as np

    # Loading the data set
    resource_package = os.path.dirname(__file__)
    csv = os.path.join(resource_package, "data", "HarzTraffic.csv")

    # Trying to read the data set
    try:
        data = pd.read_csv(csv)
    except:
        raise Exception("problems reading \"{csv}\"")

    # Convert 'data' column to datetime
    data.date = pd.to_datetime(data.date).dt.date

    # Adding season
    m = pd.DatetimeIndex(data.date).month
    data["season"] = np.repeat("winter", data.shape[0])
    data.loc[(m >= 3) & (m <=  5), "season"] = "spring"
    data.loc[(m >= 6) & (m <=  8), "season"] = "summer"
    data.loc[(m >= 9) & (m <= 11), "season"] = "autumn"
    del m

    # Boolean flag for 'weekend'
    d = pd.DatetimeIndex(data.date).dayofweek
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    data["dow"] = d # Use integer this for order
    data["dayofweek"] = np.asarray([names[x] for x in d])
    data["weekend"] = np.repeat(False, data.shape[0])
    data.loc[(d >= 5), "weekend"] = True # Saturday (5) or Sunday (6)
    del d

    return data

def _getdataset_MonthlyHarzTraffic():
    """Monthly Traffic Counts Summary Sonnenberg

    Requires `pandas` to be installed.
    """
    try:
        import pandas as pd
    except:
        raise Exception("'HarzTraffic' requires `pandas` to be installed")

    import numpy as np

    # Loading the data set
    from .datasets import dataset
    data = dataset("HarzTraffic")

    # Appending year and month 
    data["year"]  = pd.DatetimeIndex(data.date).year
    data["month"] = pd.DatetimeIndex(data.date).month
    
    # Aggregating sums (a1) and means (a2) for specific columns
    tmp = ["year", "month", "bikes", "cars", "trucks", "others", "rain"]
    a1 = data.loc[:, tmp].groupby(["year", "month"]).agg("sum")
    tmp = ["year", "month", "temp", "sunshine", "wind"]
    a2 = data.loc[:, tmp].groupby(["year", "month"]).agg("mean")
    
    # Merge and round to 1 digit
    data = a1.merge(a2, on = ["year", "month"]).reset_index()
    for col in data.columns:
        if np.issubdtype(data.loc[:, col], np.floating):
            data.loc[:, col] = np.round(data.loc[:, col], 1)

    # Adding season flat
    data["season"] = np.repeat("winter", data.shape[0])
    data.loc[(data.month >= 3) & (data.month <=  5), "season"] = "spring"
    data.loc[(data.month >= 6) & (data.month <=  8), "season"] = "summer"
    data.loc[(data.month >= 9) & (data.month <= 11), "season"] = "autumn"

    return data



def dataset(name):
    """Loading colorspace Package Example Data

    The package `colorspace` comes with a few small data sets used
    in the Examples and/or the documentation. This function allows
    for easy access to these data sets. Note that some data sets
    are require `pandas` to be installed.

    #### **volcano**: Maunga Whau Volcano

    Topographic information on Auckland's Maunga Whau Volcano on 
    a 10m x 10m grid. Will return a two-dimensional `numpy.ndarray`
    of dimension 61x87 (int64).

    Digitized from a topographic map by Ross Ihaka.  These data should
    not be regarded as accurate.

    #### **HarzTraffic**: Daily Traffic Counts at Sonnenberg

    The data set provides daily traffic counts for bikes (motor bikes),
    cars, trucks, and other vehicles in the vicinity of Sonnenberg
    located in the Harz region in Germany. The data set covers
    a period of nearly three years (2021-01-01 to 2023-11-30).

    A `pandas.DataFrame` containing 1057 observations (rows) on 16 variables:

    * `date` date, the date of the record.
    * `yday` int64, the day of the year.
    * `bikes` int64, the number of motorcycles on that day.
    * `cars` int64, the number of cars on that day.
    * `trucks` int64, the number of trucks on that day.
    * `others` int64, the number of other vehicles on that day.
    * `tempmin` float64, minimum temperature in degrees Celsius.
    * `tempmax` float64, maximum temperature in degrees Celsius.
    * `temp` float64, mean temperature in degrees Celsius.
    * `humidity` int64, mean relative humidity in percent.
    * `tempdew` float64, average dewpoint temperature in degrees Celsius.
    * `cloudiness` int64, average cloud cover in percent.
    * `rain` float64, amount of precipitation in mm (snow and rain).
    * `sunshine` int64, sunshine duration in minutes.
    * `wind` float64, mean wind speed in meters per second.
    * `windmax` float64, maximum wind speed in meters per second.
    * `season`: object, local season (sprint, summer, autumn, winter).
    * `dow`: int64, numeric day of week (0 = Mon, 6 = Sun).
    * `dayofweek`: object, short name of day of week.
    * `weekend`: bool, True if the day is Saturday or Sunday, else False.

    Weather data: Deutscher Wetterdienst (DWD), Climate Data Center (CDC),
    station Wernigerode (5490; Sachsen-Anhalt) w/ location 10.7686/51.8454/233
    (lon, lat, alt, EPSG 4326). CC-BY 4.0, available via
    <https://opendata.dwd.de/climate_environment/CDC/>.

    Traffic data: Bundesanstalt für Strassenwesen (BASt), station Sonnenberg.
    CC-BY 4.0, available via <https://www.bast.de>,
    <https://www.bast.de/DE/Verkehrstechnik/Fachthemen/v2-verkehrszaehlung/Verkehrszaehlung.html>.


    #### **MonthlyHarzTraffic**: Monthly Summary of Traffic Counts at Sonnenberg

    Based on the daily data set `HarzTraffic` (see above) but aggregated on
    a monthly basis.

    A `pandas.DataFrame` containing 35 observations (rows) on 10 variables:

    * `year`: int32, year of record.
    * `month`: int32, year of record.
    * `bikes`: int64, the total number of bikes in that month.
    * `cars`: int64, the total number of cars in that month.
    * `trucks`: int64, the total number of trucks in that month.
    * `others`: int64, the total number of other vehicles in that month.
    * `rain`: float64, monthly precipitation sum in mm (snow and rain).
    * `temp`: float64, monthly mean temperature in degrees Celsius.
    * `sunshine`: int64, monthly average of sunshine per day in minutes.
    * `wind`: float64, monthly mean wind speed in meters per second.
    * `season`: object, local season (sprint, summer, autumn, winter).

    Data source and license: see data set description 'HarzTraffic'.


    Args:
        name (str): Name of the data set to be returned.

    Returns:
        The object returned depends on the data set (see above).
    """


    from . import datasets
    from re import compile

    if not isinstance(name, str):
        raise TypeError("argument `name` must be str")


    # Create listing of all available datasets
    available = []
    pattern = compile("(?<=(^_getdataset_))(.*)")
    for fn in dir(datasets):
        tmp = pattern.findall(fn)
        if len(tmp) > 0: available.append(tmp[0][1])

    try:
        fun = getattr(datasets, f"_getdataset_{name}")
    except:
        raise ValueError(f"dataset \"{name}\" does not exist. " + \
                         f"Available data sets are: {', '.join(available)}.")

    return fun()

