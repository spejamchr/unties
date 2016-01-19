import os
units_group_file_path = os.path.dirname(__file__) + '/' + 'units_group' + '.py'

import importlib.machinery
units_group = importlib.machinery.SourceFileLoader(
    '_', units_group_file_path
).load_module()
UnitsGroup = units_group.UnitsGroup

class Units :
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
    Cc = c**2 * 10**-7 * H / m                          # Coulomb's constant
    hbar = h / (2 * pi)                                 # Reduced Planck's constant
    u0 = 4 * pi * 10**-7 * N / A**2                     # Vacuum permeability
    e0 = u0**-1 * c**-2                                 # Vacuum permittivity
    kb = Rc / Na                                        # Boltzmann's constant
    sbc = pi**2 * kb**4 / (60 * hbar**3 * c**2)         # Stefan-Boltzmann constant
    ub = q * hbar / (2 * Me)                            # Bohr magneton
    Rb = 4 * pi * u0 * hbar**2 / (Me * q**2)            # Bohr radius
    Rdb = Me * q**4 / (8 * u0**2 * h**3 * c)            # Rydberg Constant
    mfq = h / (2 * q)                                   # Magnetic flux quantum

    #### Initialize Conversion Units ####
    conversions = {
        # Length
        m: {
            'Ang': 10**-10,                 # Angstrom
            'au': 149597900000,             # Astronomical Unit
            'fath': 1.8288,                 # Fathom
            'fm': 10**-15,                  # Femtometer/Fermi
            'um': 10**-6,                   # Micron/Micrometer
            'nm': 10**-9,                   # Nanometer
            'mm': 0.001,                    # Millimeter
            'cm': 0.01,                     # Centimeter
            'dm': 0.1,                      # Decimeter
            'km': 1000,                     # Kilometer
            'inch': 0.0254,                 # Inch
            'ft': 0.3048,                   # Foot
            'yd': 0.9144,                   # Yard
            'mi': 1609.344,                 # Mile
            'fur': 201.168,                 # Furlong
            'ltyr': 9.46052840488*10**15,   # Lightyear
            'Nmi': 1852,                    # Nautical Mile
            'pc': 3.085678*10**16,          # Parsec
            'rod': 5.0292,                  # Rod
        },
        # Area
        m**2: {
            'acre': 4046.8564224,   # Acre
            'ha': 10000,            # Acre
        },
        # Volume
        m**3: {
            'cup': 2.365882365*10**-4,      # Cup
            'floz': 2.95735295625*10**-5,   # Fluid ounce
            'flozUK': 2.84130625*1**-5,     # British fluid ounce
            'gal': 0.003785411784,          # Gallon
            'galUK': 0.00454609,            # British gallon
            'l': 0.001,                     # Liter
            'ml': 10**-6,                   # Milliliter
            'pt': 4.73176473*10**-4,        # Pint
            'qt': 9.46352946*10**-4,        # Quart
            'tbsp': 1.47867647813*10**-5,   # Tablespoon
            'tsp': 4.92892159375*10**-6,    # Teaspoon
        },
        # Velocity
        m/s: {
            'knot': 0.514444444444,         # Knot
            'kph': 0.277777777778,          # Kilometers per hour
            'mph': 0.44704,                 # Miles per hour
        },
        # Amount of Substance
        mol: {
            'kmol': 1000,       # Kilomol
            'lbmol': 453.59237, # Pound-mole
        },
        # Mass
        kg: {
            'amu': 1.6605402*10**-27,   # Atomic mass unit
            'gm': 0.001,                # Gram
            'lb': 0.45359237,           # Pound mass
            'mg': 10**-6,               # Milligram
            'mton': 1000,               # Metric ton
            'oz': 0.028349523125,       # Ounce
            'slug': 14.5939029372,      # Slug
            'ton': 907.18474,           # Ton
            'tonUK': 1016.047,          # Long ton
        },
        # Force
        N: {
            'dyne': 10**-5,         # Dyne
            'kgf': 80665,           # Kilogram force
            'lbf': 4.44822161526,   # Pound force
            'tonf': 8896.44323052,  # Ton force

        },
        # Energy
        J: {
            'Btu': 1055.05585262,       # British thermal unit
            'cal': 4.1868,              # Calorie
            'erg': 10**-7,              # Erg
            'eV': 1.60217733*10**-19,   # Electron volt
            'ftlb': 1.35581794833,      # Foot-pound
            'kcal': 4186.8,             # Kilocalorie
            'kWh': 3600000,             # Kilowatt-hour
            'latm': 101.325,            # Liter-atmosphere
        },
        # Power
        W: {
            'hp': 745.699871582,    # Horsepower
            'kW': 1000,             # Kilowatt
            'mW': 10**6,            # Megawatt
            'gW': 10**9,            # Gigawatt (1.21 for time travel)
        },
        # Pressure
        Pa: {
            'atm': 101325,          # Atmosphere
            'bar': 100000,          # Bar
            'inH2O': 249.08891,     # Inches of water
            'inHg': 3386.38815789,  # Inches of mercury
            'kPa': 1000,            # Kilopascals
            'mmH2O': 9.80665,       # Millimeters of water
            'mmHg': 133.322387415,  # Millimeters of mercury
            'psi': 6894.75729317,   # Pounds-force per square inch
            'Torr': 101325 / 760,   # Torr
        },
        # Time
        s: {
            'min': 60,
            'hr': 60*60,
            'day': 60*60*24,
            'week': 60*60*24*7,
            'fortnight': 60*60*24*7*2,
            'yr': 60*60*24*365,
            'ms': 0.001,
            'us': 0.000001,
            'ns': 0.000000001,
        },
        # Power
        J: {
            'kJ': 1000,
            'MJ': 1000000,
        }
    }

    for base in conversions :
        for unit in conversions[base] :
            locals()[unit] = (base * conversions[base][unit]).rename(unit)

    #### Create a shorthand for creating new units ####
    # Example:
    # # Create a `hand` unit:
    # hand = _('hand')
    #
    # # Create a `hand*foot` unit:
    # hand_feet = _('hand', 'foot')
    #
    # # Create a `hand*foot/season` unit:
    # hand_feet_per_season = _('hand', 'foot', season= -1)
    #
    def __new__(cls, name='', *units_keys, **dictionary):
            return UnitsGroup(name=name, *units_keys, **dictionary)
