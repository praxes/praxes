import os
import sys

# Remove MANIFEST before importing distutils. distutils doesn't properly
# update it when the contents of directories change.
if os.path.exists('MANIFEST'): os.remove('MANIFEST')

from setuptools import setup

from setupbase import check_for_dependencies, find_scripts, find_package_data, \
    find_packages, convert_ui, find_extensions

if 'build' in sys.argv or 'install' in sys.argv:
    check_for_dependencies()
if 'build' in sys.argv or 'install' in sys.argv \
    or 'sdist' in sys.argv or 'bdist_egg' in sys.argv:
    convert_ui()

setup_data = dict(__name__='', __file__='setup_data.py')
execfile('setup_data.py', setup_data)
INFO = setup_data['INFO']

long_description = """
XPaXS provides a python interface for data acquisition and analysis in the
field of X-ray science.
"""

setup(
    author = 'Darren S. Dale, et. al.',
    author_email = 'dsdale24@gmail.com',
    description = 'Extensible Packages for X-ray Science',
    download_url = 'http://pypi.python.org/pypi/xpaxs',
    ext_modules = find_extensions(),
    extras_require = INFO['extras_require'],
    install_requires = INFO['install_requires'],
    keywords = [],
    license = 'GPL',
    long_description = long_description,
    maintainer = 'XPaXS Development Team',
    maintainer_email = '',
    name = 'xpaxs',
    package_data = find_package_data(),
    packages = find_packages(),
    platforms = ['Linux', 'Mac OS-X', 'Windows', 'Unix'],
    requires = INFO['requires'],
    scripts = find_scripts(),
    test_suite = 'nose.collector',
    url = 'http://www.chess.cornell.edu/software/xpaxs',
    version = INFO['version'],
)
