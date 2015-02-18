from __future__ import print_function

from distutils.command.build import build as _build
from glob import glob
import multiprocessing
import os
import subprocess
import sys

from Cython.Distutils import build_ext
import numpy
from setuptools import Command, Extension, find_packages, setup
from setuptools.command.bdist_wininst import bdist_wininst as _bdist_wininst

import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'praxes/_version.py'
versioneer.versionfile_build = 'praxes/_version.py'
versioneer.tag_prefix = 'v' # tags are like 1.2.0
versioneer.parentdir_prefix = 'praxes-' # dirname like 'myproject-1.2.0'
cmdclass = versioneer.get_cmdclass()

cmdclass['build_ext'] = build_ext
_sdist = cmdclass['sdist']


def convert_data(args):
    if not os.path.exists(args[-1]):
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError:
            print("""\
    Warning: Could not configure %s.
    See README to configure repository.
            """ % (os.path.split(args[-1]))[0])

class data(Command):

    description = "Process databases into the structures used by praxes"

    user_options = []

    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def process_elam(self):
        return (
            sys.executable,
            'praxes/physref/elam/create_db',
            'praxes/physref/elam/elam.dat',
            'praxes/physref/elam/elam.db'
            )

    def process_waasmaier(self):
        return (
            sys.executable,
            'praxes/physref/waasmaier/create_db',
            'praxes/physref/waasmaier/waasmaier_kirfel.dat',
            'praxes/physref/waasmaier/waasmaier_kirfel.db'
            )

    def run(self):
        to_process = [
            self.process_elam(),
            self.process_waasmaier(),
            ]

        if sys.platform.startswith('win'):
            #doing this in parallel on windows will crash your computer
            [convert_data(args) for args in to_process]
        else:
            pool = multiprocessing.Pool()
            pool.map(convert_data, to_process)

cmdclass['data'] = data


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

cmdclass['test'] = test


class sdist(_sdist):

    def run(self):
        self.run_command('data')
        _sdist.run(self)

cmdclass['sdist'] = sdist


class build(_build):

    def run(self):
        self.run_command('data')
        _build.run(self)

cmdclass['build'] = build


class bdist_wininst(_bdist_wininst):

    def run(self):
        self.run_command('data')
        _bdist_wininst.run(self)

cmdclass['bdist_wininst'] = bdist_wininst


packages = []
for dirpath, dirnames, filenames in os.walk('praxes'):
    if '__init__.py' in filenames:
        packages.append('.'.join(dirpath.split(os.sep)))
    else:
        del(dirnames[:])


ext_modules = [
    Extension('praxes.io.spec.file', ['praxes/io/spec/file.pyx']),
    Extension(
        'praxes.io.spec.proxies',
        ['praxes/io/spec/proxies.pyx'],
        include_dirs=[numpy.get_include()]
        ),
    Extension('praxes.io.spec.mapping', ['praxes/io/spec/mapping.pyx']),
    Extension('praxes.io.spec.scan', ['praxes/io/spec/scan.pyx']),
    Extension('praxes.rlock', ['praxes/rlock.pyx']),
    Extension(
        '_tifffile',
        ['praxes/io/tifffile.c'],
        include_dirs=[numpy.get_include()]
        )
    ]

package_data = {
    'praxes': [
        'fluorescence/ui/*.ui',
        'fluorescence/ui/*.png',
        'instrumentation/spec/macros/*.mac',
        'instrumentation/spec/ui/icons/*.*',
        'instrumentation/spec/ui/*.ui',
        ],
    }
package_data['praxes'].extend(
    [i.split('/',1)[-1] for i in glob('praxes/physref/*/*.db')]
    )

entry_points = {
    'console_scripts': [
        'praxes = praxes.cli.main:main',
        'sxfm = praxes.fluorescence:_launch_gui'
        ],
    }

scripts = []
if ('bdist_wininst' in sys.argv) or ('bdist_msi' in sys.argv):
    scripts.append('scripts/praxes_win_post_install.py')

setup(
    author = 'Darren Dale',
    author_email = 'darren.dale@cornell.edu',
    cmdclass = cmdclass,
    description = 'Praxes framework for scientific analysis',
    ext_modules = ext_modules,
    name = 'praxes',
    package_data = package_data,
    packages = find_packages(),
    entry_points = entry_points,
    requires = (
        'python (>=2.7)',
        'cython (>=0.13)',
        'numpy (>=1.5.1)',
        ),
    scripts = scripts,
    version=versioneer.get_version(),
)
