"""See the README for examples of how to use this module.
"""
from math import isclose, exp, log, cos, sin
from .counter import Counter


class UnitsGroup:
    """The meat of unties. See the README for examples.
    """
    def __init__(self, name='', **dictionary):
        self.value = 1.0
        self.normal = 1.0
        self.units = Counter()
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
            self.value *= sec
            return self

        if self.units and sec.units and set(self.units) == set(sec.units):
            unit = list(self.units)[0]
            exp = self.units[unit] / sec.units[unit]
            if (sec.value != 0 or exp >= 0) and self.units == (sec**exp).units:
                if exp < 0 and exp > -1:
                    a = self.copy()
                    return self._inplace_join(sec)._inplace_units_of(1 / a)
                else:
                    self._inplace_join(sec)._inplace_units_of(sec**(1 + exp))
                    return self

        return self._inplace_join(sec)

    def __mul__(self, sec):
        return self.copy()._inplace_mul(sec)
    __rmul__ = __mul__

    def __pow__(self, num):
        if isinstance(num, UnitsGroup) and num.is_scalar():
            num = num.value
        first = self.copy()
        for unit in list(first.units):
            first.units[unit] *= num
        for name in list(first.full_name):
            first.full_name[name] *= num
        first.value **= num
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
        first.value += units_group.value
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
            raise Exception(string)
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
        first.value = abs(first.value)
        return first

    def __str__(self):
        if self.full_name:
            return str(self.value_in_units()) + str(self.full_name)
        return str(self.value_in_units())
    __repr__ = __str__

    def value_in_units(self):
        return self.value * self.normal

    # For numpy compatability
    def exp(self):
        return exp(self)

    def log(self):
        return log(self)

    def log10(self):
        return log(self, 10)

    def cos(self):
        return cos(self)

    def sin(self):
        return sin(self)

    def copy(self):
        """Return a copy of self.
        """
        first = UnitsGroup(**self.units)
        first.set_full_name(self.full_name)
        try:
            first.value = self.value.copy()
        except:
            first.value = self.value
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
        self.value *= units_group.value
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

    def rename(self, name):
        """Create a renamed copy of the units_group.

        Useful for creating new units:

            >>> hand = (4 * inch).rename('hand')
        """
        first = self.copy()
        first.full_name = Counter()
        first.full_name[name] = 1
        first.normal = self.value**-1
        return first

    def _inplace_standardized(self):
        self.normal = 1
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
        self.value = 1.0 / self.normal
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
            raise Exception('Incompatible units: ',
                            self.units,
                            ' and ',
                            units_group.units)

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
