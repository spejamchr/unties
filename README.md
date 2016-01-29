# README #

To install, just:

    >>> easy_install unties

or

    >>> pip install unties

### What is this repository for? ###

* Another units-handling package
* Version 0.1


### How do I get set up? ###

* See install directions above
* No configuration options
* No dependencies
* To run tests: `python setup.py test`

### Contribution guidelines ###

* Contributions are welcome. Just make a pull request on bitbucket.

### Examples ###

To use, import the Units class. I like to shorthand it as `_`, after the style
of TI calculators:

    >>> from unties import Units as _

And you instantly have access to a ton of units and constants

Convert 'ft' to 'inch'

    >>> _.ft.units_of(_.inch)
    12.000000000000002 * inch

Convert 11.5 'ft' to 'inch'

    >>> 11.5 * _.ft.units_of(_.inch)
    138.00000000000003 * inch

As you can see fro the examples, the decimals are not perfectly exact

You can call units with another unit as the argument as shorthand for
conversion. So you can do:

    >>> _.ft(_.inch)
    12.000000000000002 * inch

    >>> 11.5*_.ft(_.inch)
    138.00000000000003 * inch

Each units_group does *not* have to have the same dimensions:

    >>> (_.m/_.s)(_.inch)
    39.37007874015748 * inch * s**-1

    >>> _.hp(_.cal)
    178.1073544430114 * cal * s**-1

But this isn't always very useful, so use it responsibly

Multiple units should be grouped:

    >>> (_.inch*_.fur)(_.m**2)
    5.1096672 * m**2

or else strange things happen:

    >>> _.inch*_.fur(_.m**2)
    201.16799999999998 * inch * m
