# README #

To install, just:

```bash
$ easy_install unties
```

or

```bash
$ pip install unties
```

### What is this repository for? ###

* Another units-handling package
* Version 0.1


### How do I get set up? ###

* See install directions above
* No configuration options
* No dependencies
* To run tests: `python setup.py test`

### Examples ###

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

Each units_group does *not* have to have the same dimensions; basic units will
be used to make up the difference:

```python
>>> mph(inch)
17.6 * inch / s

>>> hp(cal)
178.1073544430114 * cal / s

>>> acre(ft)
43559.99999999999 * ft**2
```

But this isn't always very useful, so use it responsibly

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

To see a full list of units, use the `all_units()` method. To see all defined
constants, use the `all_constants()` method. Or take a peek in the source.

### Contribution guidelines ###

* Contributions are welcome. Just make a pull request on bitbucket.
