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

packages = [
    'phynx',
    'phynx.tests',
    'phynx.utils',
]

# Release.py contains version, authors, license, url, keywords, etc.
execfile(os.path.join('phynx','version.py'))

description = 'An extensible high-level interface for complex HDF5 data'

long_description = \
"""
Phynx is an extensible high-level interface for working with complex
HDF5 data, building on the h5py package.
"""

classifiers = """
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Intended Audience :: Information Technology
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Database
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Unix
Operating System :: POSIX :: Linux
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
"""

setup(
    packages = packages,
    name = 'phynx',
    version = version,
    description = description,
    long_description = long_description,
    author = 'The Phynx Development Team',
    author_email = '"python-phynx-developers" at the domain "lists.launchpad.net"',
    url = 'http://packages.python.org/phynx/',
    download_url = 'http://pypi.python.org/pypi/phynx/',
    keywords = keywords,
    classifiers = [x for x in classifiers.split("\n") if x],
    requires = ['numpy (>=1.3)', 'h5py (>=1.2)'],
)
