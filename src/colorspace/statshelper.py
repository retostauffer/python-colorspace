

def nprange(x):
    """Range of Values

    Mimiking R's `range()` function, takes a numeric numpy array
    and returns an array of length `2` with the minimum and maximum.

    Args:
        x (numpy.ndarray): Numpy array, must be numeric.

    Returns:
        numpy.array: Retuns a numpy array with two elements
        containing the minimum of `x` and the maximum of `x`.
    """
    import numpy as np
    if not isinstance(x, np.ndarray):
        raise TypeError("argument `x` must be a numpy.array")
    elif not np.issubdtype(x.dtype, np.float64) and np.issubdtype(x.dtype, np.int64):
        raise TypeError("argument `x` must be float or int")

    return np.asarray([np.min(x), np.max(x)])


def natural_cubic_spline(x, y, xout):
    """Natural Cubic Spline Interpolation
 
    Natural cubic spline interpolation. Takes two arrays `x` and `y`
    trough which a spline is fitted and evaluated at `xout`.
 
    Args:
        x (numpy.ndarray): original x data points. Must be float or int
            and length > 0.
        y (numpy.ndarray): original y data points, same requirements
            as `x`. Must also be of the same length as `y`.
        xout (numpy.ndarray): numeric vectotr (float or int; length > 0)
            at which the spline should be evaluated.
 
    Returns:
        dict: Dictionary with two elements, `x` (same as input `xout`)
        and `y` with the interpolated values evaluated at `x` (`xout`).
 
    Examples:
    >>> from colorspace.statshelper import natural_cubic_spline
    >>> import numpy as np
    >>> x = np.arange(10, 20.1, 0.5)
    >>> y = np.sin((x - 3) / 2)
    >>> xout = np.arange(0, 40, 0.2)
    >>> 
    >>> res = natural_cubic_spline(x, y, xout)
    >>>
    >>> from matplotlib import pyplot as plt
    >>> plt.figure()
    >>> plt.plot(x, y, "o", label = "data points")
    >>> plt.plot(res["x"], res["y"], label = "cubic spline", color = "orange")
    >>> plt.legend()
    >>> plt.show()
    """
    import numpy as np

    if not isinstance(x, np.ndarray):
        raise TypeError("argument `x` must be numpy.ndarray")
    if not isinstance(y, np.ndarray):
        raise TypeError("argument `y` must be numpy.ndarray")
    if not isinstance(xout, np.ndarray):
        raise TypeError("argument `xout` must be numpy.ndarray")
    if len(x) == 0:
        raise ValueError("array on `x` must be of length > 0")
    if not len(x) == len(y):
        raise ValueError("length of `x` and `y` must be identical")

    def check(x):
        return np.issubdtype(x.dtype, np.float64) or np.issubdtype(x.dtype, np.integer)
    if not check(x):
        raise TypeError("argument `x` must be np.float or np.integer")
    if not check(y):
        raise TypeError("argument `y` must be np.float or np.integer")
    if not check(xout):
        raise TxoutpeError("argument `xout` must be np.float or np.integer")
    if len(xout) == 0:
        raise ValueError("array on `xout` must be of length > 0")
    
    # Enforce float
    y    = y.astype(np.float32)
    x    = x.astype(np.float32)
    xout = xout.astype(np.float32)

    # Index length
    n = len(x) - 1

    # Step 1: Calculate h_i
    h = np.diff(x)

    # Step 2: Calculate the coefficients a, b, c, and d
    a = y[:-1]

    # Step 3: Solve the tridiagonal system for c
    A = np.zeros((n + 1, n + 1))
    b = np.zeros(n + 1)

    # Natural spline boundary conditions
    A[0, 0] = 1
    A[n, n] = 1

    for i in range(1, n):
        A[i, i - 1] = h[i-1]
        A[i, i]     = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        b[i]        = 3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i-1]) / h[i-1])

    c = np.linalg.solve(A, b)

    # Step 4: Calculate b and d
    b = np.zeros(n)
    d = np.zeros(n)
    for i in range(n):
        b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

    # Organize coefficients
    coef = np.zeros((n, 4))
    for i in range(n):
        coef[i, 0] = a[i]
        coef[i, 1] = b[i]
        coef[i, 2] = c[i]
        coef[i, 3] = d[i]

    # Prediction/evaluation
    yout = np.zeros_like(xout)

    for j in range(len(xout)):
        # Extrapolation left hand side (linear)
        if xout[j] < np.min(x):
            yout[j] = y[0] - coef[0, 1] * (np.min(x) - xout[j])
        # Extrapolation right hand side (linear)
        elif xout[j] > np.max(x):
            k = coef.shape[0] - 1
            yout[j] = y[-1] + coef[k, 1] * (xout[j] - np.max(x))
        # Else interpolate btw. two neighboring points
        else:
            for i in range(n):
                if x[i] <= xout[j] <= x[i + 1]:
                    dx = xout[j] - x[i]
                    yout[j] = coef[i, 0] + coef[i, 1] * dx + coef[i, 2] * dx**2 + coef[i, 3] * dx**3

    return {"x": xout, "y": yout, "x": xout}


# Standard deviation with N - 1
def sd(a):
    from numpy import sqrt, sum, mean
    return sqrt(sum((a - mean(a))**2) / (len(a) - 1))

# Custom fn for estimator of pearson correlation with N - 1
def cor(x, y):
    from numpy import sum, mean
    from .statshelper import sd
    return sum((x - mean(x)) * (y - mean(y))) / (len(x) - 1) / (sd(x) * sd(y))


# import numpy as np
# from colorspace.statshelper import lm
# X = np.transpose(np.asarray([np.repeat(1, 5), [1, 2, 3, 4, 5]]))
# y = np.asarray([10.27, 19.48 , 28.86, 39.84, 50.54])
# print(X)
# res = lm(y = y, X = X, Xout = X)
# print(res)
def lm(y, X, Xout):
    import numpy as np
    assert isinstance(y, np.ndarray)
    assert isinstance(X, np.ndarray)
    assert len(X.shape) == 2 and len(Xout.shape) == 2
    assert isinstance(Xout, np.ndarray)
    assert len(y) == X.shape[0]
    assert X.shape[1] == Xout.shape[1]

    # Solving
    coef = np.linalg.lstsq(X, y, rcond=None)[0]

    # Fitted values
    yfit = np.dot(X, coef)

    # Residual standard error
    from .statshelper import sd
    sigma = sd(y - yfit)

    # Prediction on Xout
    Yout = np.dot(Xout, coef)

    return({"coef": coef, "sigma": sigma, "Yout": Yout})



def split(x, y):
    """Divide into Groups and Reassemble

    Helper function mimiking Rs split() function.
    Takes two numpy arrays (x, y) of same length.
    Splits x in segments according to the values of y (whenever
    the value in y changes). E.g.,

    Args:
        x (numpy.ndarray): Array containing the data to be divided into groups.
        y (numpy.ndarray): Array of the same length as `x` containing the
            grouping information. The original array `x` will be cut at each
            element in `y` where the value changes.

    Return:
        list of lists: Returns a list of lists, where each element in the
        object corresponds to one group, containing the original but now divided
        elements from `x`.

    Examples:
    >>> tmp = np.asarray([1, 2, 3, 4, 5])
    >>> split(tmp, tmp == 3)
    >>> [[1, 2], [3], [4, 5]]
    
    >>> tmp = np.asarray([1, 2, 3, 4, 5])
    >>> split(tmp, np.asarray([1, 1, 2, 2, 1]))
    >>> [[1, 2], [3, 4], [5]]
    """
    import numpy as np
    assert isinstance(x, np.ndarray), TypeError("argument `x` must be numpy array")
    assert isinstance(y, np.ndarray), TypeError("argument `y` must be numpy array")
    assert len(x) > 0, ValueError("array x must be length >= 1")
    assert len(x) == len(y), ValueError("arrays x/y must be of same length")
    if len(x) == 1: return [x]
    # Start with list-of-lists containing first element
    res = [[x[0]]]
    for i in range(1, len(x)):
        if y[i] == y[i - 1]:  res[len(res) - 1].append(x[i]) # Append
        else:                 res.append([x[i]]) # Add new list
    return res


















