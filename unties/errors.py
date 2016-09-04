class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class IncompatibleUnitsError(Error):
    """Exception raised when an action is attempted with two incompatible units
    """
    def __init__(self, unit_group1, unit_group2):
        self.units1 = unit_group1.units
        self.units2 = unit_group2.units

    def __str__(self):
        return repr(self.units1) + ' and ' + repr(self.units2)
