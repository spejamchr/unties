"""See the README for examples of how to use this module.
"""
from math import isclose, exp, log, cos
from numpy import ndarray
from numbers import Number
from .counter import Counter

class UnitsGroup:
    """The meat of unties. See the README for examples.
    """
    def __init__(self, name='', *units_keys, **dictionary):
        self.value = 1.0
        self.normal = 1.0
        self.units = Counter()
        for key in units_keys:
            self.units[key] = 1
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

    def __mul__(self, units_group):
        first = self.copy()
        if isinstance(units_group, (Number, ndarray)):
            first.value *= units_group
            return first

        second = units_group.copy()
        if not first.units and not second.units:
            return first.join(second)

        exponents = [1/3, 1/2, 1, 2, 3, -3, -2, -1]
        for exponent in exponents:
            if  second == 0 and exponent < 0:
                continue
            if first.units == (second**exponent).units:
                return first.join(second)(second**(1 + exponent))

        exceptions = [-1/2, -1/3]
        for exception in exceptions:
            if  second == 0 and exception < 0:
                continue
            if first.units == (second**exception).units:
                return first.join(second)(1 / first)

        return first.join(second)
    __rmul__ = __mul__

    def __pow__(self, num):
        if isinstance(num, UnitsGroup) and num.scalar():
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
        if self.scalar():
            return num ** self.value
        else:
            raise TypeError('Exponent must be unitless')

    def __add__(self, units_group):
        units_group = (units_group*UnitsGroup())
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

    def __eq__(self, units_group):
        first = self.standardized()
        second = (units_group * UnitsGroup()).standardized()
        if first.value == 0 and second.value == 0:
            return True
        return isclose(first.value, second.value, rel_tol=1e-15) and first.units == second.units

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
            return str(self.value * self.normal) + str(self.full_name)
        return str(self.value * self.normal)
    __repr__ = __str__

    def exp(self):
        return exp(self)

    def log(self):
        return log(self)

    def log10(self):
        return log(self, 10)

    def cos(self):
        return cos(self)


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

    def compare(self, units_group, comparator):
        """Used to DRY the comparing code.
        """
        first = self.standardized()
        second = (units_group * UnitsGroup()).standardized()
        first.must_have_same_units_as(second)
        return comparator(first.value, second.value)

    def join(self, units_group):
        """Return a new units_group that is the product of the two given.
        """
        first = self.copy()
        first.value *= units_group.value
        first.normal *= units_group.normal
        for unit in list(units_group.units):
            first.units[unit] += units_group.units[unit]
        for name in list(units_group.full_name):
            first.full_name[name] += units_group.full_name[name]
        return first

    def set_full_name(self, full_name):
        """Manually set the full name of a units_group in-place.

        Used to copy and standardize units_groups.
        """
        self.full_name = Counter()
        for name in list(full_name):
            self.full_name[name] = full_name[name]
        return self

    def rename(self, name):
        """Rename the units_group in-place.

        Useful for creating new units:

            >>> hand = (4 * inch).rename('hand')
        """
        first = self.copy()
        first.full_name = Counter()
        first.full_name[name] = 1
        first.normal = self.value**-1
        return first

    def standardized(self):
        """Return first copy of self converted to standard base units.

        Example:

            >>> Btu.standardized()
            1055.05585262 * kg * m**2 / s**2
        """
        first = self.copy()
        first.normal = 1
        first.set_full_name(first.units)
        return first

    def normalized(self):
        """Return copy of self that is only 1 unit big.

        Example:

            >>> (32 * min).normalized()
            1.0 * min
        """
        first = self.copy()
        first.value = 1.0 / first.normal
        return first

    def scalar(self):
        """Return True if self is first simple scalar.
        """
        return not self.units and not self.full_name

    def unitless(self):
        """Return True if self is first unitless unit (like Radian).
        """
        return not self.units and self.full_name

    def must_have_same_units_as(self, units_group):
        """Checks that two units_groups have the same units
        """
        if not self.units == units_group.units:
            raise Exception('Incompatible units: ', self.units, ' and ', units_group.units)

    def units_of(self, units_group):
        """Convert from one unit to another, returning first new units_group.

        Takes: self        <UnitsGroup>
               units_group <UnitsGroup>

        Returns: <UnitsGroup>

        See the README for examples.
        """
        first = self.standardized()
        second = units_group.normalized()
        return first / second.standardized() * second

    def __call__(self, units_group):
        """Shorthand for the UnitsGroup#units_of() method.
        """
        return self.units_of(units_group)
