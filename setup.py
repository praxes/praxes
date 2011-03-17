from distutils.core import setup
from distutils.cmd import Command
from distutils.command.sdist import sdist as _sdist
from distutils.command.build import build as _build
from distutils.extension import Extension
import os
import sys

from Cython.Distutils import build_ext
import numpy


class data(Command):

    description = "Process databases into the structures used by praxes"

    user_options = []

    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import shutil
        import subprocess
        for db, loc in (
            ('elam', 'praxes/phys_ref_data'),
            #('henke', 'praxes/phys_ref_data'),
            #('waasmaier', 'praxes/phys_ref_data'),
            ):
            subprocess.call('cd data && python process_%s_db.py' % db,
                shell=True
                )
            shutil.move('data/%s.db' % db, '%s/%s.db' % (loc, db))


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


class ui_cvt(Command):

    description = "Convert Qt user interface files to PyQt .py files"

    user_options = []

    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _ui_cvt(self, arg, dirname, fnames):
        ## if os.path.split(dirname)[-1] in ('ui'):
        for fname in fnames:
            if fname.endswith('.ui'):
                ui = '/'.join([dirname, fname])
                py = os.path.splitext(ui)[0]+'.py'
                if os.path.isfile(py):
                    if os.path.getmtime(ui) < os.path.getmtime(py):
                        continue
                os.system('pyuic4 -o %s %s'%(py, ui))
                print('converted %s'%fname)
            elif fname.endswith('.qrc'):
                rc = '/'.join([dirname, fname])
                py = os.path.splitext(rc)[0]+'_rc.py'
                if os.path.isfile(py):
                    if os.path.getmtime(rc) < os.path.getmtime(py):
                        continue
                os.system('pyrcc4 -o %s %s'%(py, rc))
                print('converted %s'%fname)

    def run(self):
        os.path.walk('praxes', self._ui_cvt, None)


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


packages = ['SpecClient']
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
    Extension(
        'praxes.io.spec.readonlydict',
        ['praxes/io/spec/readonlydict.pyx']
        ),
    Extension('praxes.io.spec.scan', ['praxes/io/spec/scan.pyx']),
    ]

package_data = {
    'praxes': [
        'fluorescence/ui/icons/*.svg',
        'instrumentation/spec/macros/*.mac',
        'instrumentation/spec/ui/icons/*.svg',
        'phys_ref_data/*.db',
        ]
    }

scripts = [
    'scripts/combi',
    'scripts/sxfm'
    ]
if ('bdist_wininst' in sys.argv) or ('bdist_msi' in sys.argv):
    scripts.append('praxes_win_post_install.py')

setup(
    author = 'Darren Dale',
    author_email = 'darren.dale@cornell.edu',
    cmdclass = {
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
