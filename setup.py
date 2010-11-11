import os
from distutils.core import setup
from distutils.cmd import Command



class test(Command):

    """ Run the test suite. Requires unittest2 """

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
        try:
            import unittest2
        except ImportError:
            raise ImportError('unittest2 is required to run the test suite')

        suite = unittest2.TestLoader().discover('praxes')
        unittest2.TextTestRunner(verbosity=self.verbosity+1).run(suite)


packages = []
for dirpath, dirnames, filenames in os.walk('praxes'):
    if '__init__.py' in filenames:
        packages.append('.'.join(dirpath.split(os.sep)))
    else:
        del(dirnames[:])


setup(
    author = 'Darren Dale',
    author_email = 'darren.dale@cornell.edu',
    cmdclass = {'test': test},
    description = 'Praxes framework for scientific analysis',
    name = 'praxes',
    packages = packages,
    requires = (python (>=2.7)),
)
