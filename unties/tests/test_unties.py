from unittest import TestCase

from unties import _

class TestUnties(TestCase):

    # Test Addition
    def test_add_commutative_law(self):
        self.assertTrue(1*_.m + 5*_.m == 5*_.m + 1*_.m)

    def test_can_add_scalar_units_group_and_number(self):
        scalar = _.m/_.m
        self.assertTrue(scalar + 1 == 2)

    def test_can_add_number_and_scalar_units_group(self):
        scalar = _.m/_.m
        self.assertTrue(1 + scalar == 2)


    # Test Subtraction
    def test_sub_commutative_law(self):
        self.assertTrue(3*_.m - 1*_.m == -(1*_.m - 3*_.m))

    def test_can_subtract_scalar_units_group_and_number(self):
        scalar = _.m/_.m
        self.assertTrue(scalar - 1 == 0)

    def test_can_subtract_number_and_scalar_units_group(self):
        scalar = _.m/_.m
        self.assertTrue(1 - scalar == 0)


    # Test Division
    def test_division_by_one_equals_self(self):
        self.assertTrue(_.inch == _.inch/1)

    def test_division_by_self_equals_1(self):
        self.assertTrue(_.inch/_.inch == 1)

    def test_div_commutative_law(self):
        self.assertTrue(_.m/_.inch == 1/(_.inch/_.m))


    # Test multiplication
    def test_m_times_m_equals_m_squared(self):
        self.assertTrue(_.m*_.m == _.m**2)

    def test_mult_commutative_law(self):
        self.assertTrue(_.m*2 == 2*_.m)

    # Test Conversion
    def test_inch_equals_25_point_4_mm(self):
        self.assertTrue(_.inch == 25.4 * _.mm)

    def test_conversion_does_not_affect_value_kph_to_mph(self):
        self.assertTrue(12*_.kph(_.mph) == 12*_.kph)

    def test_conversion_does_not_affect_value_J_to_hp(self):
        self.assertTrue(12*_.J(_.hp) == 12*_.J)

    def test_conversion_does_not_affect_value_m_s_to_cm(self):
        self.assertTrue(12/_.s*_.m(_.cm) == 12/_.s*_.m)

    def test_conversion_does_not_affect_value_kPa_to_hp(self):
        self.assertTrue(12*_.kPa(_.hp) == 12*_.kPa)

    def test_conversion_does_not_affect_value_custom_unit_to_m(self):
        b = _('b')
        self.assertTrue(12*b(_.m) == 12*b)

    def test_converting_scalar_does_nothing(self):
        scalar = _.m/_.m
        self.assertTrue(scalar.value == scalar(_.inch).value)


    # Test custom units
    def test_custom_unit_equals_itself(self):
        self.assertTrue(_('b') == _('b'))

    def test_different_custom_units_are_not_equal(self):
        self.assertTrue(_('b') != _('bb'))


    # Test Copy
    def copy_does_not_change_unit(self):
        a = _.m
        b = a.copy()
        assertTrue(a == b)


    # Test Join
    def join_does_not_change_unit(self):
        a = _.m.copy()
        b = _.m.copy()
        a.join(_.ft/_.mol)
        assertTrue(a == b)
