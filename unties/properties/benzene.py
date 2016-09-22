"""Benzene module of DIPPR data


## Intro

To use, do:

    >>> from unties.properties import benzene
    >>> print(benzene.MW)
    78.11184 * gm / mol

Or, to get the unitless value, use an underline before the property name:

    >>> print(benzene._MW)
    0.07811184


## Constants

The constants are stored as simple numbers. Each one has a comment that
identifies its units.


## Functions

The functions are functions of temperature (in Kelvin), and each one has a range
of usability. If a functioni is called with a temperature outside this range, an
error will be raised.

    >>> Pv = benzene._ideal_gas_heat_capacity(2280)
    Exception: 2280 is out of range: [20, 1500]

All functions accept an optional argument called `ranged` that you can use to
override this safety range.

    >>> Pv = benzene._ideal_gas_heat_capacity(2280, ranged=False)
    2280 is out of range: [20, 1500]
    >>> print(Pv)
    261.89948734432255

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
    _std_net_heat_of_comb
    _omega = _acentric_factor
    _radius_of_gyration
    _solubility_param
    _dipole_mom
    _van_der_waals_vol
    _van_der_waals_area
    _refractive_index
    _flash_point
    _lower_flammability_limit
    _upper_flammability_limit
    _lower_flamm_limit_temp
    _upper_flamm_lumit_temp
    _auto_ignition_temp
    _parachor
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
    _solid_thermal_conductivity
    _liquid_thermal_conductivity
    _vapor_thermal_conductivity
    _surface_tension
    _sat_pressure
    _sat_temp
    _kinematic_viscocity
    _Pr_liq
    _Pr_vap
"""

# Imports ######################################################################
from unties import *
from math import exp, log, sinh, cosh
from scipy.optimize import fsolve
from unties.utilities.utilities import OutOfRangeTest, function_strings


# DIPPR's Constants Without Units ##############################################
_MW = 78.11184 / 1000 # kg / mol
_Tc = 562.05 # K
_Pc = 4.89500E+06 # Pa
_Vc = 0.256 # m**3 / kmol
_CompFactorCrit = 0.268 # unitless

_Tmelt = 278.68 # K
_Ttriple = 278.68 # K
_Ptriple = 4.76422E+03 # Pa
_Tboil = 353.24 # K
_LiqMolVol = 8.94764E-02 # m**3 / kmol

_del_h_form_ig = 8.28800E+07 # J / kmol
_del_g_form_ig = l_h_form_ig = 1.29600E+08 # J / kmol
_abs_entr_ig = 2.69300E+05 # J / (kmol * K)
_std_h_form = 4.89500E+07 # J / kmol
_std_g_form = 1.24400E+08 # J / kmol

_std_abs_s = 1.73260E+05 # J / (kmol * K)
_del_h_fusion_melt_point = 9.86600E+06 # J / kmol
_std_net_heat_of_comb = -3.13600E+09 # J / kmol
_omega = _acentric_factor = 0.2103 # unitless
_radius_of_gyration = 3.00400E-10 # m

_solubility_param = 1.87300E+04 # (J / m**3)**0.5
_dipole_mom = 0.0 # C * m
_van_der_waals_vol = 4.84000E-02 # m**3 / kmol
_van_der_waals_area = 6.00000E+08 # m**2 / kmol
_refractive_index = 1.49792 # unitless

_flash_point = 262 # K
_lower_flammability_limit = 0.012 # vol% in air
_upper_flammability_limit = 0.08 # vol% in air
_lower_flamm_limit_temp = 261 # K
_upper_flamm_lumit_temp = 288 # K

_auto_ignition_temp = 833.15 # K
_parachor = 206.2 # unitless
_del_h_sublimation = 4.53000E+07 # J / kmol
_dielectric_const = 2.2825 # unitless


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
del_h_fusion_melt_point = _del_h_fusion_melt_point * J / kmol
std_net_heat_of_comb = _std_net_heat_of_comb * J / kmol
omega = acentric_factor = _omega * (m/m)
radius_of_gyration = _radius_of_gyration * m

solubility_param = _solubility_param * (J / m**3)**0.5
dipole_mom = _dipole_mom * C * m
van_der_waals_vol = _van_der_waals_vol * m**3 / kmol
van_der_waals_area = _van_der_waals_area * m**2 / kmol
refractive_index = _refractive_index * (m/m)

flash_point = _flash_point * K
lower_flammability_limit = _lower_flammability_limit * (m/m)
upper_flammability_limit = _upper_flammability_limit * (m/m)
lower_flamm_limit_temp = _lower_flamm_limit_temp * K
upper_flamm_lumit_temp = _upper_flamm_lumit_temp * K

auto_ignition_temp = _auto_ignition_temp * K
parachor = _parachor * (m/m)
del_h_sublimation = _del_h_sublimation * J / kmol
dielectric_const = _dielectric_const * (m/m)

# DIPPR's Functions Without Units ##############################################
def _solid_density(_T, ranged=True):
    """mol / m**3"""
    OutOfRangeTest(_T, 273.1, 278.68, ranged)
    A, B = 1.3061E+01, -3.5714E-04
    return A + B * _T * 1000

def _liquid_density(_T, ranged=True):
    """mol / m**3"""
    OutOfRangeTest(_T, 278.68, 562.05, ranged)
    A, B, C, D = 1.0259E+00, 2.6666E-01, 5.6205E+02, 2.8394E-01
    return (A / B**(1 + (1 - _T / C)**D)) * 1000

def _solid_vapor_pressure(_T, ranged=True):
    """Pa"""
    OutOfRangeTest(_T, 178.25, 278.68, ranged)
    A, B, C, D, E = 7.2829E+01, -7.0423E+03, -7.0610E+00, 8.6915E-06, 2.0000E+00
    return exp(A + B / _T + C * log(_T) + D * _T**E)

def _liquid_vapor_pressure(_T, ranged=True):
    """Pa"""
    OutOfRangeTest(_T, 278.68, 562.05, ranged)
    A, B, C, D, E = 8.3107E+01, -6.4862E+03, -9.2194E+00, 6.9844E-06, 2.0000E+00
    return exp(A + B / _T + C * log(_T) + D * _T**E)

def _heat_of_vaporization(_T, ranged=True):
    """J / mol"""
    OutOfRangeTest(_T, 278.68, 562.05, ranged)
    A, B, C, D = 5.0007E+07, 6.5393E-01, -2.7698E-01, 2.9569E-02
    Tr = _T / _Tc
    return A * (1 - Tr)**(B + C * _T + D * _T**2) / 1000

def _solid_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 40, 278.68, ranged)
    A, B, C, D = 7.4000E+03, 6.2490E+02, -2.6874E+00, 7.3160E-03
    return (A + B * _T + C * _T**2 + D * _T**3) / 1000

def _liquid_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 278.68, 500, ranged)
    A, B, C = 1.6294E+05, -3.4494E+02, 8.5562E-01
    return (A + B * _T + C * _T**2) / 1000

def _ideal_gas_heat_capacity(_T, ranged=True):
    """J / (mol * K)"""
    OutOfRangeTest(_T, 20, 1500, ranged)
    A, B, C, D, E, F, G= (3.3258E+04,
                          5.1445E+04,
                          -7.6109E+02,
                          1.3974E+05,
                          1.6169E+03,
                          5.6829E+04,
                          4.1114E+03)
    first = A + B * (C / _T)**2 * exp(C / _T) / (exp(C / _T) - 1)**2
    second = D * (E / _T)**2 * exp(E / _T) / (exp(E / _T) - 1)**2
    third = F * (G / _T)**2 * exp(G / _T) / (exp(G / _T) - 1)**2
    return (first + second + third) / 1000

def _second_virial_coef(_T, ranged=True):
    """m**3 / mol"""
    OutOfRangeTest(_T, 281.02, 1500, ranged)
    A, B, C, D, E = (1.5059E-01,
                    -1.8694E+02,
                    -2.3146E+07,
                    -7.0493E+18,
                    -6.8786E+20)
    return (A + B / _T + C / _T**3 + D / _T**8 + E / _T**9) / 1000

def _liquid_viscocity(_T, ranged=True):
    """Pa * s"""
    OutOfRangeTest(_T, 278.68, 545, ranged)
    A, B, C = 7.5117E+00, 2.9468E+02, -2.7940E+00
    return exp(A + B / _T + C * log(_T))

def _vapor_viscocity(_T, ranged=True):
    """Pa * s"""
    OutOfRangeTest(_T, 278.68, 1000, ranged)
    A, B, C = 3.1340E-08, 9.6760E-01, 7.9000E+00
    return A * _T**B / (1 + C / _T)

def _solid_thermal_conductivity(_T, ranged=True):
    """W / (m * K)"""
    OutOfRangeTest(_T, 90, 273.4, ranged)
    A, B, C = 1.1610E+00, -5.9308E-03, 9.8300E-06
    return A + B * _T + C * _T**2

def _liquid_thermal_conductivity(_T, ranged=True):
    """W / (m * K)"""
    OutOfRangeTest(_T, 278.68, 413.1, ranged)
    A, B = 2.3444E-01, -3.0572E-04
    return A + B * _T

def _vapor_thermal_conductivity(_T, ranged=True):
    """W / (m * K)"""
    OutOfRangeTest(_T, 339.15, 1000, ranged)
    A, B, C = 1.6520E-05, 1.3117E+00, 4.9100E+02
    return A * _T**B / (1 + C / _T)

def _surface_tension(_T, ranged=True):
    """N / m"""
    OutOfRangeTest(_T, 278.68, 562.05, ranged)
    A, B = 7.1815E-02, 1.2362E+00
    Tr = _T / _Tc
    return A * (1 - Tr)**B


# Dr. Knotts Functions Without Units, saturated benzene ########################
def _sat_pressure(_T, ranged=True):
    """Pa"""
    A, B, C, D, E = 83.107, -6486.2, -9.2194, 6.9844e-06, 2
    return exp(A + B / _T + C * log(_T) + D * _T**E)

def _sat_temp(_P, ranged=True):
    """K"""
    OutOfRangeTest(_P, 82732, 3746684, ranged) # Solver breaks outside here
    def solve(_T):
        return _P - _sat_pressure(_T)
    return fsolve(solve, _P * 0.0224 / Rc.value)[0]


# Other Functions Without Units ################################################
def _kinematic_viscocity(_T, ranged=True):
    """m**2 / s"""
    return _liquid_viscocity(_T, ranged) / (_liquid_density(_T, ranged) * _MW)

def _Pr_liq(_T, ranged=True):
    """(m/m)"""
    return _liquid_heat_capacity(_T, ranged) * _liquid_viscocity(_T, ranged) / (_liquid_thermal_conductivity(_T, ranged) * _MW)

def _Pr_vap(_T, ranged=True):
    """(m/m)"""
    return _ideal_gas_heat_capacity(_T, ranged) * _vapor_viscocity(_T, ranged) / (_vapor_thermal_conductivity(_T, ranged) * _MW)


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
    _solid_thermal_conductivity,
    _liquid_thermal_conductivity,
    _vapor_thermal_conductivity,
    _surface_tension,
    _sat_pressure,
    _sat_temp,
    _kinematic_viscocity,
    _Pr_liq,
    _Pr_vap,
]

exec(function_strings(functions))

k_l = liquid_thermal_conductivity
k_v = vapor_thermal_conductivity
