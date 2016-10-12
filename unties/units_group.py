"""See the README for examples of how to use this module.
"""
from math import isclose, exp, log, cos, sin
from unties.counter import Counter
import unties.utilities.errors as ue


class _Quantities(dict):
    def __setitem__(self, key, quantity_string):
        if key in self:
            quantity_string = self[key] + "/" + quantity_string
            del self[key]
        super().__setitem__(key, quantity_string)


class UnitsGroup:
    """The meat of unties. See the README for examples.
    """
    _quantities = _Quantities()  # Store unit quantities (length, time, etc.)
    _prefixes = {}  # Store all unit prefixes

    @classmethod
    def add_prefixes(cls, prefix_dict):
        """Add prefixes that will be applied to prefixed units.

        Prefixes do not apply retroactively, that is, they only apply to
        prefixed units created after the prefixes are added.

        Example:
            >>> UnitsGroup.add_prefixes({'ty': [10**-100, teeny]})
        """
        cls._prefixes.update(prefix_dict)

    @classmethod
    def base(cls, name, description, prefix=True):
        """Create a base unit (m, kg, s, etc).

        Be sure you want a base unit, and not a combination of other units
        (using `derived`) or a conversion from an existing unit (using
        `conversion`). Given m and kg as base units, density (kg/m**3) is a
        `derived` unit, and cm is a converted unit (100 * cm == m).

        It's usually best to use this instead of initiating a new base with the
        `__init__` method. This adds your base to the `units_dict`, and can add
        prefixes to your base

        Example:
            >>> shu = UnitsGroup.base('shu', 'Scoville heat unit')
            >>> shu
            1.0 * shu  # Scoville heat unit
        """
        units_group = cls(name, description)
        units_group._save_unit(name)
        if prefix:
            units_group._prefixer()
        return units_group

    def derived(self, name, description, prefix=True, _manual_quantity=''):
        """Create a derived unit (m/s, kg/m**3, etc).

        Example:
            >>> bz = (m/s).derived('bz', 'benz', prefix=False)
            >>> bz
            1.0 * bz  # benz [speed/velocity]
        """
        units_group = self.rename(name, description)
        units_group._manual_quantity = _manual_quantity
        units_group._save_unit(name)
        if prefix:
            units_group._prefixer()
        return units_group

    def conversion(self, name, description, factor, prefix=False):
        """Create a converted unit (ft, hour, millivolt, etc).

        Example:
            >>> hh = inch.conversion('hh', 'hand', 4)
            >>> hh
            1.0 * hh  # hand [length]
            >>> hh(inch)
            4.0 * inch
        """
        units_group = (self * factor).rename(name, description)
        units_group._manual_quantity = self._manual_quantity
        units_group._save_unit(name)
        if prefix:
            units_group._prefixer()
        return units_group

    def constant(self, name, description):
        """Create a constant (c = speed of light, g = grav. const., etc).

        Example:
            >>> Rk = (h / q**2)(ohm).constant('Rk', 'von Klitzing constant')
            >>> Rk
            25812.807456116425 * ohm  # von Klitzing constant [electr...
        """
        self.description = description
        self._locals[name] = self
        return self

    def add_quantity(self, quantity):
        """Add a quantity to the table of defined quantities.

        Since unit quantities are calculated on the fly, newly added quantites
        will apply to previously created units.

        Example:
            >>> (m/s**3).add_quantity('jerk')
            >>> (ft/hr**3).quantity()
            'jerk'
        """
        self._quantities[str(self.units)] = quantity

    def _save_unit(self, name):
        self._locals[name] = self

    def _prefixer(self):
        """Add prefixes to a unit.
        """
        for prefix in self._prefixes:
            prefixed_symbol = prefix + list(self.full_name)[0]
            description = self._prefixes[prefix][1] + self.description.lower()
            units_group = (self * self._prefixes[prefix][0])
            units_group.rename(prefixed_symbol, description)
            units_group._manual_quantity = self._manual_quantity
            units_group._save_unit(prefixed_symbol)

    def __init__(self, name='', description='', **dictionary):
        self.magnitude = 1.0
        self.normal = 1.0
        self.units = Counter()
        self.description = description
        self._manual_quantity = ''
        if not self.units and name:
            self.units[name] = 1
        for key in list(dictionary):
            self.units[key] = dictionary[key]

        self.full_name = Counter()
        if name:
            self.full_name[name] = 1
        else:
            for name in list(self.units):
                self.full_name[name] = self.units[name]

    def __truediv__(self, units_group):
        return self * units_group**-1

    def __rtruediv__(self, num):
        return num * self**-1

    def _inplace_mul(self, sec):
        if not isinstance(sec, UnitsGroup):  # Probably a Number or numpy array
            self.magnitude *= sec
            return self

        if self.units and sec.units and set(self.units) == set(sec.units):
            unit = list(self.units)[0]
            exp = self.units[unit] / sec.units[unit]
            valid_exp = sec.magnitude != 0 or exp >= 0
            if valid_exp and self.units == (sec**exp).units:
                if exp < 0 and exp > -1:
                    a = self.copy()
                    return self._inplace_join(sec)._inplace_units_of(1 / a)
                else:
                    self._inplace_join(sec)._inplace_units_of(sec**(1 + exp))
                    return self

        return self._inplace_join(sec)

    def __mul__(self, sec):
        if not isinstance(sec, UnitsGroup):
            return sec * self
        return self.__rmul__(sec)

    def __rmul__(self, sec):
        return self.copy()._inplace_mul(sec)

    def __pow__(self, num):
        if isinstance(num, UnitsGroup) and num.is_scalar():
            num = num.value
        first = self.copy()
        for unit in list(first.units):
            first.units[unit] *= num
        for name in list(first.full_name):
            first.full_name[name] *= num
        first.magnitude **= num
        first.normal **= num
        return first

    def __rpow__(self, num):
        if self.is_scalar():
            return num ** self.value
        else:
            raise TypeError('Exponent must be unitless')

    def __add__(self, units_group):
        if not isinstance(units_group, UnitsGroup):
            units_group = UnitsGroup() * units_group
        self.must_have_same_units_as(units_group)
        first = self.copy()
        first.magnitude += units_group.value * first.normal
        return first
    __radd__ = __add__

    def __sub__(self, units_group):
        return -units_group + self

    def __rsub__(self, units_group):
        return -self + units_group

    def __neg__(self):
        return self * -1

    def __float__(self):
        if self.units:
            string = 'Must be unitless: ' + str(self.standardized())
            raise TypeError(string)
        return self.value

    def __eq__(self, other):
        if not isinstance(other, UnitsGroup):
            other = UnitsGroup() * other

        return (self.units == other.units and
                isclose(self.value, other.value, rel_tol=1e-15))

    def __ne__(self, units_group):
        return not self == units_group

    def __gt__(self, units_group):
        return self.compare(units_group, lambda s, o: s > o)

    def __lt__(self, units_group):
        return self.compare(units_group, lambda s, o: s < o)

    def __ge__(self, units_group):
        return self.compare(units_group, lambda s, o: s >= o)

    def __le__(self, units_group):
        return self.compare(units_group, lambda s, o: s <= o)

    def __abs__(self):
        first = self.copy()
        first.magnitude = abs(first.magnitude)
        return first

    def __str__(self):
        s = str(self.magnitude)
        if self.full_name:
            s += str(self.full_name)
        if self.description:
            s += '  # ' + self.description
            if self.quantity():
                s += ' [' + self.quantity() + ']'
        return s
    __repr__ = __str__

    @property
    def value(self):
        return self.magnitude / self.normal

    def quantity(self):
        """Return the physical quantity measured by this units_group.

        Example:
            >>> (3 * hp / mmHg).quantity()
            'volumetric flow'
        """
        units = str(self.units)
        if self._manual_quantity:
            return self._manual_quantity
        elif units in self._quantities:
            return self._quantities[units]

    def exp(self):
        """For numpy compatability.
        """
        return exp(self)

    def log(self):
        """For numpy compatability.
        """
        return log(self)

    def log10(self):
        """For numpy compatability.
        """
        return log(self, 10)

    def cos(self):
        """For numpy compatability.
        """
        return cos(self)

    def sin(self):
        """For numpy compatability.
        """
        return sin(self)

    def copy(self):
        """Return a copy of self.
        """
        first = UnitsGroup(**self.units)
        first.set_full_name(self.full_name)
        try:
            first.magnitude = self.magnitude.copy()
        except:
            first.magnitude = self.magnitude
        first.normal = self.normal
        return first

    def compare(self, other, comparator):
        """Used to DRY the comparing code.
        """
        if not isinstance(other, UnitsGroup):
            other = UnitsGroup() * other

        self.must_have_same_units_as(other)
        return comparator(self.value, other.value)

    def _inplace_join(self, units_group):
        self.magnitude *= units_group.magnitude
        self.normal *= units_group.normal
        for unit in list(units_group.units):
            self.units[unit] += units_group.units[unit]
        for name in list(units_group.full_name):
            self.full_name[name] += units_group.full_name[name]
        return self

    def join(self, units_group):
        """Return a new units_group that is the product of the two given.
        """
        return self.copy()._inplace_join(units_group)

    def set_full_name(self, full_name):
        """Manually set the full name of a units_group in-place.

        Used to copy and standardize units_groups.
        """
        self.full_name = Counter()
        for name in list(full_name):
            self.full_name[name] = full_name[name]
        return self

    def rename(self, name='', description=''):
        """Rename a units_group in-place.

        Useful for creating new units:

            >>> hh = (4 * inch).rename('hh', 'hand')
            >>> hh
            1.0 * hh  # hand [length]
        """
        self.description = description
        self.full_name = Counter()
        self.full_name[name] = 1
        self.normal /= self.magnitude
        self.magnitude = 1.0
        return self

    def _inplace_standardized(self):
        self.magnitude = self.value
        self.normal = 1.0
        self.set_full_name(self.units)
        return self

    def standardized(self):
        """Return a copy of self converted to standard base units.

        Example:

            >>> Btu.standardized()
            1055.05585262 * kg * m**2 / s**2
        """
        return self.copy()._inplace_standardized()

    def _inplace_normalized(self):
        self.magnitude = 1.0
        return self

    def normalized(self):
        """Return copy of self that is only 1 unit big.

        Example:

            >>> (32 * minute).normalized()
            1.0 * minute
        """
        return self.copy()._inplace_normalized()

    def is_scalar(self):
        """Return True if self is a simple scalar (like m/m).
        """
        return not self.units and not self.full_name

    def is_dimensionless(self):
        """Return True if self is a dimensionless unit (like Radian).
        """
        return not self.units and self.full_name

    def must_have_same_units_as(self, units_group):
        """Checks that two units_groups have the same units
        """
        if not self.units == units_group.units:
            raise ue.IncompatibleUnitsError(self, units_group)

    def _inplace_units_of(self, units_group):
        self._inplace_standardized()
        units_group = units_group.normalized()

        self._inplace_mul((units_group**-1)._inplace_standardized())
        self._inplace_mul(units_group)
        return self

    def units_of(self, units_group):
        """Convert from one unit to another, returning first new units_group.

        Takes: self        <UnitsGroup>
               units_group <UnitsGroup>

        Returns: <UnitsGroup>

        See the README for examples.
        """
        return self.copy()._inplace_units_of(units_group)

    def __call__(self, units_group):
        """Shorthand for the UnitsGroup#units_of() method.
        """
        return self.units_of(units_group)
