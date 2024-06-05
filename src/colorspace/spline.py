
#   Natural Cubic Spline Interpolation
#
#   Natural cubic spline interpolation. Takes two arrays `x` and `y`
#   trough which a spline is fitted and evaluated at `xout`.
#
#   Args:
#       x (numpy.ndarray): original x data points. Must be float or int
#           and length > 0.
#       y (numpy.ndarray): original y data points, same requirements
#           as `x`. Must also be of the same length as `y`.
#       xout (numpy.ndarray): numeric vectotr (float or int; length > 0)
#           at which the spline should be evaluated.
#
#   Returns:
#       dict: Dictionary with two elements, `x` (same as input `xout`)
#       and `y` with the interpolated values evaluated at `x` (`xout`).
#
#   Examples:
#   >>> x = np.arange(10, 20.1, 0.5)
#   >>> y = np.sin((x - 3) / 2)
#   >>> xout = np.arange(10, 20, 0.01)
#   >>> 
#   >>> res = natural_cubic_spline(x, y, xout)
#   >>>
#   >>> from matplotlib import pyplot as plt
#   >>> plt.figure()
#   >>> plt.plot(x, y, "o", label = "data points")
#   >>> plt.plot(res["x"], res["y"], label = "cubic spline", color = "orange")
#   >>> plt.legend()
#   >>> plt.show()
def natural_cubic_spline(x, y, xout):
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
        for i in range(n):
            if x[i] <= xout[j] <= x[i + 1]:
                dx = xout[j] - x[i]
                yout[j] = coef[i, 0] + coef[i, 1] * dx + coef[i, 2] * dx**2 + coef[i, 3] * dx**3

    return {"x": xout, "y": yout}

