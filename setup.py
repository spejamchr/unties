# For information about this, see this tutorial:
# https://python-packaging.readthedocs.org/en/latest/minimal.html

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='unties',
      version='0.1.1',
      description='The unit handler',
      long_description=readme(),
      url='https://bitbucket.org/spejamchr/unties',
      author='Spencer Christiansen',
      author_email='jc.spencer92@gmail.com',
      license='MIT',
      packages=['unties'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'])
