"""
Copyright 2005, Ross Ihaka. All Rights Reserved.
Ported to python: Copyright 2018, Reto Stauffer.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

   1. Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

   3. The name of the Ross Ihaka may not be used to endorse or promote
      products derived from this software without specific prior written
      permission.

THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ROSS IHAKA BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""


import logging as log
log.basicConfig(format="[%(levelname)s] %(message)s", level=log.DEBUG)

import sys
import numpy as np

# Conversion function
def DEG2RAD(x):
    """Conver degrees into radiant.
    @param x float in degrees.
    @return Returns input x in radiants."""
    return np.pi / 180. * x

# Conversion function
def RAD2DEG(x):
    """Conver radiant into degrees.
    @param x float in radiant.
    @return Returns input x in degrees."""
    return 180. / np.pi * x



# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------



# ----- CIE-XYZ <-> Device dependent RGB -----
#
#  Gamma Correction
#
#  The following two functions provide gamma correction which
#  can be used to switch between sRGB and linearized sRGB (RGB).
#
#  The standard value of gamma for sRGB displays is approximately 2.2,
#  but more accurately is a combination of a linear transform and
#  a power transform with exponent 2.4
#
#  gtrans maps linearized sRGB to sRGB.
#  ftrans provides the inverse map.

def gtrans(u, gamma):
    """Gamma Correction
    The following two functions provide gamma correction which
    can be used to switch between sRGB and linearized sRGB (RGB).

    The standard value of gamma for sRGB displays is approximately 2.2,
    but more accurately is a combination of a linear transform and
    a power transform with exponent 2.4

    gtrans maps linearized sRGB to sRGB, ftrans provides the inverse map.

    @param u np.ndarray of length N.
    @param gamma float or np.ndarray. If float or np.ndarray of length one
        gamma will be recycled (if length u > 1).
    @returns Returns np.ndarray of the same length as input \"u\".
    """

    # Input check
    if isinstance(gamma, float): gamma = np.asarray([gamma])
    if not np.all(isinstance(x, np.ndarray) for x in [u, gamma]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Extend gamma if gamma is of length 1
    if len(gamma) == 1 and not len(gamma) == len(u):
        gamma = np.repeat(gamma, len(u))

    for i,val in np.ndenumerate(u):
        if val > 0.00304: u[i] = 1.055 * np.power(val, (1. / gamma[i])) - 0.055
        else:             u[i] = 12.92 * val

    return u

def ftrans(u, gamma):
    """Gamma Correction
    The following two functions provide gamma correction which
    can be used to switch between sRGB and linearized sRGB (RGB).

    The standard value of gamma for sRGB displays is approximately 2.2,
    but more accurately is a combination of a linear transform and
    a power transform with exponent 2.4

    gtrans maps linearized sRGB to sRGB, ftrans provides the inverse map.

    @param u np.ndarray of length N.
    @param gamma float or np.ndarray. If float or np.ndarray of length one
        gamma will be recycled (if length u > 1).
    @returns Returns np.ndarray of the same length as input \"u\".
    """

    # Input check
    if isinstance(gamma, float): gamma = np.asarray([gamma])
    if not np.all(isinstance(x, np.ndarray) for x in [u, gamma]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Extend gamma if gamma is of length 1
    if len(gamma) == 1 and not len(gamma) == len(u):
        gamma = np.repeat(gamma, len(u))

    for i,val in np.ndenumerate(u):
        if val > 0.03928: u[i] = np.power((val + 0.055) / 1.055, gamma[i])
        else:             u[i] = val / 12.92

    return u

def DEVRGB_to_RGB(R, G, B, gamma):
    """TODO"""

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [R, G, B, gamma]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Extend gamma if gamma is of length 1
    if len(gamma) == 1 and not len(gamma) == len(R):
        gamma = np.repeat(gamma, len(R))

    # Check if all elements have the same length
    if not np.all([len(R) == len(x) for x in [G, B, gamma]]):
        import inspect
        log.error("Inputs to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Apply gamma correction
    return [ftrans(x, gamma) for x in [R, G, B]]

def RGB_to_DEVRGB(R, G, B, gamma):
    """TODO"""

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [R, G, B, gamma]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Extend gamma if gamma is of length 1
    if len(gamma) == 1 and not len(gamma) == len(R):
        gamma = np.repeat(gamma, len(R))

    # Check if all elements have the same length
    if not np.all([len(R) == len(x) for x in [G, B, gamma]]):
        import inspect
        log.error("Inputs to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Apply gamma correction
    return [gtrans(x, gamma) for x in [R, G, B]]


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------


## ----- CIE-XYZ <-> Device independent RGB -----
## R, G, and B give the levels of red, green and blue as values
## in the interval [0,1].  X, Y and Z give the CIE chromaticies.
## XN, YN, ZN gives the chromaticity of the white point.
def RGB_to_XYZ(R, G, B, XN, YN, ZN):
    """Device independent RGB.
    R, G, and B give the levels of red, green and blue as values
    in the interval [0,1].  X, Y and Z give the CIE chromaticies.
    @param R np.ndarray with indensities for red ([0-1]).
    @param G np.ndarray with indensities for green ([0-1]).
    @param B np.ndarray with indensities for blue ([0-1]).
    @param XN, YN, ZN np.ndarray with chromaticity of the white point.
        If of length 1 the white point specification will be recycled
        if length of R/G/B is larger than one.
    @return Returns corresponding X/Y/Z coordinates of CIE chromaticies,
        a list of np.ndarray's of the same length as the inputs ([X, Y, Z]).
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [R, G, B, XN, YN, ZN]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if not np.all([len(XN) == len(x) for x in [YN, ZN]]):
        log.error("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(R) == len(x) for x in [G, B]]):
        log.error("Inputs R/G/B to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if len(XN) == 1 and not len(XN) == len(R):
        XN = np.repeat(XN, len(R))
        YN = np.repeat(YN, len(R))
        ZN = np.repeat(ZN, len(R))

    # TODO only YN is used as in the original code. Is this correct, or
    # correct by accident?
    return [YN * (0.412453 * R + 0.357580 * G + 0.180423 * B),   # X
            YN * (0.212671 * R + 0.715160 * G + 0.072169 * B),   # Y
            YN * (0.019334 * R + 0.119193 * G + 0.950227 * B)]   # Z

def XYZ_to_RGB(X, Y, Z, XN, YN, ZN):
    """Device independent RGB.
    R, G, and B give the levels of red, green and blue as values
    in the interval [0,1].  X, Y and Z give the CIE chromaticies.
    @param X np.ndarray with CIE chromaticies ([0-1]).
    @param Y np.ndarray with CIE chromaticies ([0-1]).
    @param Z np.ndarray with CIE chromaticies ([0-1]).
    @param XN, YN, ZN np.ndarray with chromaticity of the white point.
        If of length 1 the white point specification will be recycled
        if length of X/Y/Z is larger than one.
    @return Returns corresponding R/G/B coordinates (in [0-1])
        a list of np.ndarray's of the same length as the inputs ([R, G, B]).
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [X, Y, Z, XN, YN, ZN]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if not np.all([len(XN) == len(x) for x in [YN, ZN]]):
        log.error("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(X) == len(x) for x in [Y, Z]]):
        log.error("Inputs X/Y/Z to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if len(XN) == 1 and not len(XN) == len(X):
        XN = np.repeat(XN, len(X))
        YN = np.repeat(YN, len(X))
        ZN = np.repeat(ZN, len(X))

    # TODO only YN is used as in the original code. Is this correct, or
    # correct by accident?
    return [( 3.240479 * X - 1.537150 * Y - 0.498535 * Z) / YN,   # R
            (-0.969256 * X + 1.875992 * Y + 0.041556 * Z) / YN,   # G
            ( 0.055648 * X - 0.204043 * Y + 1.057311 * Z) / YN]   # B


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------


## ----- CIE-XYZ <-> sRGB -----
## R, G, and B give the levels of red, green and blue as values
## in the interval [0,1].  X, Y and Z give the CIE chromaticies.
## XN, YN, ZN gives the chromaticity of the white point.
def sRGB_to_XYZ(R, G, B, XN, YN, ZN):
    """sRGB to CIE-XYZ.
    R, G, and B give the levels of red, green and blue as values
    in the interval [0,1].  X, Y and Z give the CIE chromaticies.
    XN, YN, ZN gives the chromaticity of the white point.
    @param R np.ndarray, intensity of red ([0-1]).
    @param G np.ndarray, intensity of green ([0-1]).
    @param B np.ndarray, intensity of blue ([0-1]).
    @param XN, YN, ZN np.ndarray with chromaticity of the white point.
        If of length 1 the white point specification will be recycled
        if length of X/Y/Z is larger than one.
    @return Returns corresponding X/Y/Z coordinates
        a list of np.ndarray's of the same length as the inputs ([X, Y, Z]).
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [R, G, B, XN, YN, ZN]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if not np.all([len(XN) == len(x) for x in [YN, ZN]]):
        log.error("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(R) == len(x) for x in [G, B]]):
        log.error("Inputs R/G/B to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if len(XN) == 1 and not len(XN) == len(R):
        XN = np.repeat(XN, len(R))
        YN = np.repeat(YN, len(R))
        ZN = np.repeat(ZN, len(R))

    R = ftrans(R, 2.4)
    G = ftrans(G, 2.4)
    B = ftrans(B, 2.4)
    return[YN * (0.412453 * R + 0.357580 * G + 0.180423 * B),   # X
           YN * (0.212671 * R + 0.715160 * G + 0.072169 * B),   # Y
           YN * (0.019334 * R + 0.119193 * G + 0.950227 * B)]   # Z

def XYZ_to_sRGB(X, Y, Z, XN, YN, ZN):
    """CIE-XYZ to sRGB.
    R, G, and B give the levels of red, green and blue as values
    in the interval [0,1].  X, Y and Z give the CIE chromaticies.
    XN, YN, ZN gives the chromaticity of the white point.
    @param X np.ndarray, CIE chromaticies.
    @param Y np.ndarray, CIE chromaticies.
    @param Z np.ndarray, CIE chromaticies.
    @param XN, YN, ZN np.ndarray with chromaticity of the white point.
        If of length 1 the white point specification will be recycled
        if length of X/Y/Z is larger than one.
    @return Returns corresponding G/R/B coordinates (in [0-1])
        a list of np.ndarray's of the same length as the inputs ([R, G, B]).
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [X, Y, Z, XN, YN, ZN]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if not np.all([len(XN) == len(x) for x in [YN, ZN]]):
        log.error("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(X) == len(x) for x in [Y, Z]]):
        log.error("Inputs X/Y/Z to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if len(XN) == 1 and not len(XN) == len(X):
        XN = np.repeat(XN, len(X))
        YN = np.repeat(YN, len(X))
        ZN = np.repeat(ZN, len(X))

    return [gtrans(( 3.240479 * X - 1.537150 * Y - 0.498535 * Z) / YN, 2.4),   # R
            gtrans((-0.969256 * X + 1.875992 * Y + 0.041556 * Z) / YN, 2.4),   # G
            gtrans(( 0.055648 * X - 0.204043 * Y + 1.057311 * Z) / YN, 2.4)]   # B
    return [R, G, B]



# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------

## ----- CIE-XYZ <-> CIE-LAB ----- */

## Often approximated as 903.3 */
## static const double kappa = 24389.0/27.0;
kappa = 24389.0/27.0
## Often approximated as 0.08856 */
## static const double epsilon = 216.0/24389.0;
epsilon = 216.0/24389.0
## Also, instead of the oft-used approximation 7.787, below uses (kappa / 116) */

def LAB_to_XYZ(L, A, B, XN, YN, ZN):
    """TODO"""

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [L, A, B, XN, YN, ZN]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if not np.all([len(XN) == len(x) for x in [YN, ZN]]):
        log.error("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(L) == len(x) for x in [A, B]]):
        log.error("Inputs L/A/B to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if len(XN) == 1 and not len(XN) == len(L):
        XN = np.repeat(XN, len(L))
        YN = np.repeat(YN, len(L))
        ZN = np.repeat(ZN, len(L))

    kappa   = 24389.0/27.0
    epsilon = 216.0/24389.0

    # Result arrays
    X = np.ndarray(len(L), dtype = "float"); X[:] = 0.
    Y = np.ndarray(len(L), dtype = "float"); Y[:] = 0.
    Z = np.ndarray(len(L), dtype = "float"); Z[:] = 0.

    # Calculate Y
    for i,val in np.ndenumerate(L):
        if   val <= 0:    Y[i] = 0.
        elif val <= 8.0:  Y[i] = val * YN[i] / kappa
        elif val <= 100.: Y[i] = YN[i] * np.power((val + 16.) / 116., 3.)
        else:             Y[i] = YN[i]

    fy = np.ndarray(len(Y), dtype = "float")
    for i,val in np.ndenumerate(Y):
        if val <= (epsilon * YN[i]):
            fy[i] = (kappa / 116.) * val / YN[i] + 16. / 116.
        else:
            fy[i] = np.power(val / YN[i], 1. / 3.)
    
    # Calculate X
    fx = fy + (A / 500.)
    for i,val in np.ndenumerate(fx):
        if np.power(val, 3.) <= epsilon:
            X[i] = XN[i] * (val - 16. / 116.) / (kappa / 116.)
        else:
            X[i] = XN[i] * np.power(val, 3.)
    
    # Calculate Z
    fz = fy - (B / 200.)
    for i,val in np.ndenumerate(fz):
        if np.power(val, 3.) <= epsilon:
            Z[i] = ZN[i] * (val - 16. / 116.) / (kappa / 116.)
        else:
            Z[i] = ZN[i] * np.power(val, 3)

    return [X, Y, Z]

def XYZ_to_LAB(X, Y, Z, XN, YN, ZN):
    """TODO"""

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [X, Y, Z, XN, YN, ZN]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if not np.all([len(XN) == len(x) for x in [YN, ZN]]):
        log.error("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(X) == len(x) for x in [Y, Z]]):
        log.error("Inputs X/Y/Z to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if len(XN) == 1 and not len(XN) == len(X):
        XN = np.repeat(XN, len(X))
        YN = np.repeat(YN, len(X))
        ZN = np.repeat(ZN, len(X))

    # Support function
    def f(t, kappa, epsilon):
        for i,val in np.ndenumerate(t):
            if val > epsilon:
                t[i] = np.power(val, 1./3.)
            else:
                t[i] = (kappa / 116.) * val + 16. / 116.
        return t

    kappa   = 24389.0 / 27.0
    epsilon = 216.0 / 24389.0

    xr = X / XN;
    yr = Y / YN;
    zr = Z / ZN;

    # Calculate L
    L = np.ndarray(len(X), dtype = "float"); L[:] = 0.
    for i,val in np.ndenumerate(yr):
        if val > epsilon:
            L[i] = 116. * np.power(val, 1./3.) - 16.
        else:
            L[i] = kappa * val

    xt = f(xr, kappa, epsilon);
    yt = f(yr, kappa, epsilon);
    zt = f(zr, kappa, epsilon);
    return [L, 500. * (xt - yt), 200. * (yt - zt)]  # [L, A, B]


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------

def XYZ_to_HLAB(X, Y, Z, XN, YN, ZN):
    """CIE-XYZ to Hunter LAB.
    Note that the Hunter LAB is no longer part of the public API,
    but the code is still here in case needed.
    @param X np.ndarray, CIE chromaticies.
    @param Y np.ndarray, CIE chromaticies.
    @param Z np.ndarray, CIE chromaticies.
    @param XN, YN, ZN np.ndarray with chromaticity of the white point.
        If of length 1 the white point specification will be recycled
        if length of X/Y/Z is larger than one.
    @return Returns corresponding Hunter L/A/B coordinates
        a list of np.ndarray's of the same length as the inputs ([L, A, B]).
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [X, Y, Z, XN, YN, ZN]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if not np.all([len(XN) == len(x) for x in [YN, ZN]]):
        log.error("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(X) == len(x) for x in [Y, Z]]):
        log.error("Inputs X/Y/Z to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if len(XN) == 1 and not len(XN) == len(X):
        XN = np.repeat(XN, len(X))
        YN = np.repeat(YN, len(X))
        ZN = np.repeat(ZN, len(X))

    X = X / XN; Y = Y / YN; Z = Z / ZN;
    l = np.sqrt(Y);
    return [10. * l, 17.5 * (((1.02 * X) - Y) / l), 7. * ((Y - (0.847 * Z)) / l)] # [L, A, B]


def HLAB_to_XYZ(L, A, B, XN, YN, ZN):
    """Hunter LAB to CIE-XYZ.
    Note that the Hunter LAB is no longer part of the public API,
    but the code is still here in case needed.
    @param L np.ndarray, Hunter LAB coordinate L.
    @param A np.ndarray, Hunter LAB coordinate A.
    @param B np.ndarray, Hunter LAB coordinate B.
    @param XN, YN, ZN np.ndarray with chromaticity of the white point.
        If of length 1 the white point specification will be recycled
        if length of X/Y/Z is larger than one.
    @return Returns corresponding Hunter CIE X/Z/Y coordinates as
        a list of np.ndarray's of the same length as the inputs ([X, Y, Z]).
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [L, A, B, XN, YN, ZN]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if not np.all([len(XN) == len(x) for x in [YN, ZN]]):
        log.error("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(L) == len(x) for x in [A, B]]):
        log.error("Inputs L/A/B to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    if len(XN) == 1 and not len(XN) == len(L):
        XN = np.repeat(XN, len(L))
        YN = np.repeat(YN, len(L))
        ZN = np.repeat(ZN, len(L))

    vY = L / 10.;
    vX = (A / 17.5) * (L / 10);
    vZ = (B / 7) * (L / 10);
    vY = vY * vY;

    Y = vY * XN
    X = (vX + vY) / 1.02 * YN
    Z = - (vZ - vY) / 0.847 * ZN

    return [X, Y, Z]


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------

def LAB_to_polarLAB(L, A, B):
    """LAB to polarLAB.
    Converts L/A/B coordinaes into polar LAB coordinates.
    @param L np.ndarray with coordinates in the L dimension.
    @param A np.ndarray with coordinates in the A dimension.
    @param B np.ndarray with coordinates in the B dimension.
    @return Returns a list of np.ndarrays of the same length
        as the input arrays L/A/B with the coordinates in the
        polarLAB colors space. Order [L, C, H].
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [L, A, B]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(L) == len(x) for x in [A, B]]):
        log.error("Inputs L/A/B to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Compute H
    H = RAD2DEG(np.arctan2(B, A))
    for i,val in np.ndenumerate(H):
        while val > 360.:   val -= 360.
        while val <   0.:   val += 360.
        H[i] = val
    # Compute C
    C = np.sqrt(A * A + B * B)

    return [L, C, H]

def polarLAB_to_LAB(L, C, H):
    """polarLAB to LAB.
    Converts L/C/H from polar LAB to LAB coordinates.
    @param L np.ndarray with coordinates in the L dimension.
    @param C np.ndarray with coordinates in the C dimension.
    @param H np.ndarray with coordinates in the H dimension.
    @return Returns a list of np.ndarrays of the same length
        as the input arrays L/A/B with the coordinates in the
        polarLAB colors space. Order [L, C, H].
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [L, C, H]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(L) == len(x) for x in [C, H]]):
        log.error("Inputs L/C/H to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    A = np.cos(DEG2RAD(H)) * C
    B = np.sin(DEG2RAD(H)) * C

    return [L, A, B]

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------

def RGB_to_HSV(r, g, b):
    """Convert RGB to HSV.
    @param r np.ndarray with red intensities [0-1].
    @param g np.ndarray with green intensities [0-1].
    @param b np.ndarray with blue intensities [0-1].
    @return Returns a list with the corresponding coordinates in the
        HSV color space ([h, s, v]).
    """
    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [r, g, b]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(r) == len(x) for x in [g, b]]):
        log.error("Inputs r/g/b to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Support function
    def gethsv(r, g, b):
        x = np.min([r, g, b])
        y = np.max([r, g, b])
        if y != x:
            f = g - b if r == x else b - r if g == x else r - g
            i = 3. if r == x else 5. if g == x else 1.
            h = 60. * (i - f /(y - x))
            s = (y - x)/y
            v = y
        else:
            ####ifdef MONO
            ### *h = NA_REAL; *s = 0; *v = y;
            ####else
            ### *h = 0; *s = 0; *v = y;
            ####endif
            h = 0.
            s = 0.
            v = y
        return [h, s, v]

    # Result arrays
    h = np.ndarray(len(r), dtype = "float"); h[:] = 0.
    s = np.ndarray(len(r), dtype = "float"); s[:] = 0.
    v = np.ndarray(len(r), dtype = "float"); v[:] = 0.

    # Calculate h/s/v
    for i in range(0, len(r)):
        tmp = gethsv(r[i], g[i], b[i])
        h[i] = tmp[0]; s[i] = tmp[1]; v[i] = tmp[2]

    return [h, s, v]


def HSV_to_RGB(h, s, v):
    """Convert HSV to RGB.
    @param h np.ndarray with hue intensities [0-360].
    @param s np.ndarray with saturation intensities [0-1].
    @param v np.ndarray with value intensities [0-1].
    @return Returns a list with the corresponding coordinates in the
        RGB color space ([r, g, b], all in [0-1]).
    """
    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [h, s, v]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(h) == len(x) for x in [s, v]]):
        log.error("Inputs h/s/v to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)


    # Support function
    def getrgb(h, s, v):

        # If Hue is not defined:
        if h == np.nan: return np.rep(v, 3)

        # Convert to [0-6]
        h = h / 60.
        i = np.floor(h)
        f = h - i

        if (i % 2) == 0:  # if i is even 
            f = 1 - f

        m = v * (1 - s)
        n = v * (1 - s * f)
        if i in [0,6]:     return [v, n, m]
        elif i == 1:       return [n, v, m]
        elif i == 2:       return [m, v, n]
        elif i == 3:       return [m, n, v]
        elif i == 4:       return [n, m, v]
        elif i == 5:       return [v, m, n]
        else:
            import sys;
            sys.exit("Ended up in a non-defined ifelse with i = %d".format(i))

    # Result arrays
    r = np.ndarray(len(h), dtype = "float"); r[:] = 0.
    g = np.ndarray(len(h), dtype = "float"); g[:] = 0.
    b = np.ndarray(len(h), dtype = "float"); b[:] = 0.

    for i in range(0,len(h)):
       tmp = getrgb(h[i], s[i], v[i])
       r[i] = tmp[0]; g[i] = tmp[1]; b[i] = tmp[2]

    return [r, g, b]


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------

def RGB_to_HLS(r, g, b):
    """Convert RGB to HLS.
    All r/g/b values in [0-1], h in [0, 360], l and s in [0, 1].
    From: http://wiki.beyondunreal.com/wiki/RGB_To_HLS_Conversion.

    @param r np.ndarray with red intensities [0-1].
    @param g np.ndarray with green intensities [0-1].
    @param b np.ndarray with blue intensities [0-1].
    @return Returns a list with the corresponding coordinates in the
        HSV color space ([h, s, v]).
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [r, g, b]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(r) == len(x) for x in [g, b]]):
        log.error("Inputs r/g/b to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Support function
    def gethls(r, g, b):
        min = np.min([r, g, b])
        max = np.max([r, g, b])

        l = (max + min)/2.;

        if max != min:
            if   l <  0.5: s = (max - min) / (max + min)
            elif l >= 0.5: s = (max - min) / (2. - max - min)

            if r == max:  h = (g - b) / (max - min);
            if g == max:  h = 2. + (b - r) / (max - min);
            if b == max:  h = 4. + (r - g) / (max - min);

            h = h * 60.;
            if h < 0.:    h = h + 360.;
            if h > 360.:  h = h - 360.;
        else:
            s = 0
            ####ifdef MONO
            ### *h = NA_REAL; 
            ####else
            ### *h = 0;
            ####endif
            h = 0;

        return [h, l, s]

    # Result arrays
    h = np.ndarray(len(r), dtype = "float"); h[:] = 0.
    l = np.ndarray(len(r), dtype = "float"); l[:] = 0.
    s = np.ndarray(len(r), dtype = "float"); s[:] = 0.

    for i in range(0,len(h)):
       tmp = gethls(r[i], g[i], b[i])
       h[i] = tmp[0]; l[i] = tmp[1]; s[i] = tmp[2]

    return [h, l, s]


def HLS_to_RGB(h, l, s):
    """Convert HLS to RGB.
    All r/g/b values in [0-1], h in [0, 360], l and s in [0, 1].
    From: http://wiki.beyondunreal.com/wiki/RGB_To_HLS_Conversion.

    @param h np.ndarray with hue [0-1].
    @param l np.ndarray with lightness [0-1]. TODO lightness?
    @param s np.ndarray with value [0-1].
    @return Returns a list with the corresponding coordinates in the
        RGB color space ([r, g, b], all in [0-1]).
    """

    # Checking input
    if not np.all(isinstance(x, np.ndarray) for x in [h, l, s]):
        import inspect
        log.error("Inputs to {:s} have to be of class np.ndarray.".format(
            inspect.stack()[0][3])); sys.exit(9)
    if not np.all([len(h) == len(x) for x in [l, s]]):
        log.error("Inputs h/l/s to {:s} have to be of the same length.".format(
            inspect.stack()[0][3])); sys.exit(9)

    # Support function qtrans
    def qtrans(q1, q2, hue):
        if hue > 360.:   hue = hue - 360.
        if hue < 0:      hue = hue + 360.
    
        if hue < 60.:    return q1 + (q2 - q1) * hue / 60.
        elif hue < 180.: return q2
        elif hue < 240.: return q1 + (q2 - q1) * (240. - hue) / 60.
        else:            return q1
    
    # Support function
    def getrgb(h, l, s):
        p2 = l * (1. + s) if l <= 0.5 else 1 + s - (l * s)
        p1 = 2 * l - p2

        # If saturation is zero
        if (s == 0):    return np.rep(l, 3)
        # Else
        return [qtrans(p1, p2, h + 120.),   # r
                qtrans(p1, p2, h),          # g
                qtrans(p1, p2, h - 120.)]   # b

    # Result arrays
    r = np.ndarray(len(h), dtype = "float"); r[:] = 0.
    g = np.ndarray(len(h), dtype = "float"); g[:] = 0.
    b = np.ndarray(len(h), dtype = "float"); b[:] = 0.

    for i in range(0,len(r)):
       tmp = getrgb(h[i], l[i], s[i])
       r[i] = tmp[0]; g[i] = tmp[1]; b[i] = tmp[2]

    return [r, g, b]

## ----- CIE-XYZ <-> CIE-LUV ----- */

def XYZ_to_uv(X, Y, Z):
    """TODO"""

    t = X + Y + Z
    if t == 0.:
        x = 0.
        y = 0.
    else:
        x = X / t;
        y = Y / t;
    
    u = 2.0 * x / (6. * y - x + 1.5);
    v = 4.5 * y / (6. * y - x + 1.5);

    return [u, v]

def XYZ_to_LUV(X, Y, Z, XN, YN, ZN):
    [u, v]   = XYZ_to_uv(X, Y, Z)
    [uN, vN] = XYZ_to_uv(XN, YN, ZN)
    y = Y / YN;
    #DEL# L = (y > epsilon) ? 116. * np.power(y, 1.0/3.0) - 16 : kappa * y;
    L = 116. * np.power(y, 1.0/3.0) - 16 if y > epsilon else kappa * y
    U = 13. * L * (u - uN);
    V = 13. * L * (v - vN);
    return [L, U, V]

def LUV_to_XYZ(L, U, V, XN, YN, ZN):
    if L <= 0 and U == 0 and V == 0:
        X = 0.
        Y = 0.
        Z = 0.
    else:
        ## 8 = kappa*epsilon 
        #DEL# Y = YN * ((L > 8.) ? np.power((L + 16.)/116., 3.) : L / kappa)
        Y = YN * (np.power((L + 16.)/116., 3.) if L > 8. else L / kappa)
    [uN, vN] = XYZ_to_uv(XN, YN, ZN)
    u = U / (13. * L) + uN
    v = V / (13. * L) + vN
    X =  9.0 * Y * u / (4 * v)
    Z =  -X / 3 - 5 * Y + 3 * Y / v

    return [X, Y, Z]


## ----- LUV <-> polarLUV ----- */

def LUV_to_polarLUV(L, U, V):
    l = L
    c = sqrt(U * U + V * V)
    h = RAD2DEG(np.arctan2(V, U))
    while h > 360:
        h -= 360.
    while h < 0.:
        h += 360.

    return [l, c, h]

def polarLUV_to_LUV(l, c, h):
    h = DEG2RAD(h)
    L = l
    U = c * np.cos(h)
    V = c * np.sin(h)
    return [L, U, V]

## ----- Argument Checking -----
#define CIEXYZ    0
#define RGB       1
#define HSV       2
#define CIELUV    3
#define POLARLUV  4
#define CIELAB    5
#define POLARLAB  6
#define HLS       7
#define sRGB      8

#static void CheckSpace(SEXP space, int *spacecode)
#{
#    if (!isString(space) || length(space) != 1)
#  error("invalid color space in C routine \"CheckSpace\" (1)");
#    if (!strcmp(CHAR(STRING_ELT(space, 0)), "XYZ"))
#  *spacecode = CIEXYZ;
#    elif (!strcmp(CHAR(STRING_ELT(space, 0)), "RGB"))
#  *spacecode = RGB;
#    elif (!strcmp(CHAR(STRING_ELT(space, 0)), "sRGB"))
#  *spacecode = sRGB;
#    elif (!strcmp(CHAR(STRING_ELT(space, 0)), "HSV"))
#  *spacecode = HSV;
#    elif (!strcmp(CHAR(STRING_ELT(space, 0)), "HLS"))
#  *spacecode = HLS;
#    elif (!strcmp(CHAR(STRING_ELT(space, 0)), "LUV"))
#  *spacecode = CIELUV;
#    elif (!strcmp(CHAR(STRING_ELT(space, 0)), "polarLUV"))
#  *spacecode = POLARLUV;
#    elif (!strcmp(CHAR(STRING_ELT(space, 0)), "LAB"))
#  *spacecode = CIELAB;
#    elif (!strcmp(CHAR(STRING_ELT(space, 0)), "polarLAB"))
#  *spacecode = POLARLAB;
#    else
#  error("invalid color space in C routine \"CheckSpace\" (2)");
#}
#
#static void CheckColor(SEXP color, int *n)
#{
#    if (!isNumeric(color))
#        error("color error - numeric values required");
#    if (!isMatrix(color) || ncols(color) != 3)
#        error("color error - a matrix with 3 columns required");
#    *n = nrows(color);
#}
#
#static void CheckHex(SEXP hex, int *n)
#{
#    int i, j;
#    if (!isString(hex))
#        goto badhex;
#    *n = length(hex);
#    for (i = 0; i < *n; i++) {
#        if (strlen(CHAR(STRING_ELT(hex, i))) != 7 ||
#                CHAR(STRING_ELT(hex, i))[0] != '#')
#            goto badhex;
#        for (j = 1; j < 7; j++) {
#            if (!isxdigit(CHAR(STRING_ELT(hex, i))[j]))
#                goto badhex;
#        }
#    }
#    return;
#badhex:
#    error("color error - hex values required");
#}
#
#static void CheckWhite(SEXP white, double *Xn, double *Yn, double *Zn)
#{
#    int n;
#    if (isNull(white)) {
#  /* Use D65 by default. */
#  *Xn =  95.047;
#  *Yn = 100.000;
#  *Zn = 108.883;
#    }
#    else {
#  CheckColor(white, &n);
#  if (n != 1 ||
#      REAL(white)[0] <= 0 ||
#      REAL(white)[1] <= 0 ||
#      REAL(white)[2] <= 0)
#      error("color error || invalid white point");
#  *Xn = REAL(white)[0];
#  *Yn = REAL(white)[1];
#  *Zn = REAL(white)[2];
#    }
#}
#
#static void CheckGamma(SEXP gamma, double *gammaval)
#{
#    *gammaval = asReal(gamma);
#    if (!R_FINITE(*gammaval) || *gammaval <= 0)
#  error("invalid gamma value");
#}
#
#static void CheckFixup(SEXP fixup, int *fixupval)
#{
#    *fixupval = asLogical(fixup);
#    if (*fixupval == NA_LOGICAL)
#  *fixupval = 1;
#}
#
#
#/* ----- Entry Points for Coersion Methods ----- */
#
#SEXP as_XYZ(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    case RGB:
#  for(i = 0; i < n; i++) {
#      RGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      sRGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HSV:
#    case HLS:
#        error("Ambiguous conversion");
#  break;
#    case CIELUV:
#  for(i = 0; i < n; i++) {
#      LUV_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLUV:
#  for(i = 0; i < n; i++) {
#      polarLUV_to_LUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case CIELAB:
#  for(i = 0; i < n; i++) {
#      LAB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLAB:
#  for(i = 0; i < n; i++) {
#      polarLAB_to_LAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    default:
#  error("unimplemented colour space (3)");
#    }
#    return ans;
#}
#
#SEXP as_RGB(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#  for(i = 0; i < n; i++) {
#      XYZ_to_RGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case RGB:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      DEVRGB_to_RGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#                          2.4,
#                          &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HSV:
#  for(i = 0; i < n; i++) {
#      HSV_to_RGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HLS:
#  for(i = 0; i < n; i++) {
#      HLS_to_RGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case CIELUV:
#  for(i = 0; i < n; i++) {
#      LUV_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_RGB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLUV:
#  for(i = 0; i < n; i++) {
#      polarLUV_to_LUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_RGB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case CIELAB:
#  for(i = 0; i < n; i++) {
#      LAB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_RGB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLAB:
#  for(i = 0; i < n; i++) {
#      polarLAB_to_LAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_RGB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    default:
#  error("unimplemented colour space (3)");
#    }
#    return ans;
#}
#
#SEXP as_sRGB(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#  for(i = 0; i < n; i++) {
#      XYZ_to_sRGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#                        &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case RGB: 
#  for(i = 0; i < n; i++) {
#            RGB_to_DEVRGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#                          2.4,
#                          &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#        }
#        break;
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    case HSV:
#  for(i = 0; i < n; i++) {
#      HSV_to_RGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HLS:
#  for(i = 0; i < n; i++) {
#      HLS_to_RGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case CIELUV:
#  for(i = 0; i < n; i++) {
#      LUV_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_sRGB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#                        &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLUV:
#  for(i = 0; i < n; i++) {
#      polarLUV_to_LUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_sRGB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case CIELAB:
#  for(i = 0; i < n; i++) {
#      LAB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_sRGB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLAB:
#  for(i = 0; i < n; i++) {
#      polarLAB_to_LAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_sRGB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    default:
#  error("unimplemented colour space (3)");
#    }
#    return ans;
#}
#
#SEXP as_HSV(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#    case CIELUV:
#    case POLARLUV:
#    case CIELAB:
#    case POLARLAB:
#        error("Ambiguous conversion");
#  break;
#    case RGB:
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      RGB_to_HSV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HSV:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    case HLS:
#  for(i = 0; i < n; i++) {
#      HLS_to_RGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      RGB_to_HSV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    default:
#  error("unimplemented colour space (3)");
#    }
#    return ans;
#}
#
#SEXP as_HLS(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#    case CIELUV:
#    case POLARLUV:
#    case CIELAB:
#    case POLARLAB:
#        error("Ambiguous conversion");
#  break;
#    case RGB:
#  for(i = 0; i < n; i++) {
#      RGB_to_HLS(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      RGB_to_HLS(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HSV:
#  for(i = 0; i < n; i++) {
#      HSV_to_RGB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      RGB_to_HLS(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#        break;
#    case HLS:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    default:
#  error("unimplemented colour space (3)");
#    }
#    return ans;
#}
#
#
#SEXP as_LUV(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#  for(i = 0; i < n; i++) {
#      XYZ_to_LUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case RGB:
#  for(i = 0; i < n; i++) {
#      RGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      sRGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HSV:
#    case HLS:
#        error("Ambiguous conversion");
#  break;
#    case CIELUV:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    case POLARLUV:
#  for(i = 0; i < n; i++) {
#      polarLUV_to_LUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]); 
#  }
#  break;
#    case CIELAB:
#  for(i = 0; i < n; i++) {
#      LAB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLAB:
#  for(i = 0; i < n; i++) {
#      polarLAB_to_LAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    default:
#  error("unimplemented colour space (3)");
#    }
#    return ans;
#}
#
#SEXP as_polarLUV(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#  for(i = 0; i < n; i++) {
#      XYZ_to_LUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_polarLUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case RGB:
#  for(i = 0; i < n; i++) {
#      RGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_polarLUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      sRGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_polarLUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HSV:
#    case HLS:
#        error("Ambiguous conversion");
#  break;
#    case CIELUV:
#  for(i = 0; i < n; i++) {
#      LUV_to_polarLUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLUV:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    case CIELAB:
#  for(i = 0; i < n; i++) {
#      LAB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_polarLUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLAB:
#  for(i = 0; i < n; i++) {
#      polarLAB_to_LAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_polarLUV(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    default:
#  error("unimplemented colour space (3)");
#    }
#    return ans;
#}
#
#SEXP as_LAB(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#  for(i = 0; i < n; i++) {
#      XYZ_to_LAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case RGB:
#  for(i = 0; i < n; i++) {
#      RGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      sRGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HSV:
#    case HLS:
#        error("Ambiguous conversion");
#  break;
#    case CIELUV:
#  for(i = 0; i < n; i++) {
#      LUV_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLUV:
#  for(i = 0; i < n; i++) {
#      polarLUV_to_LUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case CIELAB:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    case POLARLAB:
#  for(i = 0; i < n; i++) {
#      polarLAB_to_LAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    default:
#  error("unimplemented colour space");
#    }
#    return ans;
#}
#
#SEXP as_polarLAB(SEXP color, SEXP space, SEXP white)
#{
#    double Xn, Yn, Zn;
#    int spacecode;
#    int i, n;
#    SEXP ans;
#
#    CheckColor(color, &n);
#    CheckSpace(space, &spacecode);
#    CheckWhite(white, &Xn, &Yn, &Zn);
#
#    ans = allocMatrix(REALSXP, n, 3);
#
#    switch(spacecode) {
#    case CIEXYZ:
#  for(i = 0; i < n; i++) {
#      XYZ_to_LAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_polarLAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case RGB:
#  for(i = 0; i < n; i++) {
#      RGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_polarLAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case sRGB:
#  for(i = 0; i < n; i++) {
#      sRGB_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_polarLAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case HSV:
#    case HLS:
#        error("Ambiguous conversion");
#  break;
#    case CIELUV:
#  for(i = 0; i < n; i++) {
#      LUV_to_XYZ(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_polarLAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLUV:
#  for(i = 0; i < n; i++) {
#      polarLUV_to_LUV(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LUV_to_XYZ(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      XYZ_to_LAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n], Xn, Yn, Zn,
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#      LAB_to_polarLAB(REAL(ans)[i], REAL(ans)[i+n], REAL(ans)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case CIELAB:
#  for(i = 0; i < n; i++) {
#      LAB_to_polarLAB(REAL(color)[i], REAL(color)[i+n], REAL(color)[i+2*n],
#            &REAL(ans)[i], &REAL(ans)[i+n], &REAL(ans)[i+2*n]);
#  }
#  break;
#    case POLARLAB:
#  for(i = 0; i < n; i++) {
#      REAL(ans)[i] = REAL(color)[i];
#      REAL(ans)[i+n] = REAL(color)[i+n];
#      REAL(ans)[i+2*n] = REAL(color)[i+2*n];
#  }
#  break;
#    default:
#  error("unimplemented colour space (3)");
#    }
#    return ans;
#}
#
#static int FixupColor(int *r, int *g, int *b)
#{
#    int fix = 0;
#    if (*r < 0) { *r = 0; fix = 1; } elif (*r > 255) { *r = 255; fix = 1; }
#    if (*g < 0) { *g = 0; fix = 1; } elif (*g > 255) { *g = 255; fix = 1; }
#    if (*b < 0) { *b = 0; fix = 1; } elif (*b > 255) { *b = 255; fix = 1; }
#    return fix;
#}
#
#static const char HEXDIG[] = {
#    '0', '1', '2', '3', '4', '5', '6', '7',
#    '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'
#};
#
#SEXP sRGB_to_RColor(SEXP rgb, SEXP fixup)
#{
#    double r, g, b;
#    int fixupvalue, i, ir, ig, ib, n, nagen;
#    char hex[8];
#    SEXP ans;
#
#    CheckColor(rgb, &n);
#    CheckFixup(fixup, &fixupvalue);
#
#    PROTECT(ans = allocVector(STRSXP, n));
#    nagen = 0;
#
#    for (i = 0; i < n; i++) {
#  r = REAL(rgb)[i];
#  g = REAL(rgb)[i+n];
#  b = REAL(rgb)[i+2*n];
#        if (R_FINITE(r) && R_FINITE(g) && R_FINITE(b)) {
#      /* Hardware color representation */
#      ir = 255 * r + .5;
#      ig = 255 * g + .5;
#      ib = 255 * b + .5;
#      if (FixupColor(&ir, &ig, &ib) && !fixupvalue) {
#     SET_STRING_ELT(ans, i, NA_STRING);
#      }
#      else {
#     hex[0] = '#';
#     hex[1] = HEXDIG[(ir / 16) % 16];
#     hex[2] = HEXDIG[ir % 16];
#     hex[3] = HEXDIG[(ig / 16) % 16];
#     hex[4] = HEXDIG[ig % 16];
#     hex[5] = HEXDIG[(ib / 16) % 16];
#     hex[6] = HEXDIG[ib % 16];
#     hex[7] = '\0';
#     SET_STRING_ELT(ans, i, mkChar(hex));
#      }
#  }
#  else
#            SET_STRING_ELT(ans, i, NA_STRING);
#    }
#    UNPROTECT(1);
#    return ans;
#}
#
#static int decodeHexDigit(int x)
#{
#  switch(x) {
#  case '0': case '1': case '2': case '3': case '4':
#  case '5': case '6': case '7': case '8': case '9':
#  return x - '0';
#  case 'A': case 'B': case 'C': case 'D': case 'E': case 'F':
#  return x - 'A' + 10;
#  case 'a': case 'b': case 'c': case 'd': case 'e': case 'f':
#  return x - 'a' + 10;
#  default:
#  return -1;
#  }
#}
#
#static void decodeHexStr(const char * const x, double *r, double *g, double *b)
#{
#  int d1, d2, d3, d4, d5, d6;
#  d1 = decodeHexDigit(x[1]);
#  d2 = decodeHexDigit(x[2]);
#  d3 = decodeHexDigit(x[3]);
#  d4 = decodeHexDigit(x[4]);
#  d5 = decodeHexDigit(x[5]);
#  d6 = decodeHexDigit(x[6]);
#  if (d1 >= 0 && d2 >= 0 &&
#      d3 >= 0 && d4 >= 0 &&
#      d5 >= 0 && d6 >= 0) {
#      *r = (16 *d1 + d2)/255.;
#      *g = (16 *d3 + d4)/255.;
#      *b = (16 *d5 + d6)/255.;
#  }
#  else {
#    *r = NA_REAL;
#    *g = NA_REAL;
#    *b = NA_REAL;
#  }
#}
#
#SEXP hex_to_RGB(SEXP hex, SEXP gamma)
#{
#    double r, g, b;
#    int i, n = 0;
#    SEXP ans;
#    CheckHex(hex, &n);
#    ans = allocMatrix(REALSXP, n, 3);
#    for(i = 0; i < n; i++) {
#        decodeHexStr(CHAR(STRING_ELT(hex, i)), &r, &g, &b);
#        if (asLogical(gamma))
#            DEVRGB_to_RGB(r, g, b, 2.4, &r, &g, &b);
#        REAL(ans)[i] = r;
#        REAL(ans)[i+n] = g;
#        REAL(ans)[i+2*n] = b;
#    }
#    return ans;
#}
