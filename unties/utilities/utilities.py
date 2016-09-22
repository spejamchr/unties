import unties.utilities.errors as ue


class OutOfRangeTest:
    """Test if a value is outside a given range. If it is, raise an exception.
    """

    def __init__(self, arg, mi, ma, throw_error=True):
        self.__arg = arg
        self.__mi = mi
        self.__ma = ma
        self.__throw_error = throw_error
        self.__test()

    def __test(self):
        if self.__arg < self.__mi or self.__arg > self.__ma:
            error = ue.OutOfRangeError(self.__arg, self.__mi, self.__ma)
            if self.__throw_error:
                raise error
            else:
                print(error)


def function_strings(functions):
    string = ''
    for func in functions:
        fname, name, units = func.__name__, func.__name__[1:], func.__doc__
        string += 'def ' + name + '(T, ranged=True):\n'
        string += '    return ' + fname + '(T.value, ranged) * ' + units + '\n'
    return string
