from distutils.core import setup
from distutils.cmd import Command
from distutils.extension import Extension
import os

from Cython.Distutils import build_ext
import numpy

class test(Command):

    """Run the test suite."""

    description = "Run the test suite"

    user_options = [('verbosity', 'v', 'set test report verbosity')]

    def initialize_options(self):
        self.verbosity = 0

    def finalize_options(self):
        try:
            self.verbosity = int(self.verbosity)
        except ValueError:
            raise ValueError('Verbosity must be an integer.')

    def run(self):
        import sys
        if sys.version.startswith('3.1'):
            import unittest2 as unittest
        else:
            import unittest
        suite = unittest.TestLoader().discover('.')
        unittest.TextTestRunner(verbosity=self.verbosity+1).run(suite)


packages = []
for dirpath, dirnames, filenames in os.walk('praxes'):
    if '__init__.py' in filenames:
        packages.append('.'.join(dirpath.split(os.sep)))
    else:
        del(dirnames[:])


setup(
    author = 'Darren Dale',
    author_email = 'darren.dale@cornell.edu',
    cmdclass = {'test': test, 'build_ext': build_ext},
    description = 'Praxes framework for scientific analysis',
    ext_modules = [
        Extension('praxes.io.spec.file', ['praxes/io/spec/file.pyx']),
        Extension(
            'praxes.io.spec.proxies', ['praxes/io/spec/proxies.pyx'],
            include_dirs=[numpy.get_include()]
            ),
        Extension(
            'praxes.io.spec.readonlydict', ['praxes/io/spec/readonlydict.pyx']
            ),
        Extension('praxes.io.spec.scan', ['praxes/io/spec/scan.pyx']),
        ],
    name = 'praxes',
    packages = packages,
    requires = (
        'python (>=2.7)',
        'cython (>=0.13)',
        'numpy (>=1.5.1)',
        ),
)
