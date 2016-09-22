"""Water module of DIPPR data


## Intro

To use, do:

    >>> from unties.properties import water
    >>> print(water.MW)
    18.01528 * gm / mol

Or, to get the unitless value, use an underline before the property name:

    >>> print(water._MW)
    0.01801528


## Constants

The constants are stored as simple numbers. Each one has a comment that
identifies its units.


## Functions

The functions are functions of temperature (in Kelvin), and each one has a range
of usability. If a functioni is called with a temperature outside this range, an
error will be raised.

    >>> Pv = water._ideal_gas_heat_capacity(2280)
    Exception: 2280 is out of range: [100, 2273.15]

All functions accept an optional argument called `ranged` that you can use to
override this safety range.

    >>> Pv = wather._ideal_gas_heat_capacity(2280, ranged=False)
    2280 is out of range: [100, 2273.15]
    >>> print(Pv)
    52.794569403553005

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
    _del_h_fusion_melt_point
    _omega = _acentric_factor
    _radius_of_gyration
    _solubility_param
    _dipole_mom
    _van_der_waals_vol
    _van_der_waals_area
    _refractive_index
    _del_h_sublimation
    _dielectric_const

Available Temperature-Dependant Functions:
    _solid_density
    _liquid_density
    _solid_vapor_pressure
    _liquid_vapor_pressure
    _heat_of_vaporization
    _solid_heat_capacity
    _liquid_heat_capacity
    _ideal_gas_heat_capacity
    _second_virial_coef
    _liquid_viscocity
    _vapor_viscocity
    _liquid_thermal_conductivity
    _vapor_thermal_conductivity
    _surface_tension
"""

# Imports ######################################################################
from unties import *
from math import exp, log, sinh, cosh
from unties.utilities.utilities import OutOfRangeTest, function_strings


# DIPPR's Constants Without Units ##############################################
_MW = 18.01528 / 1000 # kg / mol
_Tc = 647.096 # K
_Pc = 2.20640E+07 # Pa
_Vc = 5.59472E-02 # m**3 / kmol
_CompFactorCrit = 0.229 # unitless

_Tmelt = 273.15 # K
_Ttriple = 273.16 # K
_Ptriple = 611.73 # Pa
_Tboil = 373.15 # K
_LiqMolVol = 1.80691E-02 # m**3 / kmol

_del_h_form_ig = -2.41818E+08 # J / kmol
_del_g_form_ig = l_h_form_ig = -2.28572E+08 # J / kmol
_abs_entr_ig = 1.88825E+05 # J / (kmol * K)
_std_h_form = -2.85830E+08 # J / kmol
_std_g_form = -2.37129E+08 # J / kmol

_std_abs_s = 6.99100E+04 # J / (kmol * K)
_del_h_fusion_melt_point = 6.00174E+06 # J / kmol
_omega = _acentric_factor = 0.344861 # unitless
_radius_of_gyration = 6.15000E-11 # m

_solubility_param = 4.78600E+04 # (J / m**3)**0.5
_dipole_mom = 6.17000E-30 # C * m
_van_der_waals_vol = 1.23700E-02 # m**3 / kmol
_van_der_waals_area = 2.26000E+08 # m**2 / kmol
_refractive_index = 1.3325 # unitless

_del_h_sublimation = 5.08000E+07 # J / kmol
_dielectric_const = 80.1 # unitless


# DIPPR's Constants With Units #################################################
MW = _MW * kg / mol
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
del_h_fusion_melt_point = _del_h_fusion_melt_point * J / kmol
omega = acentric_factor = _omega * (m/m)
radius_of_gyration = _radius_of_gyration * m

solubility_param = _solubility_param * (J / m**3)**0.5
dipole_mom = _dipole_mom * C * m
van_der_waals_vol = _van_der_waals_vol * m**3 / kmol
van_der_waals_area = _van_der_waals_area * m**2 / kmol
refractive_index = _refractive_index * (m/m)

del_h_sublimation = _del_h_sublimation * J / kmol
dielectric_const = _dielectric_const * (m/m)


# DIPPR's Functions Without Units ##############################################
def _solid_density(_T, ranged=True):
    """mol / m**3"""
    OutOfRangeTest(_T, 233.15, 273.15, ranged)
    A, B = 5.3030E+01, -7.8409E-03
    return A + B * _T * 1000

def _liquid_density(_T, ranged=True):
    """mol / m**3"""
    OutOfRangeTest(_T, 273.16, 647.096, ranged)
    A, B, C, D, E, F, G = (1.7874E+01,
                           3.5618E+01,
                           1.9655E+01,
                          -9.1306E+00,
                          -3.1367E+01,
                          -8.1356E+02,
                          -1.7421E+07)
    t = 1 - _T / _Tc
    first = A
    second = B * t**(1 / 3)
    third = C * t**(2 / 3)
    fourth = D * t**(5 / 3)
    fifth = E * t**(16 / 3)
    sixth = F * t**(43 / 3)
    seventh = G * t**(110 / 3)
    return (first + second + third + fourth + fifth + sixth + seventh) * 1000

def _solid_vapor_pressure(_T, ranged=True):
    """Pa"""
    OutOfRangeTest(_T, 149.3, 273.16, ranged)
    A, B = 2.8766E+01, -6.1092E+03
    return exp(A + B / _T)

def _liquid_vapor_pressure(_T, ranged=True):
    """Pa"""
    OutOfRangeTest(_T, 273.16, 647.096, ranged)
    A, B, C, D, E = 7.3649E+01, -7.2582E+03, -7.3037E+00, 4.1653E-06, 2.0000E+00
    return exp(A + B / _T + C * log(_T) + D * _T**E)

def _heat_of_vaporization(_T, ranged=True):
    """J / mol"""
    OutOfRangeTest(_T, 273.16, 647.096, ranged)
    A, B, C, D = 5.6600E+07, 6.1204E-01, -6.2570E-01, 3.9880E-01
    Tr = _T / _Tc
    return A * (1 - Tr)**(B + C * Tr + D * Tr**2) / 1000

def _solid_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 3.15, 273.15, ranged)
    A, B = -2.6249E+02, 1.4052E+02
    return (A + B * _T) / 1000

def _liquid_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 273.16, 533.15, ranged)
    A, B, C, D, E = 2.7637E+05, -2.0901E+03, 8.1250E+00, -1.4116E-02, 9.3701E-06
    return (A + B * _T + C * _T**2 + D * _T**3 + E * _T**4) / 1000

def _ideal_gas_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 100, 2273.15, ranged)
    A, B, C, D, E = 3.3363E+04, 2.6790E+04, 2.6105E+03, 8.8960E+03, 1.1690E+03
    return (A + B * (C/_T / sinh(C/_T))**2 + D * (E/_T / cosh(E/_T))**2) / 1000

def _second_virial_coef(_T, ranged=True):
    """m**3 / mol"""
    OutOfRangeTest(_T, 273.15, 2273.1, ranged)
    A, B, C, D, E = 2.2220E-02, -2.6380E+1, -1.6750E+07, -3.8940E+19, 3.1330E+21
    return (A + B / _T + C / _T**3 + D / _T**8 + E / _T**9) / 1000

def _liquid_viscocity(_T, ranged=True):
    """Pa * s"""
    OutOfRangeTest(_T, 273.16, 646.15, ranged)
    A, B, C, D, E = -5.2843E+01, 3.7036E+03, 5.8660E+00, -5.8790E-29, 10.0
    return exp(A + B / _T + C * log(_T) + D * _T**E)

def _vapor_viscocity(_T, ranged=True):
    """Pa * s"""
    OutOfRangeTest(_T, 273.16, 1073.15, ranged)
    A, B = 1.7096E-08, 1.1146E+00
    return A * _T**B

def _liquid_thermal_conductivity(_T, ranged=True):
    """W / (m * K)"""
    OutOfRangeTest(_T, 273.16, 633.15, ranged)
    A, B, C, D = -4.3200E-01, 5.7255E-03, -8.0780E-06, 1.8610E-09
    return A + B * _T + C * _T**2 + D * _T**3

def _vapor_thermal_conductivity(_T, ranged=True):
    """W / (m * K)"""
    OutOfRangeTest(_T, 273.16, 1073.15, ranged)
    A, B = 6.2041E-06, 1.3973E+00
    return A * _T**B

def _surface_tension(_T, ranged=True):
    """N / m"""
    OutOfRangeTest(_T, 273.16, 647.096, ranged)
    A, B, C, D = 1.7766E-01, 2.5670E+00, -3.3377E+00, 1.9699E+00
    Tr = _T / _Tc
    return A * (1 - Tr)**(B + C * Tr + D * Tr**2)


# Steam Functions Without Units ################################################
_steam_viscosity = _vapor_viscocity

_steam_thermal_conductivity = _vapor_thermal_conductivity

def _steam_vol(_T, ranged=True):
    """m**3 / kg"""
    OutOfRangeTest(_T, 273.15, 430, ranged)
    Ts = [
        273.15, 275,    280,    285,    290,    295,
        300,    305,    310,    315,    320,    325,
        330,    335,    340,    345,    350,    355,
        360,    365,    370,    373.15, 375,    380,
        385,    390,    400,    410,    420,    430
    ]
    Vsats = [
        206.3,   181.7,   130.4,    99.4,    69.7,    51.94,
         39.13,   29.74,   22.93,   17.82,   13.98,   11.06,
          8.82,    7.09,    5.74,    4.683,   3.846,   3.180,
          2.645,   2.212,   1.861,   1.679,   1.574,   1.337,
          1.142,   0.980,   0.731,   0.553,   0.425,   0.331
    ]
    return float(UnivariateSpline(Ts, Vsats, s=0).__call__(_T))

def _steam_density(_T, ranged=True):
    """mol / m**3"""
    return 1 / _steam_vol(_T, ranged) / _MW

# My own Functions Without Units ###############################################
def _kinematic_viscocity(_T, ranged=True):
    """m**2 / s"""
    return _liquid_viscocity(_T, ranged) / (_liquid_density(_T, ranged) * _MW)

def _Pr(_T, ranged=True):
    # J / (mol * K) * Pa *s / (W / (m * K) * gm/mol)
    """(m/m)"""
    return _liquid_heat_capacity(_T, ranged) * _liquid_viscocity(_T, ranged) / (_liquid_thermal_conductivity(_T, ranged) * _MW)


# Programmatically create functions with units #################################
functions = [
    _solid_density,
    _liquid_density,
    _solid_vapor_pressure,
    _liquid_vapor_pressure,
    _heat_of_vaporization,
    _solid_heat_capacity,
    _liquid_heat_capacity,
    _ideal_gas_heat_capacity,
    _second_virial_coef,
    _liquid_viscocity,
    _vapor_viscocity,
    _liquid_thermal_conductivity,
    _vapor_thermal_conductivity,
    _surface_tension,
    _steam_viscosity,
    _steam_thermal_conductivity,
    _steam_vol,
    _steam_density,
    _kinematic_viscocity,
    _Pr,
]

exec(function_strings(functions))

k_l = liquid_thermal_conductivity
