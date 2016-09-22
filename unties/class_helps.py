from unties import *
from scipy.optimize import fsolve
from scipy.interpolate import UnivariateSpline
import numpy as np


#__________________________________________________________________________#
################################## CRE #####################################
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
def kr(t2, kr1, t1, ea) :
    """Solve for the rate constant k at a new temperature"""
    return kr1 * np.exp(-ea/Rc * (t2**-1 - t1**-1))

def kc_t(T, Kc, T_ref, del_H_rxn):
    """Solve for Equilibrium constant Kc.

    from the Van 't Hoff equation:
    ln(k2/k1) = -H_rxn/R *(1/T2 - 1/T1)
    k2 = k1*exp(-H_rxn/R *(1/T2 - 1/T1))
    """
    tgroup = (1/T - 1/T_ref)
    expgroup = -tgroup * del_H_rxn/Rc
    return Kc * np.exp(expgroup)


#__________________________________________________________________________#
################################## Thermo ##################################
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
def sli(x,x1,x2,m1,m2):
    """Single Linear Interpolation"""
    return ((x2 - x)/(x2-x1))*m1 + ((x-x1)/(x2-x1))*m2

def dli(x,y,x1,x2,y1,y2,m11,m12,m21,m22):
    """Double Linear Interpolation"""
    first_xs = ((x2-x)/(x2-x1))
    second_xs = ((x-x1)/(x2-x1))
    first_ys = ((y2-y)/(y2-y1))
    second_ys = ((y-y1)/(y2-y1))
    m11 *= first_xs
    m12 *= second_xs
    m21 *= first_xs
    m22 *= second_xs
    return (m11 + m12)*first_ys + (m21 + m22)*second_ys


class Fluid:
    """Peng-Robinson EOS model of a fluid.

    The underscore methods are not to be used directly. They
    are used by other methods that use python solvers and
    only take and return normal numbers.

    Public methods: P_pr, V_pr

    Examples:

    >>> T = deg_c(80)
    >>> P = 1013 * kPa
    >>> omega = 0.200164
    >>> Tc = 425.12 * K
    >>> Pc = 3796 * kPa
    >>> methane = Fluid(Tc, Pc, omega)
    >>> vols = methane.V_pr(T, P)
    >>> print(vols)
    {'vapor': 0.0023131229712340944 * m**3 / mol, 'liquid': 0.00011402510635426865 * m**3 / mol}
    """
    def __init__(self, Tc, Pc, omega):
        self.Tc = Tc        # Critical Temperature
        self.Pc = Pc        # Critical Temperature
        self.omega = omega  # Acentric Factor
        self._Tc = Tc.value
        self._Pc = Pc.value

    def P_pr(self, V, T, units=Pa):
        """Find P of fluid given T and P"""
        return self._P_pr(V.value, T.value) * Pa(units)

    def V_pr(self, T, P, units=(m**3/mol)):
        """Find Vs of fluid given T and P.

        Returns both vapor and liquid volumes.
        """
        T, P = T.value, P.value
        vols = self._V_pr(T,P)
        for key in list(vols):
            vols[key] *= (m**3/mol)(units)
        return vols

    def _k(self):
        return 0.37464 + 1.54226*self.omega - 0.26992*self.omega**2

    def _a(self, T):
        const = 0.45724
        squared = (1 + self._k()*(1-(T/self._Tc)**0.5))**2
        fraction = (Rc.value*self._Tc)**2/self._Pc
        return const * squared * fraction

    def _b(self):
        return 0.0778*Rc.value*self._Tc/self._Pc

    def _P_pr(self, V, T):
        first = Rc.value * T / (V - self._b())
        second = self._a(T) / (V**2 + 2*V*self._b() - self._b()**2)
        return first - second

    def _V_pr(self, T, P):
        vapor_guess = Rc.value*T/P
        liquid_guess = 1.1 * self._b()

        def f(V):
            return P - self._P_pr(V, T)

        vapor = fsolve(f, vapor_guess)[0]
        liquid = fsolve(f, liquid_guess)[0]
        return {'vapor': vapor, 'liquid': liquid}


#__________________________________________________________________________#
################################## HMT #####################################
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
_temperatures = [ 100,  200,  300,  400,  600,  800, 1000, 1200, 1500] # Kelvin
_short_temps  =             [ 300,  400,  600,  800, 1000]             # Kelvin

_aisi_302_ks  =             [15.1, 17.3, 20.0, 22.8, 25.4]             # W/(m*K)
_aisi_304_ks  = [ 9.2, 12.6, 14.9, 16.6, 19.8, 22.6, 25.4, 28.0, 31.7] # W/(m*K)
_aisi_316_ks  =             [13.4, 15.2, 18.3, 21.3, 24.2]             # W/(m*K)
_aisi_347_ks  =             [14.2, 15.8, 18.9, 21.9, 24.7]             # W/(m*K)

def kss302(t):
    return UnivariateSpline(_short_temps, _aisi_302_ks, s=0).__call__(t)

def kss304(t):
    return UnivariateSpline(_temperatures, _aisi_304_ks, s=0).__call__(t)

def kss316(t):
    return UnivariateSpline(_short_temps, _aisi_316_ks, s=0).__call__(t)

def kss347(t):
    return UnivariateSpline(_short_temps, _aisi_347_ks, s=0).__call__(t)
