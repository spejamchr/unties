from unittest import TestCase
import math
import numpy as np
from unties import *
from scipy.optimize import fsolve
from unties.errors import *

def _deep_map(func, *args):
    """Like map, but recursively enters iterables

    Ex:

        >>> _deep_map(lambda a, b: a + b,
                      (1, 2, (3, (4,), 5)),
                      (10, 20, (30, (40,), 50)))
        [11, 22, [33, [44], 55]]

    """
    try:
        return [_deep_map(func, *z) for z in zip(*args)]
    except TypeError:
        return func(*args)


class TestUnties(TestCase):

    def assert_display_with_units_of(self, units_group, units):
        self.assertEqual(units_group.full_name, units.full_name)

    # Test Addition
    def test_add_commutative_law(self):
        self.assertEqual(1 * m + 5 * m, 5 * m + 1 * m)

    def test_can_add_scalar_units_group_and_number(self):
        scalar = m / m
        self.assertEqual(scalar + 1, 2)

    def test_can_add_number_and_scalar_units_group(self):
        scalar = m / m
        self.assertEqual(1 + scalar, 2)

    # Test Subtraction #
    ####################
    def test_sub_commutative_law(self):
        self.assertEqual(3 * m - 1 * m, -(1 * m - 3 * m))

    def test_can_subtract_scalar_units_group_and_number(self):
        scalar = m / m
        self.assertEqual(scalar - 1, 0)

    def test_can_subtract_number_and_scalar_units_group(self):
        scalar = m / m
        self.assertEqual(1 - scalar, 0)

    # Test multiplication #
    #######################
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

    # Test Division #
    #################
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

    # Test Absolute Value #
    #######################
    def test_absolute_value_leaves_positive_positive(self):
        self.assertEqual(abs(m), m)

    def test_absolute_value_makes_negatives_positive(self):
        self.assertEqual(abs(-m), m)

    # Test comparators #
    ####################
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

    def test_np_log10_2_units_is_log10_2(self):
        self.assertEqual(np.log10(100), np.log10(100 * atm/atm))

    def test_np_cos_2_units_is_cos_2(self):
        self.assertEqual(np.cos(2), np.cos(2 * atm/atm))

    def test_np_sin_2_units_is_sin_2(self):
        self.assertEqual(np.sin(2), np.sin(2 * atm/atm))

    def test_inch_is_not_equal_to_ft(self):
        self.assertNotEqual(inch, ft)

    def test_inch_is_not_equal_to_s(self):
        self.assertNotEqual(inch, s)

    def test_inch_is_not_equal_to_4(self):
        self.assertNotEqual(inch, 4)

    # Test Smart Conversion #
    #########################
    def test_ft_times_yd_is_yd_squared(self):
        self.assert_display_with_units_of(ft * yd, yd**2.0)

    def test_ft_divided_by_yd_is_unitless_one_third(self):
        self.assertEqual(ft / yd, 1 / 3)

    def test_ft_times_acre_is_acre_to_the_one_and_a_half(self):
        self.assert_display_with_units_of(ft * acre, acre**1.5)

    def test_acre_times_ft_is_ft_cubed(self):
        self.assert_display_with_units_of(acre * ft, ft**3.0)

    def test_ft_times_gal_is_gal_to_the_four_thirds(self):
        self.assert_display_with_units_of(ft * gal, gal**(4 / 3))

    def test_gal_times_ft_is_ft_to_the_fourth(self):
        self.assert_display_with_units_of(gal * ft, ft**4.0)

    def test_acre_divided_by_ft_is_ft(self):
        self.assert_display_with_units_of(acre / ft, ft)

    def test_ft_divided_by_acre_is_inverse_ft(self):
        self.assert_display_with_units_of(ft / acre, 1 / ft)

    def test_gal_divided_by_ft_is_ft_squared(self):
        self.assert_display_with_units_of(gal / ft, ft**2.0)

    def test_cm_divided_by_gal_is_inverse_cm_squared(self):
        self.assert_display_with_units_of(cm / gal, 1 / cm**2.0)

    # Test Conversion #
    ###################
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
        self.assertEqual(scalar, scalar(inch))

    def test_specific_conversion(self):
        self.assertEqual(str((m / s)(km / minute)), '0.06 * km / minute')
        self.assertEqual(str((3 * m / m)(A)), '3.0')
        self.assertEqual(str((3 * ft / ft)(mmHg)), '3.0000000000000004')
        self.assertEqual(str((3 * ft / s)(cm)), '91.44000000000001 * cm / s')

    def test_strange_conversions_hz_to_yr(self):
        self.assertEqual(eval(str(Hz(hr))), Hz)

    def test_strange_conversions_kg_to_hr(self):
        self.assertEqual(eval(str(kg(hr))), kg)

    def test_strange_conversions_acre_to_cm(self):
        self.assertEqual(eval(str(acre(cm))), acre)

    def test_strange_conversions_gpm_to_square_inch(self):
        self.assertEqual(eval(str((gal/mi)(inch**2))), gal/mi)

    def test_strange_conversions_gpm_to_inch(self):
        self.assertEqual(eval(str((gal/mi)(inch))), gal/mi)

    def test_strange_conversions_inch_fur_to_ft_square_bad_parentheses(self):
        self.assertEqual(eval(str(inch*fur(ft**2))), inch*fur)

    def test_can_convert_to_units_of_other_measurement(self):
        a = 2 * ft
        b = 3 * m
        self.assertEqual(str(a(b)), '0.6096 * m')
        self.assertEqual(a, 2 * ft)
        self.assertEqual(b, 3 * m)

    # Test magnitude #
    #######################
    def test_magnitude(self):
        self.assertEqual((2 * yr).magnitude, 2)
        self.assertEqual((12 * ltyr).magnitude, 12)
        self.assertEqual((62 * F).magnitude, 62)

    # Test string conversions #
    ###########################
    def test_to_string(self):
        self.assertEqual(str(1 * m), '1.0 * m')
        self.assertEqual(str(m * s * kg), '1.0 * kg * m * s')
        self.assertEqual(str(m**-1), '1.0 / m')
        self.assertEqual(str(1 / (s * kg * m)), '1.0 / (kg * m * s)')
        self.assertEqual(str(m / s), '1.0 * m / s')
        self.assertEqual(str(m * A * K / (mol * s * kg)),
                         '1.0 * A * K * m / (kg * mol * s)')
        self.assertEqual(str(m**-1 * kg**-2 / A**-1), '1.0 * A / (kg**2 * m)')

    def test_description_and_quantity_work(self):
        for unit in [m, ft, ltyr, lb, mmol, mas, yr, latm, Btu, dyn, tonf]:
            self.assertTrue(unit.description, 'no description: ' + str(unit))
            self.assertTrue(unit.quantity(), 'no quantity: ' + str(unit))

    def test_single_unit_to_string(self):
        self.assertEqual(str(m), '1.0 * m  # Meter [length]')
        self.assertEqual(str(nmi), '1.0 * nmi  # Nautical Mile [length]')
        self.assertEqual(str(galUK), '1.0 * galUK  # British gallon [volume]')
        self.assertEqual(str(yr), '1.0 * yr  # Year [time]')

    def test_constant_to_string(self):
        self.assertIn('# Gas constant [', str(Rc))
        self.assertIn('# Speed of light [', str(c))
        self.assertIn('# Acceleration of gravity [', str(g))
        self.assertIn('# Gravitational constant', str(Gc))
        self.assertIn('# Planck\'s constant [', str(h))
        self.assertIn('# Electron rest mass [', str(Me))
        self.assertIn('# Neutron rest mass [', str(Mn))
        self.assertIn('# Proton rest mass [', str(Mp))
        self.assertIn('# Avogadro constant', str(Na))
        self.assertIn('# Electron charge [', str(q))
        self.assertIn('# Coulomb\'s constant', str(Cc))
        self.assertIn('# Reduced Planck\'s constant [', str(hbar))
        self.assertIn('# Vacuum permeability [', str(u0))
        self.assertIn('# Vacuum permittivity [', str(e0))
        self.assertIn('# Boltzmann\'s constant [', str(kb))
        self.assertIn('# Stefan-Boltzmann constant', str(sbc))
        self.assertIn('# Bohr magneton [', str(ub))
        self.assertIn('# Bohr radius [', str(Rb))
        self.assertIn('# Rydberg Constant [', str(Rdb))
        self.assertIn('# Magnetic flux quantum [', str(mfq))

    def test_quantity_applies_to_new_unit(self):
        hd = (4 * inch).rename('hd', 'hand')
        self.assertEqual(hd.quantity(), inch.quantity())

    # Test custom units #
    #####################
    def test_custom_unit_equals_itself(self):
        self.assertEqual(UnitsGroup('b'), UnitsGroup('b'))

    def test_different_custom_units_are_not_equal(self):
        self.assertNotEqual(UnitsGroup('b'), UnitsGroup('bb'))

    # Test Copy #
    #############
    def copy_does_not_change_unit(self):
        a = m
        b = a.copy()
        self.assertEqual(a, b)

    # Test Join #
    #############
    def join_does_not_change_unit(self):
        a = m.copy()
        b = m.copy()
        a.join(ft / mol)
        self.assertEqual(a, b)

    # Test fsolve #
    ###############
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

        self.assertRaises(IncompatibleUnitsError, fsolve, solve, 3)

    def test_my_fsolve(self):
        def other(x):
            return x + 2.0 * mm

        def solve(x):
            return x - m + other(x)
        try:
            units_fsolve(solve, 3 * ft)
        except:
            self.fail("fsolve with units failed unexpectedly!")

    # Test unitless helper #
    #######################
    def test_unitless(self):
        def spring_force(x, k):
            return x * k

        with_units = spring_force(3 * mm, 2 * N/m)(lbf)
        unitless_spring_force = unitless(lbf, (mm, N/m))(spring_force)
        without_units = unitless_spring_force(3, 2)

        self.assertEqual(without_units, with_units.magnitude)

    def test_unitless_can_handle_strange_args_and_returns(self):
        def func(x, array):
            a = x * array[1]
            b = array[0] + array[1]
            c = (a * b).standardized()
            return ((b, c), a)

        with_units = func(3 * s, [2 * N/m, 3 * lbf/ft])
        unitless_func = unitless(((N/m, kg**2/s**3), lbf*s/ft),
                                 (s, (N/m, lbf/ft)))(func)
        without_units = unitless_func(3, (2, 3))

        self.assertEqual(without_units, _deep_map(lambda u: u.magnitude,
                                                  with_units))

    # Test unitified helper #
    ##########################
    def test_with_units_helper(self):
        def emc_without_units(m):
            return m * 2.99792458**2 * 10

        without_units = emc_without_units(3)
        emc_with_units = unitified(MJ, ug)(emc_without_units)
        with_units = emc_with_units(3 * ug)

        self.assertEqual(round(without_units, 12),
                         round(with_units.magnitude, 12))

    def test_with_units_requires_compatible_units(self):
        def emc_without_units(m):
            return m * 2.99792458**2 * 10

        emc_with_units = unitified(MJ, ug)(emc_without_units)
        self.assertRaises(IncompatibleUnitsError, emc_with_units, 8 * s)

    def test_unitified_can_handle_strange_args_and_returns(self):
        def func(length, time_and_energy):
            time, energy = time_and_energy
            speed = length / time
            power = energy / time
            energy_density = energy / length**3
            return [[power, energy_density], speed]

        without_units = func(2, (4, 3))
        func_with_units = unitified(((W, J/m**3), m/s), (m, (s, J)))(func)
        with_units = func_with_units(2 * m, (4 * s, 3 * J))
        self.assertEqual(without_units, _deep_map(lambda u: u.magnitude,
                                                  with_units))

    # Test inplace methods #
    ########################
    def test_inplace_mul(self):
        a = cm.copy()
        a._inplace_mul(2)
        self.assertEqual(str(a), '2.0 * cm')
        a._inplace_mul(m)
        self.assertEqual(str(a), '0.02 * m**2.0')

    def test_inplace_join(self):
        a = cm.copy()
        a._inplace_join(s)
        self.assertEqual(str(a), '1.0 * cm * s')

    def test_inplace_standardized(self):
        a = Btu.copy()
        a._inplace_standardized()
        self.assertEqual(str(a), '1055.05585262 * kg * m**2 / s**2')

    def test_inplace_normalized(self):
        a = 212 * Btu
        a._inplace_normalized()
        self.assertEqual(str(a), '1.0 * Btu')

    def test_inplace_units_of(self):
        a = 212 * Btu
        a._inplace_units_of(kJ)
        self.assertEqual(str(a), '223.67184075543997 * kJ')
