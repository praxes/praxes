from __future__ import print_function

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.sdist import sdist as _sdist
from distutils.command.build import build as _build
from distutils.command.bdist_wininst import bdist_wininst as _bdist_wininst
from distutils.extension import Extension
import multiprocessing
import os
import subprocess
import sys

from Cython.Distutils import build_ext
import numpy


def convert_data(args):
    if not os.path.exists(args[-1]):
        subprocess.call(args)
        print('converted', args[-1])

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
            'data/elam_physical_reference/create_db.py',
            'data/elam_physical_reference/elam.dat',
            'praxes/physref/elam/elam.db'
            )

    def run(self):
        to_process = [
            self.process_elam(),
            ]

        if sys.platform.startswith('win'):
            #doing this in parallel on windows will crash your computer
            [convert_data(args) for args in to_process]
        else:
            pool = multiprocessing.Pool()
            pool.map(convert_data, to_process)


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


def convert_ui(args):
    subprocess.call(args)
    print('converted', args[-1])

class ui_cvt(Command):

    description = "Convert Qt user interface files to PyQt .py files"

    user_options = []

    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        to_process = []
        for root, dirs, files in os.walk('praxes'):
            for f in files:
                if f.endswith('.ui'):
                    source = os.path.join(root, f)
                    dest = os.path.splitext(source)[0]+'.py'
                    exe = 'pyuic4'
                elif f.endswith('.qrc'):
                    source = os.path.join(root, f)
                    dest = os.path.splitext(source)[0]+'_rc.py'
                    exe = 'pyrcc4'
                else:
                    continue

                if os.path.isfile(dest):
                    if os.path.getmtime(source) < os.path.getmtime(dest):
                            continue
                to_process.append((exe, '-o', dest, source))

        if sys.platform.startswith('win'):
            # doing this in parallel on windows will crash your computer
            [convert_ui(args) for args in to_process]
        else:
            pool = multiprocessing.Pool()
            pool.map(convert_ui, to_process)


class sdist(_sdist):

    def run(self):
        self.run_command('data')
        self.run_command('ui_cvt')
        _sdist.run(self)


class build(_build):

    def run(self):
        self.run_command('data')
        self.run_command('ui_cvt')
        _build.run(self)


class bdist_wininst(_bdist_wininst):

    def run(self):
        self.run_command('data')
        self.run_command('ui_cvt')
        _bdist_wininst.run(self)


packages = []
for dirpath, dirnames, filenames in os.walk('praxes'):
    if '__init__.py' in filenames:
        packages.append('.'.join(dirpath.split(os.sep)))
    else:
        del(dirnames[:])

with open('praxes/version.py') as f:
    for line in f:
        if line[:11] == '__version__':
            exec(line)
            break

ext_modules = [
    Extension('praxes.io.spec.file', ['praxes/io/spec/file.pyx']),
    Extension(
        'praxes.io.spec.proxies',
        ['praxes/io/spec/proxies.pyx'],
        include_dirs=[numpy.get_include()]
        ),
    Extension('praxes.io.spec.mapping', ['praxes/io/spec/mapping.pyx']),
    Extension('praxes.io.spec.scan', ['praxes/io/spec/scan.pyx']),
    ]

package_data = {
    'praxes': [
        'fluorescence/ui/icons/*.svg',
        'instrumentation/spec/macros/*.mac',
        'instrumentation/spec/ui/icons/*.svg',
        'physref/*.db',
        ],
    }

if sys.platform == 'linux2':
    packages.append('SpecClient')
    package_data['SpecClient'] = ['*.mac']

scripts = [
    'scripts/combi',
    ]
if sys.platform.startswith('win'):
    # scripts calling multiprocessing must be importable
    import shutil
    shutil.copy('scripts/sxfm', 'praxes/sxfm.py')
    scripts.append('praxes/sxfm.py')
else:
    scripts.append('scripts/sxfm')
if ('bdist_wininst' in sys.argv) or ('bdist_msi' in sys.argv):
    scripts.append('scripts/praxes_win_post_install.py')

setup(
    author = 'Darren Dale',
    author_email = 'darren.dale@cornell.edu',
    cmdclass = {
        'bdist_wininst': bdist_wininst,
        'build': build,
        'build_ext': build_ext,
        'data': data,
        'sdist': sdist,
        'test': test,
        'ui_cvt': ui_cvt,
        },
    description = 'Praxes framework for scientific analysis',
    ext_modules = ext_modules,
    name = 'praxes',
    package_data = package_data,
    packages = packages,
    requires = (
        'python (>=2.7)',
        'cython (>=0.13)',
        'numpy (>=1.5.1)',
        ),
    scripts = scripts,
    version = __version__,
)
