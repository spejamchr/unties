from numbers import Number
from .counter import Counter

class UnitsGroup :
    def __init__(self, name='', *units_keys, **dictionary) :
        self.value = 1
        self.normal = 1
        self.units = Counter()
        for key in units_keys :
            self.units[key] = 1
        if not self.units and name :
            self.units[name] = 1
        for key in list(dictionary) :
            self.units[key] = dictionary[key]

        self.full_name = Counter()
        if name :
            self.full_name[name] = 1
        else :
            for name in list(self.units) :
                self.full_name[name] = self.units[name]

    def set_full_name(self, full_name) :
        self.full_name = Counter()
        for name in list(full_name) :
            self.full_name[name] = full_name[name]
        return self

    def rename(self, name) :
        a = self.copy()
        a.full_name = Counter()
        a.full_name[name] = 1
        a.normal = self.value**-1
        return a

    def __truediv__(self, unit_group) :
        return self * unit_group**-1

    def __rtruediv__(self, num) :
        return num * self**-1

    def __mul__(self, unit_group) :
        a = self.copy()
        if isinstance(unit_group, Number) :
            a.value *= unit_group
            return a
        b = unit_group.copy()
        if a.units == b.units :
            return a.join(b).standardized()(a**2)
        if a.units == (1/b).units :
            return a.join(b).standardized()
        if a.units == (1/b**2).units :
            return a.join(b)(a**0.5)
        if a.units == (1/b**0.5).units :
            return a.join(b).standardized()(1/a)
        return a.join(b)
    __rmul__ = __mul__

    def __pow__(self, num) :
        a = self.copy()
        for unit in list(a.units) :
            a.units[unit] *= num
        for name in list(a.full_name) :
            a.full_name[name] *= num
        a.value **= num
        a.normal **= num
        return a

    def __add__(self, unit_group) :
        if self.units != unit_group.units :
            raise Exception('Incompatible units')
        a = self.copy()
        a.value += unit_group.value
        return a

    def __sub__(self, unit_group) :
        return -unit_group + self

    def __neg__(self) :
        return self * -1

    def __float__(self) :
        if self.units.present() :
            raise Exception('Must be unitless')
        return self.value

    def __eq__(self, units_group) :
        a = self.standardized()
        b = units_group.standardized()
        return a.value == b.value and a.units == b.units

    def join(self, units_group) :
        a = self.copy()
        a.value *= units_group.value
        a.normal *= units_group.normal
        for unit in list(units_group.units) :
            a.units[unit] += units_group.units[unit]
        for name in list(units_group.full_name) :
            a.full_name[name] += units_group.full_name[name]
        return a

    def __str__(self) :
        if self.units :
            return str(self.value * self.normal) + ' * ' + str(self.full_name)
            # return str(self.value) + ' * ' + str(self.units)
        return str(self.value)
    __repr__ = __str__


    def copy(self) :
        """Return a copy of self."""
        a = UnitsGroup(**self.units)
        a.set_full_name(self.full_name)
        a.value = self.value
        a.normal = self.normal
        return a

    def standardized(self) :
        """Return a copy of self converted to standard base units"""
        a = self.copy()
        a.normal = 1
        a.set_full_name(a.units)
        return a

    def normalized(self) :
        """Return a copy of self that is only 1 unit big.

        Example:

            >>> (32*_.min).normalized()
            1.0 * min
        """
        a = self.copy()
        a.value = 1/a.normal
        return a

    def units_of(self, unit_group) :
        """Convert from one unit to another, returning a new units_group.

        Takes: self        <UnitsGroup>
               units_group <UnitsGroup>

        Returns: <UnitsGroup>

        Examples:

        Convert 'ft' to 'inch'

            >>> _.ft.units_of(_.inch)
            12.000000000000002 * inch

        Convert 11.5 'ft' to 'inch'

            >>> 11.5 * _.ft.units_of(_.inch)
            138.00000000000003 * inch

        As you can see from the examples, the decimals are not perfectly exact

        You can call units with another unit as the argument as shorthand for
        conversion. So you can do:

            >>> _.ft(_.inch)
            12.000000000000002 * inch

            >>> 11.5*_.ft(_.inch)
            138.00000000000003 * inch

        Each unit_group does *not* have to have the same dimensions:

            >>> (_.m/_.s)(_.inch)
            39.37007874015748 * inch * s**-1

            >>> _.hp(_.cal)
            178.1073544430114 * cal * s**-1

        But this isn't always very useful:

            >>> (_.m**2)(_.inch**3)
            61023.74409473229 * inch**3 * m**-1

            >>> _.hp(_.Pa)
            745.699871582 * Pa * m**3 * s**-1

        Multiple units should be grouped:

            >>> (_.inch*_.fur)(_.m**2)
            5.1096672 * m**2

        or else:

            >>> _.inch*_.fur(_.m**2)
            201.16799999999998 * inch * m
        """
        a = self.copy().standardized()
        b = unit_group.copy().normalized().standardized()
        c = a/b

        c.value /= c.normal
        b = unit_group.copy()
        b.value = 1/b.normal
        c *= b
        c.normal = unit_group.normal
        return c

    def __call__(self, unit_group) :
        """Shorthand for the <units_of> method.

        Simply call the units_group with a new units_group
        Examples:

        Convert 'ft/s' to 'fur/fortnight'

            >>> (_.ft/_.s)(_.fur/_.fortnight)
            1832.7272727272723 * fortnight**-1 * fur

        Very simple. Maybe too simple.
        """
        return self.units_of(unit_group)
