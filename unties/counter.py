"""Storage logic for UnitsGroup#units and UnitsGroup#full_name attributes.
"""


class Counter(dict):
    """Custom dict implementation for use with UnitsGroup.
    """
    def __init__(self):
        self.positives = {}
        self.negatives = {}

    def __missing__(self, key):
        return 0

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.negatives.pop(key, None)
        self.positives.pop(key, None)
        if self[key] == 0:
            self.pop(key)
        elif self[key] > 0:
            self.positives[key] = self[key]
        elif self[key] < 0:
            self.negatives[key] = self[key] * -1

    def __str__(self):
        return self.joining_symbol() + self.unit_name_string()

    def joining_symbol(self):
        """Return the symbol to join the unit_name to the numerical value (`*` or `/`).
        """
        if not self.negatives and not self.positives:
            return ''
        else:
            return ' / ' if not self.positives else ' * '

    def positive_string(self):
        pos_strings = [str(key) + exp_str(self.positives, key)
                       for key in sorted(self.positives)]

        return ' * '.join(pos_strings)

    def negative_string(self):
        neg_strings = [str(key) + exp_str(self.negatives, key)
                       for key in sorted(self.negatives)]

        if len(neg_strings) <= 1:
            return ''.join(neg_strings)
        else:
            return '(' + ' * '.join(neg_strings) + ')'

    def unit_name_string(self):
        """Return textual, python-compatible, representation of the unit
        """
        name = self.positive_string()
        if self.positives and self.negatives:
            name += ' / '
        if self.negatives:
            name += self.negative_string()
        return name


def exp_str(dictionary, key):
    """Return exponent string. An empty string if exponent is 1.
    """
    if dictionary[key] == 1:
        return ''
    else:
        return '**' + str(dictionary[key])
