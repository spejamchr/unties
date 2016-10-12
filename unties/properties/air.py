"""Air module of DIPPR data


## Intro

To use, do:

    >>> from unties.properties import air
    >>> print(air.MW)
    28.96 * gm / mol

Or, to get the unitless value, use an underline before the property name:

    >>> print(air._MW)
    0.02896


## Constants

The constants are stored as simple numbers. Each one has a comment that
identifies its units.


## Functions

The functions are functions of temperature (in Kelvin), and each one has a range
of usability. If a function is called with a temperature outside this range, an
error will be raised.

    >>> Pv = air._ideal_gas_heat_capacity(1511)
    Exception: 1511 is out of range: [50, 1500]

All functions accept an optional argument called `ranged` that you can use to
override this safety range.

    >>> Pv = air._ideal_gas_heat_capacity(1511, ranged=False)
    1511 is out of range: [50, 1500]
    >>> print(Pv)
    34.9886888587968

Check the docstring of each function to find the units of the returned value.


## Data Lists

Available Constants:
    _MW
    _Tc
    _Pc
    _Vc
    _CompFactorCrit
    _Tmelt
    _Ttriple
    _Ptriple
    _Tboil
    _LiqMolVol
    _del_h_form_ig
    _del_g_form_ig
    _abs_entr_ig
    _std_h_form
    _std_g_form
    _std_abs_s
    _omega = _acentric_factor
    _radius_of_gyration
    _solubility_param
    _dipole_mom
    _refractive_index
    _dielectric_const

Available Temperature-Dependant Functions:
    _liquid_density
    _solid_vapor_pressure
    _vapor_pressure
    _heat_of_vaporization
    _solid_heat_capacity
    _liquid_heat_capacity
    _ideal_gas_heat_capacity
    _second_virial_coef
    _liquid_viscocity
    _vapor_viscocity
    _liquid_thermal_conductivity
    _vapor_thermal_conductivity
    _ro_one_atm
    _volume_1_atm
    _kinematic_viscocity_one_atm
    _alpha_one_atm
    _Pr_one_atm
"""

# Imports ######################################################################
from scipy.interpolate import UnivariateSpline
from math import exp, log, sinh, cosh
from unties.utilities.utilities import OutOfRangeTest, function_strings
from unties import *


# DIPPR's Constants Without Units ##############################################
_MW = 28.96 / 1000 # kg / mol
_Tc = 132.45 # K
_Pc = 3.77400E+06 # Pa
_Vc = 9.14700E-02 # m**3 / kmol
_CompFactorCrit = 0.313

_Tmelt = 59.15 # K
_Ttriple = 59.15 # K
_Ptriple = 5.64215E+03 # Pa
_Tboil = 78.67 # K
_LiqMolVol = 3.29147E-02 # m**3 / kmol

_del_h_form_ig = 0 # J / kmol
_del_g_form_ig = 0 # J / kmol
_abs_entr_ig = 1.94452E+05 # J / (kmol * K)
_std_h_form = 0 # J / kmol
_std_g_form = 0 # J / kmol

_std_abs_s = 1.94452E+05 # J / (kmol * K)
_omega = _acentric_factor = 0
_radius_of_gyration = 0 # m

_solubility_param = 1.25800E+04 # (J / m**3)**0.5
_dipole_mom = 0 # C * m
_refractive_index = 1.00102

_dielectric_const = 1.463


# DIPPR's Constants With Units #################################################
MW = (_MW * kg / mol)(gm / mol)
Tc = _Tc * K
Pc = _Pc * Pa
Vc = _Vc * m**3 / kmol
CompFactorCrit = _CompFactorCrit * (m/m)

Tmelt = _Tmelt * K
Ttriple = _Ttriple * K
Ptriple = _Ptriple * Pa
Tboil = _Tboil * K
LiqMolVol = _LiqMolVol * m**3 / kmol

del_h_form_ig = _del_h_form_ig * J / kmol
del_g_form_ig = _del_g_form_ig * J / kmol
abs_entr_ig = _abs_entr_ig * J / (kmol * K)
std_h_form = _std_h_form * J / kmol
std_g_form = _std_g_form * J / kmol

std_abs_s = _std_abs_s * J / (kmol * K)
omega = acentric_factor = _omega * (m/m)
radius_of_gyration = _radius_of_gyration * m

solubility_param = _solubility_param * (J / m**3)**0.5
dipole_mom = _dipole_mom * (m/m)
refractive_index = _refractive_index * (m/m)

dielectric_const = _dielectric_const * (m/m)


# DIPPR's Functions Without Units ##############################################
def _liquid_density(_T, ranged=True):
    """mol / m**3"""
    OutOfRangeTest(_T, 59.15, 132.45, ranged)
    A, B, C, D = 2.8963E+00, 2.6733E-01, 1.3245E+02, 2.7341E-01
    return A / (B**(1 + (1 - _T / C)**D)) * 1000

def _solid_vapor_pressure(_T, ranged=True):
    """Pa"""
    OutOfRangeTest(_T, 59.15, 59.15, ranged)
    A = 5.6420E+03
    return A

def _vapor_pressure(_T, ranged=True):
    """Pa"""
    OutOfRangeTest(_T, 59.15, 132.45, ranged)
    A, B, C, D, E = 2.1662E+01, -6.9239E+02, -3.9208E-01, 4.7574E-03, 1.0000E+00
    return exp(A + B / _T + C * log(_T) + D * _T**E)

def _heat_of_vaporization(_T, ranged=True):
    """J / mol"""
    OutOfRangeTest(_T, 59.15, 132.45, ranged)
    A, B, C, D = 7.4587E+06, 4.7571E-01, -7.1131E-01, 6.0517E-01
    Tr = _T / _Tc
    return A * (1 - Tr)**(B + C * _T + D * _T**2) / 1000

def _solid_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 1.2, 4, ranged)
    A, B, C, D, E = -6.6748E+02, 1.7834E+03, -7.6100E+02, 1.4284E+02, -1.0229E+01
    return (A + B * _T + C * _T**2 + D * _T**3 + E * _T**4) / 1000

def _liquid_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 75, 115, ranged)
    A, B, C, D = -2.1446E+05, 9.1851E+03, -1.0612E+02, 4.1616E-01
    return (A + B * _T + C * _T**2 + D * _T**3) / 1000

def _ideal_gas_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 50, 1500, ranged)
    A, B, C, D, E = 2.8958E+04, 9.3900E+03, 3.0120E+03, 7.5800E+03, 1.4840E+03
    return (A + B * (C/_T / sinh(C/_T))**2 + D * (E/_T / cosh(E/_T))**2) / 1000

def _second_virial_coef(_T, ranged=True):
    """m**3 / mol"""
    OutOfRangeTest(_T, 118.15, 248.15, ranged)
    A, B, C, D, E = 4.3045E-02, -1.7121E+01, 1.1731E+05, -3.4138E+15, 3.0380E+17
    return (A + B / _T + C / _T**3 + D / _T**8 + E / _T**9) / 1000

def _liquid_viscocity(_T, ranged=True):
    """Pa * s"""
    OutOfRangeTest(_T, 59.15, 130, ranged)
    A, B, C, D, E = -2.0077E+01, 2.8515E+02, 1.7840E+00, -6.2382E-22, 10.0
    return exp(A + B / _T + C * log(_T) + D * _T**E)

def _vapor_viscocity(_T, ranged=True):
    """Pa * s"""
    OutOfRangeTest(_T, 80, 2000, ranged)
    A, B, C = 1.4250E-06, 5.0390E-01, 1.0830E+02
    return (A * _T**B) / (1 + C / _T)

def _liquid_thermal_conductivity(_T, ranged=True):
    """W / (m * K)"""
    OutOfRangeTest(_T, 75, 125, ranged)
    A, B = 2.8472E-01, -1.7393E-03
    return A + B * _T

def _vapor_thermal_conductivity(_T, ranged=True):
    """W / (m * K)"""
    OutOfRangeTest(_T, 70, 2000, ranged)
    A, B, C, D = 3.1417E-04, 7.7860E-01, -7.1160E-01, 2.1217E+03
    return (A * _T**B) / (1 + C / _T + D / _T**2)


# Dr Knott's Functions Without Units ###########################################
def _ro_one_atm(_T, ranged=True):
    """mol / m**3"""
    OutOfRangeTest(_T, 100, 3000, ranged)
    Ts = [100, 150, 200, 250, 300,
          350, 400, 450, 500, 550,
          600, 650, 700, 750, 800,
          850, 900, 950, 1000, 1100,
          1200, 1300, 1400, 1500, 1600,
          1700, 1800, 1900, 2000, 2100,
          2200, 2300, 2400, 2500, 3000]
    ros = [3.5562, 2.3364, 1.7458, 1.3947, 1.1614,
           0.9950, 0.8711, 0.7740, 0.6964, 0.6329,
           0.5804, 0.5356, 0.4975, 0.4643, 0.4354,
           0.4097, 0.3868, 0.3666, 0.3482, 0.3166,
           0.2902, 0.2679, 0.2488, 0.2322, 0.2177,
           0.2049, 0.1935, 0.1833, 0.1741, 0.1658,
           0.1582, 0.1513, 0.1488, 0.1389, 0.1135]
    return float(UnivariateSpline(Ts, ros, s=0).__call__(_T)) / _MW


# My own Functions Without Units ###############################################
def _volume_1_atm(_T, ranged=True):
    """m**3 / mol"""
    return 1 / _ro_one_atm(_T, ranged)

def _kinematic_viscocity_one_atm(_T, ranged=True):
    """m**2 / s"""
    return _vapor_viscocity(_T, ranged) * _volume_1_atm(_T, ranged) / _MW

def _alpha_one_atm(_T, ranged=True):
    """m**2 / s"""
    return _vapor_thermal_conductivity(_T, ranged) * _volume_1_atm(_T, ranged) / _ideal_gas_heat_capacity(_T, ranged)

def _Pr_one_atm(_T, ranged=True):
    """(m/m)"""
    return _kinematic_viscocity_one_atm(_T, ranged) / _alpha_one_atm(_T, ranged)


# Programmatically create functions with units #################################
functions = [
    _liquid_density,
    _solid_vapor_pressure,
    _vapor_pressure,
    _heat_of_vaporization,
    _solid_heat_capacity,
    _liquid_heat_capacity,
    _ideal_gas_heat_capacity,
    _second_virial_coef,
    _liquid_viscocity,
    _vapor_viscocity,
    _liquid_thermal_conductivity,
    _vapor_thermal_conductivity,
    _ro_one_atm,
    _volume_1_atm,
    _kinematic_viscocity_one_atm,
    _alpha_one_atm,
    _Pr_one_atm,
]

exec(function_strings(functions))

k_v = vapor_thermal_conductivity
