from numbers import Number

class Counter(dict) :
    def __missing__(self, key) :
        return 0

    def __setitem__(self,key,value) :
        super().__setitem__(key,value)
        if self[key] == 0 :
            self.pop(key)

    def __str__(self) :
        strings = [str(x) + self.exp_str(x) for x in sorted(list(self))]
        return ' * '.join(strings)

    def exp_str(self, key) :
        if self[key] == 1 :
            return ''
        else :
            return '**' + str(self[key])

    def present(self) :
        return self

class UnitsGroup :
    def __init__(self, value=1.0, units_keys=[], dictionary={}) :
        self.value = float(value)
        self.units = Counter()
        if isinstance(units_keys, str) :
            self.units[units_keys] = 1
        else :
            for key in units_keys :
                self.units[key] = 1
        for key in list(dictionary) :
            self.units[key] = dictionary[key]

    def __truediv__(self, unit_group) :
        numer = self.copy()
        if isinstance(unit_group, Number) :
            numer.value /= unit_group
            return numer
        denom = unit_group.copy() ** -1
        return numer.join(denom)

    def __rtruediv__(self, num) :
        denom = self.copy() ** -1
        denom.value *= num
        return denom

    def __mul__(self, unit_group) :
        a = self.copy()
        if isinstance(unit_group, Number) :
            a.value *= unit_group
            return a
        b = unit_group.copy()
        return a.join(b)
    __rmul__ = __mul__

    def __pow__(self, num) :
        a = self.copy()
        for unit in list(a.units) :
            a.units[unit] *= num
        a.value **= num
        return a

    def __add__(self, unit_group) :
        if self.units != unit_group.units :
            raise Exception('Cannot add dislike units')
        a = self.copy()
        b = unit_group.copy()
        a.value += b.value
        return a

    def __radd__(self, num) :
        # You can't add a unitless number and a unit number
        raise Exception('Cannot add dislike units')

    def __sub__(self, unit_group) :
        if self.units != unit_group.units :
            raise Exception('Cannot subtract dislike units')
        a = self.copy()
        b = unit_group.copy()
        a.value -= b.value
        return a

    def __rsub__(self, num) :
        # You can't subtract a unitless number and a unit number
        raise Exception('Cannot subtract dislike units')

    def __neg__(self) :
        return self * -1

    def __float__(self) :
        if self.units.present() :
            raise Exception('Must be unitless')
        return self.value

    # If we use Python's __eq__ method, we won't be able to use UnitGroups as
    # keys in our Counter class. So let's just do it this way.
    def eq(self, units_group) :
        return self.value == units_group.value and self.units == units_group.units

    def join(self, units_group) :
        self.value *= units_group.value
        for unit in list(units_group.units) :
            self.units[unit] += units_group.units[unit]
        return self

    def __str__(self) :
        if self.units :
            return str(self.value) + ' * ' + str(self.units)
        return str(self.value)

    def old_str(self) :
        return str(self.value) + ' ' + str(self.units)

    def copy(self) :
        return UnitsGroup(value=self.value, dictionary=self.units)

    #### Conversion Method ####
    #
    # Takes: self <UnitsGroup>
    #        units_group <UnitsGroup>
    #
    # Returns: <str>
    #
    # To convert to a new UnitGroup, we just divide our original by the new
    # UnitGroup. Very simple. However, this returns just an float, *not* a new
    # UnitGroup, sadly. We won't return the float
    #
    # Instead, we return a string of valid python code that, when evaluated,
    # returns a UnitsGroup equivalent to <self>. This is nice, because we can
    # either print the string and show the result, and someone seeing the result
    # can copy/paste it into their own version of unties and us it.
    #
    # TODO: Implement this method with some type of Converter class, that can
    #       return a smarter object so that it can be multiplied by other units,
    #       or be printed as a string.
    #
    # Examples:
    #
    ### Convert 'ft' to 'inch'
    #
    # _.ft.units_of(_.inch)
    # #=> '12.000000000000002 * (0.0254 * _.m)'
    #
    ### Convert 12.5 'ft' to 'inch'
    #
    # (11.5 * _.ft).units_of(_.inch)
    # #=> '138.00000000000003 * (0.0254 * _.m)'
    #
    # # As you can see fro the examples, the decimals are not perfectly exact
    #
    ### Each unit_group does *not* have to have the same dimensions:
    #
    # (_.m/_.s).units_of(_.inch)
    # #=> '39.37007874015748 * _.s**-1 * (0.0254 * _.m)'
    #
    # But this isn't always very useful:
    #
    # (_.m**2).units_of(_.inch**3)
    # #=> '61023.74409473229 * _.m**-1 * (1.6387064e-05 * _.m**3)'
    #
    ### Multiple units have to be grouped:
    #
    # (_.inch*_.fur).units_of(_.m**2)
    # #=> '5.1096672 * (1.0 * _.m**2)'
    #
    # # or else:
    # _.inch*_.fur.units_of(_.m**2)
    # #=> Exception: AttributeError: 'str' object has no attribute 'copy'
    #
    # # This is because methods have higher priority than the <*> operator
    #
    ### Optionally takes a string representing the units of your units_group:
    #
    # _.ft(_.inch, '_.inch')
    # #=> '12.000000000000002 * (_.inch)'
    #
    # # but this is easily misused:
    #
    # _.ft(_.inch, '_.ltyr')
    # #=> '12.000000000000002 * (_.ltyr)'
    #
    def units_of(self, unit_group, string='') :
        a = self / unit_group
        if string :
            return str(a) + ' * (' + string + ')'
        return str(a) + ' * (' + str(unit_group) + ')'

    #### Shorthand for the <units_of> method ####
    # Simply call the units_group with a new units_group
    # Examples:
    #
    ### Convert 'ft/s' to 'fur/fortnight'
    # (ft/s)(fur/fortnight)
    #
    # Very simple. Maybe too simple.
    #
    def __call__(self, unit_group, string='') :
        return self.units_of(unit_group, string)

class Units :
    # I don't want to import math just for this...
    pi = 3.14159265358979323846264338327950288419716939937510

    #### Initialize Base Units ####
    m   = UnitsGroup(1, '_.m')    # meter for length
    kg  = UnitsGroup(1, '_.kg')   # kilogram for mass
    s   = UnitsGroup(1, '_.s')    # second for time
    A   = UnitsGroup(1, '_.A')    # ampere for electric current
    K   = UnitsGroup(1, '_.K')    # kelvin for temperature
    cd  = UnitsGroup(1, '_.cd')   # candela for luminous intensity
    mol = UnitsGroup(1, '_.mol')  # mole for the amount of substance

    #### Initialize Derived Units ####
    # Official SI derived units
    N = kg * m / s**2   # Newton    (force)
    J = N * m           # Joule     (energy)
    Pa = N / m**2       # Pascal    (pressure)
    Hz = s**-1          # Hertz     (frequency)
    rad = m / m         # Radian    (angle)             [unitless]
    W = J / s           # Watt      (power)
    C = s * A           # Coulomb   (electric charge)
    V = W / A           # Volt      (voltage)
    F = C / V           # Farad     (capacitance)
    ohm = V / A         # Ohm       (electrical resistance)
    S = 1 / ohm         # Siemen    (electrical conductance)
    Wb =  J / A         # Weber     (magnetic flux)
    T = V * s / m**2    # Tesla     (magnetic field strength)
    H = V * s / A       # Henry     (inductance)

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
            'kmol': 1000,   # Kilomol
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

    for base_unit in conversions :
        for unit in conversions[base_unit] :
            locals()[unit] = base_unit * conversions[base_unit][unit]

    # print(__units)

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
    def __new__(cls, *units_keys, **dictionary):
            return UnitsGroup(1, units_keys, dictionary)

# Follow the calculator pattern of _.<unit>
_ = Units

class Test :
    def perform(self) :
        print('Liter:   ', L)
        print('Newton:  ', N)
        print('Joule:   ', J)
        print('Pascal:  ', Pa)
        print('Hertz:   ', Hz)
        print('Radian:  ', rad)
        print('Watt:    ', W)
        print('Coulomb: ', C)
        print('Volt:    ', V)
        print('Farad:   ', F)
