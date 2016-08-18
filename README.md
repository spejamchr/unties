# README

To install, just:

```bash
$ easy_install unties
```

or

```bash
$ pip install unties
```

### What is this repository for?

* Another units-handling package

### How do I get set up?

* See install directions above
* No configuration options
* No dependencies
* To run tests: `python setup.py test`

### Examples

To use, import the Units class. I like to shorthand it as `_`, after the style
of TI calculators:

```python
>>> import unties as _
```

Or, especially if you're just playing in a python console, feel free to wildcard
import everything:

```python
>>> from unties import *
```

And you instantly have access to a ton of units and constants

Convert 11.5 'ft' to 'inch'

```python
>>> 11.5 * ft.units_of(inch)
138.00000000000003 * inch
```

As you can see from the examples, floating-point math is hard

You can call units with another unit as the argument as shorthand for
conversion. So you can do:

```python
>>> 11.5 * ft(inch)
138.00000000000003 * inch
```

Conversion will *not* raise an error if the units groups have different
dimensions; instead, basic units will be used to make up the difference, without
affecting the value:

```python
>>> mph(inch)
17.6 * inch / s

>>> hp(cal)
178.1073544430114 * cal / s

>>> acre(ft)
43559.99999999999 * ft**2
```

Multiple units should be grouped:

```python
>>> (yd / hr)(mm / s)
0.254 * mm / s
```

or else strange things happen:

```python
>>> yd / hr(mm / s)
2.7777777777777776e-07 * m * yd / (mm * s)
```

Please note, though, that conversion never changes the value of a measurement.
In the previous example, `2.7777777777777776e-07 * m * yd / (mm * s) == yd / hr`

If you're ever unsure what a unit symbol represents, just type it into the
console, and the unit's name and quantity will be shown:

```python
>>> print(amu)
1.0 * amu  # Atomic mass unit [mass]
```

If you've done some calculations and want to check what quantity your new unit
group measures, use the `quantity()` method:

```python
>>> (3 * hp / mmHg).quantity()
'volumetric flow'
```

### Contribution guidelines

* Contributions are welcome. Just make a pull request.
* Use [pep8](https://pypi.python.org/pypi/pep8) to lint your Python code.
* Write new tests for any new features
