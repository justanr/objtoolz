#!/usr/bin/env python
import functools
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


install_requires = ['toolz']

if not hasattr(functools, 'singledispatch'):
    install_requires.append('singledispatch')

if __name__ == '__main__':
    setup(
        name='objtoolz',
        version='0.1.0',
        description='Tools for building better objects',
        author='Alec Nikolas Reiter',
        packages=['objtoolz'],
        install_requires=install_requires,
        license='MIT',
        url='https://github.com/justanr/objtoolz',
        keywords='objects classes metaclasses descriptors',
        test_suite='tests',
        tests_require=['py', 'pytest'],
        cmdclass={'test': PyTest}
        )
