from unittest import TestCase

import unties

class TestUnties(TestCase):
    def test_inch_is_254_mm(self):
        inch = unties._.inch
        mm = unties._.mm
        string = inch(mm)
        self.assertTrue(string == '25.4 * mm')
