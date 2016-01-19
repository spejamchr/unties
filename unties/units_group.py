from numbers import Number
from .counter import Counter

class UnitsGroup :
    def __init__(self, name='', *units_keys, **dictionary) :
        self.value = 1
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
        return a.join(b)
    __rmul__ = __mul__

    def __pow__(self, num) :
        a = self.copy()
        for unit in list(a.units) :
            a.units[unit] *= num
        for name in list(a.full_name) :
            a.full_name[name] *= num
        a.value **= num
        return a

    def __add__(self, unit_group) :
        if self.units != unit_group.units :
            raise Exception('Incompatible units')
        a, b = self.copy(), unit_group.copy()
        a.value += b.value
        return a

    def __sub__(self, unit_group) :
        return -unit_group + self

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
        for name in list(units_group.full_name) :
            self.full_name[name] += units_group.full_name[name]
        return self

    def __str__(self) :
        if self.units :
            return str(self.value) + ' * ' + str(self.units)
        return str(self.value)

    def copy(self) :
        a = UnitsGroup(**self.units)
        a.set_full_name(self.full_name)
        a.value = self.value
        return a

    #### Conversion Method ####
    #
    # Takes: self <UnitsGroup>
    #        units_group <UnitsGroup>
    #
    # Returns: <str>
    #
    # To convert to a new UnitGroup, we just divide our original by the new
    # UnitGroup. Very simple. However, this returns just an float, *not* a new
    # UnitGroup, sadly. We won't return the float.
    #
    # Instead, we return a string of valid python code that, when evaluated,
    # returns a UnitsGroup equivalent to <self>. This is nice, because we can
    # either print the string and show the result, and someone seeing the result
    # can copy/paste it into their own version of unties and use it.
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
    def units_of(self, unit_group) :
        a = self / unit_group
        return str(a) + ' * ' + str(unit_group.full_name)

    #### Shorthand for the <units_of> method ####
    # Simply call the units_group with a new units_group
    # Examples:
    #
    ### Convert 'ft/s' to 'fur/fortnight'
    #
    # (_.ft/_.s)(_.fur/_.fortnight)
    #  #=> '1832.727272727273 * (0.00016630952380952381 * _.m * _.s**-1)'
    #
    # Very simple. Maybe too simple.
    #
    def __call__(self, unit_group) :
        return self.units_of(unit_group)
