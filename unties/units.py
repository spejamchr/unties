"""Define all units and constants
"""
from unties.units_group import UnitsGroup

UnitsGroup._locals = globals()

# I don't want to import math just for this...
pi = 3.14159265358979323846264338327950288419716939937510

UnitsGroup.add_prefixes({
    # 'Y': [10**24, 'Yotta'],
    # 'Z': [10**21, 'Zetta'],
    # 'E': [10**18, 'Exa'],
    # 'P': [10**15, 'Peta'],
    # 'T': [10**12, 'Tera'],
    'G': [10**9, 'Giga'],
    'M': [10**6, 'Mega'],
    'k': [10**3, 'Kilo'],
    'h': [10**2, 'Hecto'],
    'da': [10**1, 'Deca'],
    'd': [10**-1, 'Deci'],
    'c': [10**-2, 'Centi'],
    'm': [10**-3, 'Milli'],
    'u': [10**-6, 'Micro'],
    'n': [10**-9, 'Nano'],
    'p': [10**-12, 'Pico'],
    'f': [10**-15, 'Femto'],
    # 'a': [10**-18, 'Atto'],
    # 'z': [10**-21, 'Zepto'],
    # 'y': [10**-24, 'Yocto'],
})


# Initialize Base Units #
#########################
UnitsGroup.base('m', 'Meter')
UnitsGroup.base('kg', 'Kilogram', prefix=False)
UnitsGroup.base('s', 'Second')
UnitsGroup.base('A', 'Ampere')
UnitsGroup.base('K', 'Kelvin')
UnitsGroup.base('cd', 'Candela')
UnitsGroup.base('mol', 'Mole')

# Initialize Derived Units #
############################

# Official SI derived units
(m / m).derived('rad', 'Radian', _manual_quantity='angle')
(s**-1).derived('Hz', 'Hertz')
(kg * m / s**2).derived('N', 'Newton')
(N / m**2).derived('Pa', 'Pascal')
(N * m).derived('J', 'Joule')
(J / s).derived('W', 'Watt')
(s * A).derived('C', 'Coulomb')
(W / A).derived('V', 'Volt')
(C / V).derived('F', 'Farad')
(V / A).derived('ohm', 'Ohm')
(1 / ohm).derived('S', 'Siemen')
(J / A).derived('Wb', 'Weber')
(V * s / m**2).derived('T', 'Tesla')
(V * s / A).derived('H', 'Henry')

# Unofficial Units
(1000*mol/m**3).derived('M', 'Molar')

# Initialize Conversion Units #
###############################
# Conversions for m:
m.conversion('Ang', 'Angstrom', 10**-10)
m.conversion('au', 'Astronomical Unit', 149597900000)
m.conversion('pc', 'Parsec', 3.08567758149137*10**16)
m.conversion('fath', 'Fathom', 1.8288)
m.conversion('inch', 'Inch', 0.0254)
m.conversion('ft', 'Foot', 0.3048)
m.conversion('yd', 'Yard', 0.9144)
m.conversion('mi', 'Mile', 1609.344)
m.conversion('fur', 'Furlong', 201.168)
m.conversion('ltyr', 'Lightyear', 9.46052840488*10**15)
m.conversion('nmi', 'Nautical Mile', 1852)
m.conversion('rod', 'Rod', 5.0292)

# Conversions for m**2:
(m**2).conversion('acre', 'Acre', 4046.8564224)
(m**2).conversion('ha', 'Hectare', 10**4)

# Conversions for m**3:
(m**3).conversion('cup', 'Cup', 2.365882365*10**-4)
(m**3).conversion('floz', 'Fluid ounce', 2.95735295625*10**-5)
(m**3).conversion('flozUK', 'British fluid ounce', 2.84130625*1**-5)
(m**3).conversion('gal', 'Gallon', 0.003785411784)
(m**3).conversion('galUK', 'British gallon', 0.00454609)
(m**3).conversion('l', 'Liter', 0.001, prefix=True)
(m**3).conversion('pt', 'Pint', 4.73176473*10**-4)
(m**3).conversion('qt', 'Quart', 9.46352946*10**-4)
(m**3).conversion('tbsp', 'Tablespoon', 1.47867647813*10**-5)
(m**3).conversion('tsp', 'Teaspoon', 4.92892159375*10**-6)

# Conversions for m/s:
(m/s).conversion('knot', 'Knot', 0.514444444444)
(m/s).conversion('kph', 'Kilometers per hour', 0.277777777778)
(m/s).conversion('mph', 'Miles per hour', 0.44704)

# Conversions for m/s**2:
(m/s**2).conversion('Gal', 'gal (galileo)', 0.01, prefix=True)

# Conversions for kg/(m*s):
(kg/(m*s)).conversion('P', 'poise', 0.1, prefix=True)

# Conversions for m**2/s:
(m**2/s).conversion('St', 'stokes', 10**-4, prefix=True)

# Conversions for mol:
mol.conversion('lbmol', 'Pound-mole', 453.59237)

# Conversions for kg:
kg.conversion('amu', 'Atomic mass unit', 1.6605402*10**-27)
# Use `g` to add prefixes (kg, mg, etc), but use `gm` for the actual symbol of
# gram. `g` is used for the acceleration of gravity
kg.conversion('g', 'Gram', 0.001, prefix=True)
kg.conversion('gm', 'Gram', 0.001)
kg.conversion('lb', 'Pound mass', 0.45359237)
kg.conversion('mton', 'Metric ton', 1000)
kg.conversion('oz', 'Ounce', 0.028349523125)
kg.conversion('slug', 'Slug', 14.5939029372)
kg.conversion('ton', 'Ton', 907.18474)
kg.conversion('tonUK', 'Long ton', 1016.047)

# Conversions for N:
N.conversion('dyn', 'Dyne', 10**-5)
N.conversion('kgf', 'Kilogram force', 9.80665)
N.conversion('lbf', 'Pound force', 4.44822161526)
N.conversion('tonf', 'Ton force', 8896.44323052)

# Conversions for J:
J.conversion('Btu', 'British thermal unit', 1055.05585262)
# The are multiple definitions for the calorie. This is the current standard.
J.conversion('cal', 'Gram calorie', 4.184)
J.conversion('Cal', 'Kilogram calorie', 4184)
J.conversion('kcal', 'Kilogram calorie', 4184)
J.conversion('erg', 'Erg', 10**-7)
J.conversion('eV', 'Electron volt', 1.60217733*10**-19)
J.conversion('ftlb', 'Foot-pound', 1.35581794833)
# Use prefixes to create kWh & MWh
J.conversion('Wh', 'Watt-hour', 3600, prefix=True)
J.conversion('latm', 'Liter-atmosphere', 101.325)

# Conversions for W:
W.conversion('hp', 'Horsepower', 745.699871582)

# Conversions for Pa:
Pa.conversion('atm', 'Atmosphere', 101325)
Pa.conversion('bar', 'Bar', 10**5)
Pa.conversion('inH2O', 'Inches of water', 249.08891)
Pa.conversion('inHg', 'Inches of mercury', 3386.38815789)
Pa.conversion('mmH2O', 'Millimeters of water', 9.80665)
Pa.conversion('mmHg', 'Millimeters of mercury', 133.322387415)
Pa.conversion('psi', 'Pounds per square inch', 6894.75729317)
Pa.conversion('torr', 'Torr', 101325 / 760)
Pa.conversion('Ba', 'Barye', 0.1)

# Conversions for s:
s.conversion('minute', 'Minute', 60)
s.conversion('hr', 'Hour', 60*60)
s.conversion('day', 'Day', 60*60*24)
s.conversion('week', 'Week', 60*60*24*7)
s.conversion('fortnight', 'Fortnight', 60*60*24*7*2)
s.conversion('yr', 'Year', 60*60*24*365.242198781)

# Conversions for rad:
rad.conversion('deg', 'Degree', pi / 180)
rad.conversion('arcmin', 'Arcminute', pi / (180 * 60))
rad.conversion('arcsec', 'Arcsecond', pi / (180 * 60 * 60))
rad.conversion('mas', 'Milliarcsecond', pi / (180 * 60 * 60 * 1000))
rad.conversion('uas', 'Microarcsecond', pi / (180 * 60 * 60 * 1000 * 1000))

# Conversions for K:
# Celcius and Fahrenheit require offsets, so we won't do those here
K.conversion('R', 'Rankine', 5 / 9)

# Conversions for A:
# Conversions for cd:
# Conversions for Hz:
# Conversions for C:
# Conversions for V:
# Conversions for F:
# Conversions for ohm:
# Conversions for S:
# Conversions for Wb:
# Conversions for T:
# Conversions for H:
# Conversions for M:

# Initialize Constants #
########################

# Measured Constants
(8.3144598 * J / (mol * K)).constant("Rc", "Gas constant")
(299792458 * m / s).constant("c", "Speed of light")
(9.80665 * m / s**2).constant("g", "Acceleration of gravity")
(6.67408 * 10**-11 * N * m**2 / kg**2).constant("Gc", "Gravitational constant")
(6.626070040 * 10**-34 * J * s).constant("h", "Planck's constant")
(9.10938356 * 10**-31 * kg).constant("Me", "Electron rest mass")
(1.674927471 * 10**-27 * kg).constant("Mn", "Neutron rest mass")
(1.672621777 * 10**-27 * kg).constant("Mp", "Proton rest mass")
(6.022140857 * 10**23 / mol).constant("Na", "Avogadro constant")
(1.6021766208 * 10**-19 * C).constant("q", "Electron charge")

# Defined constants
(c**2 * 10**-7 * H / m)(m/F).constant("Cc", "Coulomb's constant")
(h / (2 * pi)).constant("hbar", "Reduced Planck's constant")
(4 * pi * 10**-7 * N / A**2).constant("u0", "Vacuum permeability")
(u0**-1 * c**-2)(F/m).constant("e0", "Vacuum permittivity")
(Rc / Na).constant("kb", "Boltzmann's constant")
(pi**2 * kb**4 / (60 * hbar**3 * c**2)).constant("sbc",
                                                 "Stefan-Boltzmann constant")
(q * hbar / (2 * Me))(J/T).constant("ub", "Bohr magneton")
(4 * pi * e0 * hbar**2 / (Me * q**2))(m).constant("Rb", "Bohr radius")
(Me * q**4 / 8 / e0**2 / h**3 / c)(1/m).constant("Rdb", "Rydberg Constant")
(h / (2 * q))(Wb).constant("mfq", "Magnetic flux quantum")

# Initialize Quantities #
#########################
m.add_quantity('length')
kg.add_quantity('mass')
s.add_quantity('time')
A.add_quantity('electric current')
K.add_quantity('temperature')
cd.add_quantity('luminous intensity')
mol.add_quantity('amount of substance')
Hz.add_quantity('frequency')
N.add_quantity('force/weight')
Pa.add_quantity('pressure/stress')
J.add_quantity('energy/work/heat')
W.add_quantity('power/radiant flux')
C.add_quantity('electric charge')
V.add_quantity('voltage/electromotive force')
F.add_quantity('electric capacitance')
ohm.add_quantity('electrical resistance/impedance/reactance')
S.add_quantity('electrical conductance')
Wb.add_quantity('magnetic flux')
T.add_quantity('magnetic flux density')
H.add_quantity('inductance')
M.add_quantity('concentration')
(m**2).add_quantity('area')
(m**3).add_quantity('volume')
(m / s).add_quantity('speed/velocity')
(m / s**2).add_quantity('acceleration')
(m**3 / s).add_quantity('volumetric flow')
(N * s).add_quantity('momentum/impulse')
(N * m * s).add_quantity('angular momentum')
(mol / s).add_quantity('molar flow rate/catalytic activity')

# I grabbed these from a table at:
# https://en.wikipedia.org/wiki/SI_derived_unit
(N * m).add_quantity('torque')
(N / s).add_quantity('yank')
(m**-1).add_quantity('wavenumber/optical power/curvature/spatial frequency')
(kg / m**2).add_quantity('area density')
(kg / m**3).add_quantity('density/mass density')
(m**3 / kg).add_quantity('specific volume')
(mol / m**3).add_quantity('molarity')
(m**3 / mol).add_quantity('molar volume')
(J * s).add_quantity('action')
(J / K).add_quantity('heat capacity/entropy')
(J / (K * mol)).add_quantity('molar heat capacity/molar entropy')
(J / (K * kg)).add_quantity('specific heat capacity/specific entropy')
(J / mol).add_quantity('molar energy')
(J / kg).add_quantity('specific energy')
(J / m**3).add_quantity('energy density')
(N / m).add_quantity('surface tension/stiffness')
(W / m**2).add_quantity('heat flux density/irradiance')
(W / (m * K)).add_quantity('thermal conductivity')
(m**2 / s).add_quantity('kinematic viscosity/thermal diffusivity')
(m**2 / s).add_quantity('diffusion coefficient')
(Pa * s).add_quantity('dynamic viscosity')
(C / m**2).add_quantity('electric displacement field/polarization density')
(C / m**3).add_quantity('electric charge density')
(A / m**2).add_quantity('electric current density')
(S / m).add_quantity('electrical conductivity')
(S * m**2 / mol).add_quantity('molar conductivity')
(F / m).add_quantity('permittivity')
(H / m).add_quantity('magnetic permeability')
(V / m).add_quantity('electric field strength')
(A / m).add_quantity('magnetization/magnetic field strength')
(cd / m**2).add_quantity('luminance')
(C / kg).add_quantity('exposure (X and gamma rays)')
(ohm * m).add_quantity('resistivity')
(kg / m).add_quantity('linear mass density')
(C / m).add_quantity('linear charge density')
(mol / kg).add_quantity('molality')
(kg / mol).add_quantity('molar mass')
(m / m**3).add_quantity('fuel efficiency')
(kg / s).add_quantity('mass flow rate')
(J / T).add_quantity('magnetic dipole moment')
(W / m**3).add_quantity('spectral irradiance/power density')
(K / W).add_quantity('thermal resistance')
(K**-1).add_quantity('thermal expansion coefficient')
(K / m).add_quantity('temperature gradient')
(m**2 / (V * s)).add_quantity('electron mobility')
(Pa**-1).add_quantity('compressibility')
(H**-1).add_quantity('magnetic reluctance')
(Wb / m).add_quantity('magnetic vector potential')
(Wb * m).add_quantity('magnetic moment')
(T * m).add_quantity('magnetic rigidity')
(J / m**2).add_quantity('radiant exposure')
(m**3 / (mol * s)).add_quantity('catalytic efficiency')
(kg * m**2).add_quantity('moment of inertia')
(N * m * s / kg).add_quantity('specific angular momentum')
(Hz / s).add_quantity('frequency drift')
(m / H).add_quantity('magnetic susceptibility')
(W / m).add_quantity('spectral power')


def deg_c(num):
    """Return temperature in Kelvin

    Accepts a number representing the temperature in Celsius.
    """
    return (num + 273.15) * K


def deg_f(num):
    """Return temperature in Rankine

    Accepts a number representing the temperature in Fahrenheit.
    """
    return (num + 459.67) * R
