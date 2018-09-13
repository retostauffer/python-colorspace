# """
# Copyright 2005, Ross Ihaka. All Rights Reserved.
# Ported to python: Copyright 2018, Reto Stauffer.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
# 
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
# 
#    3. The name of the Ross Ihaka may not be used to endorse or promote
#       products derived from this software without specific prior written
#       permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ROSS IHAKA BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# """


import sys
import numpy as np
import inspect

class colorlib(object):
    """The colorlib class is a collection of methods
    used to convert or transform colors between different
    color spaces."""


    # No initialization method, but some constants are specified here

    # Often approximated as 903.3 */
    # static const double self.KAPPA = 24389.0/27.0;
    KAPPA   = 24389.0/27.0

    # Often approximated as 0.08856
    # static const double EPSILON = 216.0/24389.0;
    # Also, instead of the oft-used approximation 7.787 we use (self.KAPPA / 116)
    EPSILON = 216.0/24389.0

    # Default white spot
    XN = np.asarray([ 95.047])
    YN = np.asarray([100.000])
    ZN = np.asarray([108.883])

    # Conversion function
    def DEG2RAD(self, x):
        """DEG2RAD(x)

        ParameterConver degrees into radiant.

        Parameters
        ----------
        x : float or array of floats
            values in degrees

        Returns
        -------
        float or float array
            Returns input ``x`` in radiant.
        """
        return np.pi / 180. * x

    
    # Conversion function
    def RAD2DEG(self, x):
        """RAD2DEG(x)
        
        ParameterConver radiant to degrees.

        Parameters
        ----------
        x : float or array of floats
            values in radiant

        Returns
        -------
        float or array of floats
            Returns input ``x`` in degrees.
        """
        return 180. / np.pi * x
    
    
    def _get_white_(self, __fname__, n, XN = None, YN = None, ZN = None):
        """_get_white_(__fname__, n, XN = None, YN = None, ZN = None)
        
        For some color conversion functions the "white" definition (default
        white color) has to be specified. This function checks and prepares the
        XN, YN, ZN definition. Defaults are used if the user does not specify a
        custom white splot. If set, XN, YN, ZN have to be of type np.ndarray
        either of length one (will be expanded to length "n") or of length n.

        Parameters
        ----------
        __fname__ : str
            string, name of the parent method, only used if errors are dropped.
            @TODO get rid of this thing and write a proper exception.
        n : int
            integer, number of colors to which NX, NY, NZ will be expanded
        XN : None, numpy.ndarray
            either None (default) or an nd.array of length one
            or length n. White point specification for dimension X
        YN : None, numpy.ndarray
            see XN. White point specification for dimension Y
        YZ : None, numpy.ndarray
            see XN. White point specification for dimension Z

        Returns
        -------
        list
            Returns a list ``[XN, YN, ZN]`` with three ``numpy.ndarrays`` of length ``n``.
            If the inputs XN, YN, ZN (or some) were ``None``: take class defaults.
        """

        # Take defaults if not further specified
        if not XN: XN = self.XN
        if not YN: YN = self.YN
        if not ZN: ZN = self.ZN

        if isinstance(XN,float): XN = np.asarray([XN])
        if isinstance(YN,float): YN = np.asarray([YN])
        if isinstance(ZN,float): ZN = np.asarray([ZN])

        # Checking type
        if not np.all(isinstance(x, np.ndarray) for x in [XN, YN, ZN]):
            raise ValueError("Inputs to {:s} have to be of class np.ndarray.".format(__fname__))
    
        # Expand if required
        if len(XN) == 1 and not len(XN) == n: XN = np.repeat(XN, n)
        if len(YN) == 1 and not len(YN) == n: YN = np.repeat(YN, n)
        if len(ZN) == 1 and not len(ZN) == n: ZN = np.repeat(ZN, n)
    
        # Check if all lengths match
        if not np.all([len(x) == n for x in [XN, YN, ZN]]):
            raise ValueError("Inputs XN/YN/ZN to {:s} have to be of the same length.".format(__fname__))

        return [XN, YN, ZN]
    

    def _check_input_arrays_(self, __fname__, **kwargs):
        """__check_input_arrays__(__fname__, **kwargs)
        
        Checks if all inputs in ``kwargs`` are of type ``numpy.ndarray`` and
        of the same length. If not, the script will drop some error messsages
        and stop.

        Parameters
        ----------
        __fname__ : str
            name of the method who called this check routine.
            Only used to drop a useful error message if required
        kwargs : ...
            named keywords, objects to be checked

        Returns
        -------
        bool
            Returns ``True`` if everything is ok, else a ValueError will be raised. 
        """

        # Message will be dropped if problems occur
        msg = "Problem while checking inputs \"{:s}\" to method \"{:s}\":".format(
                ", ".join(kwargs.keys()), __fname__)

        from numpy import asarray
        lengths = []
        for key,val in kwargs.items():

            try:
                val = asarray(val)
            except Exception as e:
                raise ValueError("input {:s} to {:s}".format(key, self.__class__.__name__) + \
                        " could not have been converted to numpy.ndarray")
            # Else append length and proceed
            lengths.append(len(val))

        # Check if all do have the same length
        if not np.all([x == lengths[0] for x in lengths]):
            msg += " Arguments of different lengths: {:s}".format(
                   ", ".join(["{:s} = {:d}".format(kwargs.keys()[i],lengths[i]) \
                   for i in range(0,len(kwargs))]))
            raise ValueError(msg)


        return True

    
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
    
    def gtrans(self, u, gamma):
        """gtrans(u, gamma)
        
        Gamma Correction.

        Function ``gtrans`` and ``ftrans`` provide gamma correction which
        can be used to switch between sRGB and linearized sRGB (RGB).
    
        The standard value of gamma for sRGB displays is approximately ``2.2``,
        but more accurately is a combination of a linear transform and
        a power transform with exponent ``2.4``
        gtrans maps linearized sRGB to sRGB, ftrans provides the inverse map.
    
        Parameters
        ----------
        u : numpy.ndarray
            float array of length N
        gamma : float or numpy.ndarray
            gamma value. If float or `numpy.ndarray` of length one
            gamma will be recycled (if length ``u > 1``)

        Returns
        -------
        numpy.ndarray
            Same length as input ``u``.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Input check
        if isinstance(gamma, float): gamma = np.asarray([gamma])
        if len(gamma) == 1 and not len(gamma) == len(u):
            gamma = np.repeat(gamma, len(u))

        # Checking inputs
        self._check_input_arrays_(__fname__, u = u, gamma = gamma)

        # Transform
        for i,val in np.ndenumerate(u):
            if val > 0.00304: u[i] = 1.055 * np.power(val, (1. / gamma[i])) - 0.055
            else:             u[i] = 12.92 * val
    
        return u
    
    def ftrans(self, u, gamma):
        """ftrans(u, gamma)
        
        Gamma Correction.

        Function :py:func:`gtrans` and :py:func:`ftrans` provide gamma
        correction between the RGB (device independent) and sRGB (device
        dependent) color space.
    
        The standard value of gamma for sRGB displays is approximately ``2.2``,
        but more accurately is a combination of a linear transform and
        a power transform with exponent ``2.4``.
        :py:func:`gtrans` maps linearized sRGB to sRGB, :py:func:`ftrans`
        provides the inverse map.
    
        Parameters
        ----------
        u : numpy.ndarray
            float array of length N
        gamma : float or numpy.ndarray
            gamma value. If float or `numpy.ndarray` of length one
            gamma will be recycled (if length ``u > 1``)

        Returns
        -------
        numpy.ndarray
            Same length as input ``u``.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method

        # Input check
        if isinstance(gamma, float): gamma = np.asarray([gamma])
        if len(gamma) == 1 and not len(gamma) == len(u):
            gamma = np.repeat(gamma, len(u))

        # Checking inputs
        self._check_input_arrays_(__fname__, u = u, gamma = gamma)
    
        # Transform 
        for i,val in np.ndenumerate(u):
            if val > 0.03928: u[i] = np.power((val + 0.055) / 1.055, gamma[i])
            else:             u[i] = val / 12.92
    
        return u
    
    def DEVRGB_to_RGB(self, R, G, B, gamma = 2.4):
        """DEVRGB_to_RGB(R, G, B, gamma = 2.4)

        Device dependent sRGB to device independent RGB.

        Parameters
        ----------
        R : numpy.ndarray
            indensities for red (``[0.,1.]``)
        G : numpy.ndarray
            indensities for green (``[0.,1.]``)
        B : numpy.ndarray
            indensities for blue  (``[0.,1.]``)
        gamma : float
            gamma adjustment.

        Returns
        -------
        list
            Returns a list of `numpy.ndarrays` with adjusted R, G, and B values.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method

        # Input check
        if isinstance(gamma, float): gamma = np.asarray([gamma])
        if len(gamma) == 1 and not len(gamma) == len(R):
            gamma = np.repeat(gamma, len(R))

        # Checking inputs
        self._check_input_arrays_(__fname__, R = R, G = G, B = B, gamma = gamma)
    
        # Apply gamma correction
        return [self.ftrans(x, gamma) for x in [R, G, B]]
    
    def RGB_to_DEVRGB(self, R, G, B, gamma = 2.4):
        """DEVRGB_to_RGB(R, G, B, gamma = 2.4)

        Device independent RGB to device dependent sRGB.

        Parameters
        ----------
        R : numpy.ndarray
            indensities for red (``[0.,1.]``).
        G : numpy.ndarray
            indensities for green (``[0.,1.]``).
        B : numpy.ndarray
            indensities for blue  (``[0.,1.]``).
        gamma : float
            gamma adjustment.

        Returns
        -------
        list
            Returns a list of `numpy.ndarrays` with adjusted R, G, and B values.
        """
    
        __fname__ = inspect.stack()[0][3] # Name of this method

        # Input check
        if isinstance(gamma, float): gamma = np.asarray([gamma])
        if len(gamma) == 1 and not len(gamma) == len(R):
            gamma = np.repeat(gamma, len(R))

        # Checking inputs
        self._check_input_arrays_(__fname__, R = R, G = G, B = B, gamma = gamma)
    
        # Apply gamma correction
        return [self.gtrans(x, gamma) for x in [R, G, B]]
    
    
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    
    ## ----- CIE-XYZ <-> Device independent RGB -----
    ## R, G, and B give the levels of red, green and blue as values
    ## in the interval [0,1].  X, Y and Z give the CIE chromaticies.
    ## XN, YN, ZN gives the chromaticity of the white point.
    def RGB_to_XYZ(self, R, G, B, XN = None, YN = None, ZN = None):
        """RGB_to_XYZ(R, G, B, XN = None, YN = None, ZN = None)
        
        Device independent RGB to XYZ.

        R, G, and B give the levels of red, green and blue as values
        in the interval ``[0.,1.]``.  X, Y and Z give the CIE chromaticies.

        Parameters
        ----------
        R : numpy.ndarray
            indensities for red (``[0.,1.]``)
        G : numpy.ndarray
            indensities for green (``[0.,1.]``)
        B : numpy.ndarray
            indensities for blue  (``[0.,1.]``)
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three ``None``) default values will be used

        Returns
        -------
        list
            Returns corresponding X/Y/Z coordinates of CIE chromaticies,
            a list of `numpy.ndarray`'s of the same length as the inputs (``[X, Y, Z]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(R) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, R = R, G = G, B = B)
    
        # TODO only YN is used as in the original code. Is this correct, or
        # correct by accident?
        return [YN * (0.412453 * R + 0.357580 * G + 0.180423 * B),   # X
                YN * (0.212671 * R + 0.715160 * G + 0.072169 * B),   # Y
                YN * (0.019334 * R + 0.119193 * G + 0.950227 * B)]   # Z
    
    def XYZ_to_RGB(self, X, Y, Z, XN = None, YN = None, ZN = None):
        """XYZ_to_RGB(X, Y, Z, XN = None, YN = None, ZN = None)
        
        CIEXYZ to device independent RGB.

        R, G, and B give the levels of red, green and blue as values
        in the interval ``[0.,1.]``.  X, Y and Z give the CIE chromaticies.

        Parameters
        ----------
        X : numpy.ndarray
            values for the Z dimension
        Y : numpy.ndarray
            values for the Z dimension
        Z : numpy.ndarray
            values for the Z dimension
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three ``None``) default values will be used

        Returns
        -------
        list
            Returns corresponding X/Y/Z coordinates of CIE chromaticies, a list
            of `numpy.ndarray`'s of the same length as the inputs (``[R, G,
            B]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(X) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, X = X, Y = Y, Z = Z)
    
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
    def sRGB_to_XYZ(self, R, G, B, XN = None, YN = None, ZN = None):
        """sRGB_to_XYZ(R, G, B, XN = None, YN = None, ZN = None)
        
        sRGB to CIEXYZ.
        
        R, G, and B give the levels of red, green and blue as values
        in the interval ``[0.,1.]``.  X, Y and Z give the CIE chromaticies.

        Parameters
        ----------
        R : numpy.ndarray
            indensities for red (``[0.,1.]``)
        G : numpy.ndarray
            indensities for green (``[0.,1.]``)
        B : numpy.ndarray
            indensities for blue  (``[0.,1.]``)
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three ``None``) default values will be used

        Returns
        -------
        list
            Returns corresponding X/Y/Z coordinates of CIE chromaticies, a list
            of `numpy.ndarray`'s of the same length as the inputs (``[X, Y,
            Z]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(R) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, R = R, G = G, B = B)
    
        # Transform R/G/B
        R = self.ftrans(R, 2.4)
        G = self.ftrans(G, 2.4)
        B = self.ftrans(B, 2.4)

        # Convert to X/Y/Z coordinates
        return[YN * (0.412453 * R + 0.357580 * G + 0.180423 * B),   # X
               YN * (0.212671 * R + 0.715160 * G + 0.072169 * B),   # Y
               YN * (0.019334 * R + 0.119193 * G + 0.950227 * B)]   # Z
    
    def XYZ_to_sRGB(self, X, Y, Z, XN = None, YN = None, ZN = None):
        """XYZ_to_sRGB(X, Y, Z, XN = None, YN = None, ZN = None)
        
        CIEXYZ to sRGB.

        R, G, and B give the levels of red, green and blue as values
        in the interval ``[0.,1.]``.  X, Y and Z give the CIE chromaticies.

        Parameters
        ----------
        X : numpy.ndarray
            values for the Z dimension
        Y : numpy.ndarray
            values for the Z dimension
        Z : numpy.ndarray
            values for the Z dimension
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three NA) default values will be used

        Returns
        -------
        list
            Returns corresponding X/Y/Z coordinates of CIE chromaticies, a list
            of `numpy.ndarray`'s of the same length as the inputs (``[R, G,
            B]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(X) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, X = X, Y = Y, Z = Z)
    
        # Transform and return
        return [self.gtrans(( 3.240479 * X - 1.537150 * Y - 0.498535 * Z) / YN, 2.4),   # R
                self.gtrans((-0.969256 * X + 1.875992 * Y + 0.041556 * Z) / YN, 2.4),   # G
                self.gtrans(( 0.055648 * X - 0.204043 * Y + 1.057311 * Z) / YN, 2.4)]   # B
    
    
    
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    
    ## ----- CIE-XYZ <-> CIE-LAB ----- */
    
    
    def LAB_to_XYZ(self, L, A, B, XN = None, YN = None, ZN = None):
        """LAB_to_XYZ(L, A, B, XN = None, YN = None, ZN = None)
        
        CIELAB to CIEXYZ.

        Parameters
        ----------
        L : numpy.ndarray
            values for the L dimension
        A : numpy.ndarray
            values for the A dimension
        B : numpy.ndarray
            values for the B dimension
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three NA) default values will be used

        Returns
        -------
        list
            Returns corresponding X/Y/Z coordinates of CIE chromaticies, a list
            of `numpy.ndarray`'s of the same length as the inputs (``[X, Y, Z]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(L) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)

        # Checking input
        self._check_input_arrays_(__fname__, L = L, A = A, B = B)
    
        # Result arrays
        X = np.ndarray(len(L), dtype = "float"); X[:] = 0.
        Y = np.ndarray(len(L), dtype = "float"); Y[:] = 0.
        Z = np.ndarray(len(L), dtype = "float"); Z[:] = 0.
    
        # Calculate Y
        for i,val in np.ndenumerate(L):
            if   val <= 0:    Y[i] = 0.
            elif val <= 8.0:  Y[i] = val * YN[i] / self.KAPPA
            elif val <= 100.: Y[i] = YN[i] * np.power((val + 16.) / 116., 3.)
            else:             Y[i] = YN[i]
    
        fy = np.ndarray(len(Y), dtype = "float")
        for i,val in np.ndenumerate(Y):
            if val <= (self.EPSILON * YN[i]):
                fy[i] = (self.KAPPA / 116.) * val / YN[i] + 16. / 116.
            else:
                fy[i] = np.power(val / YN[i], 1. / 3.)
        
        # Calculate X
        fx = fy + (A / 500.)
        for i,val in np.ndenumerate(fx):
            if np.power(val, 3.) <= self.EPSILON:
                X[i] = XN[i] * (val - 16. / 116.) / (self.KAPPA / 116.)
            else:
                X[i] = XN[i] * np.power(val, 3.)
        
        # Calculate Z
        fz = fy - (B / 200.)
        for i,val in np.ndenumerate(fz):
            if np.power(val, 3.) <= self.EPSILON:
                Z[i] = ZN[i] * (val - 16. / 116.) / (self.KAPPA / 116.)
            else:
                Z[i] = ZN[i] * np.power(val, 3)
    
        return [X, Y, Z]
    
    def XYZ_to_LAB(self, X, Y, Z, XN = None, YN = None, ZN = None):
        """XYZ_to_LAB(X, Y, Z, XN = None, YN = None, ZN = None)
        
        CIEXYZ to CIELAB.

        Parameters
        ----------
        X : numpy.ndarray
            values for the X dimension
        Y : numpy.ndarray
            values for the Y dimension
        Z : numpy.ndarray
            values for the Z dimension
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three NA) default values will be used

        Returns
        -------
        list
            Returns corresponding L/A/B coordinates, a list of
            `numpy.ndarray`'s of the same length as the inputs (``[L, A, B]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(X) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, X = X, Y = Y, Z = Z)
    
        # Support function
        def f(t, KAPPA, EPSILON):
            for i,val in np.ndenumerate(t):
                if val > EPSILON:
                    t[i] = np.power(val, 1./3.)
                else:
                    t[i] = (KAPPA / 116.) * val + 16. / 116.
            return t
    
        # Scaling
        xr = X / XN;
        yr = Y / YN;
        zr = Z / ZN;
    
        # Calculate L
        L = np.ndarray(len(X), dtype = "float"); L[:] = 0.
        for i,val in np.ndenumerate(yr):
            if val > self.EPSILON:
                L[i] = 116. * np.power(val, 1./3.) - 16.
            else:
                L[i] = self.KAPPA * val
    
        xt = f(xr, self.KAPPA, self.EPSILON);
        yt = f(yr, self.KAPPA, self.EPSILON);
        zt = f(zr, self.KAPPA, self.EPSILON);
        return [L, 500. * (xt - yt), 200. * (yt - zt)]  # [L, A, B]
    
    
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    def XYZ_to_HLAB(self, X, Y, Z, XN = None, YN = None, ZN = None):
        """XYZ_to_HLAB(X, Y, Z, XN = None, YN = None, ZN = None)
        
        CIE-XYZ to Hunter LAB.

        .. note::
            Note that the Hunter LAB is no longer part of the public API,
            but the code is still here in case needed.

        Parameters
        ----------
        X : numpy.ndarray
            values for the Z dimension
        Y : numpy.ndarray
            values for the Z dimension
        Z : numpy.ndarray
            values for the Z dimension
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three ``None``) default values will be used

        Returns
        -------
        list
            Returns corresponding Hunter LAB chromaticies, a list of
            `numpy.ndarray`'s of the same length as the inputs (``[L, A, B]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(X) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, X = X, Y = Y, Z = Z)
    
        # Transform
        X = X / XN; Y = Y / YN; Z = Z / ZN;
        l = np.sqrt(Y);
        return [10. * l, 17.5 * (((1.02 * X) - Y) / l), 7. * ((Y - (0.847 * Z)) / l)] # [L, A, B]
    
    
    def HLAB_to_XYZ(self, L, A, B, XN = None, YN = None, ZN = None):
        """HLAB_to_XYZ(L, A, B, XN = None, YN = None, ZN = None)

        Hunter LAB to CIE-XYZ.

        .. note::
            Note that the Hunter LAB is no longer part of the public API,
            but the code is still here in case needed.

        Parameters
        ----------
        L : numpy.ndarray
            values for the L dimension
        A : numpy.ndarray
            values for the A dimension
        B : numpy.ndarray
            values for the B dimension
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three NA) default values will be used

        Returns
        -------
        list
            Returns corresponding CIE-XYZ chromaticies, a list of
            `numpy.ndarray`'s of the same length as the inputs (``[X, Y, Z]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(L) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, L = L, A = A, B = B)
    
        # Transform
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
    
    def LAB_to_polarLAB(self, L, A, B):
        """LAB_to_polarLAB(L, A, B)

        Convert from CIELAB to the polar representation polarLAB.

        Parameters
        ----------
        L : numpy.ndarray
            values for the L dimension of the CIELAB color space
        A : numpy.ndarray
            values for the A dimension of the CIELAB color space
        B : numpy.ndarray
            values for the B dimension of the CIELAB color space

        Returns
        -------
        list
            Returns corresponding polar LAB chromaticies, a list of
            `numpy.ndarray`'s of the same length as the inputs (``[L, A, B]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Checking input
        self._check_input_arrays_(__fname__, L = L, A = A, B = B)
    
        # Compute H
        H = self.RAD2DEG(np.arctan2(B, A))
        for i,val in np.ndenumerate(H):
            while val > 360.:   val -= 360.
            while val <   0.:   val += 360.
            H[i] = val
        # Compute C
        C = np.sqrt(A * A + B * B)
    
        return [L, C, H]
    
    def polarLAB_to_LAB(self, L, C, H):
        """polarLAB_to_LAB(L, A, B)

        Convert form polarLAB to onvert CIELAB.

        Parameters
        ----------
        L : numpy.ndarray
            values for the L dimension of the polar LAB color space
        A : numpy.ndarray
            values for the A dimension of the polar LAB color space
        B : numpy.ndarray
            values for the B dimension of the polar LAB color space

        Returns
        -------
        list
            Returns corresponding CIELAB chromaticies, a list of
            `numpy.ndarray`'s of the same length as the inputs (``[L, A, B]``).
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Checking input
        self._check_input_arrays_(__fname__, L = L, C = C, H = H)
    
        A = np.cos(self.DEG2RAD(H)) * C
        B = np.sin(self.DEG2RAD(H)) * C
    
        return [L, A, B]
    
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    
    def RGB_to_HSV(self, r, g, b):
        """RGB_to_HSV(r, g, b)
        
        Convert RGB to HSV.

        Parameters
        ----------
        r : numpy.ndarray
            intensities for red (``[0.,1.]``)
        g : numpy.ndarray
            intensities for green (``[0.,1.]``)
        b : numpy.ndarray
            intensities for blue (``[0.,1.]``)

        Returns
        -------
        list
            Returns a `numpy.ndarray` with the corresponding coordinates in the
            HSV color space (``[h, s, v]``). Same length as the inputs.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Checking input
        self._check_input_arrays_(__fname__, r = r, g = g, b = b)
    
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
    
    
    def HSV_to_RGB(self, h, s, v):
        """HSV_to_RGB(r, g, b)
        
        Convert RGB to HSV.

        Parameters
        ----------
        h : nympy.ndarray
            hue values
        s : numpy.ndarray
            saturation
        v : numpy.ndarray
            value (the value-dimension of HSV)

        Returns
        -------
        list
            Returns a `numpy.ndarray` with the corresponding coordinates in the
            RGB color space (``[r, g, b]``). Same length as the inputs.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Checking input
        self._check_input_arrays_(__fname__, h = h, s = s, v = v)
    
        # Support function
        def getrgb(h, s, v):
    
            # If Hue is not defined:
            if h == np.nan: return np.repeat(v, 3)
    
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
    
    def RGB_to_HLS(self, r, g, b):
        """RGB_to_HLS(r, g, b)
        
        Convert RGB to HLS.
    
        All r/g/b values in ``[0.,1.]``, h in ``[[0., 360.]``, l and s in ``[0., 1.]``.
        From: http://wiki.beyondunreal.com/wiki/RGB_To_HLS_Conversion.

        Parameters
        ----------
        r : numpy.ndarray
            intensities for red (``[0.,1.]``)
        g : numpy.ndarray
            intensities for green (``[0.,1.]``)
        b : numpy.ndarray
            intensities for blue (``[0.,1.]``)

        Returns
        -------
        list
            Returns a `numpy.ndarray` with the corresponding coordinates in the
            HLS color space (``[h, l, s]``). Same length as the inputs.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Checking input
        self._check_input_arrays_(__fname__, r = r, g = g, b = b)
    
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
    
    
    def HLS_to_RGB(self, h, l, s):
        """HLS_to_RGB(h, l, s)

        Convert RLS to HLS.
    
        All r/g/b values in ``[0.,1.]``, h in ``[[0., 360.]``, l and s in ``[0., 1.]``.
        From: http://wiki.beyondunreal.com/wiki/RGB_To_HLS_Conversion.

        Parameters
        ----------
        h : nympy.ndarray
            hue values
        l : numpy.ndarray
            lightness
        s : numpy.ndarray
            saturation

        Returns
        -------
        list
            Returns a `numpy.ndarray` with the corresponding coordinates in the
            RGB color space (``[r, g, b]``). Same length as the inputs.
        """
    
        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Checking input
        self._check_input_arrays_(__fname__, h = h, l = l, s = s)
    
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
            if (s == 0):    return np.repeat(l, 3)
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
    
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    
    def XYZ_to_uv(self, X, Y, Z):
        """XYZ_to_uv(X, Y, Z)
        
        CIE-XYZ to u and v.

        Parameters
        ----------
        X : numpy.ndarray
            values for the Z dimension.
        Y : numpy.ndarray
            values for the Y dimension.
        Z : numpy.ndarray
            values for the Z dimension.

        Returns
        -------
        list
            Returns a list of `numpy.ndarrays` containing u and v (``[u, v]``). 
        """
    
        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Checking input
        self._check_input_arrays_(__fname__, X = X, Y = Y, Z = Z)
    
        # Result array
        x = np.ndarray(len(X), dtype = "float"); x[:] = 0.
        y = np.ndarray(len(X), dtype = "float"); y[:] = 0.
    
        t = X + Y + Z
        idx = np.where(t != 0)
        x[idx] = X[idx] / t[idx];
        y[idx] = Y[idx] / t[idx];
        
        return [2.0 * x / (6. * y - x + 1.5),    # u
                4.5 * y / (6. * y - x + 1.5)]    # v
    
    def XYZ_to_LUV(self, X, Y, Z, XN = None, YN = None, ZN = None):
        """XYZ_to_LUV(X, Y, Z, XN = None, YN = None, ZN = None)

        CIE-XYZ to CIE-LUV.

        Parameters
        ----------
        X : numpy.ndarray
            values for the X dimension
        Y : numpy.ndarray
            values for the Y dimension
        Z : numpy.ndarray
            values for the Z dimension
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three NA) default values will be used.

        Returns
        -------
        list
            Returns a list of CIELUV coordinates (``[L, U, V]``) with the same
            length as the input arrays.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(X) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, X = X, Y = Y, Z = Z)
    
        # Convert X/Y/Z and XN/YN/ZN to uv
        [u,  v]  = self.XYZ_to_uv(X,  Y,  Z )
        [uN, vN] = self.XYZ_to_uv(XN, YN, ZN)
    
        # Calculate L
        L = np.ndarray(len(X), dtype = "float"); L[:] = 0.
        y = Y / YN
        for i,val in np.ndenumerate(y):
            L[i] = 116. * np.power(val, 1./3.) - 16. if val > self.EPSILON else self.KAPPA * val
    
        # Calculate U/V
        return [L, 13. * L * (u - uN), 13. * L * (v - vN)]  # [L, U, V]
    
    def LUV_to_XYZ(self, L, U, V, XN = None, YN = None, ZN = None):
        """LUV_to_XYZ(L, U, V, XN = None, YN = None, ZN = None)

        CIE-LUV to CIE-XYZ.

        Parameters
        ----------
        L : numpy.ndarray
            values for the L dimension
        U : numpy.ndarray
            values for the U dimension
        V : numpy.ndarray
            values for the V dimension
        XN, YN, ZN : None or numpy.ndarray
            chromaticity of the white point. If of length 1 the white point
            specification will be recycled if length of R/G/B is larger than
            one. If not specified (all three NA) default values will be used

        Returns
        -------
        list
            Returns a list of CIE-XYZ coordinates (``[X, Y, Z]``) with the same
            length as the input arrays.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
        n = len(L) # Number of colors

        # Loading definition of white
        [XN, YN, ZN] = self._get_white_(__fname__, n, XN, YN, ZN)
    
        # Checking input
        self._check_input_arrays_(__fname__, L = L, U = U, V = V)
    
        # Result arrays
        X = np.ndarray(len(L), dtype = "float"); X[:] = 0.
        Y = np.ndarray(len(L), dtype = "float"); Y[:] = 0.
        Z = np.ndarray(len(L), dtype = "float"); Z[:] = 0.
    
        # Check for which values we do have to do the transformation
        def fun(L, U, V):
            return False if L <= 0. and U == 0. and V == 0. else True
        idx = np.where([fun(L[i], U[i], V[i]) for i in range(0, len(L))])[0]
        if len(idx) == 0: return [X, Y, Z]

        # Compute Y
        for i in idx:
            Y[i] = YN[i] * (np.power((L[i] + 16.)/116., 3.) if L[i] > 8. else L[i] / self.KAPPA)
    
        # Calculate X/Z
        from numpy import finfo, fmax

        # Avoiding division by zero
        eps = np.finfo(float).eps*10
        L = fmax(eps, L)

        [uN, vN] = self.XYZ_to_uv(XN, YN, ZN)
        u = U / (13. * L) + uN
        v = V / (13. * L) + vN
        X =  9.0 * Y * u / (4 * v)
        Z =  -X / 3. - 5. * Y + 3. * Y / v
    
        return [X, Y, Z]
    
    
    ## ----- LUV <-> polarLUV ----- */
    def LUV_to_polarLUV(self, L, U, V):
        """LUV_to_polarLUV(L, U, V)
        
        LUV to polarLUV (HCL).

        Parameters
        ----------
        L : numpy.ndarray
            values for the X dimension
        U : numpy.ndarray
            values for the Y dimension
        V : numpy.ndarray
            values for the Z dimension

        Returns
        -------
        list
            Returns a list of polarLUV or HCL coordinates (``[L, C, H]``) with the
            same length as the input arrays. The HCL color space is simply the
            polar representation of the CIE-LUV color space.
        """

        __fname__ = inspect.stack()[0][3] # Name of this method
    
        self._check_input_arrays_(__fname__, L = L, U = U, V = V)
    
        # Calculate polarLUV coordinates
        C = np.sqrt(U * U + V * V)
        H = self.RAD2DEG(np.arctan2(V, U))
        for i,val in np.ndenumerate(H):
            while val > 360: val -= 360.
            while val < 0.:  val += 360.
            H[i] = val
    
        return [L, C, H]
    
    def polarLUV_to_LUV(self, L, C, H):
        """polarLUV_to_LUV(L, C, H)
        
        polarLUV (HCL) to LUV.

        Parameters
        ----------
        L : numpy.ndarray
            values for the L or luminance dimension
        C : numpy.ndarray
            values for the C or chroma dimension
        H : numpy.ndarray
            values for the H or hue dimension

        Returns
        -------
        list
            Returns a list of polarLUV or HCL coordinates (``[L, U, V]``) with the
            same length as the input arrays.
        """
    
        __fname__ = inspect.stack()[0][3] # Name of this method
    
        # Checking input
        self._check_input_arrays_(__fname__, L = L, C = C, H = H)
    
        H = self.DEG2RAD(H)
        return [L, C * np.cos(H), C * np.sin(H)] # [L, U, V]
    
    
    def sRGB_to_hex(self, r, g, b, fixup = True):
        """sRGB_to_hex(r, g, , fixup = True)

        sRGB colors to hex colors.

        Parameters
        ----------
        r : numpy.ndarray
            intensities for red (``[0.,1.,]``)
        g : numpy.ndarray
            intensities for green (``[0.,1.,]``)
        b : numpy.ndarray
            intensities for blue (``[0.,1.,]``)
        fixup : bool
            whether or not the rgb values should be corrected if
            they lie outside the defined RGB space (outside ``[0.,1.,]``)

        Returns
        -------
        list
            A list with hex colors as strings.
        """

        # Color fixup: limit r/g/b to [0-1]
        def rgbfixup(r, g, b):
            def fun(x):
                return np.asarray([np.max([0, np.min([1, e])]) \
                       if np.isfinite(e) else np.nan for e in x])
            return [fun(r), fun(g), fun(b)]

        def rgbcleanup(r, g, b):
            def fun(x):
                return np.asarray([e if np.logical_and(e >= 0., e <= 1.)
                       else np.nan for e in x])
            return [fun(r), fun(g), fun(b)]

        # Checking which r/g/b values are outside limits.
        # This only happens if fixup = FALSE.
        def validrgb(r, g, b):
            idxr = np.isfinite(r)
            idxg = np.isfinite(g)
            idxb = np.isfinite(b)
            return np.where(idxr * idxg * idxb)[0]

        # Support function to create hex coded colors
        def gethex(r, g, b):

            # Converts integers to hex string
            def applyfun(x):
                x = np.asarray(x * 255. + .5, dtype = np.int)
                return "#{:02x}{:02x}{:02x}".format(x[0], x[1], x[2]).upper()

            h = np.vstack([r,g,b]).transpose().flatten().reshape([len(r),3])
            return np.apply_along_axis(applyfun, 1, h)

        # Let's do the conversion!
        if fixup: [r, g, b] = rgbfixup(r, g, b)
        else:     [r, g, b] = rgbcleanup(r, g, b)

        # Create return array
        res = np.ndarray(len(r), dtype = "|S7"); res[:] = ""

        # Check valid r/g/b coordinates
        valid = validrgb(r,g,b)
        if len(valid) > 0:
            # Convert valid colors to hex
            res[valid] = gethex(r[valid], g[valid], b[valid])

        # Create return list with NAN's for invalid colors
        ans = [np.nan if len(x) == 0 else x for x in res]

        return ans;

    # RETO RETO RETO
    def hex_to_sRGB(self, hex_, gamma = 2.4):
        """hex_to_sRGB(hex_, gamma = 2.4)

        Convert hex colors to sRGB.

        Parameters
        ----------
        hex_ : str, list of str
            hex strings.
        gamma : float
            gamma correction factor.

        Returns
        -------
        list
            Returns a list of numpy.ndarrays with the corresponding
            red, green, and blue intensities (``[0.,1.]``).
        """

        if isinstance(hex_,str): hex_ = [hex_]
        hex_ = np.asarray(hex_)

        # Check for valid hex colors
        def validhex(hex_):
            from re import match
            ##return np.where([match("^#[A-Za-z0-9]{6}([0-9]{2})?$", x) is not None for x in hex_])[0]
            return np.where([match("^#[0-9A-Fa-f]{6}(o-9]{2})?$$", x) is not None for x in hex_])[0]

        # Convert hex to rgb
        def getrgb(x):
            def applyfun(x):
                return np.asarray([int(x[i:i+2], 16) for i in (1, 3 ,5)])
            rgb = [applyfun(e) for e in x]
            rgb = np.vstack(rgb).transpose().flatten().reshape([3,len(x)])
            return [rgb[0] / 255., rgb[1] / 255., rgb[2] / 255.]

        # Result arrays
        r = np.ndarray(len(hex_), dtype = "float"); r[:] = np.nan 
        g = np.ndarray(len(hex_), dtype = "float"); g[:] = np.nan 
        b = np.ndarray(len(hex_), dtype = "float"); b[:] = np.nan 

        # Check valid hex colors
        valid = validhex(hex_)
        if not len(valid) == 0:

            # Decode valid hex strings
            rgb = getrgb(hex_[valid])
            r[valid] = rgb[0]
            g[valid] = rgb[1]
            b[valid] = rgb[2]

        return [r, g, b]


# -------------------------------------------------------------------
# Color object base class
# will be extended by the different color classes.
# -------------------------------------------------------------------
class colorobject(object):
    """
    This is the base class of all color objects and provides some
    default methods.
    """

    # Allowed/defined color spaces
    ALLOWED = ["CIEXYZ", "CIELUV", "CIELAB", "polarLUV", "polarLAB",
               "RGB", "sRGB", "HCL",
               "HSV", "HLS", "hex"]

    # Used to store alpha if needed. Will only be used for some of
    # the colorobject objects as only few color spaces allow alpha
    # values.
    ALPHA = None

    # GAMMA
    GAMMA = 2.4 # Used to adjust RGB (DEVRGB_to_RGB and back).

    # Standard representation of colorspace colorobject objects.
    def __repr__(self, digits = 2):
        """__repr__(digits = 2)

        Standard representation of the :py:class:`colorobject` objects.

        Returns
        -------
        str
            Returns a string of the colors/coordinates of the current
            object.
        """
        dims = self._data_.keys()     # Dimensions

        # Sorting the dimensions
        from re import match
        if   match("^(R|G|B|alpha){3,4}$", "".join(dims)): dims = ["R", "G", "B"]
        elif match("^(L|A|B|alpha){3,4}$", "".join(dims)): dims = ["L", "A", "B"]
        elif match("^(L|U|V|alpha){3,4}$", "".join(dims)): dims = ["L", "U", "V"]
        elif match("^(H|C|L|alpha){3,4}$", "".join(dims)): dims = ["H", "C", "L"]
        elif match("^(X|Y|Z|alpha){3,4}$", "".join(dims)): dims = ["X", "Y", "Z"]
        elif match("^(H|S|V|alpha){3,4}$", "".join(dims)): dims = ["H", "S", "V"]
        elif match("^(H|L|S|alpha){3,4}$", "".join(dims)): dims = ["H", "L", "S"]
        if self.hasalpha(): dims.append("alpha")

        # Number of colors
        ncol = len(self._data_[dims[0]])

        # Start creating the string:
        res = ["{:s} color object ({:d} colors)".format(self.__class__.__name__, ncol)]

        # Show header
        fmt = "".join(["{:>", "{:d}".format(digits+6), "s}"])
        res.append("    " + "".join([fmt.format(x) for x in dims]))

        # Show data
        # In case of a hexcols object: string formatting and
        # nan-replacement beforehand.
        if self.__class__.__name__ == "hexcols":
            data = {}
            fmt = "".join(["{:", "{:d}.{:d}".format(6+digits, 3), "f}"])
            for d in self._data_.keys():
                data[d] = np.ndarray(ncol, dtype = "|S7")
                for n in range(0, ncol):
                    x = self._data_[d][n]
                    if isinstance(x, float):
                        data[d][n] = fmt.format(x)
                    else:
                        data[d][n] = x[0:7]
            fmt = "{:>8s}"
        else:
            fmt = "".join(["{:", "{:d}.{:d}".format(6+digits, digits), "f}"])
            data = self._data_

        # Print object content
        count = 0
        for n in range(0, ncol):
            if (n % 10) == 0: 
                tmp = "{:3d}:".format(n+1)
            else:
                tmp = "    "
            for d in dims:
                tmp += fmt.format(data[d][n])
            count += 1
            res.append(tmp)

            if count >= 30 and ncol > 40:
                res.append("".join([" ......"]*len(dims)))
                res.append("And {:d} more [truncated]".format(ncol - count))
                break

        return "\n".join(res)

    def __call__(self, fixup = True, rev = False):
        """object(fixup = True, rev = False)

        Default call of :py:class:`colorlib.colorobj` return hex colors,
        same as ``.colors()`` does.

        Returns
        -------
        list
            Returns a list of hex colors.
        """
        return self.colors(fixup = fixup, rev = rev)

    def get_whitepoint(self):
        """get_whitepoint()

        A white point definition is used to adjust the colors.
        If not explicitly set via :py:func:`set_whitepoint`
        default values are used. This method returns the definition of the
        white point in use.

        Returns
        -------
        dict
            Returns a dict with `X`, `Y`, `Z`, the white point specification
            for the three dimensions.

        Examples
        --------
        >>> from colorspace.colorlib import hexcols
        >>> c = hexcols("#ff0000")
        >>> c.get_whitepoint()
        """
        return {"X": self.WHITEX, "Y": self.WHITEY, "Z": self.WHITEZ}

    def set_whitepoint(self, **kwargs):
        """set_whitepoint(**kwargs)

        A white point definition is used to adjust the colors.
        This method allows to set custom values. If not explicitly
        set a default specification is used.

        No return, stores the new definition on the object.
        :py:func:`get_whitepoint` can be used to get the current specification.

        Parameters
        ----------
        X : float
            white specification for dimension X
        Y : float
            white specification for dimension Y
        Z : float
            white specification for dimension Z

        Examples
        --------
        >>> from colorspace.colorlib import hexcols
        >>> c = hexcols("#ff0000")
        >>> c.set_whitepoint(X = 100., Y = 100., Z = 101.)
        >>> c.get_whitepoint()
        """
        for key,arg in kwargs.items():
            if   key == "X":  self.WHITEX = float(arg)
            elif key == "Y":  self.WHITEY = float(arg)
            elif key == "Z":  self.WHITEZ = float(arg)
            else: 
                raise ValueError("error in {:s}.set_whitepoint: ".format(self.__class__name__) + \
                        "argument \"{:s}\" not recognized.".format(key))


    def _check_if_allowed_(self, x):
        """_check_if_allowed_(x)

        Helper function to check if the transformation of the current
        object to ``x`` is allowed or not.
        raises a ValueError if the conversion is not possible.

        No return, raises an Exception if the the transformation is
        not possible. Should never happen except that the colorobject
        is not well defined.

        Parameters
        ----------
        x : str
            name of the target color space
        """
        if not x in self.ALLOWED:
            raise Exception("transformation from {:s}".format(self.__class__.__name__) + \
                    " to \"{:s}\" is unknown (not implemented).".format(x) + \
                    "The following are allowed: {:s}".format(", ".join(self.ALLOWED)))
        return


    def _transform_via_path_(self, via, fixup):
        """_transform_via_path_(via, fixup)

        Helper function to transform a colorobject into a new color
        space. Calls the .to method one or several times along 'a path'
        as specified by ``via``.

        No return, converts the current color space object (see method
        :py:func:`to`.

        Parameters
        ----------
        via : list of strings
            the path via which the current color object should be transformed.
            an example: a :py:class:`hexcols` object can be transformed into
            CIEXYZ by specifying ``via = ["sRGB", "RGB", "CIEXYZ"]``
        fixup : bool
            whether or not to correct invalid rgb values outside ``[0.,1.]`` if
            necessary
        """
        for v in via:   self.to(v, fixup = fixup)

    def _colorobject_check_input_arrays_(self, **kwargs):
        """_colorobject_check_input_arrays_(**kwargs)
        
        Checks if all inputs in **kwargs are of type np.ndarray OR lists
        (will be converted to ndarrays) and that all are of the same length
        If not, the script will drop some error messsages and stop.
        If ``alpha`` is given it is handled in a special way. If ``None``
        it will simply be dropped (no alpha channel specified), else it is
        handled like the rest and  has to fulfill the requirements (length, type).

        Parameters
        ----------
        kwargs : ...
            named keywords, objects to be checked

        Returns
        -------
        bool
            Returns ``True`` if all checks where fine, raises a ValueError
            if the inputs do not fulfil the requirements.
        """

        # Message will be dropped if problems occur
        msg = "Problem while checking inputs \"{:s}\" to class \"{:s}\":".format(
                ", ".join(kwargs.keys()), self.__class__.__name__)


        res = {}
        lengths = []
        for key,val in kwargs.items():
            # No alpha provided, simply proceed
            if key == "alpha" and val is None: continue
            # If is list: convert to ndarray no matter how long the element is
            if isinstance(val,float) or isinstance(val,int):
                val = np.asarray([val])
            elif isinstance(val,list):
                val = np.asarray(val)

            # For alpha, R, G, and B: check range
            if isinstance(self, RGB) or isinstance(self, sRGB):
                if np.max(val) > 1. or np.max(val) < 0.:
                    raise ValueError("wrong values specified for " + \
                            "dimension {:s} in {:s}: ".format(key, self.__class__.__name__) + \
                            "values have to lie within [0.,1.]")

            # Check object type
            from numpy import asarray
            try:
                val = asarray(val)
            except Exception as e:
                raise ValueError("input {:s} to {:s}".format(key, self.__class__.__name__) + \
                        " could not have been converted to numpy.ndarray: {:s}".format(e))

            # Else append length and proceed
            lengths.append(len(val))
            # Append to result vector
            res[key] = val

        # Check if all do have the same length
        if not np.all([x == lengths[0] for x in lengths]):
            msg += "Arguments of different lengths: {:s}".format(
                   ", ".join(["{:s} = {:d}".format(kwargs.keys()[i],lengths[i]) \
                    for i in range(0,len(kwargs))]))
            raise ValueError(msg)

        return res

    def hasalpha(self):
        """hasalpha()

        Small helper function to check whether the current color object
        has alpha values or not.

        Returns
        -------
        bool
            Returns ``True`` if alpha values are present, ``False`` if not.
        """
        if not "alpha" in self._data_.keys():
            return False
        elif self._data_["alpha"] is None:
            return False
        else:
            return True


    def dropalpha(self):
        """dropalpha()

        Remove alpha information from the color object, if defined.
        """
        if self.hasalpha():
            del self._data_["alpha"]

        return


    def specplot(self, **kwargs):
        """specplot(**kwargs)

        Plotting a specplot (see :py:func:`specplot.specplot`) of
        the current color object. Additional arguments can be used
        to control the specplot.

        Parameters
        ----------
        kwargs : ...
            named list of additional arguments forwarded to the
            specplot function

        Examples
        --------
        >>> from colorspace.colorlib import HCL
        >>> cols = HCL([260, 80, 30], [80, 0, 80], [30, 90, 30])
        >>> cols.specplot()
        >>> cols.specplot(rgb = False)
        """
        from copy import copy
        cols = copy(self)
        cols.to("hex")

        if isinstance(cols, colorobject):
            from specplot import specplot
            specplot(cols.colors(), **kwargs)


    def colors(self, fixup = True, rev = False):
        """colors(fixup = True)
        
        Returns hex colors of the current :py:class:`colorobject`.
        Converts the colors into a :py:class:`hexcols` object
        to retrieve hex colors which are returned as list.

        If the object contains alpha values the alpha level
        is added to the hex string if and only if alpha is
        not equal to 1.0.

        Parameters
        ----------
        fixup : bool
            whether or not to correct rgb values outside the
            defined range of ``[0., 1.]``
        rev : bool
            return colors in reversed order?

        Returns
        -------
        list
            Returns a list of hex colors.

        Examples
        --------
        >>> from colorspace.colorlib import HCL
        >>> cols = HCL([0, 40, 80], [30, 60, 80], [85, 60, 35])
        >>> cols.colors()
        """

        from copy import copy
        x = copy(self)
        x.to("hex", fixup = fixup)
        if x.hasalpha():
            res = x.get("hex_")
            # Appending alpha if alpha < 1.0
            for i in range(0, len(res)):
                if self._data_["alpha"][i] < 1.0:
                    res[i] += "{:02d}".format(int(self._data_["alpha"][i] * 100.))
            # Return hex with alpha
            colors = res
        else:
            colors = x.get("hex_")

        if rev: colors.reverse()
        return colors


    def get(self, dimname = None):
        """get(dimname = None)

        Returns the current color coordinates. Either a single coordinate
        (if ``dimname`` is set) or all coordinates of the current
        :py:class:`colorobject`. The latter will return a dictionary containing
        the data with all defined dimensions.

        Parameters
        ----------
        dimname : None, st
            can be set to only retrieve one very specific coordinate.

        Returns
        -------
        dict or numpy.ndarray
            Either a dictionary or a single numpy.ndarray if input ``dimname``
            was not specified. If a specific dimension is requested bu the
            dimension does not exist a ValueError is raised.

        Examples
        --------
        >>> from colorspace.colorlib import HCL
        >>> cols = HCL([260, 80, 30], [80, 0, 80], [30, 90, 30])
        >>> cols.get()
        >>> cols.get("H")
        """

        # Return all coordinates
        from copy import copy
        if dimname is None:
            return copy(self._data_)
        # No string?
        elif not isinstance(dimname, str):
            raise ValueError("input dimname to {:s} ".format(self.__class__.__name__) + \
                    "has to be None or a string.")
        # Else only the requested dimension
        elif not dimname in self._data_.keys():
            # Alpha channel never defined, return None (which
            # is a valid value for "no alpha")
            if dimname == "alpha":
                return None
            else:
                raise ValueError("{:s} has no dimension {:s}".format(self.__class__.__name__, dimname))
        return copy(self._data_[dimname])

    def set(self, **kwargs):
        """set(kwargs)

        Allows to manipulate the current colors. The named input arguments
        have to fulfil a specific set or requirements. If not, the function
        raises a ValueError.

        The dimension has to exist, and the new data have to be of the same
        type and of the same length to be accepted.

        No return, modifies the current object.

        Parameters
        ----------
        kwargs : ...
            named arguments. The key is the name of the dimension to be changed,
            the value an object which fulfills the requirements (see description
            of this method)

        Examples
        --------
        >>> from colorspace.colorlib import HCL
        >>> cols = HCL([260, 80, 30], [80, 0, 80], [30, 90, 30])
        >>> print cols
        >>> cols.set(H = [150, 150, 30])
        >>> print cols
        """
        # Looping over inputs
        for key,vals in kwargs.items():
            key.upper()
            # Return all coordinates
            if not key in self._data_.keys():
                raise ValueError("{:s} has no dimension {:s}".format(self.__class__.__name__, key))

            # New values do have to have the same length as the old ones,
            n = len(self.get(key))
            t = type(self.get(key)[0])
            from numpy import asarray
            try:
                vals = asarray(vals, dtype = t)
            except Exception as e:
                raise ValueError("problems converting new data to {:s} ".format(t) + \
                    " in {:s}: {:s}".format(self.__class__.__name__, e))
            if not len(vals) == n:
                raise ValueError("number of values to be stored on the object " + \
                    "{:s} have to match the current dimension".format(self.__class__.__name__))
            self._data_[key] = vals


    def _cannot(self, from_, to):
        """_cannot(from_, to)

        Helper function, raises an exception if a transformation is
        not possible by definition.

        Parameters
        ----------
        from_ : str
            name of the current color space
        to : str
            name of the target color space
        """
        raise Exception("Cannot convert class \"{:s}\" to \"{:s}\".".format(
            from_, to))
        return

    def _ambiguous(self, from_, to):
        """_ambiguous(from_, to)

        Helper function, raises an exception if a transformation is
        ambiguous by definition and thus, not possible.

        Parameters
        ----------
        from_ : str
            name of the current color space.
        to : str
            name of the target color space.
        """
        raise Exception("Ambiguous conversion from " + \
                "\"{:s}\" to \"{:s}\" (object unchanged).".format(from_, to))


# -------------------------------------------------------------------
# PolarLUV or HCL object
# -------------------------------------------------------------------
class polarLUV(colorobject):
    """polarLUV(H, C, L, alpha = None)
    
    polarLUV or HCL color object. The polar representation of the CIELUV
    (:class:`colorspace.CIELUV`) color space is also known as
    Hue-Chroma-Luminance (HCL) color space.  polarLUV colors can be converted
    into: CIEXYZ , CIELUV , CIELAB , RGB , sRGB , polarLAB , hex.  Not allowed
    (ambiguous) to convert into: HSV, HLS.

    Parameters
    ----------
    L : numeric
        single value or vector for hue dimension ``[-360.,360.]``
    U : numeric
        single value or vector for chroma dimension ``[0., 100.+]``
    V : numeric
        single value or vector for luminance dimension ``[0., 100.]``
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added
        

    Examples
    --------
    >>> from colorspace.colorlib import polarLUV, HCL
    >>> c = polarLUV(100., 30, 50.)
    >>> c = HCL(100., 30, 50.) # Equivalent to the command above
    >>> c = HCL([100.], [30.], [50.])
    >>> c = HCL([100, 80], [30,50], [30,80])
    >>> from numpy import asarray
    >>> c = HCL(asarray([100,80]), asarray([30,50]), asarray([30,80]))

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, H, C, L, alpha = None):

        # Checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(H = H, C = C, L = L, alpha = alpha)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)

    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to in ["HCL", self.__class__.__name__]:
            return

        # This is the only transformation from polarLUV -> LUV
        elif to == "CIELUV":
            [L, U, V] = clib.polarLUV_to_LUV(self.get("L"), self.get("C"), self.get("H"))
            self._data_ = {"L" : L, "U" : U, "V" : V, "alpha" : self.get("alpha")}
            self.__class__ = CIELUV

        # The rest are transformations along a path
        elif to == "CIEXYZ":
            via = ["CIELUV", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "CIELAB":
            via = ["CIELUV", "CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "RGB":
            via = ["CIELUV", "CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "sRGB":
            via = ["CIELUV", "CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "polarLAB":
            via = ["CIELUV", "CIEXYZ", "CIELAB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "hex":
            via = ["CIELUV", "CIEXYZ", "sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HLS", "HSV"]:
            self._ambiguous(self.__class__.__name__, to)

        else: self._cannot(self.__class__.__name__, to)

# polarLUV is HCL, make copy
HCL = polarLUV


# -------------------------------------------------------------------
# CIELUV color object
# -------------------------------------------------------------------
class CIELUV(colorobject):
    """CIELUV(L, U, V, alpha = None)
    
    CIELUV color object.

    polarLUV colors can be converted into: CIEXYZ, CIELUV, CIELAB, RGB, sRGB,
    polarLAB, hex. Not allowed (ambiguous) to convert into: HSV, HLS.

    Parameters
    ----------
    L : numeric
        single value or multiple values for L-dimension
    U : numeric
        single value or multiple values for U-dimension
    V : numeric
        single value or multiple values for V-dimension
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added

    Examples
    --------
    >>> from colorspace.colorlib import CIELUV
    >>> c = CIELUV(0, 10, 10)
    >>> c = CIELUV([10, 30], [20, 80], [100, 40])
    >>> from numpy import asarray
    >>> c = CIELUV(asarray([10, 30]), asarray([20, 80]), asarray([100, 40]))

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """
    def __init__(self, L, U, V, alpha = None):

        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(L = L, U = U, V = V, alpha = alpha)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to == self.__class__.__name__:
            return
        # Transformation from CIELUV -> CIEXYZ
        elif to == "CIEXYZ":
            [X, Y, Z] = clib.LUV_to_XYZ(self.get("L"), self.get("U"), self.get("V"),
                                        self.WHITEX, self.WHITEY, self.WHITEZ)
            self._data_ = {"X" : X, "Y" : Y, "Z" : Z, "alpha" : self.get("alpha")}
            self.__class__ = CIEXYZ

        # Transformation from CIELUV -> polarLUV (HCL)
        elif to in ["HCL","polarLUV"]:
            [L, C, H] = clib.LUV_to_polarLUV(self.get("L"), self.get("U"), self.get("V"))
            self._data_ = {"L" : L, "C" : C, "H" : H, "alpha" : self.get("alpha")}
            self.__class__ = polarLUV

        # The rest are transformations along a path
        elif to == "CIELAB":
            via = ["CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "RGB":
            via = ["CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "sRGB":
            via = ["CIEXYZ", "RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "polarLAB":
            via = ["CIEXYZ", "CIELAB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "hex":
            via = ["CIEXYZ", "RGB", "sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HLS", "HSV"]:
            self._ambiguous(self.__class__.__name__, to)

        else: self._cannot(self.__class__.__name__, to)

# -------------------------------------------------------------------
# CIEXYZ color object
# -------------------------------------------------------------------
class CIEXYZ(colorobject):
    """CIEXYZ(X, Y, Z, alpha = None)
    
    CIEXYZ color object.

    Allowes conversions to: :py:class:`CIEXYZ`, :py:class:`CIELUV`,
    :py:class:`CIELAB`, :py:class:`RGB`, :py:class:`polarLUV`,
    :py:class:`polarLAB`, :py:class:`hexcols`.  Not possible are conversions to
    (ambiguous): :py:class:`HSV`, :py:class:`HLS`.

    Parameters
    ----------
    X : numeric
        single value or multiple values for X-dimension
    Y : numeric
        single value or multiple values for Y-dimension
    Z : numeric
        single value or multiple values for Z-dimension
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added

    Examples
    --------
    >>> from colorspace.colorlib import CIEXYZ
    >>> c = CIEXYZ(80, 30, 10)
    >>> c = CIEXYZ([10, 0], [20, 80], [40, 40])
    >>> from numpy import asarray
    >>> c = CIEXYZ(asarray([10, 0]), asarray([20, 80]), asarray([40, 40]))

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, X, Y, Z, alpha = None):

        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(X = X, Y = Y, Z = Z, alpha = alpha)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to == self.__class__.__name__:
            return

        # Transformation from CIEXYZ -> CIELUV
        elif to == "CIELUV":
            [L, U, V] = clib.XYZ_to_LUV(self.get("X"), self.get("Y"), self.get("Z"),
                                        self.WHITEX, self.WHITEY, self.WHITEZ) 
            self._data_ = {"L" : L, "U" : U, "V" : V, "alpha" : self.get("alpha")}
            self.__class__ = CIELUV

        # Transformation from CIEXYZ -> CIELAB
        elif to == "CIELAB":
            [L, A, B] = clib.XYZ_to_LAB(self.get("X"), self.get("Y"), self.get("Z"),
                                        self.WHITEX, self.WHITEY, self.WHITEZ) 
            self._data_ = {"L" : L, "A" : A, "B" : B, "alpha" : self.get("alpha")}
            self.__class__ = CIELAB

        # Transformation from CIEXYZ -> RGB
        elif to == "RGB":
            [R, G, B] = clib.XYZ_to_RGB(self.get("X"), self.get("Y"), self.get("Z"),
                                        self.WHITEX, self.WHITEY, self.WHITEZ) 
            self._data_ = {"R" : R, "G" : G, "B" : B, "alpha" : self.get("alpha")}
            self.__class__ = RGB

        # The rest are transformations along a path
        elif to == "polarLAB":
            via = ["CIELAB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HCL", "polarLUV"]:
            via = ["CIELUV", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "sRGB":
            via = ["RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "hex":
            via = ["RGB", "sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HLS", "HSV"]:
            self._ambiguous(self.__class__.__name__, to)

        else: self._cannot(self.__class__.__name__, to)


class RGB(colorobject):
    """RGB(R, G, B, alpha = None)

    Device independent RGB color object.

    Allowes conversions to: :py:class:`CIEXYZ`, :py:class:`CIELUV`,
    :py:class:`CIELAB`, :py:class:`sRGB`, :py:class:`HSV`, :py:class:`HLS`,
    :py:class:`polarLUV`, :py:class:`polarLAB`, `"hex"` (:py:class:`hexcols`).
    Allows additional alpha input. Note that the alpha channel will not be
    modified but preserved.

    Parameters
    ----------
    R : numeric
        intensity of red ``[0.,1.]``
    G : numeric
        intensity of green ``[0.,1.]``
    B : numeric
        intensity of blue ``[0.,1.]``
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added

    Examples
    --------
    >>> from colorspace.colorlib import sRGB
    >>> c = sRGB(1., 0.3, 0.5)
    >>> c = sRGB([1.,0.8], [0.5,0.5], [0.0,0.2])
    >>> 
    >>> from numpy import asarray
    >>> c = sRGB(asarray([1.,0.8]), asarray([0.5,0.5]), asarray([0.0,0.2]))

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, R, G, B, alpha = None):

        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions

        tmp = self._colorobject_check_input_arrays_(R = R, G = G, B = B, alpha = alpha)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary.
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to == self.__class__.__name__:
            return

        # Transform from RGB -> HLS
        elif to == "HLS":
            [H, L, S] = clib.RGB_to_HLS(self.get("R"), self.get("G"), self.get("B"))
            self._data_ = {"H" : H, "L" : L, "S" : S, "alpha" : self.get("alpha")}
            self.__class__ = HLS

        # Transform from RGB -> HSV
        elif to == "HSV":
            [H, S, V] = clib.RGB_to_HSV(self.get("R"), self.get("G"), self.get("B"))
            self._data_ = {"H" : H, "S" : S, "V" : V, "alpha" : self.get("alpha")}
            self.__class__ = HSV

        # Transform from RGB -> sRGB
        elif to == "sRGB":
            [R, G, B] = clib.RGB_to_DEVRGB(self.get("R"), self.get("G"), self.get("B"),
                                           self.GAMMA)
            self._data_ = {"R" : R, "G" : G, "B" : B, "alpha" : self.get("alpha")}
            self.__class__ = sRGB

        # Transform from RGB -> CIEXYZ
        elif to == "CIEXYZ":
            [X, Y, Z] = clib.RGB_to_XYZ(self.get("R"), self.get("G"), self.get("B"),
                                        self.WHITEX, self.WHITEY, self.WHITEZ)
            self._data_ = {"X" : X, "Y" : Y, "Z" : Z, "alpha" : self.get("alpha")}
            self.__class__ = CIEXYZ

        # The rest are transformations along a path
        elif to in ["CIELUV", "CIELAB"]: 
            via = ["CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HCL","polarLUV"]:
            via = ["CIEXYZ", "CIELUV", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "polarLAB":
            via = ["CIEXYZ", "CIELAB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "hex":
            via = ["sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        else: self._cannot(self.__class__.__name__, to)


class sRGB(colorobject):
    """sRGB(R, G, B, alpha = None, gamma = None)
    
    sRGB (device dependent RGB) color object.

    Allowes conversions to: :py:class:`CIEXYZ`, :py:class:`CIELUV`,
    :py:class:`CIELAB`, :py:class:`RGB`, :py:class:`HSV`, :py:class:`HLS`,
    :py:class:`polarLUV`, :py:class:`polarLAB`, `"hex"` (:py:class:`hexcols`).
    Allows additional alpha input. Note that the alpha channel will not be
    modified but preserved.  R, G, and B have to be within ``[0., 1.]``.

    Parameters
    ----------
    R : float, list of floats, numpy.ndarray
        intensity of red ``[0.,1.]``
    G : float, list of floats, numpy.ndarray
        intensity of green ``[0.,1]``
    B : float, list of floats, numpy.ndarray
        intensity of blue ``[0.,1]``
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added
    gamma : None, float
        gamma parameter. Used to convert from device dependent sRGB
        to RGB. If not set the default of 2.4 is used

    Examples
    --------
    >>> from colorspace.colorlib import sRGB
    >>> c = sRGB(1., 0.3, 0.5)
    >>> c = sRGB([1.,0.8], [0.5,0.5], [0.0,0.2])
    >>> 
    >>> from numpy import asarray
    >>> c = sRGB(asarray([1.,0.8]), asarray([0.5,0.5]), asarray([0.0,0.2]))

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, R, G, B, alpha = None, gamma = None):

        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(R = R, G = G, B = B, alpha = alpha)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)

        if isinstance(gamma, float): self.GAMMA = gamma


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary.
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to == self.__class__.__name__:
            return

        # Transformation sRGB -> RGB
        elif to == "RGB":
            [R, G, B] = clib.DEVRGB_to_RGB(self.get("R"), self.get("G"), self.get("B"),
                                           gamma = self.GAMMA)
            self._data_ = {"R" : R, "G" : G, "B" : B, "alpha" : self.get("alpha")}
            self.__class__ = RGB

        # Transformation sRGB -> hex
        elif to == "hex":
            hex_ = clib.sRGB_to_hex(self.get("R"), self.get("G"), self.get("B"), fixup)
            self._data_ = {"hex_" : hex_, "alpha" : self.get("alpha")}
            self.__class__ = hexcols

        # The rest are transformations along a path
        elif to in ["HSV", "HLS", "CIEXYZ"]:
            via = ["RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["CIELUV", "CIELAB"]:
            via = ["RGB", "CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HCL","polarLUV"]:
            via = ["RGB", "CIEXYZ", "CIELUV", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "polarLAB":
            via = ["RGB", "CIEXYZ", "CIELAB", to] 
            self._transform_via_path_(via, fixup = fixup)

        else: self._cannot(self.__class__.__name__, to)


class CIELAB(colorobject):
    """CIELAB(L, A, B, alpha = None)
    
    CIELAB color object.

    Allowes conversions to: :py:class:`CIEXYZ`, :py:class:`CIELUV`,
    :py:class:`CIELAB`, :py:class:`RGB`, :py:class:`polarLUV`,
    :py:class:`polarLAB`, `"hex"` (:py:class:`hexcols`).  Not possible are
    conversions to (ambiguous): :py:class:`HSV`, :py:class:`HLS`.

    Parameters
    ----------
    L : numeric
        single value or multiple values for L dimension
    A : numeric
        single value or multiple values for A dimension
    B : numeric
        single value or multiple values for B dimension
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added

    Examples
    --------
    >>> from colorspace.colorlib import CIELAB
    >>> c = CIELAB(-30, 10, 10)
    >>> c = CIELAB([-30, 30], [20, 80], [40, 40])
    >>> from numpy import asarray
    >>> c = CIELAB(asarray([-30, 30]), asarray([20, 80]), asarray([40, 40]))

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, L, A, B, alpha = None):

        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(L = L, A = A, B = B, alpha = alpha)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to == self.__class__.__name__:
            return

        # Transformations CIELAB -> CIEXYZ
        elif to == "CIEXYZ":
            [X, Y, Z] = clib.LAB_to_XYZ(self.get("L"), self.get("A"), self.get("B"),
                                        self.WHITEX, self.WHITEY, self.WHITEZ)
            self._data_ = {"X" : X, "Y" : Y, "Z" : Z, "alpha" : self.get("alpha")}
            self.__class__ = CIEXYZ

        # Transformation CIELAB -> polarLAB
        elif to == "polarLAB":
            [L, A, B] = clib.LAB_to_polarLAB(self.get("L"), self.get("A"), self.get("B"))
            self._data_ = {"L" : L, "A" : A, "B" : B, "alpha" : self.get("alpha")}
            self.__class__ = polarLAB

        # The rest are transformations along a path
        elif to == "CIELUV":
            via = ["CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HCL","polarLUV"]:
            via = ["CIEXYZ", "CIELUV", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "RGB":
            via = ["CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "sRGB":
            via = ["CIEXYZ", "RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "hex":
            via = ["CIEXYZ", "RGB", "sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HLS", "HSV"]:
            self._ambiguous(self.__class__.__name__, to)

        else: self._cannot(self.__class__.__name__, to)


class polarLAB(colorobject):
    """polarLAB(L, A, B, alpha = None)
    
    polarLAB color object.

    Allowes conversions to: :py:class:`CIEXYZ`, :py:class:`CIELUV`,
    :py:class:`CIELAB`, :py:class:`RGB`, :py:class:`polarLUV`,
    :py:class:`polarLAB`, `"hex"` (:py:class:`hexcols`).  Not possible are
    conversions to (ambiguous): :py:class:`HSV`, :py:class:`HLS`.

    Parameters
    ----------
    L : numeric
        single value or multiple values for L dimension
    A : numeric
        single value or multiple values for A dimension
    B : numeric
        single value or multiple values for B dimension
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, L, A, B, alpha = None):

        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(L = L, A = A, B = B, alpha = alpha)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary.
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to == self.__class__.__name__:
            return

        # The only transformation we need is from polarLAB -> LAB
        elif to == "CIELAB":
            [L, A, B] = clib.polarLAB_to_LAB(self.get("L"), self.get("A"), self.get("B"))
            self._data_ = {"L" : L, "A" : A, "B" : B, "alpha" : self.get("alpha")}
            self.__class__ = CIELAB

        # The rest are transformationas along a path
        elif to == "CIEXYZ":
            via = ["CIELAB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "CIELUV":
            via = ["CIELAB", "CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HCL", "polarLUV"]:
            via = ["CIELAB", "CIEXYZ", "CIELUV", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "RGB":
            via = ["CIELAB", "CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "sRGB":
            via = ["CIELAB", "CIEXYZ", "RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "hex":
            via = ["CIELAB", "CIEXYZ", "RGB", "sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HLS", "HSV"]:
            self._ambiguous(self.__class__.__name__, to)

        else: self._cannot(self.__class__.__name__, to)


class HSV(colorobject):
    """HSV(H, S, V, alpha = None)
    
    HSV (Hue-Saturation-Value) color object.

    Allowes conversions to: :py:class:`RGB`, :py:class:`sRGB`, :py:class:`HLS`,
    and `"hex"` (:py:class:`hexcols`).  Not possible are conversions to
    (ambiguous): :py:class:`CIEXYZ`, :py:class:`CIELUV`, :py:class:`CIELAB`,
    :py:class:`polarLUV`, :py:class:`polarLAB`,

    Parameters
    ----------
    H : numeric
        single value or multiple values for the hue dimension
    S : numeric
        single value or multiple values for the saturation dimension
    V : numeric
        single value or multiple values for the value dimension
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added

    Examples
    --------
    >>> from colorspace.colorlib import HSV
    >>> cols = HSV([150, 150, 10], [1.5, 0, 1.5], [0.1, 0.7, 0.1])

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, H, S, V, alpha = None):

        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(H = H, S = S, V = V, alpha = alpha)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary.
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to == self.__class__.__name__:
            return

        # The only transformation we need is back to RGB
        elif to == "RGB":
            [R, G, B] = clib.HSV_to_RGB(self.get("H"), self.get("S"), self.get("V"))
            self._data_ = {"R" : R, "G" : G, "B" : B, "alpha" : self.get("alpha")}
            self.__class__ = RGB

        # The rest are transformations along a path
        elif to == "sRGB":
            via = ["RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "hex":
            via = ["RGB", "sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "HLS":
            via = ["RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["CIEXYZ","CIELUV","CIELAB","polarLUV", "HCL","polarLAB"]:
            self._ambiguous(self.__class__.__name__, to)

        else: self._cannot(self.__class__.__name__, to)


class HLS(colorobject):
    """HLS(H, L, S, alpha = None)
    
    HLS (Hue-Lightness-Saturation) color space.

    Allowes conversions to: :py:class:`RGB`, :py:class:`sRGB`, :py:class:`HLS`,
    and `"hex"` (:py:class:`hexcols`).  Not possible are conversions to
    (ambiguous): :py:class:`CIEXYZ`, :py:class:`CIELUV`, :py:class:`CIELAB`,
    :py:class:`polarLUV`, :py:class:`polarLAB`,

    Parameters
    ----------
    H : numeric
        single value or multiple values for the hue dimension
    L : numeric
        single value or multiple values for the lightness dimension
    S : numeric
        single value or multiple values for the saturation dimension
    alpha : None or numeric
        single value or vector of numerics in ``[0.,1.]`` for the alpha channel
        (``0.`` means transparent, ``1.`` opaque). If ``None`` no
        transparency is added

    Examples
    --------
    >>> from colorspace.colorlib import HLS
    >>> cols = HLS([150, 0, 10], [0.1, 0.7, 0.1], [3, 0, 3])

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, H, L, S, alpha = None):

        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(H = H, L = L, S = S, alpha = None)
        for key,val in tmp.items(): self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary.
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to == self.__class__.__name__:
            return

        # The only transformation we need is back to RGB
        elif to == "RGB":
            [R, G, B] = clib.HLS_to_RGB(self.get("H"), self.get("L"), self.get("S"))
            self._data_ = {"R" : R, "G" : G, "B" : B, "alpha" : self.get("alpha")}
            self.__class__ = RGB

        # The rest are transformations along a path
        elif to == "sRGB":
            via = ["RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "hex":
            via = ["RGB", "sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to == "HSV":
            via = ["RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["CIEXYZ","CIELUV","CIELAB","polarLUV","HCL","polarLAB"]:
            self._ambiguous(self.__class__.__name__, to)

        else: self._cannot(self.__class__.__name__, to)


class hexcols(colorobject):
    """hexcols(hex_)
    
    Color object for hex colors.

    Takes up a set of hex colors. Can be converted to all other color spaces
    including :py:class:`RGB`, :py:class:`sRGB`, :py:class:`HLS`, and `"hex"`
    (:py:class:`hexcols`), :py:class:`CIEXYZ`, :py:class:`CIELUV`,
    :py:class:`CIELAB`, :py:class:`polarLUV`, :py:class:`polarLAB`,

    Parameters
    ----------
    hex_ : str, list of str, or numpy.ndarray of type str
        hex colors. Only six and eight digit hex colors are allowed (e.g.,
        ``#000000`` or ``#00000050`` if with alpha value). If invalid hex
        colors are provided the object will raise a ValueError.  Input can be a
        single string, a list of strings, or a `numpy.ndarray` containing a set
        of hex colors. Invalid hex colors will be handled as `numpy.nan`, alpha
        values can be provided but will be ignored

    Examples
    --------
    >>> from colorspace.colorlib import hexcols
    >>> c = hexcols("#cecece")
    >>> c = hexcols(["#ff0000", "#00ff00"])
    >>> from numpy import asarray
    >>> c = hexcols(asarray(["#ff000030", "#00ff0030"], dtype = "|S9"))
    >>> #Convert hex colors to another color space (CIEXYZ for example):
    >>> c.to("CIEXYZ")

    .. seealso::
        This object extens the :py:class:`colorlib.colorobject` which
        provides some methods to e.g., extract color or to modify the
        whitepoint.
    """

    def __init__(self, hex_):

        if isinstance(hex_,str): hex_ = np.asarray([hex_])
        # checking inputs, save inputs on object
        self._data_ = {} # Dict to store the colors/color dimensions
        tmp = self._colorobject_check_input_arrays_(hex_ = hex_)

        # Checking for valid hex colors and alpha values
        tmp = self._check_hex_(tmp["hex_"])
        for key,val in tmp.items():
            self._data_[key] = val
        # White spot definition (the default)
        self.set_whitepoint(X = 95.047, Y = 100.000, Z = 108.883)


    def _check_hex_(self, hex_):
        """_check_hex_(hex_)

        Checking hex colors for validity. Only 6 and 8 digit
        hex colors with or without alpha (e.g., "#000000", "#00000050")
        are allowed. The method raises a ValueError if invalid hex colors
        are found.

        Parameters
        ----------
        hex_ : list of strings
            a list of (hopefully) valid hex colors

        Returns
        -------
        dict
            Returns a dict with two elements named hex_ and alpha. The hex_
            element contains valid six-digit hex strings, the alpha element
            a list of the same length with alpha values. For all hex colors
            with no alpha an alpha value of ``1.0`` is set.
        """

        from re import compile, match

        r = compile("^(nan|#[0-9A-Fa-f]{6}([0-9]{2})?)$")
        check = filter(r.match, hex_)
        if not len(check) == len(hex_):
            raise ValueError("invalid hex colors provided while " + \
                    "initializing class {:s}".format(self.__class__.__name__))

        r = compile("^#[0-9A-Fa-f]{6}([0-9]{2})$")
        check = [1 if match(r, x) else 0 for x in hex_]
        # No colors with alpha
        if sum(check) == 0:
            return {"hex_": hex_}
        # Else extracting alpha colors
        else:
            alpha = []
            for h in hex_:
                m = match(r, h)
                if not m:
                    alpha.append(1.)
                else:
                    alpha.append(int(m.group(1)) / 100.)
            return {"hex_": hex_, "alpha": alpha}


    def to(self, to, fixup = True):
        """to(to, fixup = True)

        Transforms the colors into a new color space, if possible.

        No return, converts the object into a new color space and modifies
        the underlying object. After calling this method the original
        object will be of a different type.

        Parameters
        ----------
        to : str
            name of the color space into which the colors should be
            converted (e.g., ``CIEXYZ``, ``HCL``, ``hex``, ``RGB``, ...)
        fixup : bool
            whether or not colors outside the defined rgb color space
            should be corrected if necessary
        """
        self._check_if_allowed_(to)
        from . import colorlib
        clib = colorlib()

        # Nothing to do (converted to itself)
        if to in ["hex", self.__class__.__name__]:
            return

        # The only transformation we need is from hexcols -> sRGB
        elif to == "sRGB":
            [R, G, B] = clib.hex_to_sRGB(self.get("hex_"))
            self._data_ = {"R": R, "G": G, "B": B}
            self.__class__ = sRGB

        # The rest are transformations along a path
        elif to == "RGB":
            via = ["sRGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["CIEXYZ", "HLS", "HSV"]:
            via = ["sRGB", "RGB", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["CIELUV", "CIELAB"]:
            via = ["sRGB", "RGB", "CIEXYZ", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in ["HCL", "polarLUV"]:
            via = ["sRGB", "RGB", "CIEXYZ", "CIELUV", to]
            self._transform_via_path_(via, fixup = fixup)

        elif to in "polarLAB":
            via = ["sRGB", "RGB", "CIEXYZ", "CIELAB", to]
            self._transform_via_path_(via, fixup = fixup)

        else: self._cannot(self.__class__.__name__, to)





