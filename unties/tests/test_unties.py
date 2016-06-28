from unittest import TestCase
import math
import numpy as np
from unties import *
from scipy.optimize import fsolve

class TestUnties(TestCase):

    def assert_display_with_units_of(self, units_group, units):
        self.assertEqual(str(units_group), str(units_group(units)))

    def assert_display_equal(self, first_units_group, second_units_group):
        self.assertEqual(str(first_units_group), str(second_units_group))

    # Test Addition
    def test_add_commutative_law(self):
        self.assertEqual(1 * m + 5 * m, 5 * m + 1 * m)

    def test_can_add_scalar_units_group_and_number(self):
        scalar = m / m
        self.assertEqual(scalar + 1, 2)

    def test_can_add_number_and_scalar_units_group(self):
        scalar = m / m
        self.assertEqual(1 + scalar, 2)


    # Test Subtraction
    def test_sub_commutative_law(self):
        self.assertEqual(3 * m - 1 * m, -(1 * m - 3 * m))

    def test_can_subtract_scalar_units_group_and_number(self):
        scalar = m / m
        self.assertEqual(scalar - 1, 0)

    def test_can_subtract_number_and_scalar_units_group(self):
        scalar = m / m
        self.assertEqual(1 - scalar, 0)


    # Test multiplication
    def test_m_times_m_equals_m_squared(self):
        self.assertEqual(m * m, m**2)

    def test_mult_commutative_law(self):
        self.assertEqual(m * 2, 2 * m)

    def test_np_mult_unit(self):
        try:
            np.array([5 * m, 2 * ft, 3 * inch]) * cm
        except:
            self.fail("np array * unit raised an error unexpectedly!")

    def test_unit_mult_np(self):
        try:
            cm * np.array([5 * m, 2 * ft, 3 * inch])
        except:
            self.fail("unit * np array raised an error unexpectedly!")

    def test_mult_by_zero_to_get_zero(self):
        try:
            K * (0 / K)
        except:
            self.fail("K * (0 / K) raised an error unexpectedly!")

    def test_mult_by_zero_to_get_zero_2(self):
        try:
            (0 / K) * K
        except:
            self.fail("(0 / K) * K raised an error unexpectedly!")


    # Test Division
    def test_division_by_one_equals_self(self):
        self.assertEqual(inch, inch / 1)

    def test_division_by_self_equals_1(self):
        self.assertEqual(inch / inch, 1)

    def test_div_commutative_law(self):
        self.assertEqual(m / inch, 1 / (inch / m))

    def test_mi_per_hr_div_by_mi_leaves_per_hr(self):
        self.assertEqual(eval(str((mi / hr) / mi)), 1 / hr)

    def test_np_div_unit(self):
        try:
            np.array([5 * m, 2 * ft, 3 * inch]) / cm
        except:
            self.fail("np array / unit raised an error unexpectedly!")

    def test_unit_div_np(self):
        try:
            cm / np.array([5 * m, 2 * ft, 3 * inch])
        except:
            self.fail("unit / np array raised an error unexpectedly!")


    # Test Absolute Value
    def test_absolute_value_leaves_positive_positive(self):
        self.assertEqual(abs(m), m)

    def test_absolute_value_makes_negatives_positive(self):
        self.assertEqual(abs(-m), m)


    # Test comparators
    def test_one_meter_is_larger_than_one_foot(self):
        self.assertTrue(m > ft)

    def test_kph_is_less_than_mph(self):
        self.assertTrue(kph < mph)

    def test_ltet(self):
        self.assertTrue(kmol <= kmol)
        self.assertTrue(mol <= kmol)

    def test_gtet(self):
        self.assertTrue(kPa >= kPa)
        self.assertTrue(kPa >= Pa)

    def test_math_log_2_units_is_log_2(self):
        self.assertEqual(math.log(2), math.log(2 * atm / atm))

    def test_np_log_2_units_is_log_2(self):
        self.assertEqual(np.log(2), np.log(2 * atm / atm))

    def test_math_exp_2_units_is_exp_2(self):
        self.assertEqual(math.log(2), math.log(2 * atm / atm))

    def test_np_exp_2_units_is_exp_2(self):
        self.assertEqual(np.exp(2), np.exp(2 * atm / atm))

    def test_inch_is_not_equal_to_ft(self):
        self.assertNotEqual(inch, ft)

    def test_inch_is_not_equal_to_s(self):
        self.assertNotEqual(inch, s)

    def test_inch_is_not_equal_to_4(self):
        self.assertNotEqual(inch, 4)


    # Test Smart Conversion
    def test_rad_times_deg_is_deg_squared(self):
        self.assert_display_with_units_of(rad * deg, deg**2)

    def test_ft_times_yd_is_yd_squared(self):
        self.assert_display_with_units_of(ft * yd, yd**2)

    def test_ft_divided_by_yd_is_unitless_one_third(self):
        self.assertEqual(ft / yd, 1 / 3)

    def test_ft_times_acre_is_acre_to_the_one_and_a_half(self):
        self.assert_display_with_units_of(ft * acre, acre**1.5)

    def test_acre_times_ft_is_ft_cubed(self):
        self.assert_display_with_units_of(acre * ft, ft**3)

    def test_ft_times_gal_is_gal_to_the_four_thirds(self):
        self.assert_display_with_units_of(ft * gal, gal**(4 / 3))

    def test_gal_times_ft_is_ft_to_the_fourth(self):
        self.assert_display_with_units_of(gal * ft, ft**4)

    def test_acre_divided_by_ft_is_ft(self):
        self.assert_display_with_units_of(acre / ft, ft)

    def test_ft_divided_by_acre_is_inverse_ft(self):
        self.assert_display_with_units_of(ft / acre, 1 / ft)

    def test_gal_divided_by_ft_is_ft_squared(self):
        self.assert_display_with_units_of(gal / ft, ft**2)

    def test_cm_divided_by_gal_is_inverse_cm_squared(self):
        self.assert_display_with_units_of(cm / gal, 1 / cm**2)


    # Test Conversion
    def test_inch_equals_25_point_4_mm(self):
        self.assertEqual(inch, 25.4 * mm)

    def test_ft_equals_12_inches(self):
        self.assertEqual(ft, 12 * inch)

    def test_conversion_does_not_affect_value_kph_to_mph(self):
        self.assertEqual(eval(str(kph(mph))), kph)

    def test_conversion_does_not_affect_value_J_to_hp(self):
        self.assertEqual(eval(str(J(hp))), J)

    def test_conversion_does_not_affect_value_m_s_to_cm(self):
        self.assertEqual(eval(str(12 / s * m(cm))), 12 / s * m)

    def test_conversion_does_not_affect_value_kPa_to_hp(self):
        self.assertEqual(eval(str(12 * kPa(hp))), 12 * kPa)

    def test_conversion_does_not_affect_value_yr_to_hr(self):
        self.assertEqual(eval(str(yr(hr))), yr)

    def test_conversion_does_not_affect_value_custom_unit_to_m(self):
        b = UnitsGroup('b')
        self.assertEqual(eval(str(12 * b(m))), 12 * b)

    def test_converting_scalar_does_nothing(self):
        scalar = m / m
        self.assertEqual(scalar.value, scalar(inch).value)

    def test_specific_conversion(self):
        self.assertEqual(str((m / s)(km / min)), '0.06 * km / min')
        self.assertEqual(str((3 * m / m)(A)), '3.0')
        self.assertEqual(str((3 * ft / ft)(mmHg)), '3.0')
        self.assertEqual(str((3 * ft / s)(inch)), '36.00000000000001 * inch / s')

    def test_strange_conversions_hz_to_yr(self):
        self.assertEqual(eval(str(Hz(hr))), Hz)

    def test_strange_conversions_kg_to_yr(self):
        self.assertEqual(eval(str(kg(hr))), kg)

    def test_strange_conversions_acre_to_cm(self):
        self.assertEqual(eval(str(acre(cm))), acre)

    def test_strange_conversions_gpm_to_square_inch(self):
        self.assertEqual(eval(str((gal/mi)(inch**2))), gal/mi)

    def test_strange_conversions_gpm_to_inch(self):
        self.assertEqual(eval(str((gal/mi)(inch))), gal/mi)

    def test_strange_conversions_inch_fur_to_ft_square_bad_parentheses(self):
        self.assertEqual(eval(str(inch*fur(ft**2))), inch*fur)


    # Test string conversions
    def test_to_string(self):
        self.assertEqual(str(m), '1.0 * m')
        self.assertEqual(str(m * s * kg), '1.0 * kg * m * s')
        self.assertEqual(str(m**-1), '1.0 / m')
        self.assertEqual(str(1 / (s * kg * m)), '1.0 / (kg * m * s)')
        self.assertEqual(str(m / s), '1.0 * m / s')
        self.assertEqual(str(m * A * K / (mol *s * kg)), '1.0 * A * K * m / (kg * mol * s)')
        self.assertEqual(str(m**-1 * kg**-2 / A**-1), '1.0 * A / (kg**2 * m)')


    # Test custom units
    def test_custom_unit_equals_itself(self):
        self.assertEqual(UnitsGroup('b'), UnitsGroup('b'))

    def test_different_custom_units_are_not_equal(self):
        self.assertNotEqual(UnitsGroup('b'), UnitsGroup('bb'))


    # Test Copy
    def copy_does_not_change_unit(self):
        a = m
        b = a.copy()
        self.assertEqual(a, b)


    # Test Join
    def join_does_not_change_unit(self):
        a = m.copy()
        b = m.copy()
        a.join(ft / mol)
        self.assertEqual(a, b)


    # Test np.arrays
    def test_solve_np_array_with_unitify(self):
        def other(x):
            return x + 2.0 * mm
        def solve(x):
            return unitify(x * ft - m + other(x * ft)).value
        try:
            fsolve(solve, 3)
        except:
            self.fail("fsolve with units failed unexpectedly!")

    def test_solve_np_array_with_other_order(self):
        def other(x):
            return x + 2.0 * mm
        def solve(x):
            return (ft * x - m + other(ft * x)).value
        try:
            fsolve(solve, 3)
        except:
            self.fail("fsolve with units failed unexpectedly!")

    def test_solve_np_array_with_mixed_method_should_fail(self):
        def other(x):
            return x + 2.0 * mm
        def solve(x):
            return (ft * x - m + other(x * ft)).value
        try:
            fsolve(solve, 3)
            self.fail("fsolve should have failed!")
        except:
            pass
