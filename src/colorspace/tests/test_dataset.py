

from colorspace import dataset
from pytest import raises
import numpy as np
import pandas as pd


# -------------------------------------------------
# Wrong usage
# -------------------------------------------------
def test_dataset_wrong_usage():

    raises(TypeError, dataset, 1)
    raises(TypeError, dataset, name = True)
    raises(TypeError, dataset, name = ["foo"])

    raises(ValueError, dataset, "name_of_non_existing_dataset")
    raises(ValueError, dataset, name = "name_of_non_existing_dataset")


def test_dataset_volcano():

    x = dataset("volcano")

    assert isinstance(x, np.ndarray)
    assert np.all(x.shape == np.asarray((61, 87)))
    assert np.isdtype(x.dtype, np.int64)

def test_dataset_HarzTraffic():

    # Expected columns (in this order)
    expected = np.asarray(["date", "yday", "bikes", "cars", "trucks", "others",
        "tempmin", "tempmax", "temp", "humidity", "tempdew", "cloudiness", "rain",
        "sunshine", "wind", "windmax", "season", "weekend"])

    # Loading data
    x = dataset("HarzTraffic")

    assert isinstance(x, pd.DataFrame)
    assert np.all(x.shape == np.asarray((1057, len(expected))))

    # checking expected column names
    assert np.all(x.columns == expected)

    # Quick data check
    assert x.bikes.sum() == 214234
    assert x.cars.sum() == 2017941
    assert np.isclose(x.temp.mean(), 10.718353831598865)


def test_dataset_MonthlyHarzTraffic():

    # Expected columns (in this order)
    expected = np.asarray(["year", "month", "bikes", "cars", "trucks", "others",
        "rain", "temp", "sunshine", "wind", "season"])

    # Loading data
    x = dataset("MonthlyHarzTraffic")

    assert isinstance(x, pd.DataFrame)
    assert np.all(x.shape == np.asarray((35, len(expected))))
    # checking expected column names
    assert np.all(x.columns == expected)

    # Quick data check
    assert x.bikes.sum() == 214234
    assert x.cars.sum() == 2017941
    assert np.isclose(x.temp.mean(), 10.665714285714287)
