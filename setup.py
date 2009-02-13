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
    find_packages, convert_ui, setup_args, find_extensions

check_for_dependencies()
packages = find_packages()
scripts = find_scripts()
package_data = find_package_data()
ext_modules = find_extensions()

convert_ui()

setup(
    packages = packages,
    package_data = package_data,
    scripts = scripts,
    ext_modules = ext_modules,
    **setup_args
)
