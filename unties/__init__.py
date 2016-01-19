# To import this file, do:
#
# import importlib.machinery
# unties = importlib.machinery.SourceFileLoader(
#     '_','/full/path/to/this/file/unties.py'
# ).load_module()
# _ = unties._

# import units
import os

units_file_path = os.path.dirname(__file__) + '/' + 'units' + '.py'

import importlib.machinery
units = importlib.machinery.SourceFileLoader(
    '_', units_file_path
).load_module()

# Follow the calculator pattern of _.<unit>
_ = units.Units

class Test :
    def perform(self) :
        print('Liter:   ', L)
        print('Newton:  ', N)
        print('Joule:   ', J)
        print('Pascal:  ', Pa)
        print('Hertz:   ', Hz)
        print('Radian:  ', rad)
        print('Watt:    ', W)
        print('Coulomb: ', C)
        print('Volt:    ', V)
        print('Farad:   ', F)
