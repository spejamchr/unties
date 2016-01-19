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

    _.ft.units_of(_.inch)
    #=> '12.000000000000002 * (0.0254 * _.m)'

Convert 12.5 'ft' to 'inch'

    (11.5 * _.ft).units_of(_.inch)
    #=> '138.00000000000003 * (0.0254 * _.m)'

As you can see fro the examples, the decimals are not perfectly exact

Each unit_group does *not* have to have the same dimensions:

    (_.m/_.s).units_of(_.inch)
    #=> '39.37007874015748 * _.s**-1 * (0.0254 * _.m)'

But this isn't always very useful:

    (_.m**2).units_of(_.inch**3)
    #=> '61023.74409473229 * _.m**-1 * (1.6387064e-05 * _.m**3)'

Multiple units have to be grouped:

    (_.inch*_.fur).units_of(_.m**2)
    #=> '5.1096672 * (1.0 * _.m**2)'

or else:
    _.inch*_.fur.units_of(_.m**2)
    #=> Exception: AttributeError: 'str' object has no attribute 'copy'

This is because methods have higher priority than the <*> operator