import os
import sys

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.sdist import sdist as _sdist


with open('xpaxs/version.py') as f:
    for line in f:
        if line[:11] == '__version__':
            exec(line)
            break


class sdist(_sdist):

    def ui_cvt(self, arg, dirname, fnames):
        if os.path.split(dirname)[-1] in ('ui'):
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
        os.path.walk('xpaxs', self.ui_cvt, None)
        _sdist.run(self)

setup(
    author = 'Darren Dale',
    author_email = 'praxes@googlegroups.com',
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        ],
    cmdclass = {
        'install' : install,
        'sdist' : sdist,
        },
    description = 'Extensible packages for x-ray science',
    entry_points = {
        'console_scripts' : [
            #'foo = my_package.some_module:main_func',
            ],
        'gui_scripts' : [
            'xpaxs = xpaxs.frontend.mainwindow:main',
            ],
        },
    extras_require = {
        #
        },
    include_package_data = True,
    install_requires = [
        'h5py >= 1.3.0',
        'matplotlib >= 0.98.3',
        'numpy >= 1.3.0',
        'pp >= 1.6.0',
        'PyMca >= 4.4.0',
        'setuptools'
        ],
    license = 'BSD',
    long_description = """
        XPaXS provides a python interface for data acquisition and
        analysis in the field of X-ray science.
        """,
    name = 'XPaXS',
    package_data = {
        '' : [
            '*.svg',
            ]
        },
    packages = find_packages(),
    platforms = 'Any',
    requires = [
        'python (>=2.6, <3.0)',
        'PyQt4 (>=4.5.2)'
        ],
    scripts = ['scripts/xpaxs_win_post_install.py'] if 'bdist_wininst' in sys.argv else [],
    test_suite = 'nose.collector',
    url = 'http://packages.python.org/xpaxs/',
    version = __version__,
    zip_safe = False,
)
