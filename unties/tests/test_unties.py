from unittest import TestCase
import math
import numpy as np
from scipy.optimize import fsolve

import unties as _
import unties.utilities.errors as ue


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
        self.assertEqual(1 * _.m + 5 * _.m, 5 * _.m + 1 * _.m)

    def test_can_add_scalar_units_group_and_number(self):
        scalar = _.m / _.m
        self.assertEqual(scalar + 1, 2)

    def test_can_add_number_and_scalar_units_group(self):
        scalar = _.m / _.m
        self.assertEqual(1 + scalar, 2)

    # Test Subtraction #
    ####################
    def test_sub_commutative_law(self):
        self.assertEqual(3 * _.m - 1 * _.m, -(1 * _.m - 3 * _.m))

    def test_can_subtract_scalar_units_group_and_number(self):
        scalar = _.m / _.m
        self.assertEqual(scalar - 1, 0)

    def test_can_subtract_number_and_scalar_units_group(self):
        scalar = _.m / _.m
        self.assertEqual(1 - scalar, 0)

    # Test multiplication #
    #######################
    def test_m_times_m_equals_m_squared(self):
        self.assertEqual(_.m * _.m, _.m**2)

    def test_mult_commutative_law(self):
        self.assertEqual(_.m * 2, 2 * _.m)

    def test_np_mult_unit(self):
        try:
            np.array([5 * _.m, 2 * _.ft, 3 * _.inch]) * _.cm
        except:
            self.fail("np array * unit raised an error unexpectedly!")

    def test_unit_mult_np(self):
        try:
            _.cm * np.array([5 * _.m, 2 * _.ft, 3 * _.inch])
        except:
            self.fail("unit * np array raised an error unexpectedly!")

    def test_np_mult_is_commutative(self):
        linspace = np.linspace(1, 2)
        a = linspace * _.ft
        b = _.ft * linspace
        self.assertTrue(np.all(a == b))

    def test_mult_by_zero_to_get_zero(self):
        try:
            _.K * (0 / _.K)
        except:
            self.fail("_.K * (0 / _.K) raised an error unexpectedly!")

    def test_mult_by_zero_to_get_zero_2(self):
        try:
            (0 / _.K) * _.K
        except:
            self.fail("(0 / _.K) * _.K raised an error unexpectedly!")

    # Test Division #
    #################
    def test_division_by_one_equals_self(self):
        self.assertEqual(_.inch, _.inch / 1)

    def test_division_by_self_equals_1(self):
        self.assertEqual(_.inch / _.inch, 1)

    def test_div_commutative_law(self):
        self.assertEqual(_.m / _.inch, 1 / (_.inch / _.m))

    def test_mi_per_hr_div_by_mi_leaves_per_hr(self):
        self.assertEqual((_.mi / _.hr) / _.mi, 1 / _.hr)

    def test_np_div_unit(self):
        try:
            np.array([5 * _.m, 2 * _.ft, 3 * _.inch]) / _.cm
        except:
            self.fail("np array / unit raised an error unexpectedly!")

    def test_unit_div_np(self):
        try:
            _.cm / np.array([5 * _.m, 2 * _.ft, 3 * _.inch])
        except:
            self.fail("unit / np array raised an error unexpectedly!")

    # Test Absolute Value #
    #######################
    def test_absolute_value_leaves_positive_positive(self):
        self.assertEqual(abs(_.m), _.m)

    def test_absolute_value_makes_negatives_positive(self):
        self.assertEqual(abs(-_.m), _.m)

    # Test comparators #
    ####################
    def test_one_meter_is_larger_than_one_foot(self):
        self.assertTrue(_.m > _.ft)

    def test_kph_is_less_than_mph(self):
        self.assertTrue(_.kph < _.mph)

    def test_ltet(self):
        self.assertTrue(_.kmol <= _.kmol)
        self.assertTrue(_.mol <= _.kmol)

    def test_gtet(self):
        self.assertTrue(_.kPa >= _.kPa)
        self.assertTrue(_.kPa >= _.Pa)

    def test_math_log_2_units_is_log_2(self):
        self.assertEqual(math.log(2), math.log(2 * _.atm / _.atm))

    def test_np_log_2_units_is_log_2(self):
        self.assertEqual(np.log(2), np.log(2 * _.atm / _.atm))

    def test_math_exp_2_units_is_exp_2(self):
        self.assertEqual(math.log(2), math.log(2 * _.atm / _.atm))

    def test_np_exp_2_units_is_exp_2(self):
        self.assertEqual(np.exp(2), np.exp(2 * _.atm / _.atm))

    def test_np_log10_2_units_is_log10_2(self):
        self.assertEqual(np.log10(100), np.log10(100 * _.atm/_.atm))

    def test_np_cos_2_units_is_cos_2(self):
        self.assertEqual(np.cos(2), np.cos(2 * _.atm/_.atm))

    def test_np_sin_2_units_is_sin_2(self):
        self.assertEqual(np.sin(2), np.sin(2 * _.atm/_.atm))

    def test_inch_is_not_equal_to_ft(self):
        self.assertNotEqual(_.inch, _.ft)

    def test_inch_is_not_equal_to_s(self):
        self.assertNotEqual(_.inch, _.s)

    def test_inch_is_not_equal_to_4(self):
        self.assertNotEqual(_.inch, 4)

    # Test Smart Conversion #
    #########################
    def test_ft_times_yd_is_yd_squared(self):
        self.assert_display_with_units_of(_.ft * _.yd, _.yd**2.0)

    def test_ft_divided_by_yd_is_unitless_one_third(self):
        self.assertEqual(_.ft / _.yd, 1 / 3)

    def test_ft_times_acre_is_acre_to_the_one_and_a_half(self):
        self.assert_display_with_units_of(_.ft * _.acre, _.acre**1.5)

    def test_acre_times_ft_is_ft_cubed(self):
        self.assert_display_with_units_of(_.acre * _.ft, _.ft**3.0)

    def test_ft_times_gal_is_gal_to_the_four_thirds(self):
        self.assert_display_with_units_of(_.ft * _.gal, _.gal**(4 / 3))

    def test_gal_times_ft_is_ft_to_the_fourth(self):
        self.assert_display_with_units_of(_.gal * _.ft, _.ft**4.0)

    def test_acre_divided_by_ft_is_ft(self):
        self.assert_display_with_units_of(_.acre / _.ft, _.ft)

    def test_ft_divided_by_acre_is_inverse_ft(self):
        self.assert_display_with_units_of(_.ft / _.acre, 1 / _.ft)

    def test_gal_divided_by_ft_is_ft_squared(self):
        self.assert_display_with_units_of(_.gal / _.ft, _.ft**2.0)

    def test_cm_divided_by_gal_is_inverse_cm_squared(self):
        self.assert_display_with_units_of(_.cm / _.gal, 1 / _.cm**2.0)

    # Test Conversion #
    ###################
    def test_inch_equals_25_point_4_mm(self):
        self.assertEqual(_.inch, 25.4 * _.mm)

    def test_ft_equals_12_inches(self):
        self.assertEqual(_.ft, 12 * _.inch)

    def test_conversion_does_not_affect_value_kph_to_mph(self):
        self.assertEqual(_.kph(_.mph), _.kph)

    def test_conversion_does_not_affect_value_J_to_hp(self):
        self.assertEqual(_.J(_.hp), _.J)

    def test_conversion_does_not_affect_value_m_s_to_cm(self):
        self.assertEqual(12 / _.s * _.m(_.cm), 12 / _.s * _.m)

    def test_conversion_does_not_affect_value_kPa_to_hp(self):
        self.assertEqual(12 * _.kPa(_.hp), 12 * _.kPa)

    def test_conversion_does_not_affect_value_yr_to_hr(self):
        self.assertEqual(_.yr(_.hr), _.yr)

    def test_conversion_does_not_affect_value_custom_unit_to_m(self):
        b = _.UnitsGroup('b')
        self.assertEqual(12 * b(_.m), 12 * b)

    def test_converting_scalar_does_nothing(self):
        scalar = _.m / _.m
        self.assertEqual(scalar, scalar(_.inch))

    def test_specific_conversion(self):
        self.assertEqual(str((_.m / _.s)(_.km / _.minute)),
                         '0.06 * km / minute')
        self.assertEqual(str((3 * _.m / _.m)(_.A)), '3.0')
        self.assertEqual(str((3 * _.ft / _.ft)(_.mmHg)), '3.0000000000000004')
        self.assertEqual(str((3 * _.ft / _.s)(_.cm)),
                         '91.44000000000001 * cm / s')

    def test_strange_conversions_hz_to_yr(self):
        self.assertEqual(_.Hz(_.hr), _.Hz)

    def test_strange_conversions_kg_to_hr(self):
        self.assertEqual(_.kg(_.hr), _.kg)

    def test_strange_conversions_acre_to_cm(self):
        self.assertEqual(_.acre(_.cm), _.acre)

    def test_strange_conversions_gpm_to_square_inch(self):
        self.assertEqual((_.gal/_.mi)(_.inch**2), _.gal/_.mi)

    def test_strange_conversions_gpm_to_inch(self):
        self.assertEqual((_.gal/_.mi)(_.inch), _.gal/_.mi)

    def test_strange_conversions_inch_fur_to_ft_square_bad_parentheses(self):
        self.assertEqual(_.inch*_.fur(_.ft**2), _.inch*_.fur)

    def test_can_convert_to_units_of_other_measurement(self):
        a = 2 * _.ft
        b = 3 * _.m
        self.assertEqual(str(a(b)), '0.6096 * m')
        self.assertEqual(a, 2 * _.ft)
        self.assertEqual(b, 3 * _.m)

    # Test magnitude #
    #######################
    def test_magnitude(self):
        self.assertEqual((2 * _.yr).magnitude, 2)
        self.assertEqual((12 * _.ltyr).magnitude, 12)
        self.assertEqual((62 * _.F).magnitude, 62)

    # Test string conversions #
    ###########################
    def test_to_string(self):
        self.assertEqual(str(1 * _.m), '1.0 * m')
        self.assertEqual(str(_.m * _.s * _.kg), '1.0 * kg * m * s')
        self.assertEqual(str(_.m**-1), '1.0 / m')
        self.assertEqual(str(1 / (_.s * _.kg * _.m)), '1.0 / (kg * m * s)')
        self.assertEqual(str(_.m / _.s), '1.0 * m / s')
        self.assertEqual(str(_.m * _.A * _.K / (_.mol * _.s * _.kg)),
                         '1.0 * A * K * m / (kg * mol * s)')
        self.assertEqual(str(_.m**-1 * _.kg**-2 / _.A**-1),
                         '1.0 * A / (kg**2.0 * m)')

    def test_description_and_quantity_work(self):
        for unit in [_.m, _.ft, _.ltyr, _.lb, _.mmol, _.mas, _.yr, _.latm,
                     _.Btu, _.dyn, _.tonf]:
            self.assertTrue(unit.description, 'no description: ' + str(unit))
            self.assertTrue(unit.quantity, 'no quantity: ' + str(unit))

    def test_single_unit_to_string(self):
        self.assertEqual(str(_.m), '1.0 * m  # Meter [length]')
        self.assertEqual(str(_.nmi), '1.0 * nmi  # Nautical Mile [length]')
        self.assertEqual(str(_.galUK),
                         '1.0 * galUK  # British gallon [volume]')
        self.assertEqual(str(_.yr), '1.0 * yr  # Year [time]')

    def test_constant_to_string(self):
        self.assertIn('# Gas constant [', str(_.Rc))
        self.assertIn('# Speed of light [', str(_.c))
        self.assertIn('# Acceleration of gravity [', str(_.g))
        self.assertIn('# Gravitational constant', str(_.Gc))
        self.assertIn('# Planck\'s constant [', str(_.h))
        self.assertIn('# Electron rest mass [', str(_.Me))
        self.assertIn('# Neutron rest mass [', str(_.Mn))
        self.assertIn('# Proton rest mass [', str(_.Mp))
        self.assertIn('# Avogadro constant', str(_.Na))
        self.assertIn('# Electron charge [', str(_.q))
        self.assertIn('# Coulomb\'s constant', str(_.Cc))
        self.assertIn('# Reduced Planck\'s constant [', str(_.hbar))
        self.assertIn('# Vacuum permeability [', str(_.u0))
        self.assertIn('# Vacuum permittivity [', str(_.e0))
        self.assertIn('# Boltzmann\'s constant [', str(_.kb))
        self.assertIn('# Stefan-Boltzmann constant', str(_.sbc))
        self.assertIn('# Bohr magneton [', str(_.ub))
        self.assertIn('# Bohr radius [', str(_.Rb))
        self.assertIn('# Rydberg Constant [', str(_.Rdb))
        self.assertIn('# Magnetic flux quantum [', str(_.mfq))

    def test_quantity_applies_to_new_unit(self):
        hd = (4 * _.inch).rename('hd', 'hand')
        self.assertEqual(hd.quantity, _.inch.quantity)

    # Test custom units #
    #####################
    def test_custom_unit_equals_itself(self):
        self.assertEqual(_.UnitsGroup('b'), _.UnitsGroup('b'))

    def test_different_custom_units_are_not_equal(self):
        self.assertNotEqual(_.UnitsGroup('b'), _.UnitsGroup('bb'))

    # Test Copy #
    #############
    def copy_does_not_change_unit(self):
        a = _.m
        b = a.copy()
        self.assertEqual(a, b)

    # Test Join #
    #############
    def join_does_not_change_unit(self):
        a = _.m.copy()
        b = _.m.copy()
        a.join(_.ft / _.mol)
        self.assertEqual(a, b)

    # Test fsolve #
    ###############
    def test_solve_np_array_with_other_order(self):
        def other(x):
            return x + 2.0 * _.mm

        def solve(x):
            return [x.value for x in _.ft * x - _.m + other(_.ft * x)]
        try:
            fsolve(solve, 3)
        except:
            self.fail("fsolve with units failed unexpectedly!")

    def test_solve_np_array_with_mixed_order_should_work(self):
        def other(x):
            return x + 2.0 * _.mm

        def solve(x):
            return [x.value for x in _.ft * x - _.m + other(x * _.ft)]
        try:
            fsolve(solve, 3)
        except:
            self.fail("fsolve with units failed unexpectedly!")

    def test_my_fsolve(self):
        def other(x):
            return x + 2.0 * _.mm

        def solve(x):
            return x - _.m + other(x)
        try:
            _.units_fsolve(solve, 3 * _.ft)
        except:
            self.fail("fsolve with units failed unexpectedly!")

    # Test unitless helper #
    #######################
    def test_unitless(self):
        def spring_force(x, k):
            return x * k

        with_units = spring_force(3 * _.mm, 2 * _.N/_.m)(_.lbf)
        unitless_spring_force = _.unitless(_.lbf,
                                           (_.mm, _.N/_.m))(spring_force)
        without_units = unitless_spring_force(3, 2)

        self.assertEqual(without_units, with_units.magnitude)

    def test_unitless_can_handle_strange_args_and_returns(self):
        def func(x, array):
            a = x * array[1]
            b = array[0] + array[1]
            c = (a * b).standardized()
            return ((b, c), a)

        with_units = func(3 * _.s, [2 * _.N/_.m, 3 * _.lbf/_.ft])
        unitless_func = _.unitless(((_.N/_.m, _.kg**2/_.s**3), _.lbf*_.s/_.ft),
                                   (_.s, (_.N/_.m, _.lbf/_.ft)))(func)
        without_units = unitless_func(3, (2, 3))

        self.assertEqual(without_units, _deep_map(lambda u: u.magnitude,
                                                  with_units))

    def test_unitless_can_handle_numpy_arrays(self):
        def spring_force(x):
            k = 2 * _.N/_.m
            return x * k

        unitless_func = _.unitless(_.N, _.ft)(spring_force)
        try:
            unitless_func(np.linspace(1, 2, 4))
        except:
            self.fail("unitless with np array failed unexpectedly!")

    # Test unitified helper #
    ##########################
    def test_with_units_helper(self):
        def emc_without_units(mass):
            return mass * 2.99792458**2 * 10

        without_units = emc_without_units(3)
        emc_with_units = _.unitified(_.MJ, _.ug)(emc_without_units)
        with_units = emc_with_units(3 * _.ug)

        self.assertEqual(round(without_units, 12),
                         round(with_units.magnitude, 12))

    def test_with_units_requires_compatible_units(self):
        def emc_without_units(m):
            return m * 2.99792458**2 * 10

        emc_with_units = _.unitified(_.MJ, _.ug)(emc_without_units)
        self.assertRaises(ue.IncompatibleUnitsError, emc_with_units, 8 * _.s)

    def test_unitified_can_handle_numpy_arrays(self):
        def some_function(x):
            return 311 / x**2

        unitified_func = _.unitified(_.Pa, _.ft)(some_function)
        try:
            unitified_func(np.linspace(1, 2, 4) * _.ft)
        except:
            self.fail("unitified with np array failed unexpectedly!")

    def test_unitified_can_handle_strange_args_and_returns(self):
        def func(length, time_and_energy):
            time, energy = time_and_energy
            speed = length / time
            power = energy / time
            energy_density = energy / length**3
            return [[power, energy_density], speed]

        without_units = func(2, (4, 3))
        func_with_units = _.unitified(((_.W, _.J/_.m**3), _.m/_.s),
                                      (_.m, (_.s, _.J)))(func)
        with_units = func_with_units(2 * _.m, (4 * _.s, 3 * _.J))
        self.assertEqual(without_units, _deep_map(lambda u: u.magnitude,
                                                  with_units))

    # Test inplace methods #
    ########################
    def test_inplace_mul(self):
        a = _.cm.copy()
        a._inplace_mul(2)
        self.assertEqual(str(a), '2.0 * cm')
        a._inplace_mul(_.m)
        self.assertEqual(str(a), '0.02 * m**2.0')

    def test_inplace_join(self):
        a = _.cm.copy()
        a._inplace_join(_.s)
        self.assertEqual(str(a), '1.0 * cm * s')

    def test_inplace_standardized(self):
        a = _.Btu.copy()
        a._inplace_standardized()
        self.assertEqual(str(a), '1055.05585262 * kg * m**2.0 / s**2.0')

    def test_inplace_normalized(self):
        a = 212 * _.Btu
        a._inplace_normalized()
        self.assertEqual(str(a), '1.0 * Btu')

    def test_inplace_units_of(self):
        a = 212 * _.Btu
        a._inplace_units_of(_.kJ)
        self.assertEqual(str(a), '223.67184075543997 * kJ')
