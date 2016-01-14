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
        return '*'.join(strings)

    def exp_str(self, key) :
        if self[key] == 1 :
            return ''
        else :
            return '^' + str(self[key])

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

    def join(self, units_group) :
        self.value *= units_group.value
        for unit in list(units_group.units) :
            self.units[unit] += units_group.units[unit]
        return self

    def __str__(self) :
        return str(self.value) + ' ' + str(self.units)
        # return "*".join(str(unit) for unit in self.units)

    def copy(self) :
        return UnitsGroup(value=self.value, dictionary=self.units)

class Units :
    # I don't want to import math...
    pi = 3.14159265358979323846264338327950288419716939937510

    #### Initialize Base Units ####
    m = UnitsGroup(1, 'meter')      # meter for length
    kg = UnitsGroup(1, 'kilogram')  # kilogram for mass
    s = UnitsGroup(1, 'second')     # second for time
    A = UnitsGroup(1, 'ampere')     # ampere for electric current
    K = UnitsGroup(1, 'kelvin')     # kelvin for temperature
    cd = UnitsGroup(1, 'candela')   # candela for luminous intensity
    mol = UnitsGroup(1, 'mole')     # mole for the amount of substance

    #### Initialize Derived Units ####
    L = m ** 3 / 1000   # Liter     (volume)
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
    Cc = 8987551787.36 * kg * m**3 / (A**2 * s**4)      # Coulomb's constant
    Cc = c**2 * 10**-7 * H / m


    g = 9.80665 * m / s**2                              # Acceleration of gravity
    Gc = 6.67408 * 10**-11 * N * m**2 / kg**2           # Gravitational constant
    h = 6.626070040 * 10**-34 * J * s                   # Planck's constant
    Me = 9.10938356 * 10**-31 * kg                      # Electron rest mass
    Mn = 1.674927471 * 10**-27 * kg                     # Neutron rest mass
    Mp = 1.672621777 * 10**-27 * kg                     # Proton rest mass
    Na = 6.022140857 * 10**23 / mol                     # Avogadro constant
    q = 1.6021766208 * 10**-19 * C                      # Electron charge

    # Defined constants
    hbar = h / (2 * pi)                                 # Reduced Planck's constant
    u0 = 4 * pi * 10-7 * N / A**2                         # Vacuum permeability
    kb = Rc / Na                                        # Boltzmann's constant
    ub = q * hbar / (2 * Me)                            # Bohr magneton
    Rb = 4 * pi * u0 * hbar**2 / (Me * q**2)            # Bohr radius
    Rdb = Me * q**4 / (8 * u0**2 * h**3 * c)            # Rydberg Constant

    #### Initialize Conversion Units ####
    conversions = {
        # Length
        m: {
            'mm': 0.001,
            'cm': 0.01,
            'km': 1000,
            'in': 0.0254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mi': 1609.344,
            'furlong': 201.168,
        },
        # Pressure
        Pa: {
            'atm': 101325,
            'mmHg': 133.322387415,
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
