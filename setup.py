# BEFORE importing disutils, remove MANIFEST. distutils doesn't properly
# update it when the contents of directories change.
import os
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

from distutils.core import Extension, setup
from distutils.version import LooseVersion
import glob
import sys
import warnings

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
    npReq = '1.0.4'
    import numpy
    npVer = numpy.__version__
    if LooseVersion(npVer) < LooseVersion(npReq):
        raise ImportError(
        'found numpy-%s, numpy-%s or later required'%(npVer, npReq))
except ImportError:
    raise RuntimeError("""You must have numpy-%s or later installed. See
http://sourceforge.net/project/showfiles.php?group_id=1369&package_id=175103
"""%npReq)

try:
    import PyMca
except ImportError:
    raise RuntimeError("""You must have PyMca-4.2.3 or later installed from
source (this also requires PyQwt-5 or later). See
http://sourceforge.net/project/showfiles.php?group_id=164626
""")

try:

    mplReq = '0.91.2'
    import matplotlib
    mplVer = matplotlib.__version__
    if LooseVersion(mplVer) < LooseVersion(mplReq):
        raise ImportError(
        'found matplotlib-%s, matplotlib-%s or later required'%(mplVer, mplReq))
except ImportError:
    raise RuntimeError("""You must have matplotlib-%s or later installed. See
http://sourceforge.net/project/showfiles.php?group_id=80706
"""%mplReq)

try:
    qtReq = '4.3'
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

try:
    ppReq = '1.4.3'
    import pp
    ppVer = pp.version
    if LooseVersion(ppVer) < LooseVersion(ppReq):
        raise ImportError(
        'found pp-%s, pp-%s or later required'%(ppVer, ppReq))
except ImportError:
    raise RuntimeError("""You must have pp-%s or later installed. See
http://www.parallelpython.com/
"""%ppReq)

try:
    pxReq = '2.3'
    import pexpect
    pxVer = pexpect.__version__
    if LooseVersion(pxVer) < LooseVersion(pxReq):
        warnings.warn(
        'found pexpect-%s, pexpect-%s or later suggested'%(pxVer, pxReq))
except ImportError:
    warnings.warn("""pexpect-%s or later is suggested, but not necessary. See
http://sourceforge.net/project/showfiles.php?group_id=59762
"""%pxReq)

try:
    tbReq = '2.0.3'
    import tables
    tbVer = tables.__version__
    if LooseVersion(tbVer) < LooseVersion(tbReq):
        warnings.warn(
        'found pytables-%s, pytables-%s or later suggested'%(tbVer, tbReq))
except ImportError:
    warnings.warn("""You must have pytables-%s or later installed. See
http://www.pytables.org/moin/Downloads
"""%pxReq)


for line in file('xpaxs/__init__.py').readlines():
    if line[:11] == '__version__':
        exec(line)
        break

if sys.platform == "win32":
    define_macros = [('WIN32',None)]
else:
    define_macros = []

def build_specfile(ext_modules):
    sources = 'xpaxs/datalib/specfile/external/specfile/src/*.c'
    headers = 'xpaxs/datalib/specfile/external/specfile/include'
    module  = Extension(name = 'specfile',
                        sources = glob.glob(sources),
                        define_macros = define_macros,
                        include_dirs = [headers,
                                        numpy.get_include()])
    ext_modules.append(module)

ext_modules = []
build_specfile(ext_modules)

description = 'Extensible Packages for X-ray Science'
long_description = \
"""XPaXS provides a python interface for data acquisition and analysis in the
field of X-ray science.
"""

# TODO: add documentation
scriptfiles = filter(os.path.isfile, glob.glob('scripts/*'))
package_data = {'xpaxs': ['spec/macros/*',
                          'resources/icons/*',
                          'resources/cursors/*']}

packages = ['xpaxs',
            'xpaxs/datalib',
            'xpaxs/datalib/specfile',
            'xpaxs/datalib/hdf5',
            'xpaxs/plotwidgets',
            'xpaxs/resources',
            'xpaxs/spec',
            'xpaxs/spec/client',
            'xpaxs/spec/ui',
            'xpaxs/spectromicroscopy',
            'xpaxs/spectromicroscopy/ui',
            'SpecClient']
package_dir = {'SpecClient': 'xpaxs/spec/external/SpecClient'}

setup(name = 'xpaxs',
      version = __version__,
      author = 'Darren S. Dale',
      author_email = 'dd55@cornell.edu',
      url = 'staff.chess.cornell.edu/~dale',
      description = description,
      long_description = long_description,
      platforms = 'any',
      packages = packages,
      package_dir = package_dir,
      ext_modules = ext_modules,
      package_data = package_data,
      scripts = scriptfiles)

