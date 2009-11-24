import os
import sys

# Remove MANIFEST before importing distutils. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

if 'develop' in sys.argv or 'build_sphinx' in sys.argv \
        or 'nosetests' in sys.argv:
    # only use setuptools for development, not for distribution
    from setuptools import setup
else:
    from distutils.core import setup

from setupbase import check_for_dependencies, find_scripts, find_package_data, \
    find_packages, convert_ui, find_extensions

if 'build' in sys.argv or 'install' in sys.argv:
    check_for_dependencies()
    convert_ui()

execfile(os.path.join('xpaxs', 'version.py'))

long_description = """
XPaXS provides a python interface for data acquisition and analysis in the
field of X-ray science.
"""

setup(
    name = 'xpaxs',
    version = __version__,
    description = 'Extensible Packages for X-ray Science',
    long_description = long_description,
    author = 'XPaXS Development Team',
    author_email = 'dsdale24@gmail.com',
    url = 'http://www.chess.cornell.edu/software/xpaxs',
    download_url = 'http://pypi.python.org/pypi/xpaxs',
    license = 'GPL',
    platforms = ['Linux', 'Mac OSX', 'Windows Vista/XP/2000'],
    keywords = [],
    requires = [
        'python (>=2.6, <3.0)',
        'numpy (>=1.3)',
        'matplotlib (>=0.99.1)',
        'PyQt4 (>=4.5.1)',
        'PyQwt (>=5.2.0)',
        'PyMca (>=4.3.1)',
        'pp (>=1.5.7)',
        'h5py (>=1.2.0)',
    ],
    packages = find_packages(),
    package_data = find_package_data(),
    scripts = find_scripts(),
    ext_modules = find_extensions(),
)
