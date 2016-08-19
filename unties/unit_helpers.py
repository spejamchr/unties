"""Define some helper methods for dealing with units.
"""


def unitless(ret_units, arg_units):
    """Wrap a function that takes and returns units as arguments

    Ex: (stupid example, but it shows how to use this)

        >>> def spring_force(x, k):
        >>>     return x * k
        >>>
        >>> spring_force(3 * mm, 2 * N/m)(lbf)
        0.0013488536585984146 * lbf
        >>> unitless_spring_force = unitless(lbf, (mm, N/m))(spring_force)
        >>> unitless_spring_force(3, 2)
        0.0013488536585984146

    """
    if not isinstance(arg_units, tuple):
        arg_units = (arg_units,)

    def wrap_function(func):
        def new_function(*unitless_args):
            zipped = zip(arg_units, unitless_args)
            new_args = [unit * arg for unit, arg in zipped]
            return func(*new_args)(ret_units).magnitude
        return new_function
    return wrap_function


def unitified(ret_units, arg_units):
    """Convert a non-units function into a unit-friendly function.

    Ex: Calculate e = mc**2, e in MJ, m in ug

        >>> def emc(m):
        >>>     return m * 2.99792458**2 * 10
        >>>
        >>> emc(1)
        89.87551787368176
        >>> unitified_emc = unitified(MJ, ug)(emc)
        >>> unitified_emc(ug)
        89.87551787368174 * MJ

    """
    if not isinstance(arg_units, tuple):
        arg_units = (arg_units,)

    def wrap_function(func):
        def new_function(*unitified_args):
            for unit, arg in zip(arg_units, unitified_args):
                arg.must_have_same_units_as(unit)
            zipped = zip(arg_units, unitified_args)
            unitless_args = [arg(unit).magnitude for unit, arg in zipped]
            return func(*unitless_args) * ret_units
        return new_function
    return wrap_function


def units_fsolve(func, guess):
    """A wrapper method so fsolve can deal with units

    Ex: For a spring with k = 3 N / m, find the distance where the spring
    exerts a force of 2 N.

        >>> def solve_F(x):
        >>>     return x * 3 * N / m - 2 * N
        >>>
        >>> units_fsolve(solve_F, 4 * m)
        0.6666666666666666 * N
    """
    from scipy.optimize import fsolve
    ret_units = func(guess).normalized()
    arg_units = guess.normalized()
    unitless_func = unitless(ret_units, arg_units)(func)
    return fsolve(unitless_func, guess.value)[0] * ret_units
