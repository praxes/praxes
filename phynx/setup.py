import os

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages


with open('phynx/version.py') as f:
    for line in f:
        if line[:11] == '__version__':
            exec(line)
            break

setup(
    author = 'Darren Dale',
    author_email = 'praxes@googlegroups.com',
    classifiers = [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        ],
    description = 'An extensible high-level interface for complex HDF5 data',
    entry_points = {
        'console_scripts' : [
            #'foo = my_package.some_module:main_func'
        ],
        'gui_scripts' : [
            #'bar = my_package_gui.start_func',
        ],
    },
    install_requires = [
        'numpy >= 1.2.0',
        'h5py >= 1.3.0'
        ],
    license = 'BSD',
    long_description = """
        Phynx is an extensible high-level interface for working with
        complex HDF5 data, building on the h5py package.
        """,
    name = 'phynx',
    package_data = {
        'phynx' : [
            'tests/citrus_leaves.dat.h5',
        ]
    },
    packages = find_packages(),
    platforms = 'Any',
    requires = [
        'python (>=2.5.0, <3.0)',
        'hdf5 (>=1.8.4)'
        ],
    url = 'http://darrendale.github.com/phynx',
    version = __version__,
    zip_safe = False,
)
