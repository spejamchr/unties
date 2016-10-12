# For information about this, see this tutorial:
# https://python-packaging.readthedocs.org/en/latest/minimal.html

from setuptools import setup

def text_of(file_name):
    with open(file_name) as f:
        return f.read()

def long_description():
    readme = text_of('README.md')
    license = text_of('LICENSE')
    authors = text_of('AUTHORS')
    return "\n\n".join([readme, license, authors])

setup(name='unties',
      version='0.3.0',
      description='The unit handler',
      long_description=long_description(),
      url='https://github.com/spejamchr/unties',
      author='Spencer Christiansen',
      author_email='jc.spencer92@gmail.com',
      license='MIT',
      packages=['unties', 'unties.properties', 'unties.utilities'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
