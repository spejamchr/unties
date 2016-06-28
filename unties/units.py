"""Define all units and constants

Units:
    Use the all_units() method to see the most updated version of this list.
    This does not include any units defined outside this file.

Constants:
    Use the all_constants() method to see the most updated version of this list.

Defined Methods:
    deg_c()             Convert a Celsius temperature to Kelvin
    deg_f()             Convert a Fahrenheit temperature to Rankine
    all_units()         Display all units
    all_constants()     Display all constants
    unitify()           Convert ndarray of units into unit with array of values
"""
from .units_group import UnitsGroup

# I don't want to import math just for this...
pi = 3.14159265358979323846264338327950288419716939937510

#### Initialize Base Units ####
m   = UnitsGroup('m')    # meter for length
kg  = UnitsGroup('kg')   # kilogram for mass
s   = UnitsGroup('s')    # second for time
A   = UnitsGroup('A')    # ampere for electric current
K   = UnitsGroup('K')    # kelvin for temperature
cd  = UnitsGroup('cd')   # candela for luminous intensity
mol = UnitsGroup('mol')  # mole for the amount of substance

#### Initialize Derived Units ####
# Official SI derived units
N = (kg * m / s**2).rename('N') # Newton    (force)
J = (N * m).rename('J')         # Joule     (energy)
Pa = (N / m**2).rename('Pa')    # Pascal    (pressure)
Hz = (s**-1).rename('Hz')       # Hertz     (frequency)
rad = (m / m).rename('rad')     # Radian    (angle)             [unitless]
W = (J / s).rename('W')         # Watt      (power)
C = (s * A).rename('C')         # Coulomb   (electric charge)
V = (W / A).rename('V')         # Volt      (voltage)
F = (C / V).rename('F')         # Farad     (capacitance)
ohm = (V / A).rename('ohm')     # Ohm       (electrical resistance)
S = (1 / ohm).rename('S')       # Siemen    (electrical conductance)
Wb =  (J / A).rename('Wb')      # Weber     (magnetic flux)
T = (V * s / m**2).rename('T')  # Tesla     (magnetic field strength)
H = (V * s / A).rename('H')     # Henry     (inductance)

# Unofficial Units
M = (1000*mol/m**3).rename('M') # Molar     (concentration)

#### Initialize Constants ####
# Measured Constants
Rc = 8.3144598 * J / (mol * K)                      # Gas constant
c = 299792458 * m / s                               # Speed of light
g = 9.80665 * m / s**2                              # Acceleration of gravity
Gc = 6.67408 * 10**-11 * N * m**2 / kg**2           # Gravitational constant
h = 6.626070040 * 10**-34 * J * s                   # Planck's constant
Me = 9.10938356 * 10**-31 * kg                      # Electron rest mass
Mn = 1.674927471 * 10**-27 * kg                     # Neutron rest mass
Mp = 1.672621777 * 10**-27 * kg                     # Proton rest mass
Na = 6.022140857 * 10**23 / mol                     # Avogadro constant
q = 1.6021766208 * 10**-19 * C                      # Electron charge

# Defined constants
Cc = (c**2 * 10**-7 * H / m)                  (m/F) # Coulomb's constant
hbar = h / (2 * pi)                                 # Reduced Planck's constant
u0 = 4 * pi * 10**-7 * N / A**2                     # Vacuum permeability
e0 = (u0**-1 * c**-2)                         (F/m) # Vacuum permittivity
kb = Rc / Na                                        # Boltzmann's constant
sbc = pi**2 * kb**4 / (60 * hbar**3 * c**2)         # Stefan-Boltzmann constant
ub = (q * hbar / (2 * Me))                    (J/T) # Bohr magneton
Rb = (4 * pi * e0 * hbar**2 / (Me * q**2))      (m) # Bohr radius
# Rdb = (Me * q**4 / 8 / e0**2 / h**3 / c)      (1/m) # Rydberg Constant
mfq = (h / (2 * q))                            (Wb) # Magnetic flux quantum
omega = 2 / 15 * pi**5 * kb**4 / (c**2 * h**3)      # This is for black body radiation: Eb = omega * T**4

#### Initialize Conversion Units ####
conversions = [
    ['Length', m, 'Meter',
        {
            'Ang':  [10**-10,                   'Angstrom'],
            'au':   [149597900000,              'Astronomical Unit'],
            'fath': [1.8288,                    'Fathom'],
            'fm':   [10**-15,                   'Femtometer/Fermi'],
            'um':   [10**-6,                    'Micron/Micrometer'],
            'nm':   [10**-9,                    'Nanometer'],
            'mm':   [0.001,                     'Millimeter'],
            'cm':   [0.01,                      'Centimeter'],
            'dm':   [0.1,                       'Decimeter'],
            'km':   [1000,                      'Kilometer'],
            'inch': [0.0254,                    'Inch'],
            'ft':   [0.3048,                    'Foot'],
            'yd':   [0.9144,                    'Yard'],
            'mi':   [1609.344,                  'Mile'],
            'fur':  [201.168,                   'Furlong'],
            'ltyr': [9.46052840488*10**15,      'Lightyear'],
            'Nmi':  [1852,                      'Nautical Mile'],
            'pc':   [3.085678*10**16,           'Parsec'],
            'rod':  [5.0292,                    'Rod'],
        }
    ],

    ['Area', m**2, 'Square Meter',
        {
            'acre': [4046.8564224,   'Acre'],
            'ha':   [10**4,          'Hectare'],
        }
    ],

    ['Volume', m**3, 'Cubic meter',
        {
            'cup':      [2.365882365*10**-4,    'Cup'],
            'floz':     [2.95735295625*10**-5,  'Fluid ounce'],
            'flozUK':   [2.84130625*1**-5,      'British fluid ounce'],
            'gal':      [0.003785411784,        'Gallon'],
            'galUK':    [0.00454609,            'British gallon'],
            'l':        [0.001,                 'Liter'],
            'ml':       [10**-6,                'Milliliter'],
            'pt':       [4.73176473*10**-4,     'Pint'],
            'qt':       [9.46352946*10**-4,     'Quart'],
            'tbsp':     [1.47867647813*10**-5,  'Tablespoon'],
            'tsp':      [4.92892159375*10**-6,  'Teaspoon'],
        }
    ],

    ['Velocity', m/s, 'Meters per second',
        {
            'knot': [0.514444444444,         'Knot'],
            'kph':  [0.277777777778,         'Kilometers per hour'],
            'mph':  [0.44704,                'Miles per hour'],
        }
    ],

    ['Amount Of Substance', mol, 'Mole',
        {
            'kmol':     [1000,       'Kilomol'],
            'lbmol':    [453.59237,  'Pound-mole'],
        }
    ],

    ['Mass', kg, 'Kilogram',
        {
            'amu':      [1.6605402*10**-27, 'Atomic mass unit'],
            'gm':       [0.001,             'Gram'],
            'lb':       [0.45359237,        'Pound mass'],
            'mg':       [10**-6,            'Milligram'],
            'mton':     [1000,              'Metric ton'],
            'oz':       [0.028349523125,    'Ounce'],
            'slug':     [14.5939029372,     'Slug'],
            'ton':      [907.18474,         'Ton'],
            'tonUK':    [1016.047,          'Long ton'],
        }
    ],

    ['Force', N, 'Newton',
        {
            'dyne': [10**-5,        'Dyne'],
            'kgf':  [80665,         'Kilogram force'],
            'lbf':  [4.44822161526, 'Pound force'],
            'tonf': [8896.44323052, 'Ton force'],
        }
    ],

    ['Energy', J, 'Joule',
        {
            'Btu':  [1055.05585262,         'British thermal unit'],
            'cal':  [4.1868,                'Calorie'],
            'erg':  [10**-7,                'Erg'],
            'eV':   [1.60217733*10**-19,    'Electron volt'],
            'ftlb': [1.35581794833,         'Foot-pound'],
            'kcal': [4186.8,                'Kilocalorie'],
            'kJ':   [1000,                  'Kilojoule'],
            'kWh':  [3600000,               'Kilowatt-hour'],
            'latm': [101.325,               'Liter-atmosphere'],
            'MJ':   [10**6,                 'Megajoule'],
        }
    ],

    ['Power', W, 'Watt',
        {
            'hp':   [745.699871582,    'Horsepower'],
            'kW':   [1000,             'Kilowatt'],
            'MW':   [10**6,            'Megawatt'],
            'GW':   [10**9,            'Gigawatt'], # (1.21 for time travel)
        }
    ],

    ['Pressure', Pa, 'Pascal',
        {
            'atm':      [101325,            'Atmosphere'],
            'bar':      [10**5,             'Bar'],
            'inH2O':    [249.08891,         'Inches of water'],
            'inHg':     [3386.38815789,     'Inches of mercury'],
            'kPa':      [1000,              'Kilopascals'],
            'MPa':      [10**6,             'Megapascals'],
            'mmH2O':    [9.80665,           'Millimeters of water'],
            'mmHg':     [133.322387415,     'Millimeters of mercury'],
            'psi':      [6894.75729317,     'Pounds per square inch'],
            'torr':     [101325 / 760,      'Torr'],
        }
    ],

    ['Time', s, 'Second',
        {
            'minute':       [60,                         'Minute'],
            'hr':           [60*60,                      'Hour'],
            'day':          [60*60*24,                   'Day'],
            'week':         [60*60*24*7,                 'Week'],
            'fortnight':    [60*60*24*7*2,               'Fortnight'],
            'yr':           [60*60*24*365.242198781,     'Year'],
            'ms':           [0.001,                      'Millisecond'],
            'us':           [10**-6,                     'Microsecond'],
            'ns':           [10**-9,                     'Nanosecond'],
        }
    ],

    ['Angle', rad, 'Radian',
        {
            'deg':  [pi / 180,    'Degree'],
        }
    ],

    # Celcius and Fahrenheit require offsets, so we won't do those here
    ['Temperature', K, 'Kelvin',
        {
            'R':    [5 / 9,   'Rankine'],
        }
    ],

    ['Current', A, 'Ampere',
        {
        }
    ],

    ['Luminous Intensity', cd, 'Candela',
        {
        }
    ],

    ['Frequency', Hz, 'Hertz',
        {
        }
    ],

    ['Electric Charge', C, 'Coulomb',
        {
        }
    ],

    ['Voltage', V, 'Volt',
        {
        }
    ],

    ['Capacitance', F, 'Farad',
        {
        }
    ],

    ['Electrical Resistance', ohm, 'Ohm',
        {
        }
    ],

    ['Electrical Conductance', S, 'Siemen',
        {
        }
    ],

    ['Magnetic Flux', Wb, 'Weber',
        {
        }
    ],

    ['Magnetic Field Strength', T, 'Tesla',
        {
        }
    ],

    ['Inductance', H, 'Henry',
        {
        }
    ],
]

__all_units = {}
for group in conversions :
    dimension, base, base_name, units_dict = group
    __all_units[dimension] = {base.full_name.unit_name_string(): base_name}
    for unit in units_dict :
        unit_list = units_dict[unit]
        locals()[unit] = (base * unit_list[0]).rename(unit)
        __all_units[dimension][unit] = unit_list[1]

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

def all_units():
    """Print all units in tables
    """
    maximums = []
    for dimension in list(__all_units):
        maximums.append(max([len(a) for a in list(__all_units[dimension])]))

    maximum = max(maximums)
    pre = ''
    strings = {}
    for dimension in sorted(list(__all_units)):
        strings[dimension] = []
        for unit in sorted(list(__all_units[dimension])):
            inter = ' ' * (2 + maximum - len(unit))
            string = pre + str(unit) + inter + str(__all_units[dimension][unit])
            strings[dimension].append(string)

    maximums = []
    for dimension in list(strings):
        maximums.append(max([len(a) for a in strings[dimension]]))

    maximum = max(maximums) + 4

    for dimension in sorted(list(strings)):
        pre = '|' + ' ' * int((maximum - len(dimension)) / 2 - 1)
        post = ' ' * (maximum - len(pre) - len(dimension) - 1) + '|'
        print('-' * maximum)
        print(pre + dimension + post)
        print('=' * maximum)
        max_string = max([len(s) for s in strings[dimension]]) + 2
        for string in strings[dimension]:
            pre = '|' + ' ' * (int((maximum - max_string) / 2))
            post = ' ' * (maximum - len(string) - len(pre) - 1) + '|'
            print(pre + string + post)
        print('-' * maximum)
        print("\n")

def all_constants():
    """Print all constants.
    """
    string = """
    Rc      (Gas constant)
    c       (Speed of light)
    g       (Acceleration of gravity)
    Gc      (Gravitational constant)
    h       (Planck's constant)
    Me      (Electron rest mass)
    Mn      (Neutron rest mass)
    Mp      (Proton rest mass)
    Na      (Avogadro constant)
    q       (Electron charge)
    Cc      (Coulomb's constant)
    hbar    (Reduced Planck's constant)
    u0      (Vacuum permeability)
    e0      (Vacuum permittivity)
    kb      (Boltzmann's constant)
    sbc     (Stefan-Boltzmann constant)
    ub      (Bohr magneton)
    Rb      (Bohr radius)
    Rdb     (Rydberg Constant)
    mfq     (Magnetic flux quantum)"""
    print(string)

# Delete temporary variables
del conversions, unit_list, dimension, base, base_name, units_dict, unit, group

from numpy import nditer
def unitify(ndarray):
    """Convert a numpy.ndarray of units into one unit with an array of values"""
    a = ndarray.copy()
    unit = a.flatten()[0].normalized()
    for x in nditer(a, flags=['refs_ok'], op_flags=['readwrite']):
        x[...] = x / unit
    return unit * a.astype(float)
