# BEFORE importing disutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.

import os
import sys
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

try:
    from setuptools import Extension, find_packages, setup
except ImportError:
    raise ImportError("""Please install setuptools""")

from distutils.version import LooseVersion
import glob
import sys
#import warnings

def convert_qt_version(version):
    version = '%x'%version
    temp = []
    while len(version) > 0:
        version, chunk = version[:-2], version[-2:]
        temp.insert(0, str(int(chunk, 16)))
    return '.'.join(temp)

pyVer = sys.version.split()[0]
pyReq = '2.5'
if LooseVersion(pyVer) < LooseVersion(pyReq):
    raise ImportError(
        'found python-%s, python-%s or later required'%(pyVersion, pyReq))

try:
    import PyMca
except ImportError:
    raise ImportError("""You must have PyMca-4.2.4 or later installed from
source (this also requires PyQwt-5 or later). See
http://sourceforge.net/project/showfiles.php?group_id=164626
""")

qtReq = '4.3'
try:
    if sys.platform == "win32":
        from PyQt4 import Qt
        qtVer = Qt.qVersion()
        pyqtVer = Qt.PYQT_VERSION_STR
    else:
        from PyQt4 import pyqtconfig
        qtVer = convert_qt_version(pyqtconfig.Configuration().qt_version)
        pyqtVer = pyqtconfig.Configuration().pyqt_version_str
    if ( LooseVersion(qtVer) < LooseVersion(qtReq) ) |\
        ( LooseVersion(pyqtVer) < LooseVersion(qtReq) ):
        raise ImportError(
        'found Qt-%s and PyQt-%s, version %s or later required'%(qtVer, pyqtVer,
                                                             qtReq))
except ImportError:
    raise RuntimeError(
"""You must have Qt and PyQt version %s or later installed. See
http://trolltech.com/downloads/opensource and
http://www.riverbankcomputing.co.uk/pyqt/download.php
"""%qtReq)

for line in file('xpaxs/__init__.py').readlines():
    if line[:11] == '__version__':
        exec(line)
        break

if sys.platform == "win32":
    define_macros = [('WIN32',None)]
else:
    define_macros = []

def build_specfile(ext_modules):
    import numpy
    sources = 'specfile/src/*.c'
    headers = 'specfile/include'
    module  = Extension(name = 'specfile',
                        sources = glob.glob(sources),
                        define_macros = define_macros,
                        include_dirs = [headers,
                                        numpy.get_include()])
    ext_modules.append(module)

ext_modules = []

def ui_cvt(arg, dirname, fnames):
    for fname in fnames:
        if fname.endswith('.ui'):
            ui = '/'.join([dirname, fname])
            py = os.path.splitext(ui)[0]+'.py'
            os.system('pyuic4 -o %s %s'%(py, ui))
            print 'converted %s'%fname
        elif fname.endswith('.qrc'):
            rc = '/'.join([dirname, fname])
            py = os.path.splitext(rc)[0]+'_rc.py'
            os.system('pyrcc4 -o %s %s'%(py, rc))
            print 'converted %s'%fname

if 'build' in sys.argv or 'install' in sys.argv:

    build_specfile(ext_modules)

    sys.stdout.write('creating qt resources... ')
    sys.stdout.flush()
    os.path.walk('xpaxs', ui_cvt, None)
    sys.stdout.write('Done!\n')

description = 'Extensible Packages for X-ray Science'
long_description = \
"""XPaXS provides a python interface for data acquisition and analysis in the
field of X-ray science.
"""

# TODO: add documentation
scriptfiles = filter(os.path.isfile, glob.glob('scripts/*'))
package_data = {'xpaxs': ['instrumentation/spec/macros/*',
                          'instrumentation/spec/ui/icons/*',
                          'frontends/base/ui/resources/icons/*',
                          'frontends/base/ui/resources/cursors/*']}

packages = find_packages()
#packages.extend(find_packages('external'))
#package_dir = {'SpecClient': 'external/SpecClient'}
print packages

setup(name = 'xpaxs',
      version = __version__,
      maintainer = 'Darren S. Dale',
      maintainer_email = 'darren.dale@cornell.edu',
      license = "GPL2",
      url = 'http://www.chess.cornell.edu/software/xpaxs',
      download_url = "http://pypi.python.org/pypi/xpaxs",
      description = description,
      long_description = long_description,
      platforms = ['any'],
      packages = packages,
#      package_dir = package_dir,
      ext_modules = ext_modules,
      package_data = package_data,
      scripts = scriptfiles,
      test_suite = 'nose.collector',
      install_requires = ['numpy>=1.0.99',
                          'matplotlib>=0.98pre',
                          'PyMca>=4.2.4',
                          'pp>=1.5.3',
                          'tables>=2.0.2',
                          'pexpect>=2.3',
                          ])

